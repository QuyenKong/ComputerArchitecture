"""Chuyển tài liệu sang Markdown và ngược lại.

Đọc (sang Markdown):
    python tools/docconv.py to-md <file.pdf|pptx|docx|xlsx|html> [-o out.md] [--engine markitdown|pdftotext]
Viết (từ Markdown):
    python tools/docconv.py from-md <file.md> -o <out.docx|pptx|pdf|html> [--reference <mẫu.docx|pptx>]

- pptx/docx/xlsx/html -> markitdown (giữ bảng, speaker notes của slide).
- pdf -> mặc định pdftotext -layout (poppler): PDF do LaTeX sinh ra thì markitdown làm dính chữ tiếng Việt.
  Dùng --engine markitdown nếu cần.
- Markdown -> docx/pptx/html bằng pandoc; -> pdf bằng pandoc + xelatex (font Times New Roman, tiếng Việt).
Không có -o thì in ra stdout (UTF-8).
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

MARKITDOWN_EXT = {".pptx", ".docx", ".xlsx", ".xls", ".html", ".htm", ".csv", ".json", ".xml", ".epub"}


def run(cmd):
    # markitdown là script Python: khi stdout là pipe trên Windows nó ghi cp1252 -> mất dấu tiếng Việt
    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(cmd, capture_output=True, env=env)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode("utf-8", "replace"))
        sys.exit(f"Lỗi khi chạy: {' '.join(map(str, cmd))}")
    return r.stdout


def need(tool, hint):
    if shutil.which(tool) is None:
        sys.exit(f"Không tìm thấy '{tool}'. {hint}")


def to_md(src: Path, out, engine):
    ext = src.suffix.lower()
    if ext == ".pdf" and engine != "markitdown":
        need("pdftotext", "Cài poppler (winget install oschwartz10612.Poppler).")
        data = run(["pdftotext", "-enc", "UTF-8", "-layout", str(src), "-"])
    elif ext == ".pdf" or ext in MARKITDOWN_EXT:
        need("markitdown", 'Cài: pip install "markitdown[pdf,docx,pptx,xlsx]"')
        data = run(["markitdown", str(src)])
    else:
        sys.exit(f"Chưa hỗ trợ đuôi {ext}")
    text = data.decode("utf-8", "replace").replace("\r\n", "\n")
    write(text, out)


def from_md(src: Path, out: Path, reference):
    need("pandoc", "Cài pandoc (winget install JohnMacFarlane.Pandoc).")
    ext = out.suffix.lower()
    cmd = ["pandoc", str(src), "-f", "markdown", "-o", str(out), "--resource-path", str(src.parent)]
    if ext == ".pdf":
        need("xelatex", "Cần TinyTeX/MiKTeX có xelatex.")
        cmd += ["--pdf-engine=xelatex", "-V", "mainfont=Times New Roman", "-V", "geometry:margin=2.5cm"]
    elif ext in (".docx", ".pptx"):
        if reference:
            cmd += ["--reference-doc", str(reference)]
    elif ext in (".html", ".htm"):
        cmd += ["--standalone", "--embed-resources"]
    else:
        sys.exit(f"Chưa hỗ trợ xuất {ext}")
    run(cmd)
    print(f"Đã tạo {out}")


def write(text, out):
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"Đã ghi {out}")
    else:
        sys.stdout.buffer.write(text.encode("utf-8"))


def main():
    # Console Windows mặc định cp1252, không in được tiếng Việt
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8")
    ap =argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("to-md")
    a.add_argument("src", type=Path)
    a.add_argument("-o", "--out", type=Path)
    a.add_argument("--engine", choices=["auto", "markitdown", "pdftotext"], default="auto")
    b = sub.add_parser("from-md")
    b.add_argument("src", type=Path)
    b.add_argument("-o", "--out", type=Path, required=True)
    b.add_argument("--reference", type=Path, help="file mẫu docx/pptx để lấy style")
    args = ap.parse_args()
    if not args.src.exists():
        sys.exit(f"Không thấy file {args.src}")
    if args.cmd == "to-md":
        to_md(args.src, args.out, args.engine)
    else:
        from_md(args.src, args.out, args.reference)


if __name__ == "__main__":
    main()
