#!/usr/bin/env python3
"""Build the Dairyworks value-creation deck (McKinsey-style) with python-pptx.
Fallback renderer used because the CommsPro MCP is not connected in this environment.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

# ---- palette ----
NAVY   = RGBColor(0x1F, 0x2A, 0x44)
NAVY2  = RGBColor(0x2C, 0x3A, 0x5E)
TEAL   = RGBColor(0x17, 0x9C, 0x9C)
AMBER  = RGBColor(0xE2, 0x9A, 0x2B)
RED    = RGBColor(0xC0, 0x3A, 0x2B)
GREEN  = RGBColor(0x2E, 0x8B, 0x57)
GREY   = RGBColor(0x5B, 0x63, 0x70)
LGREY  = RGBColor(0xED, 0xEF, 0xF2)
MGREY  = RGBColor(0xD6, 0xDA, 0xE0)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
DARKTX = RGBColor(0x23, 0x2A, 0x36)

FONT = "Calibri"
EMU = 914400
SW, SH = 13.333, 7.5

prs = Presentation()
prs.slide_width  = Emu(int(SW*EMU))
prs.slide_height = Emu(int(SH*EMU))
BLANK = prs.slide_layouts[6]

def slide():
    return prs.slides.add_slide(BLANK)

def rect(s, x, y, w, h, fill=None, line=None, line_w=0.75, shape=MSO_SHAPE.RECTANGLE):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.shadow.inherit = False
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    return sp

def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        wrap=True, space_after=4, line_spacing=1.0):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap; tf.vertical_anchor = anchor
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    if isinstance(runs, str):
        runs = [[(runs, {})]]
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space_after); p.space_before = Pt(0)
        p.line_spacing = line_spacing
        if isinstance(para, tuple):
            para = [para]
        for text, fmt in para:
            r = p.add_run(); r.text = text
            r.font.name = FONT
            r.font.size = Pt(fmt.get("sz", 14))
            r.font.bold = fmt.get("b", False)
            r.font.italic = fmt.get("i", False)
            r.font.color.rgb = fmt.get("c", DARKTX)
    return tb

def bullets(s, x, y, w, h, items, sz=13, c=DARKTX, gap=5, bullet="–", lh=1.05):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.space_before = Pt(0); p.line_spacing = lh
        if isinstance(it, tuple):
            label, rest = it
            r = p.add_run(); r.text = f"{bullet} "; r.font.name=FONT; r.font.size=Pt(sz); r.font.color.rgb=c
            r = p.add_run(); r.text = label; r.font.name=FONT; r.font.size=Pt(sz); r.font.bold=True; r.font.color.rgb=c
            r = p.add_run(); r.text = rest; r.font.name=FONT; r.font.size=Pt(sz); r.font.color.rgb=c
        else:
            r = p.add_run(); r.text = f"{bullet} {it}"; r.font.name=FONT; r.font.size=Pt(sz); r.font.color.rgb=c
    return tb

def header(s, kicker, title, sub=None):
    """Standard content-slide header: kicker + takeaway headline + rule."""
    rect(s, 0, 0, SW, 1.55, fill=WHITE)
    txt(s, 0.55, 0.22, 11.0, 0.3, [[(kicker.upper(), {"sz":11,"b":True,"c":TEAL})]])
    txt(s, 0.55, 0.5, 12.2, 0.9, [[(title, {"sz":20,"b":True,"c":NAVY})]], line_spacing=1.0)
    rect(s, 0.55, 1.46, 12.2, 0.028, fill=TEAL)
    if sub:
        txt(s, 0.55, 1.18, 12.2, 0.3, [[(sub, {"sz":12,"i":True,"c":GREY})]])

def source(s, text):
    txt(s, 0.55, 7.12, 12.2, 0.3, [[("Source: "+text, {"sz":8.5,"c":GREY})]])
    txt(s, 11.9, 7.12, 0.9, 0.3, [[("McKinsey & Company", {"sz":8,"c":MGREY})]], align=PP_ALIGN.RIGHT)

def pagenum(s, n):
    txt(s, 12.5, 0.18, 0.6, 0.3, [[(str(n), {"sz":10,"c":MGREY})]], align=PP_ALIGN.RIGHT)

def chip(s, x, y, w, h, color):
    rect(s, x, y, w, h, fill=color)

def kpi(s, x, y, w, h, value, label, vcolor=NAVY, bg=LGREY):
    rect(s, x, y, w, h, fill=bg)
    rect(s, x, y, 0.07, h, fill=TEAL)
    txt(s, x+0.2, y+0.12, w-0.3, 0.5, [[(value, {"sz":24,"b":True,"c":vcolor})]])
    txt(s, x+0.2, y+0.66, w-0.3, h-0.7, [[(label, {"sz":10.5,"c":GREY})]], line_spacing=1.0)

def dot(s, x, y, color, d=0.14):
    rect(s, x, y, d, d, fill=color, shape=MSO_SHAPE.OVAL)

# ---------------- table helper ----------------
def table(s, x, y, w, rows, col_w, header_fill=NAVY, sz=11, row_h=0.34,
          head_sz=10.5, dot_cols=None, dot_map=None, bold_last=False, zebra=True):
    dot_cols = dot_cols or {}
    nrow = len(rows)
    tbl_h = row_h*nrow
    cum = 0
    for ci, cw in enumerate(col_w):
        pass
    for ri, row in enumerate(rows):
        ry = y + ri*row_h
        is_head = (ri == 0)
        is_last = bold_last and (ri == nrow-1)
        if is_head:
            rect(s, x, ry, w, row_h, fill=header_fill)
        elif is_last:
            rect(s, x, ry, w, row_h, fill=NAVY2)
        elif zebra and ri % 2 == 0:
            rect(s, x, ry, w, row_h, fill=LGREY)
        else:
            rect(s, x, ry, w, row_h, fill=WHITE)
        cx = x
        for ci, cell in enumerate(row):
            cw = col_w[ci]
            tcol = WHITE if (is_head or is_last) else DARKTX
            b = is_head or is_last or (ci==0 and not is_head)
            align = PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER
            # dot encoding
            if (not is_head) and (ci in dot_cols) and dot_map:
                key = cell.strip()
                color = dot_map.get(key.upper())
                if color:
                    dot(s, cx+0.12, ry+row_h/2-0.07, color)
                    txt(s, cx+0.34, ry, cw-0.4, row_h, [[(cell, {"sz":sz,"c":tcol,"b":b})]],
                        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE)
                    cx += cw; continue
            txt(s, cx+0.1, ry, cw-0.2, row_h, [[(cell, {"sz":(head_sz if is_head else sz),"c":tcol,"b":b})]],
                align=align, anchor=MSO_ANCHOR.MIDDLE)
            cx += cw
    # outer border
    rect(s, x, y, w, tbl_h, fill=None, line=MGREY, line_w=0.75)
    return tbl_h

DOTMAP = {"HIGH":RED, "MED":AMBER, "MEDIUM":AMBER, "LOW":GREEN,
          "SCALE":GREEN, "FIX":AMBER, "DEFEND":AMBER, "FIX/DEFEND":AMBER, "REVIEW":RED}

# ============================================================ SLIDE 0: COVER
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 0, 0.35, SH, fill=TEAL)
rect(s, 0.9, 2.35, 5.2, 0.05, fill=TEAL)
txt(s, 0.9, 1.5, 11, 0.5, [[("DAIRYWORKS  ·  BOARD STRATEGY READOUT", {"sz":13,"b":True,"c":TEAL})]])
txt(s, 0.9, 2.55, 11.4, 1.8, [[("A 5-Year Value Creation Plan", {"sz":46,"b":True,"c":WHITE})]], line_spacing=1.0)
txt(s, 0.9, 4.15, 11.2, 1.0,
    [[("Restoring full potential: ~4.5x EBITDA to approximately ", {"sz":20,"c":MGREY}),
      ("AED 495M by 2026", {"sz":20,"b":True,"c":WHITE})]], line_spacing=1.1)
txt(s, 0.9, 6.35, 11, 0.4, [[("Prepared for the CEO and Board  ·  October 2026  ·  Strictly confidential", {"sz":12,"c":MGREY})]])
txt(s, 0.9, 6.75, 11, 0.4, [[("McKinsey & Company", {"sz":12,"b":True,"c":WHITE})]])

# ============================================================ SLIDE 1: EXEC SUMMARY
s = slide()
header(s, "Executive summary",
       "Dairyworks can roughly 4.5x EBITDA to ~AED 495M by 2026 — the decline is self-inflicted and reversible",
       "A four-initiative value creation plan in markets growing 5–8% per year")
# KPI strip
kpi(s, 0.55, 1.75, 2.9, 1.15, "5.8%", "2021 EBITDA margin\n(down from 18.1% in 2017)", vcolor=RED)
kpi(s, 3.6, 1.75, 2.9, 1.15, "18.3%", "Full-potential margin\nby 2026", vcolor=GREEN)
kpi(s, 6.65, 1.75, 2.9, 1.15, "+AED 384M", "EBITDA uplift\n(~4.5x the 2021 level)", vcolor=NAVY)
kpi(s, 9.7, 1.75, 3.08, 1.15, "+AED 800M", "Revenue uplift\nto ~AED 2,700M", vcolor=NAVY)
# left: situation/complication
rect(s, 0.55, 3.15, 7.55, 3.75, fill=LGREY)
rect(s, 0.55, 3.15, 7.55, 0.42, fill=NAVY)
txt(s, 0.75, 3.19, 7.2, 0.35, [[("THE SITUATION — AND WHY IT IS URGENT", {"sz":11,"b":True,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
bullets(s, 0.8, 3.75, 7.1, 3.0, [
    ("#2 in the UAE (~15% share), ", "AED 1,900M revenue across milk, yogurt and ice cream in UAE, KSA and Qatar"),
    ("EBITDA fell 69% ", "— from AED 362M (18.1%) in 2017 to AED 111M (5.8%) in 2021, a −25.6% annual decline"),
    ("The cause is internal: ", "S&D rose +7.9pp and COGS +5.2pp of revenue; brand spend stayed starved at 0.6% vs peers' 2–3%"),
    ("Markets are a tailwind: ", "UAE +7.2%, KSA +5.3%, Qatar +7.9% CAGR to 2026 — yet Dairyworks is shrinking"),
    ("Peers prove the prize: ", "Almarai 27%, NADEC 19%, SADAFCO 17% EBITDA margin today"),
], sz=12.5, gap=8)
# right: the ask
rect(s, 8.3, 3.15, 4.48, 3.75, fill=NAVY)
rect(s, 8.3, 3.15, 0.08, 3.75, fill=TEAL)
txt(s, 8.55, 3.35, 4.0, 0.4, [[("THE ASK", {"sz":12,"b":True,"c":TEAL})]])
bullets(s, 8.55, 3.9, 4.0, 2.4, [
    "Approve the 5-year value creation plan and its four initiatives",
    "Endorse the full-potential target: ~AED 2,700M revenue, ~AED 495M EBITDA",
    "Fund the Year-1 distribution and brand reset to stop the decline",
], sz=12.5, c=WHITE, gap=9)
rect(s, 8.55, 6.25, 4.0, 0.5, fill=TEAL)
txt(s, 8.55, 6.25, 4.0, 0.5, [[("Target: +AED 384M EBITDA (~4.5x)", {"sz":12.5,"b":True,"c":NAVY})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Dairyworks & peer P&Ls 2017–2021; Euromonitor 2021–2026; team analysis.")
pagenum(s, 1)

# ============================================================ SLIDE 2: SITUATION
s = slide()
header(s, "Situation · Current state",
       "A 30-year-old, three-category business across three GCC markets — scaled, but losing ground on every dimension",
       "Portfolio, footprint, channels and brand health")
cols = [
    ("PORTFOLIO & FOOTPRINT", TEAL, [
        "Founded 1990, UAE-based, mass-market across milk, yogurt and ice cream",
        "5 core SKUs from value to premium (milk AED 4.5–9/L, yogurt, ice cream AED 10/L)",
        "3 manufacturing plants, all in the UAE",
        "Distribution in-house in UAE; outsourced in KSA and Qatar",
    ]),
    ("CHANNELS", AMBER, [
        "Modern retail ~65%, traditional ~20% dominate",
        "Online full-basket ~10%, quick-commerce ~5% — small but fast-growing",
        "Distribution issues reported across all three countries",
    ]),
    ("BRAND HEALTH — 2019 NIELSEN (n=1,000)", RED, [
        "Only 1 in 5 consumers recognize the brand",
        "~60% of those who know it don't understand it",
        "Only 1 in 10 actively seek out Dairyworks",
    ]),
]
cx = 0.55
cw = 3.97
for title, color, items in cols:
    rect(s, cx, 1.9, cw, 3.9, fill=WHITE, line=MGREY)
    rect(s, cx, 1.9, cw, 0.62, fill=NAVY)
    rect(s, cx, 1.9, cw, 0.08, fill=color)
    txt(s, cx+0.15, 1.98, cw-0.3, 0.55, [[(title, {"sz":11,"b":True,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
    bullets(s, cx+0.18, 2.72, cw-0.36, 2.9, items, sz=11.5, gap=8)
    cx += cw + 0.2
rect(s, 0.55, 6.0, 12.23, 0.78, fill=NAVY2)
txt(s, 0.75, 6.0, 12.0, 0.78, [[("Implication:  ", {"sz":13,"b":True,"c":TEAL}),
    ("Dairyworks has the assets to win — scale, footprint, a premium tail — but brand, cost and distribution all work against it. Every one is a self-help lever.", {"sz":13,"c":WHITE})]],
    anchor=MSO_ANCHOR.MIDDLE)
source(s, "Dairyworks fact-pack (introduction, portfolio, footprint & channels); 2019 Nielsen survey (n=1,000).")
pagenum(s, 2)

# ============================================================ SLIDE 3: EBITDA COLLAPSE (chart)
s = slide()
header(s, "Complication · Burning platform",
       "EBITDA collapsed from AED 362M to AED 111M and margin from 18.1% to 5.8% — a −25.6% annual decline",
       "Dairyworks P&L trajectory, 2017–2021")
# chart
cd = CategoryChartData()
cd.categories = ["2017","2018","2019","2020","2021"]
cd.add_series("EBITDA (AED mn)", (362,372,307,232,111))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.55), Inches(1.95),
                        Inches(7.2), Inches(4.0), cd)
ch = gf.chart; ch.has_legend = False
plot = ch.plots[0]; plot.has_data_labels = True
plot.data_labels.font.size = Pt(11); plot.data_labels.font.bold = True
plot.data_labels.number_format = '0'; plot.data_labels.number_format_is_linked=False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
ser = plot.series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb = NAVY
ch.value_axis.visible = False; ch.value_axis.has_major_gridlines=False
ch.category_axis.tick_labels.font.size = Pt(11)
txt(s, 0.55, 5.95, 7.2, 0.3, [[("EBITDA margin:  18.1% → 18.4% → 15.3% → 11.9% → 5.8%", {"sz":11,"b":True,"c":RED})]], align=PP_ALIGN.CENTER)
# right rail
rect(s, 8.0, 1.95, 4.78, 4.3, fill=LGREY)
rect(s, 8.0, 1.95, 4.78, 0.5, fill=NAVY)
txt(s, 8.2, 1.95, 4.4, 0.5, [[("WHAT IS HAPPENING", {"sz":11,"b":True,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
bullets(s, 8.25, 2.65, 4.3, 3.4, [
    ("Flat revenue, collapsing profit: ", "revenue −1.3% CAGR but EBITDA −69% — the problem is margin, not the top line"),
    ("Masked share loss: ", "volume fell −3.5%/yr (313→272kt), offset by +2.3%/yr price rises"),
    ("Near break-even: ", "EBIT margin hit 0.6% in 2021 — one bad year from losing money"),
], sz=12, gap=10)
rect(s, 8.0, 6.4, 4.78, 0.5, fill=RED)
txt(s, 8.0, 6.4, 4.78, 0.5, [[("At 5.8%, Dairyworks earns <¼ of Almarai's margin", {"sz":11.5,"b":True,"c":WHITE})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Dairyworks P&L 2017–2021 (volume, revenue, EBITDA, EBIT).")
pagenum(s, 3)

# ============================================================ SLIDE 4: SELF-INFLICTED
s = slide()
header(s, "Complication · The market is not the problem",
       "Dairyworks lost margin and share in markets compounding 5–8% per year — the cause is internal, not the market",
       "Company performance vs. market growth")
# left dark panel: company going backwards
rect(s, 0.55, 1.9, 5.3, 4.9, fill=NAVY)
rect(s, 0.55, 1.9, 0.08, 4.9, fill=RED)
txt(s, 0.8, 2.08, 4.9, 0.4, [[("DAIRYWORKS IS GOING BACKWARDS", {"sz":12,"b":True,"c":RED})]])
bullets(s, 0.85, 2.65, 4.85, 2.2, [
    ("Revenue −1.3%/yr; ", "volume −3.5%/yr (2017–2021)"),
    ("EBITDA margin ", "down 12.3pp to 5.8%"),
    ("Thin, falling share ", "where markets are biggest:"),
], sz=12.5, c=WHITE, gap=9)
# share mini-table on dark
sr = [["Market","Share"],["UAE","~15%"],["KSA","~2%"],["Qatar","~7%"]]
yy=4.75
for i,row in enumerate(sr):
    rfill = NAVY2 if i==0 else None
    if rfill: rect(s,0.85,yy,4.6,0.4,fill=rfill)
    txt(s,1.0,yy,2.6,0.4,[[(row[0],{"sz":12,"b":i==0,"c":WHITE})]],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,3.2,yy,2.1,0.4,[[(row[1],{"sz":12,"b":True,"c":(TEAL if i>0 else WHITE)})]],anchor=MSO_ANCHOR.MIDDLE)
    yy+=0.44
# right: market tailwind + chart
txt(s, 6.1, 2.0, 6.7, 0.4, [[("THE MARKET IS A TAILWIND", {"sz":12,"b":True,"c":TEAL})]])
txt(s, 6.1, 2.38, 6.7, 0.3, [[("Core dairy market size, USD mn RSP", {"sz":10.5,"i":True,"c":GREY})]])
cd = CategoryChartData()
cd.categories = ["UAE","KSA","Qatar"]
cd.add_series("2021", (695,1790,255))
cd.add_series("2026E", (984,2319,373))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(6.1), Inches(2.75),
                        Inches(6.68), Inches(3.0), cd)
ch = gf.chart
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout=False
ch.legend.font.size = Pt(10)
ch.plots[0].series[0].format.fill.solid(); ch.plots[0].series[0].format.fill.fore_color.rgb = MGREY
ch.plots[0].series[1].format.fill.solid(); ch.plots[0].series[1].format.fill.fore_color.rgb = TEAL
ch.value_axis.visible=False; ch.value_axis.has_major_gridlines=False
ch.category_axis.tick_labels.font.size=Pt(11)
txt(s, 6.1, 5.8, 6.7, 0.4, [[("CAGR to 2026:  UAE +7.2%  ·  KSA +5.3%  ·  Qatar +7.9%", {"sz":11,"b":True,"c":NAVY})]])
rect(s, 6.1, 6.25, 6.68, 0.6, fill=LGREY)
txt(s, 6.25, 6.25, 6.5, 0.6, [[("Fastest pockets: ", {"sz":11,"b":True,"c":NAVY}),
    ("organic milk +11.8%, plant-based +9.9% (Qatar +13.6%), flavored yogurt +7–9%", {"sz":11,"c":DARKTX})]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Dairyworks P&L; Euromonitor retail value (RSP) 2021–2026 (UAE, KSA, Qatar); fact-pack share data.")
pagenum(s, 4)

# ============================================================ SLIDE 5: MARGIN BRIDGE
s = slide()
header(s, "Diagnosis A · Cost walk",
       "Two controllable lines — S&D (+7.9pp) and COGS (+5.2pp) — explain the entire 12-point collapse",
       "EBITDA margin bridge, 2017 to 2021 (% of revenue)")
rows = [
    ["Cost line","2017","2021","Change (pp)","Signal"],
    ["COGS","59.3%","64.5%","+5.2 worse","HIGH"],
    ["S&D","17.0%","24.9%","+7.9 worse","HIGH"],
    ["A&M","0.6%","0.6%","0.0 starved","HIGH"],
    ["G&A","5.0%","4.2%","−0.8 better","LOW"],
    ["EBITDA margin","18.1%","5.8%","−12.3","HIGH"],
]
th = table(s, 0.55, 1.95, 6.6, rows, [2.1,1.0,1.0,1.6,0.9],
           dot_cols={4:1}, dot_map=DOTMAP, bold_last=True, row_h=0.48)
# right rail
rect(s, 7.45, 1.95, 5.33, 4.0, fill=LGREY)
rect(s, 7.45, 1.95, 5.33, 0.5, fill=NAVY)
txt(s, 7.65, 1.95, 5.0, 0.5, [[("WHY EACH LINE MOVED", {"sz":11,"b":True,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
bullets(s, 7.7, 2.65, 4.95, 3.2, [
    ("COGS +5.2pp: ", "outdated plants, no scale economies, weak procurement"),
    ("S&D +7.9pp: ", "distribution dysfunction across all 3 countries — worst in outsourced KSA & Qatar (the single largest drag)"),
    ("A&M flat at 0.6%: ", "chronic brand under-investment vs peers' 2–3% — root of the awareness problem"),
], sz=12, gap=11)
rect(s, 0.55, 6.15, 12.23, 0.72, fill=NAVY2)
txt(s, 0.75, 6.15, 12.0, 0.72, [[("So what:  ", {"sz":13,"b":True,"c":TEAL}),
    ("Fixing distribution and cost alone closes ~13pp of the gap to peers. These are management levers, not market forces.", {"sz":13,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Dairyworks P&L 2017–2021 (COGS, S&D, A&M, G&A as % of revenue); fact-pack cost commentary.")
pagenum(s, 5)

# ============================================================ SLIDE 6: PORTFOLIO
s = slide()
header(s, "Diagnosis B · Portfolio",
       "The commodity core is melting (standard milk −8%, ice cream −10%) while premium/health compounds at 40% GP",
       "Dairyworks revenue and gross profit by SKU, 2017–2021")
rows = [
    ["Product","Rev '17","Rev '21","Rev CAGR","GP% '17","GP% '21","Verdict"],
    ["Standard milk, 1L","800","570","−8.1%","40%","30%","DEFEND"],
    ["Organic milk, 1L","360","513","+9.3%","40%","40%","SCALE"],
    ["Standard yogurt, 500g","340","285","−4.3%","40%","30%","FIX"],
    ["Flavored yogurt, 120g","160","304","+17.4%","40%","40%","SCALE"],
    ["Ice cream tub, 1L","340","228","−9.5%","44%","40%","REVIEW"],
    ["Total","2,000","1,900","−1.3%","41%","36%",""],
]
table(s, 0.55, 1.95, 8.3, rows, [2.25,0.95,0.95,1.05,0.85,0.85,1.4],
      dot_cols={6:1}, dot_map=DOTMAP, bold_last=True, row_h=0.46, sz=11, head_sz=9.5)
rect(s, 9.05, 1.95, 3.73, 4.0, fill=NAVY)
rect(s, 9.05, 1.95, 0.08, 4.0, fill=TEAL)
txt(s, 9.3, 2.1, 3.4, 0.4, [[("WHAT THE DATA SAYS", {"sz":11,"b":True,"c":TEAL})]])
bullets(s, 9.3, 2.6, 3.35, 3.2, [
    "Premium/health (organic milk + flavored yogurt) = ~43% of revenue at 40% GP, but under-scaled",
    "Commodity lines lost ~10pp of GP — where scale & cost disadvantages bite",
    "By geography: UAE −3.0%/yr; KSA +1.5% (only ~2% share = biggest headroom)",
], sz=11.5, c=WHITE, gap=10)
rect(s, 0.55, 6.15, 12.23, 0.72, fill=NAVY2)
txt(s, 0.75, 6.15, 12.0, 0.72, [[("So what:  ", {"sz":13,"b":True,"c":TEAL}),
    ("Reallocating mix to organic milk and flavored yogurt lifts blended margin and rides the fastest-growing market pockets at the same time.", {"sz":13,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Dairyworks product & geography sales and gross profit, 2017–2021 (UAE, KSA, Qatar aggregated).")
pagenum(s, 6)

# ============================================================ SLIDE 7: PEER BENCHMARK
s = slide()
header(s, "Diagnosis C · Competitive benchmark",
       "Peers earn 3–5x our margin on a similar cost base — the gap is distribution (S&D) and inverted brand spend",
       "Peer benchmark, 2021 (% of revenue)")
# chart: EBITDA margin ranked
cd = CategoryChartData()
cd.categories = ["Dairyworks","SADAFCO","NADEC","Almarai"]
cd.add_series("EBITDA margin", (5.8,17.0,19.2,27.0))
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.55), Inches(1.95),
                        Inches(5.6), Inches(3.9), cd)
ch = gf.chart; ch.has_legend=False
plot=ch.plots[0]; plot.has_data_labels=True
plot.data_labels.number_format='0.0"%"'; plot.data_labels.number_format_is_linked=False
plot.data_labels.font.size=Pt(11); plot.data_labels.font.bold=True
pts = plot.series[0].points
for i,c in enumerate([RED,TEAL,TEAL,TEAL]):
    pts[i].format.fill.solid(); pts[i].format.fill.fore_color.rgb=c
ch.value_axis.visible=False; ch.value_axis.has_major_gridlines=False
ch.category_axis.tick_labels.font.size=Pt(11)
txt(s, 0.55, 5.8, 5.6, 0.3, [[("EBITDA margin, 2021 (%)", {"sz":10.5,"i":True,"c":GREY})]], align=PP_ALIGN.CENTER)
# table on right
rows = [
    ["Company","COGS","S&D","A&M","EBITDA"],
    ["Dairyworks","64.5%","24.9%","0.6%","5.8%"],
    ["SADAFCO","64.0%","14.2%","2.2%","17.0%"],
    ["NADEC","57.0%","18.0%","2.8%","19.2%"],
    ["Almarai","55.8%","14.1%","2.0%","27.0%"],
]
table(s, 6.4, 1.95, 6.38, rows, [1.9,1.12,1.12,1.12,1.12], row_h=0.46, sz=11)
rect(s, 6.4, 4.5, 6.38, 1.35, fill=LGREY)
txt(s, 6.55, 4.6, 6.1, 0.35, [[("READ-ACROSS", {"sz":11,"b":True,"c":NAVY})]])
bullets(s, 6.55, 4.95, 6.1, 0.9, [
    "S&D is the biggest gap: 24.9% vs peers' 14–18% (~7–11pp)",
    "Brand spend inverted: 0.6% A&M vs 2–3% — starving demand, over-paying to supply",
], sz=10.5, gap=4)
rect(s, 0.55, 6.15, 12.23, 0.72, fill=NAVY2)
txt(s, 0.75, 6.15, 12.0, 0.72, [[("So what:  ", {"sz":13,"b":True,"c":TEAL}),
    ("SADAFCO proves 17% EBITDA is achievable at our COGS level — the prize is in distribution and brand, not only the factory.", {"sz":13,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Peer P&Ls (Almarai, NADEC, SADAFCO) and Dairyworks P&L, 2021 (% of revenue).")
pagenum(s, 7)

# ============================================================ SLIDE 8: FULL POTENTIAL
s = slide()
header(s, "Resolution · Full potential",
       "Four initiatives lift revenue +AED 800M and EBITDA +AED 384M — restoring an 18.3% margin in line with peers",
       "Value creation bridges, 2021 base to 2026 full potential")
# revenue waterfall-style chart
cd = CategoryChartData()
cd.categories = ["2021","Distribution","Premium.","UAE core","Adjacencies","2026 FP"]
cd.add_series("Revenue (AED mn)", (1900,260,300,180,60,2700))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.55), Inches(1.95),
                        Inches(7.3), Inches(3.5), cd)
ch=gf.chart; ch.has_legend=False
plot=ch.plots[0]; plot.has_data_labels=True
plot.data_labels.number_format='0'; plot.data_labels.number_format_is_linked=False
plot.data_labels.font.size=Pt(10); plot.data_labels.font.bold=True
plot.data_labels.position=XL_LABEL_POSITION.OUTSIDE_END
pts=plot.series[0].points
for i,c in enumerate([NAVY,TEAL,TEAL,TEAL,TEAL,GREEN]):
    pts[i].format.fill.solid(); pts[i].format.fill.fore_color.rgb=c
ch.value_axis.visible=False; ch.value_axis.has_major_gridlines=False
ch.category_axis.tick_labels.font.size=Pt(9.5)
txt(s, 0.55, 5.5, 7.3, 0.3, [[("Revenue bridge, AED mn:  1,900 → 2,700  (+7.3% CAGR)", {"sz":11,"b":True,"c":NAVY})]], align=PP_ALIGN.CENTER)
# EBITDA margin bridge table
rect(s, 8.05, 1.95, 4.73, 3.85, fill=LGREY)
rect(s, 8.05, 1.95, 4.73, 0.45, fill=NAVY)
txt(s, 8.2, 1.95, 4.5, 0.45, [[("EBITDA MARGIN BRIDGE (pp)", {"sz":11,"b":True,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
mb = [("Start 2021","5.8%",GREY),("Distribution / S&D turnaround","+8.4",GREEN),
      ("Manufacturing + procurement","+4.5",GREEN),("Portfolio premiumization","+1.5",GREEN),
      ("Brand reinvestment (A&M)","−1.9",RED),("Full potential 2026","18.3%",NAVY)]
yy=2.52
for i,(lab,val,c) in enumerate(mb):
    last=i==len(mb)-1
    if last: rect(s,8.2,yy-0.02,4.43,0.46,fill=TEAL)
    txt(s,8.3,yy,3.3,0.42,[[(lab,{"sz":11,"b":last,"c":(NAVY if last else DARKTX)})]],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,11.6,yy,0.95,0.42,[[(val,{"sz":11.5,"b":True,"c":(NAVY if last else c)})]],align=PP_ALIGN.RIGHT,anchor=MSO_ANCHOR.MIDDLE)
    yy+=0.52
rect(s, 0.55, 6.1, 12.23, 0.78, fill=NAVY)
txt(s, 0.75, 6.1, 12.0, 0.78, [[("Full potential:  ", {"sz":13.5,"b":True,"c":TEAL}),
    ("~AED 495M EBITDA by 2026 — ~4.5x the 2021 level — reached at peer-median economics, not best-in-class Almarai.", {"sz":13.5,"c":WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Team value creation model; Dairyworks P&L 2017–2021; peer benchmark; Euromonitor 2021–2026.")
pagenum(s, 8)

# ============================================================ SLIDE 9: FOUR INITIATIVES
s = slide()
header(s, "Resolution · The plan",
       "Four initiatives turn the diagnosis into value — a coherent, self-funding system",
       "Each initiative, its primary lever and target impact")
inits = [
    ("1", "DISTRIBUTION TURNAROUND", TEAL, "Largest EBITDA lever",
     ["Renegotiate/insource KSA & Qatar networks","Rebuild UAE route-to-market, win back shelf"],
     "S&D 24.9% → 16.5%  (+8.4pp)"),
    ("2", "COST & MANUFACTURING", AMBER, "Modernize & scale",
     ["Upgrade 3 UAE plants","Centralize procurement, capture scale"],
     "COGS 64.5% → 60.0%  (+4.5pp)"),
    ("3", "PORTFOLIO PREMIUMIZATION", GREEN, "Mix to premium/health",
     ["Scale organic milk & flavored yogurt","Rationalize commodity SKUs; enter plant-based"],
     "+AED 360M rev  ·  +1.5pp margin"),
    ("4", "BRAND & DEMAND RESET", RED, "Fix the awareness gap",
     ["Step up A&M 0.6% → 2.5%","Reposition to pull premium volume"],
     "Enables the full revenue bridge"),
]
positions = [(0.55,1.95),(6.67,1.95),(0.55,4.05),(6.67,4.05)]
cw, chh = 6.11, 1.95
for (num,title,color,tag,items,target),(x,y) in zip(inits,positions):
    rect(s, x, y, cw, chh, fill=WHITE, line=MGREY)
    rect(s, x, y, 0.1, chh, fill=color)
    rect(s, x+0.28, y+0.2, 0.62, 0.62, fill=color)
    txt(s, x+0.28, y+0.2, 0.62, 0.62, [[(num,{"sz":26,"b":True,"c":WHITE})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x+1.05, y+0.18, cw-1.2, 0.35, [[(title,{"sz":13,"b":True,"c":NAVY})]])
    txt(s, x+1.05, y+0.52, cw-1.2, 0.3, [[(tag,{"sz":10.5,"i":True,"c":color})]])
    bullets(s, x+1.05, y+0.88, cw-1.25, 0.8, items, sz=10.5, gap=3)
    rect(s, x+1.05, y+1.52, cw-1.35, 0.34, fill=LGREY)
    txt(s, x+1.15, y+1.52, cw-1.5, 0.34, [[("Target: ",{"sz":10.5,"b":True,"c":NAVY}),(target,{"sz":10.5,"b":True,"c":color})]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "Team synthesis of diagnostic findings; Dairyworks cost structure and portfolio data; peer benchmark.")
pagenum(s, 9)

# ============================================================ SLIDE 10: ROADMAP
s = slide()
header(s, "Implementation · Roadmap",
       "A three-horizon plan — stop the bleed, build the engine, reach full potential — each horizon self-funds the next",
       "Implementation roadmap with milestones and owners, 2026–2031")
hor = [
    ("HORIZON 1", "Stop the bleed", "0–12 months", NAVY, [
        "Renegotiate KSA & Qatar distribution contracts",
        "Procurement quick wins; rationalize loss-making SKUs",
        "Brand relaunch brief",
    ], "Milestone: S&D −3pp; break-even protected by M12", "Owner: COO · CPO · CMO"),
    ("HORIZON 2", "Build the engine", "12–36 months", NAVY2, [
        "Plant modernization capex",
        "Scale organic milk & flavored yogurt; KSA share offensive",
        "National brand campaign",
    ], "Milestone: EBITDA ~12%; KSA share 2%→4% by M36", "Owner: COO · CMO"),
    ("HORIZON 3", "Reach full potential", "36–60 months", TEAL, [
        "Enter plant-based & functional dairy",
        "Lead modern & online channels",
        "Embed premium mix",
    ], "Milestone: Rev ~AED 2,700M; EBITDA ~18.3% by Yr 5", "Owner: CEO · CSO"),
]
x=0.55; cw=3.97
for (h,name,tf_,color,items,mile,owner) in hor:
    rect(s, x, 1.95, cw, 4.5, fill=WHITE, line=MGREY)
    rect(s, x, 1.95, cw, 0.95, fill=color)
    txt(s, x+0.2, 2.02, cw-0.4, 0.3, [[(h,{"sz":11,"b":True,"c":TEAL if color!=TEAL else NAVY})]])
    txt(s, x+0.2, 2.3, cw-0.4, 0.35, [[(name,{"sz":15,"b":True,"c":WHITE})]])
    txt(s, x+0.2, 2.62, cw-0.4, 0.3, [[(tf_,{"sz":11,"c":WHITE})]])
    bullets(s, x+0.22, 3.1, cw-0.44, 2.0, items, sz=11.5, gap=8)
    rect(s, x+0.2, 5.25, cw-0.4, 0.72, fill=LGREY)
    txt(s, x+0.3, 5.3, cw-0.6, 0.65, [[(mile,{"sz":10,"b":True,"c":NAVY})]], anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x+0.2, 6.05, cw-0.4, 0.3, [[(owner,{"sz":10,"i":True,"c":GREY})]])
    x += cw + 0.2
# arrow band
source(s, "Team implementation plan; initiative economics from the value creation model.")
pagenum(s, 10)

# ============================================================ SLIDE 11: THE ASK
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 0, 0.35, SH, fill=TEAL)
txt(s, 0.9, 0.8, 11, 0.4, [[("THE ASK", {"sz":14,"b":True,"c":TEAL})]])
txt(s, 0.9, 1.25, 11.6, 1.2, [[("Approve the plan and fund the Year-1 reset", {"sz":32,"b":True,"c":WHITE})]])
rect(s, 0.9, 2.55, 5.5, 0.05, fill=TEAL)
# left: what we ask
txt(s, 0.9, 2.9, 6.2, 0.4, [[("WHAT WE ASK THE BOARD TO APPROVE", {"sz":13,"b":True,"c":TEAL})]])
bullets(s, 0.9, 3.5, 6.1, 3.0, [
    "Endorse the full-potential target: ~AED 2,700M revenue and ~AED 495M EBITDA (18.3%) by 2026",
    "Approve the four initiatives and the three-horizon sequence",
    "Authorize Horizon-1 funding: distribution renegotiation, procurement quick wins, SKU rationalization, brand relaunch",
], sz=14, c=WHITE, gap=14)
# right: why now
rect(s, 7.4, 2.9, 5.38, 3.6, fill=NAVY2)
rect(s, 7.4, 2.9, 0.08, 3.6, fill=AMBER)
txt(s, 7.65, 3.1, 5.0, 0.4, [[("WHY NOW", {"sz":13,"b":True,"c":AMBER})]])
bullets(s, 7.65, 3.7, 4.9, 2.4, [
    "At 5.8% EBITDA and near-zero EBIT, every year of inaction destroys value and cedes share in markets growing 5–8%",
    "Horizon-1 is operational self-help — low capital intensity, fast payback — and de-risks later growth investment",
], sz=13, c=WHITE, gap=12)
rect(s, 0.9, 6.75, 11.9, 0.5, fill=TEAL)
txt(s, 0.9, 6.75, 11.9, 0.5, [[("Decision: approve the plan and Year-1 reset  ·  Target outcome: +AED 384M EBITDA (~4.5x) over five years", {"sz":13.5,"b":True,"c":NAVY})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ============================================================ SLIDE 12: BACKUP DIVIDER
s = slide()
rect(s, 0, 0, SW, SH, fill=NAVY)
rect(s, 0, 3.3, SW, 0.9, fill=NAVY2)
txt(s, 0, 3.3, SW, 0.9, [[("Backup", {"sz":40,"b":True,"c":WHITE})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
rect(s, SW/2-1.2, 4.45, 2.4, 0.05, fill=TEAL)

# ============================================================ SLIDE 13: APPENDIX
s = slide()
header(s, "Appendix",
       "Discussion questions for the Board",
       "Key decisions and risks to pressure-test before committing capital")
qs = [
    ("Distribution: ", "insource KSA/Qatar or renegotiate? What is the make-vs-buy economics and transition risk?"),
    ("Capex: ", "what is the investment envelope and payback for modernizing the three UAE plants?"),
    ("Brand: ", "what A&M ramp and positioning move awareness from 1-in-5, and over what period?"),
    ("Portfolio: ", "which commodity SKUs do we exit, and how do we protect volume in the transition?"),
    ("Growth: ", "is KSA share recovery organic, or do we need M&A/partnership from a ~2% base?"),
    ("Risk: ", "key sensitivities — input-cost inflation, Almarai's competitive response — on the EBITDA bridge?"),
]
y=2.1
for i,(lab,rest) in enumerate(qs):
    rect(s, 0.6, y+0.05, 0.4, 0.4, fill=TEAL if i%2==0 else NAVY)
    txt(s, 0.6, y+0.05, 0.4, 0.4, [[(str(i+1),{"sz":14,"b":True,"c":WHITE})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, 1.2, y, 11.4, 0.7, [[(lab,{"sz":13.5,"b":True,"c":NAVY}),(rest,{"sz":13.5,"c":DARKTX})]], anchor=MSO_ANCHOR.MIDDLE)
    y+=0.78
source(s, "Team synthesis.")
pagenum(s, 13)

# ---- save ----
outdir = "commspro/2026-10-01_dairyworks-value-creation"
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, "2026-10-01_dairyworks-value-creation.pptx")
prs.save(out)
print("Saved:", out, "| slides:", len(prs.slides._sldIdLst))
