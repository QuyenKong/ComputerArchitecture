"""Dựng deck thuyết trình RV32I trên template PowerPoint của HUST.

Chạy:  python slides/build_slides.py
Đầu vào: slides/template/HUST_PPT_TEMPLATE_2026_16x9.pptx, ảnh mạch docs/img/*.png,
số liệu latex/generated/*.tex (sinh bởi latex/scripts/gen_results.py, không gõ tay).
Lời thoại (speaker notes) lấy từ slides/kich_ban.src.md.
Đầu ra:  slides/RV32I_ThuyetTrinh.pptx (20 slide) và slides/KICH_BAN.md (kịch bản đã thay số liệu).
"""
import copy
import re
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "slides/template/HUST_PPT_TEMPLATE_2026_16x9.pptx"
OUT = ROOT / "slides/RV32I_ThuyetTrinh.pptx"
SCRIPT_SRC = ROOT / "slides/kich_ban.src.md"
SCRIPT_OUT = ROOT / "slides/KICH_BAN.md"
IMG = ROOT / "docs/img"
GEN = ROOT / "latex/generated"

# ---------------------------------------------------------------- số liệu thật
NUM = dict(re.findall(r"\\newcommand\{\\(res\w+)\}\{([^}]*)\}", (GEN / "numbers.tex").read_text("utf-8")))


def read_rows(name):
    rows = []
    for line in (GEN / name).read_text("utf-8").splitlines():
        m = re.match(r"\\texttt\{(.+?)\} & (.+?) \\\\", line)
        if m:
            rows.append((m.group(1).replace("\\_", "_"), [c.strip() for c in m.group(2).split("&")]))
    return rows


CYCLES = read_rows("cycles_table.tex")   # Lệnh, SC, NH, NOP, PL, Load-use, Nhảy, CPI
TIMES = read_rows("time_table.tex")      # SC ns, NH ns, PL ns, SC/NH, SC/PL, NH/PL
VEC_TOTAL = re.search(r"Tổng & & (\S+) & (\S+) \\\\",
                      (ROOT / "latex/chapters/06_kiem_thu.tex").read_text("utf-8")).groups()

# ---------------------------------------------------------------- màu, font
RED = RGBColor(0xC0, 0x00, 0x00)
DARK = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x59, 0x59, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TINT_RED = RGBColor(0xFB, 0xE7, 0xE7)
TINT_ORG = RGBColor(0xFD, 0xF0, 0xDC)
TINT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
ORANGE = RGBColor(0xE0, 0x8A, 0x1E)
LINE = RGBColor(0xD9, 0xD9, 0xD9)
BODY = "Arial"
MONO = "Courier New"

# Màu ô giản đồ pipeline, giống báo cáo LaTeX
STAGE = {"IF": "DCEBFA", "ID": "E4F3DC", "EX": "FCE9C8", "ME": "F3DDF0", "WB": "E2E2E2", "ST": "F8C9C4"}

prs = Presentation(TEMPLATE)
L_CONTENT = prs.slide_layouts[4]   # nền trắng, thanh đỏ HUST ở đáy
L_DIVIDER = prs.slide_layouts[13]  # nền đỏ, tiêu đề giữa
SLD_NUM_SRC = None
for ph in prs.slide_layouts[4].placeholders:
    if ph.placeholder_format.type is not None and ph.placeholder_format.idx == 12:
        SLD_NUM_SRC = ph._element


# ---------------------------------------------------------------- tiện ích
def add_slide_number(slide):
    if SLD_NUM_SRC is None:
        return
    sp = copy.deepcopy(SLD_NUM_SRC)
    for t in sp.iter(qn("a:t")):
        t.text = ""
    txBody = sp.find(qn("p:txBody"))
    for p in txBody.findall(qn("a:p")):
        txBody.remove(p)
    p = etree.SubElement(txBody, qn("a:p"))
    fld = etree.SubElement(p, qn("a:fld"), id="{9EA0BE3B-158A-4EDF-80DC-E394A0D1600F}", type="slidenum")
    etree.SubElement(fld, qn("a:rPr"), lang="vi-VN")
    etree.SubElement(fld, qn("a:t")).text = "‹#›"
    spPr = sp.find(qn("p:spPr"))
    for child in list(spPr):
        spPr.remove(child)
    slide.shapes._spTree.append(sp)


def strip_placeholders(slide, keep=(0,)):
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx not in keep:
            ph._element.getparent().remove(ph._element)


def set_bullet(p, char="•", level=0, color=RED):
    pPr = p._p.get_or_add_pPr()
    indent = 228600
    pPr.set("marL", str(indent * (level + 1)))
    pPr.set("indent", str(-indent))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum", "a:buClr", "a:buFont"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buClr = etree.SubElement(pPr, qn("a:buClr"))
    etree.SubElement(buClr, qn("a:srgbClr"), val=str(color))
    etree.SubElement(pPr, qn("a:buFont"), typeface="Arial")
    etree.SubElement(pPr, qn("a:buChar"), char=char)


def no_bullet(p):
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn("a:buNone")) is None:
        etree.SubElement(pPr, qn("a:buNone"))


