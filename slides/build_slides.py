"""Dựng deck thuyết trình RV32I trên template PowerPoint của HUST.

Chạy:  python slides/build_slides.py
Đầu vào: slides/template/HUST_PPT_TEMPLATE_2026_16x9.pptx; ảnh mạch slides/img/*.png (render lại từ file .circ bằng
generator/inspect/Inspect.java, đã cắt khối ghi chú) và docs/img/RV32I_*.png; số liệu đọc từ latex/generated/*.tex
(sinh bởi latex/scripts/gen_results.py) và từ bảng trong latex/chapters/06_kiem_thu.tex, không gõ tay.
Lời thoại (speaker notes) lấy từ slides/kich_ban.src.md.
Đầu ra:  slides/RV32I_ThuyetTrinh.pptx và slides/KICH_BAN.md (kịch bản đã thay số liệu).
Mọi chữ trong deck dùng một font: Times New Roman (kể cả theme, bảng, biểu đồ, mã lệnh).
"""
import copy
import re
import shutil
import zipfile
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "slides/template/HUST_PPT_TEMPLATE_2026_16x9.pptx"
OUT = ROOT / "slides/RV32I_ThuyetTrinh.pptx"
SCRIPT_SRC = ROOT / "slides/kich_ban.src.md"
SCRIPT_OUT = ROOT / "slides/KICH_BAN.md"
SIMG = ROOT / "slides/img"
DIMG = ROOT / "docs/img"
GEN = ROOT / "latex/generated"
CH6 = (ROOT / "latex/chapters/06_kiem_thu.tex").read_text("utf-8")

# ---------------------------------------------------------------- số liệu thật
NUM = dict(re.findall(r"\\newcommand\{\\(res\w+)\}\{([^}]*)\}", (GEN / "numbers.tex").read_text("utf-8")))
NUM["resMaxProg"] = NUM["resMaxProg"].replace(chr(92) + "file{", "").rstrip("}").replace(chr(92) + "_", "_")


def read_rows(name):
    rows = []
    for line in (GEN / name).read_text("utf-8").splitlines():
        m = re.match(r"\\texttt\{(.+?)\} & (.+?) \\\\", line)
        if m:
            rows.append((m.group(1).replace("\\_", "_"), [c.strip() for c in m.group(2).split("&")]))
    return rows


CYCLES = read_rows("cycles_table.tex")   # Lệnh, SC, NH, NOP, PL, Load-use, Nhảy, CPI
TIMES = read_rows("time_table.tex")      # SC ns, NH ns, PL ns, SC/NH, SC/PL, NH/PL
CYC_TOTAL = re.search(r"Tổng & (.+?) \\\\", (GEN / "cycles_table.tex").read_text("utf-8")).group(1).split(" & ")
VEC_TOTAL = re.search(r"Tổng & & (\S+) & (\S+) \\\\", CH6).groups()
VEC = {m[0]: (m[1], m[2]) for m in re.findall(r"^\\sig\{(\w+)\} & .+? & (\S+) & (\S+) \\\\", CH6, re.M)}
PASS = [(m[0], re.sub(r"\\texttt\{-\{\}-(\w+)\}", r"--\1", m[1]), m[2], m[3])
        for m in re.findall(r"^(SC|PL|NH) & (.+?) & (.+?) & (.+?) \\\\", CH6, re.M)]
FUZZ = re.search(r"seed (\d+) đến (\d+), mỗi chương trình (\d+) đến (\d+) lệnh", CH6).groups()
RUN_DATE = re.search(r"chạy lại ngày\s+(\S+)", CH6).group(1)
assert len(VEC) == 13 and len(PASS) == 4 and len(CYCLES) == 12, (len(VEC), len(PASS), len(CYCLES))

# ---------------------------------------------------------------- màu, font
RED = RGBColor(0xC0, 0x00, 0x00)
DARK = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x59, 0x59, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TINT_RED = RGBColor(0xFB, 0xE7, 0xE7)
TINT_ORG = RGBColor(0xFD, 0xF0, 0xDC)
TINT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
LINE = RGBColor(0xD9, 0xD9, 0xD9)
FONT = "Times New Roman"

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
    txBody = sp.find(qn("p:txBody"))
    for p in txBody.findall(qn("a:p")):
        txBody.remove(p)
    p = etree.SubElement(txBody, qn("a:p"))
    fld = etree.SubElement(p, qn("a:fld"), id="{9EA0BE3B-158A-4EDF-80DC-E394A0D1600F}", type="slidenum")
    rPr = etree.SubElement(fld, qn("a:rPr"), lang="vi-VN")
    etree.SubElement(rPr, qn("a:latin"), typeface=FONT)
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
    etree.SubElement(pPr, qn("a:buFont"), typeface=FONT)
    etree.SubElement(pPr, qn("a:buChar"), char=char)


def no_bullet(p):
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn("a:buNone")) is None:
        etree.SubElement(pPr, qn("a:buNone"))


def style_run(run, size, color=DARK, bold=False, italic=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = FONT
    f.color.rgb = color


def text(slide, x, y, w, h, paras, size=16, color=DARK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, space_after=6, margin=0.05, name=None):
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
            set_bullet(p, level=para.get("level", 0), color=para.get("bullet_color", RED))
        else:
            no_bullet(p)
        for txt, opts in para["runs"]:
            r = p.add_run()
            r.text = txt
            style_run(r, opts.get("size", para.get("size", size)), opts.get("color", para.get("color", color)),
                      opts.get("bold", para.get("bold", bold)), opts.get("italic", para.get("italic", False)))
    return tb


def B(t, **kw):
    return (t, dict(bold=True, **kw))


def R(t, **kw):
    return (t, kw)


def bl(*runs, **kw):
    """Một đoạn có bullet."""
    return dict(runs=list(runs), bullet=True, **kw)


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


def arrow(slide, x, y, w, h, color=MUTED, shape=MSO_SHAPE.RIGHT_ARROW):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s


def picture(slide, path, x, y, w, h, border=True, align="center"):
    """Đặt ảnh vừa khung (x, y, w, h), giữ tỉ lệ."""
    from PIL import Image
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    px = {"left": x, "center": x + (w - pw) / 2, "right": x + w - pw}[align]
    py = y + (h - ph) / 2
    pic = slide.shapes.add_picture(str(path), Inches(px), Inches(py), Inches(pw), Inches(ph))
    if border:
        pic.line.color.rgb = LINE
        pic.line.width = Pt(0.75)
    return pic


def table(slide, x, y, w, rows, col_w, size=12, header_fill=RED, row_h=0.3, fills=None, aligns=None, bold_cells=None):
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
            cell.margin_top = cell.margin_bottom = Inches(0.01)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if i == 0 and header_fill is not None:
                cell.fill.fore_color.rgb = header_fill
            elif fills and fills.get((i, j)) is not None:
                cell.fill.fore_color.rgb = fills[(i, j)]
            else:
                cell.fill.fore_color.rgb = WHITE if i % 2 else RGBColor(0xFA, 0xFA, 0xFA)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (aligns[j] if aligns else PP_ALIGN.LEFT) if (i or header_fill is None) else PP_ALIGN.CENTER
            r = p.add_run()
            r.text = str(rows[i][j])
            head = i == 0 and header_fill is not None
            style_run(r, size, WHITE if head else DARK, head or bool(bold_cells and (i, j) in bold_cells))
    return tbl


def add_click_sequence(slide, clicks):
    """Hiệu ứng Appear theo click: clicks[k] là danh sách shape cùng hiện ở lần click thứ k+1."""
    P = "http://schemas.openxmlformats.org/presentationml/2006/main"
    ids = iter(range(1, 10000))
    groups = []
    for shapes in clicks:
        effs = []
        for j, shp in enumerate(shapes):
            effs.append(
                f'<p:par><p:cTn id="{next(ids)}" presetID="1" presetClass="entr" presetSubtype="0" fill="hold" '
                f'grpId="0" nodeType="{"clickEffect" if j == 0 else "withEffect"}">'
                '<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:set><p:cBhvr>'
                f'<p:cTn id="{next(ids)}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
                f'<p:tgtEl><p:spTgt spid="{shp.shape_id}"/></p:tgtEl>'
                '<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
                '<p:to><p:strVal val="visible"/></p:to></p:set></p:childTnLst></p:cTn></p:par>')
        groups.append(
            f'<p:par><p:cTn id="{next(ids)}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>'
            f'<p:childTnLst><p:par><p:cTn id="{next(ids)}" fill="hold"><p:stCondLst><p:cond delay="0"/>'
            f'</p:stCondLst><p:childTnLst>{"".join(effs)}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            '</p:par>')
    # id 1, 2 dành cho tmRoot và mainSeq: đánh lại id theo thứ tự xuất hiện
    body = "".join(groups)
    n = iter(range(3, 10000))
    body = re.sub(r'<p:cTn id="\d+"', lambda m: f'<p:cTn id="{next(n)}"', body)
    bld = "".join(f'<p:bldP spid="{shp.shape_id}" grpId="0"/>'
                  for shapes in clicks for shp in shapes if shp.shape_type != 13)  # 13 = PICTURE
    xml = (f'<p:timing xmlns:p="{P}"><p:tnLst><p:par>'
           '<p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
           '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq">'
           f'<p:childTnLst>{body}</p:childTnLst></p:cTn>'
           '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
           '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
           f'</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst>{bld}</p:bldLst></p:timing>')
    sld = slide._element
    ext = sld.find(qn("p:extLst"))
    timing = etree.fromstring(xml)
    if ext is not None:
        ext.addprevious(timing)
    else:
        sld.append(timing)


def content_slide(title):
    s = prs.slides.add_slide(L_CONTENT)
    strip_placeholders(s)
    s.shapes.title.text = title
    for p in s.shapes.title.text_frame.paragraphs:
        for r in p.runs:
            r.font.name = FONT
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
            r.font.name = FONT
    text(s, 1.13, 1.45, 6, 0.6, [{"runs": [B(part)]}], size=22, color=WHITE)
    text(s, 1.13, 3.75, 9.5, 0.5, [who], size=20, color=WHITE)
    tb = text(s, 1.13, 4.45, 9.5, 1.9, [{"runs": [R(i)], "bullet": True} for i in items], size=18,
              color=WHITE, space_after=4)
    for p in tb.text_frame.paragraphs:
        set_bullet(p, color=WHITE)
    return s


def heading(slide, x, y, w, label, size=18):
    return text(slide, x, y, w, 0.42, [{"runs": [B(label)]}], size=size, color=RED)


def parse_diagram(name):
    rows = []
    for line in (GEN / name).read_text("utf-8").splitlines():
        if not re.match(r"\\(texttt|textit|textcolor)", line):
            continue
        cells = [c.strip() for c in line.rstrip("\\ ").split("&")]
        label = re.sub(r"\\textcolor\{gray\}\{(.*)\}", r"\1", cells[0])
        label = re.sub(r"\\text(tt|it)\{(.*?)\}", r"\2", label)
        stages = []
        for c in cells[1:-1]:
            m = re.search(r"\\cellcolor\{c(\w+)\}\\tiny (\w+)", c)
            stages.append((m.group(1), m.group(2)) if m else None)
        rows.append((label, stages, cells[-1], "textcolor{gray}" in cells[0], "textit" in cells[0]))
    return rows


def diagram(slide, x, y, rows, name_w, cell_w, row_h, size=10):
    ncyc = len(rows[0][1])
    data = [["Lệnh"] + [str(i) for i in range(1, ncyc + 1)]]
    fills = {}
    for i, (label, stages, note, gray, ital) in enumerate(rows, start=1):
        data.append([label] + [st[1] if st else "" for st in stages])
        fills[(i, 0)] = WHITE
        for j, st in enumerate(stages, start=1):
            fills[(i, j)] = RGBColor.from_string(STAGE[st[0]]) if st else WHITE
    t = table(slide, x, y, name_w + cell_w * ncyc, data, [name_w] + [cell_w] * ncyc, size=size, row_h=row_h,
              fills=fills, aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.CENTER] * ncyc)
    for j in range(1, ncyc + 1):
        for r in t.cell(0, j).text_frame.paragraphs[0].runs:
            r.font.size = Pt(size)
        for i in range(1, len(data)):
            c = t.cell(i, j)
            c.margin_left = c.margin_right = 0
    for i, (label, stages, note, gray, ital) in enumerate(rows, start=1):
        for r in t.cell(i, 0).text_frame.paragraphs[0].runs:
            if gray:
                r.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
            r.font.italic = ital
    return t


# ---------------------------------------------------------------- bỏ slide mẫu, giữ slide bìa và cảm ơn
sld_ids = prs.slides._sldIdLst
orig = list(sld_ids)
keep_title, keep_thanks = orig[2], orig[14]  # slide 3 (tiêu đề), slide 15 (THANK YOU)
for sid in orig:
    if sid not in (keep_title, keep_thanks):
        prs.part.drop_rel(sid.get(qn("r:id")))
        sld_ids.remove(sid)
from pptx.opc.packuri import PackURI  # noqa: E402
for n, sl in enumerate(prs.slides, start=1):
    sl.part.partname = PackURI(f"/ppt/slides/slide{n}.xml")

# ================================================================ S1 tiêu đề
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
    {"runs": [B("Bài tập lớn Kiến trúc máy tính tiên tiến")]},
    "Nhóm: Quyền Đức Công · Bùi Phạm Sơn Hà · Nguyễn Đức Anh",
    "Giảng viên hướng dẫn: TS. Hoàng Văn Hiệp",
    {"runs": [R("Trường Công nghệ Thông tin và Truyền thông · 11/2026", color=MUTED)]},
], size=18, space_after=4, name="Thông tin nhóm")

# ================================================================ S2 đề bài và sản phẩm
s = content_slide("Đề bài và sản phẩm")
heading(s, 0.55, 0.95, 5.9, "Đề bài yêu cầu")
text(s, 0.55, 1.42, 5.9, 2.9, [
    bl(R("Máy tính 32 bit theo RV32I: dữ liệu, lệnh, thanh ghi, PC 32 bit; 32 thanh ghi")),
    bl(R("Hai phiên bản: đơn chu kỳ và pipeline 5 tầng IF, ID, EX, MEM, WB")),
    bl(R("Pipeline xử lý đúng data hazard và control hazard cơ bản")),
    bl(R("Chạy từ lệnh nạp vào bộ nhớ lệnh, không chỉnh tay thanh ghi")),
    bl(R("Mô phỏng và kiểm thử trên Logisim-evolution")),
], size=16, space_after=6)
heading(s, 6.85, 0.95, 5.95, "Sản phẩm: ba file mạch trong circ/")
files = [("SC", "RV32I_SingleCycle.circ", "CPU đơn chu kỳ, CPI = 1"),
         ("PL", "RV32I_Pipeline.circ", "Pipeline 5 tầng: forwarding, bypass WB→ID, stall load-use, flush khi nhảy"),
         ("NH", "extra/RV32I_Pipeline_NoHazard.circ", "Pipeline bỏ forwarding và stall; assembler chèn nop")]
for i, (tag, f, desc) in enumerate(files):
    y = 1.42 + i * 0.97
    box(s, 6.85, y, 5.95, 0.88, TINT_RED if tag == "PL" else TINT_GRAY)
    circle_num(s, 7.0, y + 0.16, 0.56, tag, RED if tag == "PL" else MUTED, 14)
    text(s, 7.7, y + 0.04, 5.0, 0.82, [{"runs": [B(f)], "space_after": 1}, desc], size=14, space_after=0)
stats = [("37", "lệnh RV32I được hiện thực,\nFENCE giải mã thành NOP"),
         (VEC_TOTAL[1].split("/")[0], f"test vector đạt trên 13 circuit\n(bản PL; bản SC {VEC_TOTAL[0].split('/')[0]})"),
         ("12 + 25", "chương trình test + fuzz PASS\ntrên SC, PL và NH --nohazard"),
         (NUM["resSpeedPL"] + "×", "PL nhanh hơn SC theo giả định\ntrễ 800 ps / 220 ps")]
for i, (big, small) in enumerate(stats):
    x = 0.55 + i * 3.08
    text(s, x, 4.45, 2.95, 0.72, [{"runs": [B(big)]}], size=38, color=RED)
    text(s, x, 5.17, 2.95, 0.8, small.split("\n"), size=13, color=MUTED, space_after=0)
text(s, 0.55, 6.0, 9.6, 0.4, [{"runs": [B("Phần 1 · Hà: "), R("kiến trúc, module   "), B("Phần 2 · Công: "),
                                         R("đơn chu kỳ, kiểm thử   "), B("Phần 3 · Đức Anh: "),
                                         R("pipeline, kết quả")]}], size=14, color=DARK)

# ================================================================ S3 tập lệnh
s = content_slide("Tập lệnh RV32I và định dạng lệnh")
fmt = [["Định dạng", "[31:25]", "[24:20]", "[19:15]", "[14:12]", "[11:7]", "[6:0]"],
       ["R", "funct7", "rs2", "rs1", "funct3", "rd", "opcode"],
       ["I", "imm[11:0]", "", "rs1", "funct3", "rd", "opcode"],
       ["S", "imm[11:5]", "rs2", "rs1", "funct3", "imm[4:0]", "opcode"],
       ["B", "imm[12|10:5]", "rs2", "rs1", "funct3", "imm[4:1|11]", "opcode"],
       ["U", "imm[31:12]", "", "", "", "rd", "opcode"],
       ["J", "imm[20|10:1|11|19:12]", "", "", "", "rd", "opcode"]]