def style_run(run, size, color=DARK, bold=False, font=BODY, italic=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = font
    f.color.rgb = color


def text(slide, x, y, w, h, paras, size=16, color=DARK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, font=BODY, space_after=6, margin=0.05, name=None):
    """paras: danh sách đoạn. Mỗi đoạn là str, hoặc dict {runs:[(text, opts)], bullet, size, ...}."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    for i, para in enumerate(paras):
        if isinstance(para, str):
            para = {"runs": [(para, {})]}
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = para.get("align", align)
        p.space_after = Pt(para.get("space_after", space_after))
        if para.get("bullet"):
            set_bullet(p, level=para.get("level", 0))
        else:
            no_bullet(p)
        for txt, opts in para["runs"]:
            r = p.add_run()
            r.text = txt
            style_run(r, opts.get("size", para.get("size", size)), opts.get("color", para.get("color", color)),
                      opts.get("bold", para.get("bold", bold)), opts.get("font", para.get("font", font)),
                      opts.get("italic", False))
    return tb


def B(t):
    return (t, {"bold": True})


def C(t, **kw):
    d = {"font": MONO}
    d.update(kw)
    return (t, d)


def box(slide, x, y, w, h, fill=TINT_GRAY, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08, name=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        s.name = name
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.text_frame.text = ""
    return s


def circle_num(slide, x, y, d, label, fill=RED, size=14):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    s.line.fill.background()
    s.shadow.inherit = False
    tf = s.text_frame
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", 0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    style_run(r, size, WHITE, True)
    return s


def arrow(slide, x, y, w, h, color=MUTED):
    s = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def picture(slide, path, x, y, w=None, h=None, border=True, left=False):
    """Đặt ảnh vừa khung (x, y, w, h), giữ tỉ lệ, căn giữa trong khung."""
    from PIL import Image
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    px, py = (x if left else x + (w - pw) / 2), y + (h - ph) / 2
    pic = slide.shapes.add_picture(str(path), Inches(px), Inches(py), Inches(pw), Inches(ph))
    if border:
        pic.line.color.rgb = LINE
        pic.line.width = Pt(0.75)
    return pic


def table(slide, x, y, w, rows, col_w, size=12, header_fill=RED, row_h=0.3, fills=None, fonts=None, aligns=None):
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    tbl = gt.table
    tblPr = tbl._tbl.tblPr
    for attr in ("bandRow", "firstRow"):
        tblPr.set(attr, "0")
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    for i in range(nr):
        tbl.rows[i].height = Inches(row_h)
        for j in range(nc):
            cell = tbl.cell(i, j)
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if i == 0 and header_fill is not None:
                cell.fill.fore_color.rgb = header_fill
            elif fills and fills.get((i, j)):
                cell.fill.fore_color.rgb = fills[(i, j)]
            else:
                cell.fill.fore_color.rgb = WHITE if i % 2 else RGBColor(0xFA, 0xFA, 0xFA)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (aligns[j] if aligns else PP_ALIGN.LEFT) if i else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = str(rows[i][j])
            font = (fonts or {}).get(j, BODY) if i else BODY
            style_run(r, size, WHITE if (i == 0 and header_fill is not None) else DARK, i == 0, font)
    return tbl


def content_slide(title):
    s = prs.slides.add_slide(L_CONTENT)
    strip_placeholders(s)
    s.shapes.title.text = title
    add_slide_number(s)
    return s


def divider_slide(part, title, who, items):
    s = prs.slides.add_slide(L_DIVIDER)
    strip_placeholders(s)
    t = s.shapes.title
    t.text = title
    t.left, t.top, t.width, t.height = Inches(1.13), Inches(2.2), Inches(11.07), Inches(1.4)
    for p in t.text_frame.paragraphs:
        p.alignment = PP_ALIGN.LEFT
        for r in p.runs:
            r.font.size = Pt(44)
    text(s, 1.13, 1.45, 6, 0.6, [{"runs": [(part, {"bold": True})]}], size=22, color=WHITE)
    text(s, 1.13, 3.75, 9.5, 0.5, [who], size=20, color=WHITE)
    tb = text(s, 1.13, 4.45, 7.5, 1.8, [{"runs": [(i, {})], "bullet": True} for i in items], size=16,
              color=WHITE, space_after=4)
    for p in tb.text_frame.paragraphs:
        set_bullet(p, color=WHITE)
    return s


# ---------------------------------------------------------------- bỏ slide mẫu, giữ slide bìa và cảm ơn
sld_ids = prs.slides._sldIdLst
orig = list(sld_ids)
keep_title, keep_thanks = orig[2], orig[14]  # slide 3 (tiêu đề), slide 15 (THANK YOU)
for sid in orig:
    if sid not in (keep_title, keep_thanks):
        prs.part.drop_rel(sid.get(qn("r:id")))
        sld_ids.remove(sid)
# python-pptx đặt tên slide mới theo số slide hiện có; đổi tên 2 slide giữ lại để không trùng part
from pptx.opc.packuri import PackURI  # noqa: E402
for n, sl in enumerate(prs.slides, start=1):
    sl.part.partname = PackURI(f"/ppt/slides/slide{n}.xml")

# ---------------------------------------------------------------- S1 tiêu đề
s1 = prs.slides[0]
for shp in s1.shapes:
    if shp.has_text_frame and shp.text_frame.text.startswith("PRESENTATION"):
        shp.text_frame.paragraphs[0].runs[0].text = "CPU RISC-V RV32I"
        shp.text_frame.paragraphs[0].runs[0].font.size = Pt(48)
        shp.top = Inches(2.05)
    elif shp.has_text_frame and shp.text_frame.text.startswith("SUBTITLE"):
        ps = shp.text_frame.paragraphs
        ps[0].runs[0].text = "Đơn chu kỳ và pipeline 5 tầng"
        ps[1].runs[0].text = "trên Logisim-evolution 4.1.0"
        for p in ps:
            p.runs[0].font.size = Pt(26)
        shp.top = Inches(2.95)
text(s1, 0.42, 4.35, 7.6, 1.9, [
    {"runs": [B("Bài tập lớn Kiến trúc máy tính tiên tiến")], "color": DARK},
    {"runs": [("Nhóm: Quyền Đức Công · Bùi Phạm Sơn Hà · Nguyễn Đức Anh", {})]},
    {"runs": [("Giảng viên hướng dẫn: TS. Hoàng Văn Hiệp", {})]},
    {"runs": [("Trường Công nghệ Thông tin và Truyền thông · 11/2026", {"color": MUTED})]},
], size=16, color=DARK, space_after=4, name="Thông tin nhóm")

# ---------------------------------------------------------------- S2 tổng quan
s = content_slide("Đề bài và sản phẩm")
files = [
    ("RV32I_SingleCycle.circ", "SC", "CPU đơn chu kỳ, CPI = 1"),
    ("RV32I_Pipeline.circ", "PL", "Pipeline 5 tầng: forwarding, bypass WB→ID, stall load-use, flush khi nhảy"),
    ("extra/RV32I_Pipeline_NoHazard.circ", "NH", "Pipeline không forwarding, không stall; assembler chèn nop"),
]
text(s, 0.55, 0.95, 6.6, 0.4, [{"runs": [B("Ba file mạch trong circ/")]}], size=18, color=RED)
for i, (f, tag, desc) in enumerate(files):
    y = 1.4 + i * 0.92
    box(s, 0.55, y, 6.6, 0.82, TINT_RED if tag == "PL" else TINT_GRAY)
    circle_num(s, 0.7, y + 0.13, 0.56, tag, RED if tag == "PL" else MUTED, 13)
    text(s, 1.42, y + 0.03, 5.6, 0.78, [{"runs": [C(f, size=13, bold=True)], "space_after": 2},
                                        {"runs": [(desc, {})], "size": 14}], size=14)
stats = [
    ("37", "lệnh RV32I, gồm cả phần tùy chọn\n(LB/LH/SB/SH, BLT/BGE...)"),
    (VEC_TOTAL[1].split("/")[0], "test vector đạt trên 13 module\n(bản PL)"),
    ("12 + 25", "chương trình test + fuzz:\nPASS trên SC, PL và NH --nohazard"),
    (NUM["resSpeedPL"] + "×", "PL nhanh hơn SC (giả định trễ\n800 ps / 220 ps)"),
]
for i, (big, small) in enumerate(stats):
    x, y = 7.6 + (i % 2) * 2.75, 0.95 + (i // 2) * 1.55
    text(s, x, y, 2.6, 0.75, [{"runs": [B(big)]}], size=36, color=RED)
    text(s, x, y + 0.72, 2.6, 0.9, small.split("\n"), size=12, color=MUTED, space_after=0)
parts = [("Phần 1 · 11 module dùng chung", "Bùi Phạm Sơn Hà"),
         ("Phần 2 · CPU đơn chu kỳ", "Quyền Đức Công"),
         ("Phần 3 · Pipeline 5 tầng", "Nguyễn Đức Anh")]
for i, (p, who) in enumerate(parts):
    x = 0.55 + i * 4.0
    box(s, x, 4.3, 3.85, 0.85, RED if i == 0 else TINT_RED)
    col = WHITE if i == 0 else DARK
    text(s, x + 0.15, 4.34, 3.6, 0.8, [{"runs": [B(p)], "space_after": 2},
                                        {"runs": [(who + " · 10 phút", {})], "size": 13}], size=15, color=col)
text(s, 0.55, 5.35, 9.0, 0.4, ["Mỗi phần kèm demo trên Logisim: quan sát register file, RAM và Pipeline Monitor."],
     size=13, color=MUTED)

# ---------------------------------------------------------------- S3 phần 1
divider_slide("PHẦN 1", "11 MODULE DÙNG CHUNG", "Bùi Phạm Sơn Hà · 10 phút", [
    "Mỗi module là một circuit con, tên chân cố định, có test vector riêng",
    "SC và PL dùng chung đúng 11 circuit này",
])

# ---------------------------------------------------------------- S4 bản đồ 11 module
s = content_slide("11 circuit con và test vector")
mods = [
    ("Control", "opcode → mọi tín hiệu điều khiển", "400/400", TINT_RED),
    ("ImmGen", "ghép immediate I, S, B, U, J", "300/300", TINT_RED),
    ("ALUControl", "ALUCtrl = {bit30, funct3}", "64/64", TINT_RED),
    ("RegisterFile", "x1..x31, 2 cổng đọc, 1 cổng ghi", "400/400", TINT_ORG),
    ("ALU", "10 phép tính song song + MUX", "250/250", TINT_ORG),
    ("BranchUnit", "so sánh rs1, rs2 → Taken", "300/300", TINT_ORG),
    ("AddrDecode", "tách WordAddr, Off, IsIO", "200/200", TINT_GRAY),
    ("LoadUnit", "LB, LH, LW, LBU, LHU", "300/300", TINT_GRAY),
    ("StoreUnit", "SB, SH, SW: đọc, sửa, ghi", "300/300", TINT_GRAY),
    ("IOController", "UART + GPIO memory-mapped", "400/400", TINT_GRAY),
    ("PerfCounters", "đếm cycles và instret", "qua bộ test", RGBColor(0xFF, 0xFF, 0xFF)),
]
for i, (name, role, vec, fill) in enumerate(mods):
    x, y = 0.55 + (i % 4) * 3.05, 0.95 + (i // 4) * 1.35
    box(s, x, y, 2.9, 1.25, fill, line=LINE if fill == RGBColor(0xFF, 0xFF, 0xFF) else None)
    text(s, x + 0.12, y + 0.06, 2.7, 1.15, [
        {"runs": [C(name, size=15, bold=True, color=RED)], "space_after": 3},
        {"runs": [(role, {})], "size": 13, "space_after": 3},
        {"runs": [("vector: " + vec, {"color": MUTED})], "size": 12},
    ])
x, y = 0.55 + 3 * 3.05, 0.95 + 2 * 1.35
box(s, x, y, 2.9, 1.25, RED)
text(s, x + 0.12, y + 0.06, 2.7, 1.15, [
    {"runs": [B("Chỉ có ở PL")], "space_after": 3},
    {"runs": [("ForwardUnit, HazardUnit, IDBypass và 4 thanh ghi pipeline (phần 3)", {})], "size": 13},
], size=15, color=WHITE)
legend = [("Giải mã", TINT_RED), ("Thực thi", TINT_ORG), ("Bộ nhớ, I/O", TINT_GRAY)]
for i, (lbl, col) in enumerate(legend):
    box(s, 0.55 + i * 2.0, 5.2, 0.3, 0.3, col, radius=0.2)
    text(s, 0.92 + i * 2.0, 5.17, 1.6, 0.4, [lbl], size=12, color=MUTED)
text(s, 0.55, 5.65, 8.5, 0.4, [f"Tổng: {VEC_TOTAL[0]} vector trên SC, {VEC_TOTAL[1]} trên PL"],
     size=12, color=MUTED)

# ---------------------------------------------------------------- S5 ALU
s = content_slide("ALU và ALUControl")
picture(s, IMG / "ALU.png", 0.55, 0.95, 6.3, 4.9)
text(s, 7.2, 0.95, 5.6, 4.0, [
    {"runs": [B("Song song rồi chọn: "), ("Adder, Subtractor, 2 Comparator, 3 cổng logic, 3 Shifter; "
                                          "MUX 8:1 theo funct3", {})], "bullet": True},
    {"runs": [B("ALUCtrl = {bit 30, funct3}: "), ("bit 3 phân biệt ADD/SUB và SRL/SRA", {})], "bullet": True},
    {"runs": [B("Bẫy ADDI âm: "), ("bit 30 thuộc immediate, chỉ dùng khi là lệnh R hoặc SRAI", {})],
     "bullet": True},
    {"runs": [B("Lượng dịch: "), ("5 bit thấp của B, đúng đặc tả RV32I", {})], "bullet": True},
], size=16, space_after=10)
tbl = table(s, 7.2, 3.75, 5.2, [
    ["0000", "1000", "0001", "0010", "0011"],
    ["ADD", "SUB", "SLL", "SLT", "SLTU"],
    ["0100", "0101", "1101", "0110", "0111"],
    ["XOR", "SRL", "SRA", "OR", "AND"],
], [1.04] * 5, size=12, header_fill=None, row_h=0.3, fonts={j: MONO for j in range(5)},
    aligns=[PP_ALIGN.CENTER] * 5,
    fills={(0, j): TINT_RED for j in range(5)} | {(2, j): TINT_RED for j in range(5)})
text(s, 7.2, 5.0, 5.0, 0.4, ["Mã ALUCtrl (hàng đỏ nhạt) và phép tính tương ứng"], size=11, color=MUTED)

# ---------------------------------------------------------------- S6 Control, ImmGen
s = content_slide("Control và ImmGen")
picture(s, IMG / "Control.png", 0.55, 0.95, 4.6, 4.9)
ctrl = [["Nhóm", "RW", "ASel", "BSel", "Imm", "MR", "MW", "WB", "B/J/Jr"],
        ["OP (R)", "1", "rs1", "rs2", "–", "0", "0", "ALU", "0/0/0"],
        ["OP-IMM", "1", "rs1", "imm", "I", "0", "0", "ALU", "0/0/0"],
        ["LOAD", "1", "rs1", "imm", "I", "1", "0", "Mem", "0/0/0"],
        ["STORE", "0", "rs1", "imm", "S", "0", "1", "–", "0/0/0"],
        ["BRANCH", "0", "PC", "imm", "B", "0", "0", "–", "1/0/0"],
        ["JAL", "1", "PC", "imm", "J", "0", "0", "PC+4", "0/1/0"],
        ["JALR", "1", "rs1", "imm", "I", "0", "0", "PC+4", "0/0/1"],
        ["LUI", "1", "0", "imm", "U", "0", "0", "ALU", "0/0/0"],
        ["AUIPC", "1", "PC", "imm", "U", "0", "0", "ALU", "0/0/0"],
        ["SYSTEM", "Halt = 1, còn lại 0", "", "", "", "", "", "", ""]]
t = table(s, 5.45, 0.95, 7.35, ctrl, [1.15, 0.5, 0.7, 0.7, 0.6, 0.5, 0.5, 0.85, 0.85], size=12, row_h=0.31,
          aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.CENTER] * 8)
t.cell(10, 1).merge(t.cell(10, 8))
text(s, 5.45, 4.5, 7.35, 1.5, [
    {"runs": [B("Decoder chỉ bật khi opcode[1:0] = 11: "), ("lệnh 0x00000000 = NOP, flush chỉ cần nạp 0", {})],
     "bullet": True},
    {"runs": [B("ImmGen: "), ("8 mảnh bit cố định → ghép I/S/B/U/J → MUX theo ImmSel", {})], "bullet": True},
    {"runs": [B("UseRs1, UseRs2: "), ("báo lệnh có thật sự đọc rs1, rs2 (dùng ở phần 3)", {})], "bullet": True},
], size=14, space_after=6)

# ---------------------------------------------------------------- S7 RegisterFile, BranchUnit
s = content_slide("RegisterFile và BranchUnit")
picture(s, IMG / "RegisterFile.png", 0.55, 0.95, 6.0, 3.2)
picture(s, IMG / "BranchUnit.png", 6.85, 0.95, 5.95, 3.2)
text(s, 0.55, 4.35, 6.0, 2.2, [
    {"runs": [B("x0 không phải thanh ghi: "), ("đầu vào 0 của MUX đọc nối hằng 0", {})], "bullet": True},
    {"runs": [B("Ghi: "), ("Decoder 5→32 bật enable của đúng x[rd] ở cạnh lên", {})], "bullet": True},
    {"runs": [B("Không bypass bên trong: "), ("tránh vòng tổ hợp ở SC; PL dùng IDBypass ngoài", {})],
     "bullet": True},
], size=15, space_after=8)
text(s, 6.85, 4.35, 5.95, 2.2, [
    {"runs": [B("2 Comparator: "), ("không dấu (bằng, nhỏ hơn) và có dấu", {})], "bullet": True},
    {"runs": [B("MUX theo funct3[2:1], "), ("XOR funct3[0] cho BNE, BGE, BGEU", {})], "bullet": True},
    {"runs": [B("Taken = "), ("kết quả AND Branch; ALU rảnh để tính PC + imm", {})], "bullet": True},
], size=15, space_after=8)

# ---------------------------------------------------------------- S8 bộ nhớ, I/O
s = content_slide("Bộ nhớ, I/O và bộ đếm")
memmap = [["Vùng", "Địa chỉ", "Ghi chú"],
          ["IMEM (ROM)", "0x0000_0000–0FFF", "1024 lệnh, ô = PC[11:2]"],
          ["DMEM (RAM)", "0x0000_0000–3FFF", "16 KiB, ô = Addr[13:2]"],
          ["UART_TXDATA", "0xF000_0000", "ghi: ký tự ra TTY"],
          ["UART_RXDATA", "0xF000_0004", "đọc: ký tự từ Keyboard"],
          ["UART_STATUS", "0xF000_0008", "bit 0 có ký tự, bit 1 TX sẵn sàng"],
          ["GPIO_OUT", "0xF000_0010", "LED 7 đoạn, 8 LED"],
          ["GPIO_IN", "0xF000_0014", "8 công tắc DIP"]]
table(s, 0.55, 0.95, 6.5, memmap, [1.55, 1.95, 3.0], size=12, row_h=0.36, fonts={1: MONO})
text(s, 0.55, 4.0, 6.5, 2.4, [
    {"runs": [B("AddrDecode: "), C("IsIO = (Addr[31:28] == 0xF)", size=13)], "bullet": True},
    {"runs": [B("LoadUnit: "), ("dịch phải Off×8 bit, mở rộng dấu/0, chọn theo funct3", {})], "bullet": True},
    {"runs": [B("IOController: "), ("KbdRE = chọn RXDATA AND MemRead, tránh mất ký tự", {})], "bullet": True},
    {"runs": [B("PerfCounters: "), ("cycles khi chưa halt, instret khi có lệnh hoàn thành", {})], "bullet": True},
], size=14, space_after=6)
picture(s, IMG / "StoreUnit.png", 7.35, 0.95, 5.45, 2.4)
box(s, 7.35, 3.5, 5.2, 1.6, TINT_RED)
text(s, 7.5, 3.55, 4.95, 1.5, [
    {"runs": [B("StoreUnit: đọc, sửa, ghi cả word")], "color": RED, "space_after": 3},
    {"runs": [C("M   = mask << (Off×8)", size=13)], "space_after": 0},
    {"runs": [C("New = (Old & ~M) | ((WData << Off×8) & M)", size=13)], "space_after": 4},
    {"runs": [("sb 0xAB, offset 2, word cũ ", {}), C("0x11223344", size=13)], "space_after": 0},
    {"runs": [("→ M = ", {}), C("0x00FF0000", size=13), (", word mới ", {}), C("0x11AB3344", size=13, bold=True)]},
], size=14)

# ---------------------------------------------------------------- S9 phần 2
divider_slide("PHẦN 2", "CPU ĐƠN CHU KỲ", "Quyền Đức Công · 10 phút", [
    "Ghép 11 module thành datapath, mỗi lệnh xong trong 1 chu kỳ",
    "Một lệnh lw đi qua mạch; next-PC và halt; đường găng",
])

# ---------------------------------------------------------------- S10 datapath SC
s = content_slide("Datapath đơn chu kỳ")
picture(s, IMG / "RV32I_SingleCycle.png", 0.55, 0.95, 8.4, 5.3)
steps = [("IF", "PC → IMEM (PC[11:2]) ra instr; bộ cộng PC + 4"),
         ("ID", "Control sinh tín hiệu; RegisterFile đọc rs1, rs2; ImmGen"),
         ("EX", "ALU: A = rs1/PC/0, B = rs2/imm; BranchUnit so sánh"),
         ("MEM", "StoreUnit ghép dữ liệu; RAM ghi ở cạnh lên; LoadUnit"),
         ("WB", "WBSel: ALU, dữ liệu load hoặc PC + 4 → x[rd]")]
for i, (st, desc) in enumerate(steps):
    y = 0.95 + i * 1.07
    circle_num(s, 9.2, y + 0.1, 0.7, st, RED, 13 if len(st) < 3 else 11)
    text(s, 10.0, y, 2.85, 1.0, [desc], size=13, anchor=MSO_ANCHOR.MIDDLE)

# ---------------------------------------------------------------- S11 ví dụ lw
s = content_slide("Ví dụ: lw t4, 8(sp) trong một chu kỳ")
fields = [("imm[11:0]", "000000001000", "= 8", 3.4), ("rs1", "00010", "x2 (sp)", 1.7), ("funct3", "010", "LW", 1.3),
          ("rd", "11101", "x29 (t4)", 1.7), ("opcode", "0000011", "LOAD", 2.3)]
x = 0.55
text(s, 0.55, 0.95, 12.2, 0.4, [{"runs": [("Mã máy ", {}), C("0x00812E83", bold=True, color=RED)]}], size=18)
for name, bits, meaning, w in fields:
    w = w * 12.2 / 10.4
    box(s, x, 1.5, w - 0.08, 1.15, TINT_RED, shape=MSO_SHAPE.RECTANGLE)
    text(s, x, 1.52, w - 0.08, 1.1, [
        {"runs": [(name, {"color": MUTED})], "size": 12, "space_after": 2, "align": PP_ALIGN.CENTER},
        {"runs": [C(bits, size=16, bold=True)], "space_after": 2, "align": PP_ALIGN.CENTER},
        {"runs": [(meaning, {"color": RED, "bold": True})], "size": 13, "align": PP_ALIGN.CENTER},
    ])
    x += w
flow = [("Control", "nhóm LOAD\nRegWrite = 1, BSel = imm\nMemRead = 1, WBSel = Mem"),
        ("ALU", "A = sp, B = 8\nY = sp + 8"),
        ("AddrDecode", "IsIO = 0\n→ đọc DMEM"),
        ("LoadUnit", "funct3 = 010\nlấy cả word"),
        ("Ghi lại", "t4 ← M[sp + 8]\nPC ← PC + 4")]
for i, (h, body) in enumerate(flow):
    x = 0.55 + i * 2.45
    box(s, x, 3.1, 2.1, 1.9, TINT_GRAY)
    text(s, x + 0.08, 3.15, 1.95, 1.8, [{"runs": [B(h)], "color": RED, "size": 16, "space_after": 6}] +
         [{"runs": [(ln, {})], "size": 13, "space_after": 2} for ln in body.split("\n")])
    if i < 4:
        arrow(s, x + 2.13, 3.88, 0.28, 0.35)
text(s, 0.55, 5.25, 9.0, 0.8, ["Cả năm bước nằm trong một chu kỳ clock: chu kỳ phải đủ dài cho đường dài nhất, "
                                "và lệnh load chính là đường đó."], size=14, color=MUTED)

# ---------------------------------------------------------------- S12 next-PC, halt, critical path
s = content_slide("Next-PC, halt và đường găng")
text(s, 0.55, 0.95, 5.9, 0.4, [{"runs": [B("Chọn PC kế tiếp")]}], size=18, color=RED)
box(s, 0.55, 1.45, 5.9, 2.15, TINT_GRAY)
text(s, 0.75, 1.55, 5.5, 2.3, [
    {"runs": [C("PCSel  = Taken | Jal | Jalr", size=14, bold=True)], "space_after": 4},
    {"runs": [C("target = ALU.Y & 0xFFFFFFFE", size=14, bold=True)], "space_after": 10},
    {"runs": [("Branch, JAL: A = PC; JALR: A = rs1. Một bộ cộng (ALU) tính đích cho cả ba lệnh.", {})],
     "size": 14, "space_after": 6},
    {"runs": [("PC.enable = NOT Halt: EBREAK giữ nguyên trạng thái, chân halt lên 1.", {})], "size": 14},
], size=14)
text(s, 6.85, 0.95, 5.95, 0.4, [{"runs": [B("Vì sao CPI = 1 nhưng vẫn chậm")]}], size=18, color=RED)
text(s, 6.85, 1.45, 5.95, 2.4, [
    {"runs": [("Lệnh load đi qua nhiều khối nhất: IMEM, Control và RegisterFile, ALU, DMEM, LoadUnit, MUX ghi lại.",
               {})], "bullet": True},
    {"runs": [("Lệnh add không dùng RAM nhưng vẫn phải chờ hết chu kỳ dài đó.", {})], "bullet": True},
], size=15, space_after=8)
text(s, 0.55, 4.25, 12.2, 0.4, [{"runs": [B("Đường găng theo giả định trễ (ps)")]}], size=16, color=DARK)
seg = [("IF 200", 200, "DCEBFA"), ("ID 100", 100, "E4F3DC"), ("EX 200", 200, "FCE9C8"),
       ("MEM 200", 200, "F3DDF0"), ("WB 100", 100, "E2E2E2")]
x = 0.55
scale = 10.2 / 800
for lbl, ps, col in seg:
    w = ps * scale
    b = box(s, x, 4.75, w - 0.04, 0.75, RGBColor.from_string(col), shape=MSO_SHAPE.RECTANGLE)
    text(s, x, 4.75, w - 0.04, 0.75, [{"runs": [B(lbl)], "align": PP_ALIGN.CENTER}], size=15,
         anchor=MSO_ANCHOR.MIDDLE)
    x += w
text(s, x + 0.1, 4.72, 1.9, 0.8, [{"runs": [B(NUM["resTSingle"] + " ps")]}], size=26, color=RED,
     anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.55, 5.65, 9.0, 0.6, ["Giả định trễ từng bước theo Patterson & Hennessy, ch. 4. Logisim không mô phỏng trễ "
                                "cổng, nên đây không phải số đo trên mạch."], size=12, color=MUTED)

# ---------------------------------------------------------------- S13 kiểm thử
demo_row = dict(CYCLES)["demo.s"]
s = content_slide("Kiểm thử tự động và kết quả bản đơn chu kỳ")
chain = [("programs/*.s", "12 chương trình\n+ 25 fuzz"), ("rvasm.py", "assembler\n→ ROM IMEM"),
         ("Logisim", "chạy không\ngiao diện"), ("so với rvsim.py", "golden model\nđộc lập")]
for i, (h, sub) in enumerate(chain):
    x = 0.55 + i * 3.1
    box(s, x, 1.0, 2.65, 1.35, TINT_RED if i == 3 else TINT_GRAY)
    text(s, x + 0.1, 1.05, 2.45, 1.25, [{"runs": [C(h, size=15, bold=True, color=RED)], "space_after": 4,
                                         "align": PP_ALIGN.CENTER}] +
         [{"runs": [(ln, {})], "size": 13, "space_after": 0, "align": PP_ALIGN.CENTER} for ln in sub.split("\n")])
    if i < 3:
        arrow(s, x + 2.7, 1.5, 0.35, 0.35)
text(s, 0.55, 2.6, 12.2, 0.5, ["So sánh: 31 thanh ghi · 16 KiB RAM · chuỗi TTY · GPIO_OUT · cycles · instret"],
     size=15, color=DARK)
res = [("12/12", "chương trình test PASS"), ("25/25", "chương trình fuzz PASS"),
       (VEC_TOTAL[0].split("/")[0], "test vector đạt"), ("1.00", "CPI: " + NUM["resTotSC"] + " lệnh = "
                                                         + NUM["resTotSC"] + " chu kỳ")]
for i, (big, small) in enumerate(res):
    x = 0.55 + i * 3.1
    text(s, x, 3.35, 2.9, 0.8, [{"runs": [B(big)]}], size=40, color=RED)
    text(s, x, 4.15, 2.9, 0.6, [small], size=13, color=MUTED)
box(s, 0.55, 4.95, 8.9, 1.25, TINT_GRAY)
text(s, 0.75, 5.0, 8.5, 1.15, [
    {"runs": [B("demo.s nạp sẵn trong ROM: "), (f"{demo_row[0]} lệnh, {demo_row[1]} chu kỳ trên SC. "
                                                "Kết thúc: TTY in ", {}), C("Hello RISC-V!"),
              (", a0 = ", {}), C("0xE8"), (", LED 7 đoạn hiện ", {}), C("00E8"), (", 8 LED sáng.", {})]},
], size=15, anchor=MSO_ANCHOR.MIDDLE)

# ---------------------------------------------------------------- S14 phần 3
divider_slide("PHẦN 3", "PIPELINE 5 TẦNG VÀ HAZARD", "Nguyễn Đức Anh · 10 phút", [
    "Chia datapath thành IF, ID, EX, MEM, WB với 4 thanh ghi pipeline",
    "Data hazard, control hazard và kết quả so với SC, NH",
])

# ---------------------------------------------------------------- S15 pipeline datapath
s = content_slide("Datapath pipeline 5 tầng")
picture(s, IMG / "RV32I_Pipeline.png", 0.55, 2.0, 12.2, 4.05, left=True)
chips = [("4 thanh ghi pipeline", "IF/ID, ID/EX, EX/MEM, MEM/WB"),
         ("Flush = nạp 0", "lệnh 0 là NOP, thành bubble"),
         (f"Chu kỳ {NUM['resTPipe']} ps", f"giả định; lý tưởng {NUM['resIdealSpeedup']}× so với SC"),
         ("Pipeline Monitor", "PC, lệnh từng tầng, Stall, FwdA/B")]
for i, (h, sub) in enumerate(chips):
    x = 0.55 + i * 3.08
    box(s, x, 0.95, 2.95, 0.9, TINT_RED)
    text(s, x + 0.1, 0.97, 2.8, 0.86, [{"runs": [B(h)], "color": RED, "space_after": 1}, sub], size=13,
         anchor=MSO_ANCHOR.MIDDLE, space_after=0)

# ---------------------------------------------------------------- S16 data hazard
s = content_slide("Data hazard: forwarding, bypass và stall")
cards = [
    ("ForwardUnit", "cách 1–2 lệnh", ["add x5, x1, x2", "sub x6, x5, x3"],
     ["FwdA = 01: lấy từ EX/MEM", "FwdA = 10: lấy từ MEM/WB", "điều kiện rd ≠ 0, EX/MEM ưu tiên", "0 chu kỳ mất"]),
    ("IDBypass", "cách 3 lệnh", ["add x5, x1, x2", "…  (2 lệnh)", "or  x7, x5, x4"],
     ["WB ghi ở cạnh lên cuối chu kỳ", "ID đọc trong chu kỳ → giá trị cũ", "bypass W_data vào ID", "0 chu kỳ mất"]),
    ("HazardUnit", "load-use", ["lw   x5, 0(x1)", "addi x6, x5, 1"],
     ["dữ liệu chỉ có cuối tầng MEM", "giữ PC và IF/ID, bubble vào ID/EX", "dùng UseRs1, UseRs2 tránh stall oan",
      "1 chu kỳ stall"]),
]
for i, (h, sub, code, pts) in enumerate(cards):
    x = 0.55 + i * 4.12
    box(s, x, 0.95, 3.92, 3.6, TINT_GRAY)
    text(s, x + 0.15, 1.02, 3.6, 0.8, [{"runs": [C(h, size=18, bold=True, color=RED)], "space_after": 0},
                                       {"runs": [(sub, {"color": MUTED})], "size": 13}])
    box(s, x + 0.15, 1.85, 3.62, 1.15, WHITE, shape=MSO_SHAPE.RECTANGLE)
    text(s, x + 0.25, 1.88, 3.45, 1.1, [{"runs": [C(c, size=13)], "space_after": 1} for c in code],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.15, 3.15, 3.65, 2.3, [{"runs": [(p, {"bold": j == 3, "color": RED if j == 3 else DARK})],
                                         "bullet": j < 3} for j, p in enumerate(pts)], size=14, space_after=5)
box(s, 0.55, 4.8, 9.4, 0.7, TINT_RED)
text(s, 0.7, 4.82, 9.2, 0.66, [{"runs": [C("LoadUse = E_MemRead & (E_rd≠0) & ((E_rd=rs1 & UseRs1) | (E_rd=rs2 & "
                                         "UseRs2))", size=13, bold=True)]}], anchor=MSO_ANCHOR.MIDDLE)

# ---------------------------------------------------------------- S17 control hazard + giản đồ
s = content_slide("Control hazard và giản đồ pipeline")
text(s, 0.55, 0.95, 4.5, 4.0, [
    {"runs": [B("Đoán không nhảy: "), ("luôn nạp PC + 4", {})], "bullet": True},
    {"runs": [B("Quyết định ở EX: "), ("Redirect khi Taken, Jal hoặc Jalr", {})], "bullet": True},
    {"runs": [B("Nhảy: "), ("flush IF/ID và ID/EX, mất 2 chu kỳ", {})], "bullet": True},
    {"runs": [B("Redirect thắng Stall: "), ("lệnh đang chờ nằm trên nhánh sai", {})], "bullet": True},
    {"runs": [B("EBREAK: "), ("stall ở ID, dừng khi tới WB", {})], "bullet": True},
], size=15, space_after=9)
box(s, 0.55, 4.55, 4.5, 1.5, TINT_RED)
text(s, 0.7, 4.62, 4.25, 1.65, [
    {"runs": [B("Số chu kỳ của PL")], "color": RED, "space_after": 4},
    {"runs": [C("cycles = N + 4", size=14, bold=True)], "space_after": 0},
    {"runs": [C("       + số lần load-use", size=14, bold=True)], "space_after": 0},
    {"runs": [C("       + 2 × số lần nhảy", size=14, bold=True)], "space_after": 0},
], size=14)
# Giản đồ: đọc từ latex/generated/t06_pl.tex
diag = []
for line in (GEN / "t06_pl.tex").read_text("utf-8").splitlines():
    if not (line.startswith("\\texttt") or line.startswith("\\textcolor")):
        continue
    cells = [c.strip() for c in line.rstrip("\\ ").split("&")]
    instr = re.sub(r"\\textcolor\{gray\}\{(.*)\}", r"\1", cells[0])
    instr = re.sub(r"\\texttt\{(.*?)\}", r"\1", instr)
    stages = []
    for c in cells[1:15]:
        m = re.search(r"\\cellcolor\{c(\w+)\}\\tiny (\w+)", c)
        stages.append((m.group(1), m.group(2)) if m else None)
    diag.append((instr, stages, cells[15]))
ncyc = 14
rows = [["Lệnh"] + [str(i) for i in range(1, ncyc + 1)]]
fills = {}
for i, (instr, stages, note) in enumerate(diag, start=1):
    row = [instr]
    for j, st in enumerate(stages, start=1):
        row.append(st[1] if st else "")
        if st:
            fills[(i, j)] = RGBColor.from_string(STAGE[st[0]])
        else:
            fills[(i, j)] = WHITE
    fills[(i, 0)] = WHITE
    rows.append(row)
t = table(s, 5.35, 0.95, 7.45, rows, [2.2] + [0.375] * ncyc, size=10, row_h=0.36, fills=fills,
          fonts={0: MONO}, aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.CENTER] * ncyc)
for i, (instr, stages, note) in enumerate(diag, start=1):
    if "flush" in note:
        for r in t.cell(i, 0).text_frame.paragraphs[0].runs:
            r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
legend = [("IF", "IF"), ("ID", "ID"), ("EX", "EX"), ("ME", "MEM"), ("WB", "WB"), ("ST", "stall ở ID")]
for i, (k, lbl) in enumerate(legend):
    x = 5.35 + i * 1.12
    box(s, x, 4.75, 0.28, 0.28, RGBColor.from_string(STAGE[k]), shape=MSO_SHAPE.RECTANGLE, line=LINE)
    text(s, x + 0.32, 4.7, 0.85, 0.4, [lbl], size=11, color=MUTED)
text(s, 5.35, 5.15, 4.3, 1.1, [
    "7 lệnh đầu của t06_hazard.s trên PL: 3 lần stall load-use, beq nhảy nên 2 lệnh xám bị flush. "
    "Bảy lệnh chiếm 14 chu kỳ; trên NH cùng đoạn cần 17 chu kỳ."], size=13, color=MUTED)

# ---------------------------------------------------------------- S18 kết quả
s = content_slide("Kết quả ba phiên bản trên 12 chương trình")
cd = CategoryChartData()
cd.categories = [n.replace(".s", "") for n, _ in TIMES]
cd.add_series("SC / NH", [float(r[3]) for _, r in TIMES])
cd.add_series("SC / PL", [float(r[4]) for _, r in TIMES])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.45), Inches(0.95), Inches(8.2), Inches(4.95), cd)
ch = gf.chart
ch.has_title = True
ch.chart_title.text_frame.text = "Tăng tốc so với SC theo giả định trễ (lần)"
for r in ch.chart_title.text_frame.paragraphs[0].runs:
    style_run(r, 14, DARK, True)
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.TOP
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(12)
ch.legend.font.name = BODY
for ser, col in zip(ch.series, (RGBColor(0xBF, 0xBF, 0xBF), RED)):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = col
ch.plots[0].gap_width = 60
ch.plots[0].overlap = -10
ca = ch.category_axis
ca.tick_labels.font.size = Pt(10)
ca.tick_labels.font.name = BODY
ca.tick_labels.font.color.rgb = MUTED
ca.format.line.color.rgb = LINE
va = ch.value_axis
va.maximum_scale = 4.0
va.minimum_scale = 0
va.major_unit = 1.0
va.tick_labels.font.size = Pt(10)
va.tick_labels.font.name = BODY
va.tick_labels.font.color.rgb = MUTED
va.major_gridlines.format.line.color.rgb = RGBColor(0xE6, 0xE6, 0xE6)
va.format.line.fill.background()
kpis = [(NUM["resSpeedPL"] + "×", "PL so với SC (lý tưởng " + NUM["resIdealSpeedup"] + "×)"),
        (NUM["resSpeedPLNH"] + "×", "PL ít chu kỳ hơn NH, cùng clock"),
        (NUM["resTotCPI"], "CPI của PL; NH là " + NUM["resTotCPINH"] + " (kể cả nop)"),
        (str(2 * int(NUM["resTotBR"])), "chu kỳ flush, so với " + NUM["resTotLU"] + " chu kỳ load-use")]
for i, (big, small) in enumerate(kpis):
    y = 0.95 + i * 1.0
    text(s, 8.95, y, 3.6, 0.55, [{"runs": [B(big)]}], size=28, color=RED)
    text(s, 8.95, y + 0.52, 3.6, 0.45, [small], size=12, color=MUTED)
text(s, 0.55, 5.95, 8.5, 0.4, ["Chu kỳ clock theo giả định trễ: SC 800 ps, NH và PL 220 ps (không phải số đo)"],
     size=11, color=MUTED)

# ---------------------------------------------------------------- S19 hạn chế, hướng phát triển
s = content_slide("Hạn chế và hướng phát triển")
text(s, 0.55, 0.95, 5.9, 0.45, [{"runs": [B("Hạn chế")]}], size=20, color=RED)
text(s, 0.55, 1.5, 5.9, 4.8, [
    {"runs": [B("Nhảy quyết định ở EX: "), (f"flush 2 × {NUM['resTotBR']} chu kỳ trên 12 chương trình, nhiều hơn "
                                            f"{NUM['resTotLU']} chu kỳ load-use", {})], "bullet": True},
    {"runs": [B("Không exception, ngắt, CSR: "), ("ECALL/EBREAK làm lệnh dừng; UART phải hỏi vòng", {})],
     "bullet": True},
    {"runs": [B("Truy cập lệch "), ("(lw ở địa chỉ không chia hết cho 4) không hỗ trợ", {})], "bullet": True},
    {"runs": [B("I/O giải mã thiếu: "), ("mọi địa chỉ 0xFxxx_xxxx khác là bí danh của 8 thanh ghi I/O", {})],
     "bullet": True},
    {"runs": [B("Thời gian là giả định: "), ("Logisim không mô phỏng trễ cổng", {})], "bullet": True},
], size=15, space_after=10)
text(s, 6.85, 0.95, 5.95, 0.45, [{"runs": [B("Hướng phát triển")]}], size=20, color=RED)
fut = [("Quyết định nhánh ở ID", f"phạt nhảy 2 → 1 chu kỳ; t09 tiết kiệm tối đa {NUM['resNineBR']} chu kỳ"),
       ("Dự đoán nhánh 2 bit + BTB", "giảm flush ở vòng lặp; đo bằng số lần E_Redirect"),
       ("Phần mở rộng M", "MUL/DIV thay vòng nhân dịch-cộng trong t09_recursion.s"),
       ("Ngắt và CSR", "UART nhận ký tự không cần hỏi vòng")]
for i, (h, sub) in enumerate(fut):
    y = 1.5 + i * 1.05
    box(s, 6.85, y, 5.95, 0.92, TINT_RED if i == 0 else TINT_GRAY)
    circle_num(s, 7.0, y + 0.18, 0.55, str(i + 1), RED if i == 0 else MUTED, 14)
    text(s, 7.7, y + 0.03, 5.0, 0.88, [{"runs": [B(h)], "space_after": 2}, {"runs": [(sub, {})], "size": 13}],
         size=15)

# ---------------------------------------------------------------- S20 cảm ơn: đưa xuống cuối
thanks = prs.slides[1]
for shp in thanks.shapes:
    if shp.has_text_frame and shp.text_frame.text.startswith("THANK"):
        shp.text_frame.paragraphs[0].runs[0].text = "CẢM ƠN THẦY VÀ CÁC BẠN!"
        for extra in shp.text_frame.paragraphs[0].runs[1:]:
            extra.text = ""
        shp.text_frame.paragraphs[0].runs[0].font.size = Pt(40)
        shp.left, shp.width = Inches(3.2), Inches(9.6)
text(thanks, 3.75, 3.75, 8.5, 0.6, ["Hỏi đáp · Demo trực tiếp trên Logisim · Video: demo/demo_RV32I.mp4"],
     size=18, color=DARK)
ids = prs.slides._sldIdLst
el = ids[1]
ids.remove(el)
ids.append(el)

assert len(prs.slides) <= 20, len(prs.slides)

# ---------------------------------------------------------------- lời thoại: slides/kich_ban.src.md → speaker notes
SUBS = dict(NUM, vecSC=VEC_TOTAL[0], vecPL=VEC_TOTAL[1], flushTot=str(2 * int(NUM["resTotBR"])))
src = SCRIPT_SRC.read_text("utf-8").format_map(SUBS)
head, *blocks = re.split(r"^## Slide (\d+) · .*$", src, flags=re.M)
notes = {int(blocks[i]): blocks[i + 1].strip() for i in range(0, len(blocks), 2)}
assert sorted(notes) == list(range(1, len(prs.slides) + 1)), sorted(notes)
for i, sl in enumerate(prs.slides, start=1):
    # nối các dòng bị ngắt cứng trong file nguồn thành đoạn liền, giữ dòng trống giữa các đoạn
    paras = [" ".join(par.split()) for par in notes[i].split("\n\n")]
    sl.notes_slide.notes_text_frame.text = "\n\n".join(paras)
SCRIPT_OUT.write_text(src.replace(head, re.sub(r"Nguồn của speaker notes[^\n]*\n[^\n]*\n[^\n]*\n",
                                                 "Bản đã thay số liệu, sinh từ kich_ban.src.md. Lời thoại giống speaker "
                                                 "notes trong RV32I_ThuyetTrinh.pptx.\n\n", head), 1), "utf-8")

prs.save(OUT)
print(f"{OUT} : {len(prs.slides)} slide")