t = table(s, 0.55, 0.95, 7.3, fmt, [1.05, 1.45, 0.85, 0.85, 0.85, 1.25, 1.0], size=13, row_h=0.34,
          aligns=[PP_ALIGN.CENTER] * 7)
t.cell(2, 1).merge(t.cell(2, 2))
for r_ in (5, 6):
    t.cell(r_, 1).merge(t.cell(r_, 4))
text(s, 0.55, 3.5, 7.3, 2.8, [
    bl(B("32 thanh ghi x0–x31: "), R("x0 luôn đọc ra 0, ghi vào x0 bị bỏ qua; phần cứng chỉ cần 31 thanh ghi thật")),
    bl(B("rd, funct3, rs1, rs2 cùng vị trí "), R("trong mọi định dạng: đọc thanh ghi song song với giải mã")),
    bl(B("Bit dấu immediate luôn là bit 31: "), R("mở rộng dấu không cần biết định dạng")),
    bl(B("Lệnh dài 4 byte, PC tăng 4: "), R("ROM, RAM lưu mỗi ô một word, IMEM dùng PC[11:2], DMEM dùng Addr[13:2]")),
], size=15, space_after=7)
heading(s, 8.2, 0.95, 4.6, "37 lệnh được hiện thực")
groups = [("10", "lệnh R"), ("9", "lệnh I số học"), ("5", "lệnh load"), ("3", "lệnh store"), ("6", "rẽ nhánh"),
          ("4", "JAL, JALR, LUI, AUIPC")]
for i, (n, lbl) in enumerate(groups):
    x, y = 8.2 + (i % 2) * 2.33, 1.45 + (i // 2) * 0.82
    box(s, x, y, 2.2, 0.72, TINT_RED)
    text(s, x + 0.08, y, 0.62, 0.72, [{"runs": [B(n)]}], size=24, color=RED, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + 0.66, y, 1.5, 0.72, [lbl], size=13, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
text(s, 8.2, 3.98, 4.6, 2.4, [
    bl(B("FENCE → NOP: "), R("một luồng thực thi, không cache, truy cập RAM và I/O theo đúng thứ tự")),
    bl(B("ECALL, EBREAK → dừng CPU "), R("để bộ test có điểm kết thúc")),
    bl(B("CSR thuộc Zicsr, "), R("không nằm trong RV32I base, không hiện thực")),
], size=14, space_after=6)

# ================================================================ S4 sơ đồ khối và quyết định thiết kế
s = content_slide("Sơ đồ khối và quyết định thiết kế")
blocks = [("IF", "PC → IMEM\n(ROM)"), ("ID", "Control, ImmGen\nRegisterFile"), ("EX", "ALU\nBranchUnit"),
          ("MEM", "DMEM, LoadUnit\nStoreUnit, I/O"), ("WB", "MUX ghi lại\n→ x[rd]")]
for i, (st, body) in enumerate(blocks):
    x = 0.55 + i * 2.5
    box(s, x, 0.98, 2.1, 1.3, RGBColor.from_string(STAGE["ME" if st == "MEM" else st]))
    text(s, x + 0.05, 1.0, 2.0, 1.26, [{"runs": [B(st)], "color": RED, "space_after": 2, "align": PP_ALIGN.CENTER}] +
         [{"runs": [R(ln)], "size": 14, "space_after": 0, "align": PP_ALIGN.CENTER} for ln in body.split("\n")],
         size=16, anchor=MSO_ANCHOR.MIDDLE)
    if i < 4:
        arrow(s, x + 2.14, 1.47, 0.32, 0.32)
text(s, 0.55, 2.38, 12.2, 0.4, ["11 circuit con dùng chung cho SC và PL; PL thêm 4 thanh ghi pipeline và 3 khối xử lý "
                                 "hazard"], size=14, color=MUTED)
dec = [("Kiến trúc Harvard", "IMEM là ROM, DMEM là RAM riêng: nạp lệnh và load/store không tranh một cổng bộ nhớ. "
                              "Đổi lại chương trình không tự sửa mã được."),
       ("ALU tính địa chỉ đích", "Branch, JAL: A = PC; JALR: A = rs1; đích = ALU AND 0xFFFFFFFE. Không cần bộ cộng "
                                 "PC + imm riêng, so sánh làm ở BranchUnit."),
       ("Lệnh 0x00000000 là NOP", "Decoder trong Control chỉ bật khi opcode[1:0] = 11, nên lệnh toàn 0 cho mọi tín "
                                  "hiệu bằng 0. Flush một tầng chỉ cần nạp 0."),
       ("SB, SH: đọc, sửa, ghi", "RAM của Logisim chỉ có byte enable khi đọc đồng bộ, không dùng được cho CPU đơn chu "
                                 "kỳ, nên ghi lại cả word."),
       ("Memory-mapped I/O", "UART và GPIO là vài địa chỉ 0xF000_00xx; CPU dùng lw, sw, lb, sb để điều khiển, không "
                             "cần lệnh mới.")]
for i, (h, body) in enumerate(dec):
    x = 0.55 + i * 2.48
    box(s, x, 2.95, 2.33, 3.35, TINT_GRAY)
    circle_num(s, x + 0.12, 3.07, 0.45, str(i + 1), RED, 14)
    text(s, x + 0.12, 3.6, 2.12, 2.65, [{"runs": [B(h)], "color": RED, "size": 15, "space_after": 5}, body],
         size=13, space_after=0)

# ================================================================ S5 phần 1
divider_slide("PHẦN 1", "THIẾT KẾ CÁC MODULE", "Bùi Phạm Sơn Hà", [
    "18 circuit con: 11 dùng chung, 7 chỉ có ở pipeline",
    "ALU, Control, ImmGen, RegisterFile, BranchUnit, bộ nhớ và I/O",
])

# ================================================================ S6 18 circuit con
s = content_slide("18 circuit con và test vector")
mods =[("Control", "opcode → mọi tín hiệu điều khiển", TINT_RED),
        ("ImmGen", "ghép immediate I, S, B, U, J", TINT_RED),
        ("ALUControl", "ALUOp, funct3, bit 30 → ALUCtrl", TINT_RED),
        ("RegisterFile", "x1–x31, 2 cổng đọc, 1 cổng ghi", TINT_ORG),
        ("ALU", "10 phép tính song song + MUX", TINT_ORG),
        ("BranchUnit", "so sánh rs1, rs2 → Taken", TINT_ORG),
        ("AddrDecode", "tách WordAddr, Off, IsIO", TINT_GRAY),
        ("LoadUnit", "LB, LH, LW, LBU, LHU", TINT_GRAY),
        ("StoreUnit", "SB, SH, SW: đọc, sửa, ghi", TINT_GRAY),
        ("IOController", "UART và GPIO memory-mapped", TINT_GRAY),
        ("PerfCounters", "đếm cycles và instret", TINT_GRAY),
        ("ForwardUnit", "FwdA, FwdB: forward từ EX/MEM, MEM/WB", RED),
        ("HazardUnit", "load-use stall, flush khi nhảy", RED),
        ("IDBypass", "bypass dữ liệu WB → ID", RED),
        ("IF_ID, ID_EX, EX_MEM, MEM_WB", "4 thanh ghi pipeline", RED)]
for i, (name, role, fill) in enumerate(mods):
    x, y = 0.55 + (i % 5) * 2.46, 0.95 + (i // 5) * 1.6
    box(s, x, y, 2.34, 1.48, fill)
    col = WHITE if fill == RED else DARK
    text(s, x + 0.1, y + 0.06, 2.16, 1.38, [
        {"runs": [B(name, color=WHITE if fill == RED else RED)], "size": 14 if len(name) < 20 else 12,
         "space_after": 3},
        {"runs": [R(role)], "size": 13},
    ], color=col)
legend = [("Giải mã", TINT_RED), ("Thực thi", TINT_ORG), ("Bộ nhớ, I/O, bộ đếm", TINT_GRAY), ("Chỉ có ở PL", RED)]
for i, (lbl, c) in enumerate(legend):
    box(s, 0.55 + i * 2.5, 5.82, 0.28, 0.28, c, radius=0.2)
    text(s, 0.9 + i * 2.5, 5.77, 2.1, 0.4, [lbl], size=13, color=MUTED)
text(s, 0.55, 6.12, 9.4, 0.5, [f"13 circuit có file test vector: {VEC_TOTAL[0]} trên SC, {VEC_TOTAL[1]} trên PL. "
                                 "PerfCounters và 4 thanh ghi pipeline được kiểm tra qua chương trình chạy trên toàn CPU."],
     size=13, color=MUTED)

# ================================================================ S7 ALU
s = content_slide("ALU và ALUControl")
picture(s, SIMG / "ALU.png", 0.55, 0.95, 5.6, 5.35, align="left")
text(s, 6.5, 0.95, 6.3, 3.6, [
    bl(B("Tính song song rồi chọn: "), R("Adder, Subtractor, 2 Comparator (có dấu, không dấu), 3 cổng logic, "
                                         "3 Shifter")),
    bl(B("MUX 8:1 theo ALUCtrl[2:0] = funct3; "), R("hai MUX 2:1 theo ALUCtrl[3] chọn ADD/SUB, SRL/SRA")),
    bl(B("Lượng dịch "), R("lấy 5 bit thấp của B; SLT, SLTU mở rộng 0 kết quả 1 bit lên 32 bit")),
    bl(B("Bẫy ADDI âm: "), R("với lệnh I, bit 30 thuộc immediate (addi x1, x1, -1024 có bit 30 = 1). ALUControl chỉ "
                             "lấy bit 30 khi lệnh là R hoặc SRAI; t01_alu.s kiểm tra lỗi này")),
], size=15, space_after=8)
heading(s, 6.5, 4.55, 6.3, "Mã ALUCtrl", size=15)
table(s, 6.5, 4.98, 6.25, [
    ["0000", "1000", "0001", "0010", "0011"],
    ["ADD", "SUB", "SLL", "SLT", "SLTU"],
    ["0100", "0101", "1101", "0110", "0111"],
    ["XOR", "SRL", "SRA", "OR", "AND"],
], [1.25] * 5, size=14, header_fill=None, row_h=0.32, aligns=[PP_ALIGN.CENTER] * 5,
    fills={(0, j): TINT_RED for j in range(5)} | {(2, j): TINT_RED for j in range(5)})

# ================================================================ S8 Control, ImmGen
s = content_slide("Control và ImmGen")
ctrl = [["Nhóm", "opcode", "RW", "ASel", "BSel", "ALUOp", "Imm", "MR", "MW", "WB", "B/J/Jr"],
        ["OP (R)", "0110011", "1", "0", "0", "10", "–", "0", "0", "0", "0/0/0"],
        ["OP-IMM", "0010011", "1", "0", "1", "11", "0", "0", "0", "0", "0/0/0"],
        ["LOAD", "0000011", "1", "0", "1", "00", "0", "1", "0", "1", "0/0/0"],
        ["STORE", "0100011", "0", "0", "1", "00", "1", "0", "1", "–", "0/0/0"],
        ["BRANCH", "1100011", "0", "1", "1", "00", "2", "0", "0", "–", "1/0/0"],
        ["JAL", "1101111", "1", "1", "1", "00", "4", "0", "0", "2", "0/1/0"],
        ["JALR", "1100111", "1", "0", "1", "00", "0", "0", "0", "2", "0/0/1"],
        ["LUI", "0110111", "1", "2", "1", "00", "3", "0", "0", "0", "0/0/0"],
        ["AUIPC", "0010111", "1", "1", "1", "00", "3", "0", "0", "0", "0/0/0"],
        ["SYSTEM", "1110011", "Halt = 1, các tín hiệu khác bằng 0", "", "", "", "", "", "", "", ""]]
t = table(s, 0.55, 0.95, 7.25, ctrl, [1.0, 0.9, 0.5, 0.58, 0.58, 0.78, 0.52, 0.5, 0.52, 0.5, 0.87], size=13,
          row_h=0.34, aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.CENTER] * 10)
t.cell(10, 2).merge(t.cell(10, 10))
text(s, 0.55, 4.8, 7.25, 1.5, [
    "RW = RegWrite, Imm = ImmSel, MR = MemRead, MW = MemWrite, WB = WBSel, B/J/Jr = Branch/Jal/Jalr.",
    "ASel: 0 = rs1, 1 = PC, 2 = hằng 0. WBSel: 0 = kết quả ALU, 1 = dữ liệu bộ nhớ, 2 = PC + 4.",
], size=12, color=MUTED, space_after=2)
heading(s, 8.15, 0.95, 4.65, "Control")
text(s, 8.15, 1.4, 4.65, 2.4, [
    bl(R("Decoder 5→32 theo opcode[6:2], enable = opcode[1] AND opcode[0]; mỗi tín hiệu là OR của các nhóm cần nó")),
    bl(R("Lệnh 0x00000000 cho mọi tín hiệu bằng 0, tức là NOP")),
    bl(R("UseRs1, UseRs2: không stall oan khi trường rs1 của LUI, JAL trùng rd của lệnh load")),
], size=14, space_after=5)
heading(s, 8.15, 3.75, 4.65, "ImmGen")
text(s, 8.15, 4.2, 4.65, 2.2, [
    bl(R("8 mảnh bit vị trí cố định → ghép I, S, B, U, J → mở rộng dấu → MUX theo ImmSel")),
    bl(R("Offset B, J là bội của 2: không mã hóa bit 0, ImmGen nối hằng 0. Bit 1 vẫn mã hóa để dùng chung với phần "
         "mở rộng C (lệnh nén 2 byte)")),
], size=14, space_after=5)

# ================================================================ S9 RegisterFile, BranchUnit
s = content_slide("RegisterFile và BranchUnit")
picture(s, SIMG / "RegisterFile.png", 0.55, 0.95, 6.1, 3.45)
picture(s, SIMG / "BranchUnit.png", 6.95, 0.95, 5.85, 3.45)
text(s, 0.55, 4.6, 6.1, 1.8, [
    bl(B("31 thanh ghi thật x1–x31: "), R("đầu vào 0 của MUX đọc nối hằng 0, nên x0 luôn đọc ra 0")),
    bl(B("Ghi: "), R("Decoder 5→32 bật enable của đúng x[rd], chụp ở cạnh lên")),
    bl(B("Không bypass bên trong: "), R("addi x1, x1, 1 trên SC sẽ thành vòng tổ hợp; PL dùng IDBypass bên ngoài")),
], size=14, space_after=5)
text(s, 6.95, 4.6, 5.85, 1.8, [
    bl(B("2 Comparator: "), R("không dấu (bằng, nhỏ hơn) và có dấu")),
    bl(B("MUX theo funct3[2:1]: "), R("00 bằng, 10 nhỏ hơn có dấu, 11 nhỏ hơn không dấu")),
    bl(B("XOR funct3[0] "), R("cho BNE, BGE, BGEU; AND với Branch ra Taken")),
], size=14, space_after=5)

# ================================================================ S10 bộ nhớ, I/O, bộ đếm
s = content_slide("Bộ nhớ, I/O và bộ đếm")
memmap = [["Vùng", "Địa chỉ", "Ghi chú"],
          ["IMEM (ROM)", "0x0000_0000–0FFF", "1024 lệnh, ô = PC[11:2]"],
          ["DMEM (RAM)", "0x0000_0000–3FFF", "16 KiB, ô = Addr[13:2]"],
          ["Vùng dump test", "0x0000_0700–077F", "x1–x31 lưu tại 0x704–0x77C"],
          ["UART_TXDATA", "0xF000_0000 (ghi)", "ký tự ra TTY"],
          ["UART_RXDATA", "0xF000_0004 (đọc)", "ký tự từ Keyboard"],
          ["UART_STATUS", "0xF000_0008 (đọc)", "bit 0 có ký tự, bit 1 TX sẵn sàng"],
          ["GPIO_OUT", "0xF000_0010", "[15:0] LED 7 đoạn, [23:16] 8 LED"],
          ["GPIO_IN", "0xF000_0014 (đọc)", "8 công tắc DIP"]]
table(s, 0.55, 0.95, 6.35, memmap, [1.55, 1.95, 2.85], size=13, row_h=0.33)
text(s, 0.55, 4.05, 6.35, 2.4, [
    bl(B("AddrDecode: "), R("IsIO = (Addr[31:28] = 0xF); RamWE = MemWrite AND NOT IsIO")),
    bl(B("LoadUnit: "), R("dịch phải Off×8 bit, mở rộng dấu hoặc 0, chọn theo funct3")),
    bl(B("IOController: "), R("KbdRE AND MemRead, nếu không một lệnh add ra 0xF0000004 cũng làm mất ký tự")),
    bl(B("PerfCounters: "), R("cycles khi chưa halt, instret khi lệnh hoàn thành (bubble không đếm)")),
], size=14, space_after=4)
picture(s, SIMG / "StoreUnit.png", 7.2, 0.95, 5.6, 1.85)
box(s, 7.2, 3.0, 5.6, 3.3, TINT_RED)
text(s, 7.4, 3.08, 5.25, 3.15, [
    {"runs": [B("StoreUnit: đọc, sửa, ghi cả word")], "color": RED, "size": 16, "space_after": 6},
    {"runs": [R("mask = 0xFF (SB), 0xFFFF (SH), 0xFFFFFFFF (SW)")], "space_after": 2},
    {"runs": [B("M = mask << (Off × 8)")], "space_after": 2},
    {"runs": [B("New = (Old AND NOT M) OR ((WData << Off×8) AND M)")], "size": 14, "space_after": 8},
    {"runs": [R("Ví dụ: sb 0xAB vào offset 2 của word 0x11223344")], "space_after": 2},
    {"runs": [R("→ M = 0x00FF0000, word mới "), B("0x11AB3344")]},
], size=15)

# ================================================================ S11 phần 2
divider_slide("PHẦN 2", "CPU ĐƠN CHU KỲ VÀ KIỂM THỬ", "Quyền Đức Công", [
    "Ghép 11 module thành datapath, mỗi lệnh xong trong 1 chu kỳ",
    "Một lệnh lw đi qua mạch; next-PC, halt và đường găng",
    "Toolchain, golden model và kết quả kiểm thử",
])

# ================================================================ S12 datapath SC
s = content_slide("Datapath đơn chu kỳ")
# Ảnh top-level cắt thành 5 khung cùng kích thước (px trên RV32I_SingleCycle.png), mỗi khung ôm cụm khối của một tầng.
# Năm ảnh đặt chồng cùng một chỗ; mỗi click hiện ảnh của tầng kế tiếp (đè lên ảnh trước) cùng lời giải thích.
SC_CROP_W, SC_CROP_H = 620, 940
steps = [("IF", "Nạp lệnh", "PC → IMEM (PC[11:2]) ra instr; song song bộ cộng tính PC + 4", (90, 130)),
         ("ID", "Giải mã, đọc thanh ghi", "Control sinh tín hiệu điều khiển; RegisterFile đọc rs1, rs2; "
                                         "ImmGen tạo immediate", (670, 130)),
         ("EX", "Thực thi", "ALU: A = rs1, PC hoặc 0; B = rs2 hoặc imm. BranchUnit so sánh rs1, rs2",
          (1240, 130)),
         ("MEM", "Truy cập bộ nhớ", "StoreUnit ghép dữ liệu ghi; RAM ghi ở cạnh lên clock; LoadUnit tách dữ liệu đọc",
          (1680, 290)),
         ("WB", "Ghi lại", "MUX WBSel chọn kết quả ALU, dữ liệu load hoặc PC + 4 → x[rd]", (2200, 290))]
from PIL import Image  # noqa: E402
sc_full = Image.open(DIMG / "RV32I_SingleCycle.png").convert("RGB")
pic_h = 5.6
pic_w = pic_h * SC_CROP_W / SC_CROP_H
clicks = []
for i, (st, name, desc, (cx, cy)) in enumerate(steps):
    crop = SIMG / f"SC_{st}.png"
    sc_full.crop((cx, cy, cx + SC_CROP_W, cy + SC_CROP_H)).save(crop)
    pic = picture(s, crop, 0.55, 0.95, pic_w, pic_h)
    y = 0.95 + i * 1.13
    c = circle_num(s, pic_w + 0.95, y + 0.14, 0.75, st, RED, 15 if len(st) < 3 else 13)
    # mép phải 10.3": tránh họa tiết sóng của template ở góc phải dưới
    t = text(s, pic_w + 1.9, y, 10.3 - pic_w - 1.9, 1.05, [
        {"runs": [B(name, color=RED)], "size": 17, "space_after": 2},
        {"runs": [R(desc.replace("PC + 4", "PC\u00a0+\u00a04"))], "size": 15},  # không ngắt dòng giữa "PC + 4"
    ], anchor=MSO_ANCHOR.MIDDLE)
    clicks.append([pic, c, t])
add_click_sequence(s, clicks)

# ================================================================ S13 ví dụ lw
s = content_slide("Ví dụ: lw t4, 8(sp) trong một chu kỳ")
fields = [("imm[11:0]", "000000001000", "= 8", 3.4), ("rs1", "00010", "x2 (sp)", 1.7), ("funct3", "010", "LW", 1.3),
          ("rd", "11101", "x29 (t4)", 1.7), ("opcode", "0000011", "LOAD", 2.3)]
x = 0.55
text(s, 0.55, 0.95, 12.2, 0.4, [{"runs": [R("Mã máy "), B("0x00812E83", color=RED)]}], size=20)
for name, bits, meaning, w in fields:
    w = w * 12.2 / 10.4
    box(s, x, 1.5, w - 0.08, 1.2, TINT_RED, shape=MSO_SHAPE.RECTANGLE)
    text(s, x, 1.52, w - 0.08, 1.15, [
        {"runs": [R(name, color=MUTED)], "size": 13, "space_after": 2, "align": PP_ALIGN.CENTER},
        {"runs": [B(bits)], "size": 18, "space_after": 2, "align": PP_ALIGN.CENTER},
        {"runs": [B(meaning, color=RED)], "size": 14, "align": PP_ALIGN.CENTER},
    ])
    x += w
flow = [("Control", "nhóm LOAD\nRegWrite = 1\nBSel = 1 (imm)\nMemRead = 1\nWBSel = 1"),
        ("ALU", "A = sp, B = 8\nY = sp + 8"),
        ("AddrDecode", "IsIO = 0\n→ đọc DMEM"),
        ("LoadUnit", "funct3 = 010\nlấy cả word"),
        ("Ghi lại", "t4 ← M[sp + 8]\nPC ← PC + 4")]
for i, (h, body) in enumerate(flow):
    x = 0.55 + i * 2.45
    box(s, x, 3.1, 2.1, 1.95, TINT_GRAY)
    text(s, x + 0.08, 3.15, 1.95, 1.85, [{"runs": [B(h)], "color": RED, "size": 17, "space_after": 6}] +
         [{"runs": [R(ln)], "size": 14, "space_after": 2} for ln in body.split("\n")])
    if i < 4:
        arrow(s, x + 2.13, 3.9, 0.28, 0.35)
text(s, 0.55, 5.3, 12.2, 0.8, ["Cả năm bước nằm trong một chu kỳ clock. Lệnh load đi qua nhiều khối nhất (IMEM, "
                                "RegisterFile, ALU, DMEM, LoadUnit), nên nó quyết định độ dài chu kỳ."],
     size=15, color=MUTED)

# ================================================================ S14 next-PC, halt, đường găng
s = content_slide("Next-PC, halt và đường găng")
heading(s, 0.55, 0.95, 5.9, "Chọn PC kế tiếp")
box(s, 0.55, 1.45, 5.9, 2.45, TINT_GRAY)
text(s, 0.75, 1.55, 5.5, 2.3, [
    {"runs": [B("PCSel = Taken OR Jal OR Jalr")], "size": 16, "space_after": 2},
    {"runs": [B("target = ALU.Y AND 0xFFFFFFFE")], "size": 16, "space_after": 8},
    {"runs": [R("Branch, JAL: A = PC; JALR: A = rs1. Đặc tả JALR yêu cầu xóa bit 0; với branch và JAL bit này "
                "vốn bằng 0, nên một mạch dùng chung cho cả ba.")], "size": 14, "space_after": 6},
    {"runs": [R("PC.enable = NOT Halt: gặp EBREAK, CPU giữ nguyên trạng thái, chân halt lên 1.")], "size": 14},
], size=14)
heading(s, 6.85, 0.95, 5.95, "CPI = 1 nhưng chu kỳ dài")
text(s, 6.85, 1.45, 5.95, 2.4, [
    bl(R("Chu kỳ clock phải đủ cho đường tổ hợp dài nhất: lệnh load qua IMEM, Control và RegisterFile, ALU, DMEM, "
         "LoadUnit, MUX ghi lại")),
    bl(R("Lệnh add không dùng RAM vẫn phải chờ hết chu kỳ đó")),
], size=15, space_after=8)
text(s, 0.55, 4.2, 12.2, 0.4, [{"runs": [B("Đường găng theo giả định trễ (ps)")]}], size=17)
seg = [("IF 200", 200, "IF"), ("ID 100", 100, "ID"), ("EX 200", 200, "EX"), ("MEM 200", 200, "ME"),
       ("WB 100", 100, "WB")]
x = 0.55
scale = 10.2 / 800
for lbl, ps, k in seg:
    w = ps * scale
    box(s, x, 4.72, w - 0.04, 0.78, RGBColor.from_string(STAGE[k]), shape=MSO_SHAPE.RECTANGLE)
    text(s, x, 4.72, w - 0.04, 0.78, [{"runs": [B(lbl)], "align": PP_ALIGN.CENTER}], size=16,
         anchor=MSO_ANCHOR.MIDDLE)
    x += w
text(s, x + 0.1, 4.7, 1.9, 0.8, [{"runs": [B(NUM["resTSingle"] + " ps")]}], size=28, color=RED,
     anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.55, 5.7, 12.2, 0.6, ["Giả định trễ từng bước theo Patterson & Hennessy, ch. 4. Logisim không mô phỏng trễ "
                                "cổng, nên đây là con số để so sánh, không phải số đo trên mạch."], size=13, color=MUTED)

# ================================================================ S15 kiểm thử: cách làm
s = content_slide("Kiểm thử hai mức: module và toàn CPU")
chain = [("programs/*.s", "12 chương trình\n+ 25 fuzz"), ("rvasm.py", "assembler\n→ ROM IMEM"),
         ("Logisim", "chạy không\ngiao diện"), ("so với rvsim.py", "golden model\nviết độc lập")]
for i, (h, sub) in enumerate(chain):
    x = 0.55 + i * 1.83
    box(s, x, 0.98, 1.55, 1.45, TINT_RED if i == 3 else TINT_GRAY)
    text(s, x + 0.04, 1.02, 1.47, 1.38, [{"runs": [B(h, color=RED)], "size": 14, "space_after": 3,
                                          "align": PP_ALIGN.CENTER}] +
         [{"runs": [R(ln)], "size": 13, "space_after": 0, "align": PP_ALIGN.CENTER} for ln in sub.split("\n")],
         anchor=MSO_ANCHOR.MIDDLE)
    if i < 3:
        arrow(s, x + 1.57, 1.55, 0.24, 0.3)
text(s, 0.55, 2.6, 7.1, 3.8, [
    bl(B("So sánh: "), R("31 thanh ghi x1–x31, 16 KiB RAM, chuỗi TTY, GPIO_OUT, cycles và instret")),
    bl(B("So cả số chu kỳ: "), R("bắt được lỗi thời gian khi kết quả cuối vẫn đúng, ví dụ stall thừa, flush thiếu")),
    bl(B("12 chương trình: "), R("demo.s; t01–t05 phủ từng nhóm lệnh; t06_hazard.s gom các ca forwarding, "
                                 "load-use, ghi x0; t07–t09 (Fibonacci, sắp xếp nổi bọt, đệ quy); t10, t11 UART, GPIO")),
    bl(B("25 chương trình fuzz: "), R(f"seed {FUZZ[0]}–{FUZZ[1]}, mỗi chương trình {FUZZ[2]}–{FUZZ[3]} lệnh, "
                                      "nhiều phụ thuộc gần")),
    bl(B("rvasm.py --nohazard "), R("chèn nop cho bản NH")),
], size=14, space_after=5)
vrows = [["Module", "SC", "PL"]] + [[n, a.replace("--", "–"), b] for n, (a, b) in VEC.items()] + \
        [["Tổng", VEC_TOTAL[0], VEC_TOTAL[1]]]
fills = {(len(vrows) - 1, j): TINT_RED for j in range(3)}
table(s, 8.05, 0.95, 4.75, vrows, [1.95, 1.4, 1.4], size=12, row_h=0.355, fills=fills,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT], bold_cells={(len(vrows) - 1, j) for j in range(3)})

# ================================================================ S16 kết quả kiểm thử
s = content_slide("Kết quả kiểm thử")
prow = [["File mạch", "Chế độ assemble", "12 chương trình", "25 chương trình fuzz"]] + [list(r) for r in PASS]
fills = {(3, j): TINT_RED for j in range(4)}
table(s, 0.55, 0.95, 7.3, prow, [1.4, 2.0, 1.9, 2.0], size=15, row_h=0.42, fills=fills,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER])
text(s, 0.55, 3.25, 7.3, 0.4, [f"Chạy lại ngày {RUN_DATE} trên Logisim-evolution 4.1.0, Java 21, Windows 11"],
     size=13, color=MUTED)
res = [(VEC_TOTAL[0].split("/")[0], "test vector đạt trên SC"), (VEC_TOTAL[1].split("/")[0], "test vector đạt trên PL"),
       ("1.00", f"CPI bản SC: {NUM['resTotSC']} lệnh = {NUM['resTotSC']} chu kỳ")]
for i, (big, small) in enumerate(res):
    y = 0.92 + i * 1.0
    text(s, 8.3, y, 4.5, 0.58, [{"runs": [B(big)]}], size=32, color=RED)
    text(s, 8.3, y + 0.56, 4.5, 0.4, [small], size=13, color=MUTED)
box(s, 0.55, 4.0, 12.25, 1.05, TINT_GRAY)
text(s, 0.75, 4.02, 11.9, 1.0, [
    {"runs": [B("Số chu kỳ khớp: "), R("ở mọi lần PASS, cycles mà Logisim đếm bằng đúng con số của golden model "
                                       "(trừ t11_io.s: thời điểm ký tự đến phụ thuộc Logisim, không so số chu kỳ).")]},
], size=15, anchor=MSO_ANCHOR.MIDDLE)
box(s, 0.55, 5.2, 12.25, 1.1, TINT_RED)
text(s, 0.75, 5.22, 11.9, 1.05, [
    {"runs": [B("NH chạy chương trình bình thường thì sai ngay từ demo.s: "), R("sp ra 0xFFFFFFF0 thay vì "
                                                                                "0x00003FF0, vì addi sp, sp, -16 đọc sp "
                                                                                "trước khi lui sp, 4 kịp ghi.")]},
], size=15, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================ S17 phần 3
divider_slide("PHẦN 3", "PIPELINE 5 TẦNG VÀ HAZARD", "Nguyễn Đức Anh", [
    "Năm tầng IF, ID, EX, MEM, WB và 4 thanh ghi pipeline",
    "Ba loại hazard và cách xử lý; bản NoHazard",
    "Số chu kỳ, CPI và tăng tốc của ba phiên bản",
])

# ================================================================ S18 năm tầng, thanh ghi pipeline
s = content_slide("Năm tầng và thanh ghi pipeline")
picture(s, DIMG / "RV32I_Pipeline.png", 0.55, 0.95, 8.2, 3.45, align="left")
chips = [(f"{NUM['resTPipe']} ps", "chu kỳ = max(200, 100, 200, 200, 100) + 20 ps thanh ghi (giả định)"),
         (NUM["resIdealSpeedup"] + "×", f"tăng tốc lý tưởng {NUM['resTSingle']}/{NUM['resTPipe']} nếu CPI = 1"),
         ("Pipeline Monitor", "PC, lệnh ở 5 tầng và Stall, LoadUse, E_Redirect, FwdA, FwdB")]
for i, (h, sub) in enumerate(chips):
    y = 0.95 + i * 1.17
    box(s, 9.0, y, 3.8, 1.05, TINT_RED)
    text(s, 9.12, y + 0.02, 3.6, 1.0, [{"runs": [B(h)], "color": RED, "size": 18 if i < 2 else 16,
                                        "space_after": 1}, sub], size=13, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
pregs = [["Thanh ghi", "Trường"],
         ["IF/ID", "valid, pc, pc4, instr"],
         ["ID/EX", "valid, pc, pc4, instr, rs1d, rs2d, imm, rs1, rs2, rd, funct3, ALUCtrl, ASel, BSel, RegWrite, "
                   "MemRead, MemWrite, WBSel, Branch, Jal, Jalr, Halt"],
         ["EX/MEM", "valid, pc, instr, exres, sdata, rd, funct3, RegWrite, MemRead, MemWrite, MemToReg, Halt"],
         ["MEM/WB", "valid, pc, instr, exres, mdata, rd, RegWrite, MemToReg, Halt"]]
table(s, 0.55, 4.55, 7.6, pregs, [1.1, 6.5], size=12, row_h=0.33)
text(s, 8.4, 4.5, 4.4, 1.9, [
    bl(B("Stall: "), R("EN = 0 giữ giá trị. "), B("Flush: "), R("nạp toàn 0 qua MUX, thành bubble")),
    bl(B("exres "), R("= PC + 4 (JAL/JALR) hoặc kết quả ALU")),
    bl(R("instr của IF/ID vào Control, ImmGen; pc của ID/EX vào MUX ASel; pc4 vào MUX exres. Các pc, instr còn lại "
         "chỉ để hiển thị")),
], size=13, space_after=4)

# ================================================================ S19 ba loại hazard, forwarding, bypass
s = content_slide("Ba loại hazard; forwarding và bypass WB→ID")
hz = [("Structural", "Không xảy ra: IMEM và DMEM tách riêng, register file có 2 cổng đọc, 1 cổng ghi", TINT_GRAY),
      ("Data", "Forwarding, bypass WB→ID; riêng load-use phải stall 1 chu kỳ", TINT_RED),
      ("Control", "Đoán không nhảy, quyết định ở EX, flush 2 lệnh nạp sai", TINT_ORG)]
for i, (h, body, fill) in enumerate(hz):
    x = 0.55 + i * 4.12
    box(s, x, 0.95, 3.92, 1.25, fill)
    text(s, x + 0.15, 0.99, 3.65, 1.18, [{"runs": [B(h + " hazard")], "color": RED, "size": 17, "space_after": 2},
                                         body], size=14, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
picture(s, SIMG / "ForwardUnit.png", 0.55, 2.4, 5.6, 3.0)
text(s, 0.55, 5.5, 5.6, 0.8, ["ForwardUnit: so rs1, rs2 của lệnh ở EX với rd của lệnh ở MEM và WB"], size=13,
     color=MUTED)
heading(s, 6.5, 2.4, 6.3, "Lệnh cách 1–2 vị trí: ForwardUnit, 0 chu kỳ mất", size=16)
text(s, 6.5, 2.85, 6.3, 1.8, [
    bl(B("FwdA = 01 "), R("lấy từ EX/MEM khi EX/MEM.RegWrite = 1, rd ≠ 0, rd = rs1")),
    bl(B("FwdA = 10 "), R("lấy từ MEM/WB khi điều kiện tương tự đúng, còn điều kiện 01 sai")),
    bl(R("rd ≠ 0: không forward giá trị khác 0 cho lệnh đọc x0; EX/MEM ưu tiên vì là giá trị mới nhất")),
], size=14, space_after=4)
heading(s, 6.5, 4.6, 6.3, "Lệnh cách 3 vị trí: IDBypass, 0 chu kỳ mất", size=16)
text(s, 6.5, 5.05, 6.3, 1.3, [
    bl(R("WB ghi register file ở cạnh lên cuối chu kỳ, ID đọc trong chu kỳ đó nên nhận giá trị cũ")),
    bl(R("IDBypass đưa W_data vào ID khi W_RegWrite = 1, W_rd ≠ 0, W_rd = rs")),
], size=14, space_after=4)

# ================================================================ S20 load-use, control hazard, HazardUnit
s = content_slide("Load-use, control hazard và HazardUnit")
heading(s, 0.55, 0.95, 6.1, "Load-use: stall 1 chu kỳ", size=17)
text(s, 0.55, 1.4, 6.1, 1.6, [
    bl(R("Dữ liệu load có ở cuối MEM, lệnh ngay sau cần nó ở đầu EX: forwarding không kịp")),
    bl(R("PCWrite = 0, IFID_Write = 0 giữ PC và IF/ID; IDEX_Flush = 1 chèn bubble; chu kỳ sau forward từ MEM/WB")),
], size=14, space_after=4)
box(s, 0.55, 3.0, 6.1, 0.7, TINT_RED)
text(s, 0.65, 3.0, 5.9, 0.7, [{"runs": [B("LoadUse = E_MemRead ∧ (E_rd ≠ 0) ∧ ((E_rd = rs1 ∧ UseRs1) ∨ "
                                          "(E_rd = rs2 ∧ UseRs2))")]}], size=13, anchor=MSO_ANCHOR.MIDDLE)
heading(s, 0.55, 3.85, 6.1, "Control hazard: flush 2 chu kỳ", size=17)
text(s, 0.55, 4.3, 6.1, 2.1, [
    bl(R("Luôn nạp PC + 4; E_Redirect = Taken ∨ Jal ∨ Jalr quyết định ở EX")),
    bl(R("Redirect: PC nhận địa chỉ đích, flush IF/ID và ID/EX")),
    bl(R("Có cả stall và redirect thì redirect thắng: lệnh đang chờ nằm trên nhánh sai")),
    bl(R("EBREAK ở ID làm Stall = 1; CPU dừng khi EBREAK tới WB")),
], size=14, space_after=4)
picture(s, SIMG / "HazardUnit.png", 6.95, 0.95, 5.85, 3.0)
box(s, 6.95, 4.1, 5.85, 1.25, TINT_GRAY)
text(s, 7.1, 4.12, 5.6, 1.2, [
    {"runs": [B("Stall = LoadUse ∨ D_Halt")], "space_after": 2},
    {"runs": [B("PCWrite = IFID_Write = ¬Stall ∨ Redirect")], "space_after": 2},
    {"runs": [B("IFID_Flush = Redirect;  IDEX_Flush = Redirect ∨ LoadUse")]},
], size=14, anchor=MSO_ANCHOR.MIDDLE)
box(s, 6.95, 5.5, 5.85, 0.85, TINT_RED)
text(s, 7.1, 5.5, 5.6, 0.85, [{"runs": [B("cycles = N + 4 + số lần load-use + 2 × số lần nhảy")], "color": RED}],
     size=15, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================ S21 NoHazard, giản đồ
s = content_slide("Bản NoHazard và giản đồ pipeline của t06_hazard.s")
pl_rows, nh_rows = parse_diagram("t06_pl.tex"), parse_diagram("t06_nh.tex")
text(s, 0.55, 0.92, 5.9, 0.4, [{"runs": [B("PL: forwarding, stall bằng phần cứng · 14 chu kỳ")]}], size=14,
     color=RED)
diagram(s, 0.55, 1.3, pl_rows, 1.6, 0.3, 0.3, size=10)
text(s, 6.75, 0.92, 6.1, 0.4, [{"runs": [B("NH: assembler chèn nop · 17 chu kỳ")]}], size=14, color=RED)
diagram(s, 6.75, 1.3, nh_rows, 1.15, 0.29, 0.3, size=10)
legend = [("IF", "IF"), ("ID", "ID"), ("EX", "EX"), ("ME", "MEM"), ("WB", "WB"), ("ST", "stall ở ID")]
for i, (k, lbl) in enumerate(legend):
    x = 0.55 + i * 0.98
    box(s, x, 4.65, 0.26, 0.26, RGBColor.from_string(STAGE[k]), shape=MSO_SHAPE.RECTANGLE, line=LINE)
    text(s, x + 0.3, 4.59, 0.7, 0.4, [lbl], size=11, color=MUTED)
text(s, 0.55, 4.98, 5.9, 0.6, ["PL: ba lệnh dùng ngay kết quả lw mỗi lệnh chờ 1 chu kỳ; beq nhảy nên 2 lệnh xám bị "
                               "flush. NH: mọi phụ thuộc gần chờ bằng nop."], size=12, color=MUTED, space_after=0)
box(s, 0.55, 5.55, 5.9, 0.9, TINT_GRAY)
text(s, 0.67, 5.56, 5.7, 0.88, [
    {"runs": [B("NH: "), R("MUX forwarding chọn hằng 0, E_MemRead của HazardUnit nối 0; giữ flush, IDBypass")],
     "space_after": 2},
    {"runs": [B("--nohazard: "), R("phụ thuộc lệnh ngay trước → 2 nop, cách 2 lệnh → 1 nop; chỉ đặt lại bộ đếm "
                                   "sau jal, jalr")]},
], size=12, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================ S22 số chu kỳ, CPI
s = content_slide("Số chu kỳ và CPI trên 12 chương trình")
crow = [["Chương trình", "Lệnh", "SC", "NH", "NOP", "PL", "Load-use", "Nhảy", "CPI (PL)"]]
crow += [[n] + v for n, v in CYCLES] + [["Tổng"] + CYC_TOTAL]
hi = {NUM["resMaxProg"], "t09_recursion.s"}
fills, bold = {}, set()
for i, r_ in enumerate(crow[1:], start=1):
    if r_[0] in hi:
        for j in range(9):
            fills[(i, j)] = TINT_RED
    if r_[0] == "Tổng":
        for j in range(9):
            fills[(i, j)] = TINT_GRAY
            bold.add((i, j))
table(s, 0.55, 0.95, 8.2, crow, [1.75, 0.75, 0.75, 0.85, 0.75, 0.8, 0.95, 0.75, 0.85], size=13, row_h=0.36,
      fills=fills, aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.RIGHT] * 8, bold_cells=bold)
kp = [(NUM["resTotCPI"], "CPI của PL trên cả 12 chương trình"),
      (NUM["resMaxCPI"], f"CPI cao nhất, {NUM['resMaxProg']}: {NUM['resMaxN']} lệnh, {NUM['resMaxBR']} lần nhảy"),
      (NUM["resNineCPI"], f"t09_recursion.s: {NUM['resNineBR']} lần nhảy tốn {NUM['resNineFlush']} chu kỳ, "
                          f"gấp hơn 5 lần {NUM['resNineLU']} chu kỳ load-use"),
      (NUM["resTotCPINH"], f"CPI của NH tính trên số lệnh gốc: thực thi {NUM['resTotNOP']} lệnh nop")]
for i, (big, small) in enumerate(kp):
    y = 0.95 + i * 1.33
    text(s, 9.05, y, 3.75, 0.6, [{"runs": [B(big)]}], size=30, color=RED)
    text(s, 9.05, y + 0.58, 3.75, 0.75, [small], size=13, color=MUTED, space_after=0)
text(s, 0.55, 6.0, 8.2, 0.4, ["Số liệu từ golden model, đã khớp từng chu kỳ với Logisim; không tính đoạn 31 lệnh sw "
                               "mà run_tests.py chèn thêm."], size=12, color=MUTED)

# ================================================================ S23 tăng tốc
s = content_slide("Tăng tốc so với đơn chu kỳ theo giả định trễ")
cd = CategoryChartData()
cd.categories = [n.replace(".s", "") for n, _ in TIMES]
cd.add_series("SC / NH", [float(r[3]) for _, r in TIMES])
cd.add_series("SC / PL", [float(r[4]) for _, r in TIMES])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.45), Inches(0.95), Inches(8.3), Inches(4.95), cd)
ch = gf.chart
ch.font.name = FONT
ch.font.size = Pt(12)
ch.has_title = True
ch.chart_title.text_frame.text = "Tăng tốc so với SC (lần)"
for r in ch.chart_title.text_frame.paragraphs[0].runs:
    style_run(r, 14, DARK, True)
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.TOP
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(12)
ch.legend.font.name = FONT
for ser, col in zip(ch.series, (RGBColor(0xBF, 0xBF, 0xBF), RED)):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = col
ch.plots[0].gap_width = 60
ch.plots[0].overlap = -10
ca = ch.category_axis
ca.tick_labels.font.size = Pt(11)
ca.tick_labels.font.name = FONT
ca.tick_labels.font.color.rgb = MUTED
ca.format.line.color.rgb = LINE
va = ch.value_axis
va.maximum_scale = 4.0
va.minimum_scale = 0
va.major_unit = 1.0
va.tick_labels.font.size = Pt(11)
va.tick_labels.font.name = FONT
va.tick_labels.font.color.rgb = MUTED
va.major_gridlines.format.line.color.rgb = RGBColor(0xE6, 0xE6, 0xE6)
va.format.line.fill.background()
kpis = [(NUM["resSpeedPL"] + "×", f"PL so với SC (lý tưởng {NUM['resIdealSpeedup']}×)"),
        (NUM["resSpeedNH"] + "×", "NH so với SC"),
        (NUM["resSpeedPLNH"] + "×", "PL ít chu kỳ hơn NH, cùng chu kỳ clock: phần đóng góp của forwarding và stall "
                                    "bằng phần cứng")]
for i, (big, small) in enumerate(kpis):
    y = 0.95 + i * 1.12
    text(s, 9.05, y, 3.75, 0.55, [{"runs": [B(big)]}], size=30, color=RED)
    text(s, 9.05, y + 0.55, 3.75, 0.6, [small], size=13, color=MUTED, space_after=0)
box(s, 9.05, 4.4, 3.75, 1.5, TINT_GRAY)
text(s, 9.15, 4.42, 3.55, 1.45, [
    {"runs": [B("Chưa đạt mức lý tưởng vì:")], "space_after": 2},
    bl(R("CPI của PL > 1 do flush và stall"), bullet_color=MUTED),
    bl(R("ID, WB chỉ cần 100 ps nhưng chiếm trọn 220 ps"), bullet_color=MUTED),
], size=13, space_after=2)
text(s, 0.55, 6.0, 12.2, 0.4, [f"Thời gian = số chu kỳ × chu kỳ clock giả định: SC {NUM['resTSingle']} ps, NH và PL "
                                f"{NUM['resTPipe']} ps. Logisim không mô phỏng trễ cổng, đây không phải số đo."],
     size=12, color=MUTED)

# ================================================================ S24 mở rộng, hạn chế, hướng phát triển
s = content_slide("Phần mở rộng, hạn chế và hướng phát triển")
heading(s, 0.55, 0.95, 3.85, "Đã làm thêm")
text(s, 0.55, 1.42, 3.85, 4.9, [
    bl(R("Lệnh tùy chọn LB, LH, LBU, LHU, SB, SH, BLT, BGE, BLTU, BGEU; LUI, AUIPC")),
    bl(R("UART (TTY, Keyboard) và GPIO (LED 7 đoạn, 8 LED, 8 công tắc DIP)")),
    bl(R("Forwarding hai nguồn và bypass WB→ID")),
    bl(R("Bộ đếm cycles, instret; Pipeline Monitor")),
    bl(R("Toolchain kiểm thử tự động và bản NH để đo lợi ích phần cứng")),
], size=14, space_after=6)
heading(s, 4.7, 0.95, 3.85, "Hạn chế")
text(s, 4.7, 1.42, 3.85, 4.9, [
    bl(R(f"Nhảy quyết định ở EX: flush 2 × {NUM['resTotBR']} chu kỳ trên 12 chương trình, nhiều hơn "
         f"{NUM['resTotLU']} chu kỳ load-use")),
    bl(R("Không exception, ngắt, CSR; UART phải hỏi vòng")),
    bl(R("Truy cập bộ nhớ lệch không hỗ trợ; đích nhảy lệch (bit 1 = 1) không bị phát hiện")),
    bl(R("I/O chỉ giải mã Addr[31:28] và Addr[4:2]: địa chỉ 0xFxxx_xxxx khác là bí danh")),
], size=14, space_after=6)
heading(s, 8.85, 0.95, 3.95, "Hướng phát triển")
fut = [("Quyết định nhánh ở ID", f"phạt nhảy 2 → 1 chu kỳ; t09 tiết kiệm tối đa {NUM['resNineBR']} chu kỳ, trừ stall "
                                 "mới"),
       ("Dự đoán 2 bit + BTB", "giảm flush ở vòng lặp; đo bằng số lần E_Redirect"),
       ("Phần mở rộng M", "MUL, DIV thay vòng nhân dịch-cộng trong t09"),
       ("Ngắt và CSR", "UART nhận ký tự không cần hỏi vòng")]
for i, (h, sub) in enumerate(fut):
    y = 1.42 + i * 1.22
    box(s, 8.85, y, 3.95, 1.1, TINT_RED if i == 0 else TINT_GRAY)
    circle_num(s, 8.97, y + 0.28, 0.5, str(i + 1), RED if i == 0 else MUTED, 14)
    text(s, 9.55, y + 0.03, 3.2, 1.05, [{"runs": [B(h)], "space_after": 1}, {"runs": [R(sub)], "size": 13}],
         size=15, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================ S25 cảm ơn: đưa xuống cuối
thanks = prs.slides[1]
for shp in thanks.shapes:
    if shp.has_text_frame and shp.text_frame.text.startswith("THANK"):
        shp.text_frame.paragraphs[0].runs[0].text = "CẢM ƠN THẦY VÀ CÁC BẠN!"
        for extra in shp.text_frame.paragraphs[0].runs[1:]:
            extra.text = ""
        shp.text_frame.paragraphs[0].runs[0].font.size = Pt(40)
        shp.text_frame.paragraphs[0].runs[0].font.name = FONT
        shp.left, shp.width = Inches(3.2), Inches(9.6)
text(thanks, 3.75, 3.75, 8.5, 0.6, ["Hỏi đáp · Demo trực tiếp trên Logisim · Video: demo/demo_RV32I_v2.mp4"],
     size=18, color=DARK)
ids = prs.slides._sldIdLst
el = ids[1]
ids.remove(el)
ids.append(el)

# ---------------------------------------------------------------- lời thoại: slides/kich_ban.src.md → speaker notes
SUBS = dict(NUM, vecSC=VEC_TOTAL[0], vecPL=VEC_TOTAL[1], flushTot=str(2 * int(NUM["resTotBR"])),
            fuzzLo=FUZZ[2], fuzzHi=FUZZ[3], runDate=RUN_DATE)
src = SCRIPT_SRC.read_text("utf-8").format_map(SUBS)
head, *blocks = re.split(r"^## Slide (\d+) · .*$", src, flags=re.M)
notes = {int(blocks[i]): blocks[i + 1].strip() for i in range(0, len(blocks), 2)}
assert sorted(notes) == list(range(1, len(prs.slides) + 1)), (sorted(notes), len(prs.slides))
for i, sl in enumerate(prs.slides, start=1):
    paras = [" ".join(par.split()) for par in notes[i].split("\n\n")]
    sl.notes_slide.notes_text_frame.text = "\n\n".join(paras)
    for p in sl.notes_slide.notes_text_frame.paragraphs:
        for r in p.runs:
            r.font.name = FONT
SCRIPT_OUT.write_text(src.replace(head, re.sub(r"Nguồn của speaker notes[^\n]*\n[^\n]*\n[^\n]*\n",
                                                 "Bản đã thay số liệu, sinh từ kich_ban.src.md. Lời thoại giống speaker "
                                                 "notes trong RV32I_ThuyetTrinh.pptx.\n\n", head), 1), "utf-8")

prs.save(OUT)


# ---------------------------------------------------------------- một font cho toàn bộ deck
def force_font(path):
    """Đổi mọi typeface Latin cụ thể (theme, master, layout, slide, chart, notes) thành Times New Roman."""
    tmp = path.with_name(path.stem + ".tmp.pptx")
    pat = re.compile(r'(<a:(?:latin|ea|cs) typeface=")([^"]*)(")')

    def sub(m):
        face = m.group(2)
        keep = face.startswith("+") or face in ("", "Wingdings", "Symbol")
        return m.group(1) + (face if keep else FONT) + m.group(3)

    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(".xml") and item.filename.startswith(
                    ("ppt/theme/", "ppt/slideMasters/", "ppt/slideLayouts/", "ppt/slides/", "ppt/charts/",
                     "ppt/notesMasters/", "ppt/notesSlides/")):
                data = pat.sub(sub, data.decode("utf-8")).encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)


force_font(OUT)
print(f"{OUT} : {len(prs.slides)} slide")
