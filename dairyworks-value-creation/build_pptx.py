#!/usr/bin/env python3
"""Build a fully-native, editable PPTX of the Dairyworks value-creation deck.
Every element is a real PowerPoint shape/text box, positioned from the HTML
pixel coordinates (1280x720 canvas -> 13.333in x 7.5in at 96px/in)."""
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

EMU_PER_PX = 9525
def px(v): return Emu(int(round(v * EMU_PER_PX)))
def sz(px_size): return Pt(round(px_size * 0.75, 1))

# palette
INK   = RGBColor(0x19,0x1B,0x3A)
NAVY  = RGBColor(0x2B,0x2E,0x86)
NAVY2 = RGBColor(0x23,0x26,0x5f)
PERI  = RGBColor(0x6F,0x74,0xDB)
PERI2 = RGBColor(0x94,0x97,0xE8)
GREY  = RGBColor(0x6A,0x6E,0x7E)
MGREY = RGBColor(0xAE,0xB2,0xC0)
LINE  = RGBColor(0xCB,0xCF,0xDA)
LGREY = RGBColor(0xEE,0xF0,0xF7)
WHITE = RGBColor(0xFF,0xFF,0xFF)
TN_RED = RGBColor(0xE7,0x00,0x13)
EG_RED = RGBColor(0xCE,0x11,0x26)
GOLD   = RGBColor(0xC0,0x93,0x00)
MA_RED = RGBColor(0xC1,0x27,0x2D)
GREEN  = RGBColor(0x00,0x62,0x33)
BLACK  = RGBColor(0x00,0x00,0x00)
SERIF = "Georgia"
SANS  = "Arial"

prs = Presentation()
prs.slide_width  = px(1280)
prs.slide_height = px(720)
BLANK = prs.slide_layouts[6]

def add_slide():
    return prs.slides.add_slide(BLANK)

def _apply_runs(tf, paras, default):
    """paras: list of paragraphs; each paragraph is list of runs (text, style)."""
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = default.get('align', PP_ALIGN.LEFT)
        if default.get('line_spacing'): p.line_spacing = default['line_spacing']
        p.space_before = Pt(0)
        p.space_after = Pt(default.get('space_after', 0))
        if isinstance(para, tuple): para = [para]
        for run in para:
            txt = run[0]; st = run[1] if len(run) > 1 else {}
            r = p.add_run(); r.text = txt
            f = r.font
            f.name  = st.get('font', default.get('font', SANS))
            f.size  = st.get('size', default.get('size', sz(12)))
            f.bold  = st.get('bold', default.get('bold', False))
            f.italic= st.get('italic', default.get('italic', False))
            f.color.rgb = st.get('color', default.get('color', INK))

def box(slide, x, y, w, h, paras, **kw):
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = kw.get('wrap', True)
    tf.vertical_anchor = kw.get('anchor', MSO_ANCHOR.TOP)
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    _apply_runs(tf, paras, kw)
    return tb

def rect(slide, x, y, w, h, fill=None, line=None, line_w=1, rounded=False, rad=0.06, oval=False):
    shape_type = MSO_SHAPE.OVAL if oval else (MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE)
    shp = slide.shapes.add_shape(shape_type, px(x), px(y), px(w), px(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    if rounded:
        try: shp.adjustments[0] = rad
        except Exception: pass
    return shp

def shape_text(shp, paras, **kw):
    tf = shp.text_frame
    tf.word_wrap = kw.get('wrap', True)
    tf.vertical_anchor = kw.get('anchor', MSO_ANCHOR.MIDDLE)
    tf.margin_left = px(kw.get('ml', 0)); tf.margin_right = px(kw.get('mr', 0))
    tf.margin_top = 0; tf.margin_bottom = 0
    _apply_runs(tf, paras, kw)

def hline(slide, x, y, w, color=LINE, thick=1):
    rect(slide, x, y, w, thick, fill=color)
def vline(slide, x, y, h, color=LINE, thick=1):
    rect(slide, x, y, thick, h, fill=color)

# ---------- shared chrome ----------
def chrome(slide, crumb_pre, crumb_b, title_runs, pageno):
    box(slide, 760, 20, 480, 20,
        [[(crumb_pre, {'color':GREY,'size':sz(12)}), (crumb_b, {'color':INK,'size':sz(12),'bold':True})]],
        align=PP_ALIGN.RIGHT)
    box(slide, 52, 34, 1120, 70, [title_runs], font=SERIF, size=sz(26), bold=True,
        color=INK, line_spacing=1.08)
    hline(slide, 52, 138, 1176)
    box(slide, 1200, 695, 40, 18, [[(str(pageno), {'color':MGREY,'size':sz(11)})]], align=PP_ALIGN.RIGHT)

def src_note(slide, text, y=None, width=1176, note=False):
    yy = 686 if not note else 668
    box(slide, 52, yy, width, 26, [[(text, {'color':GREY,'size':sz(10.5)})]], line_spacing=1.3)

def hbar2(slide, x, y, w, label):
    r = rect(slide, x, y, w, 30, fill=NAVY, rounded=True, rad=0.12)
    shape_text(r, [[(label, {'color':WHITE,'size':sz(13),'bold':True})]],
               anchor=MSO_ANCHOR.MIDDLE, ml=14, mr=14)
    return r

def sowhat(slide, lab, text):
    r = rect(slide, 52, 610, 1176, 40, fill=PERI, rounded=True, rad=0.08)
    shape_text(r, [[(lab, {'color':WHITE,'size':sz(14.5),'bold':True}),
                    (text, {'color':WHITE,'size':sz(14.5)})]],
               anchor=MSO_ANCHOR.MIDDLE, ml=18, mr=18, line_spacing=1.2)

def prize(slide, x, y, w, big, small, h=70):
    r = rect(slide, x, y, w, h, fill=NAVY, rounded=True, rad=0.06)
    shape_text(r, [[(big, {'color':WHITE,'size':sz(28),'bold':True})],
                   [(small, {'color':WHITE,'size':sz(12.5)})]],
               anchor=MSO_ANCHOR.MIDDLE, ml=18, mr=16, line_spacing=1.1)

def chip(slide, x, y, w, runs, h=52):
    rect(slide, x, y, 4, h, fill=PERI)               # left accent
    r = rect(slide, x, y, w, h, fill=LGREY)
    r.line.fill.background()
    shape_text(r, [runs], anchor=MSO_ANCHOR.MIDDLE, ml=16, mr=14, size=sz(13), line_spacing=1.25)

def hbar_impact(slide, x, y, rows):
    """rows: list of (label, fill, bar_px_width, value_text). Drawn as a bar chart."""
    box(slide, x, y, 400, 18, [[('Revenue uplift by Year 5 — AED Mn (illustrative)',
        {'color':INK,'size':sz(13),'font':SERIF,'bold':True})]])
    row_y = y + 36
    track_left = x + 126
    for (label, fill, bw, val) in rows:
        box(slide, x, row_y+2, 118, 20, [[(label, {'color':INK,'size':sz(13),'bold':True})]],
            anchor=MSO_ANCHOR.MIDDLE)
        rect(slide, track_left, row_y, bw, 22, fill=fill, rounded=True, rad=0.12)
        box(slide, track_left+bw+8, row_y, 120, 22, [[(val, {'color':INK,'size':sz(12),'bold':True})]],
            anchor=MSO_ANCHOR.MIDDLE)
        row_y += 42

def solution_card(slide, x, y, w, h, num, name, what, why):
    rect(slide, x, y, w, h, fill=WHITE, line=LINE, rounded=True, rad=0.04)
    cy = y + h/2
    circ = rect(slide, x+18, cy-23, 46, 46, fill=NAVY, oval=True)
    shape_text(circ, [[(str(num), {'color':WHITE,'size':sz(20),'bold':True})]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tx = x + 82; tw = w - 100
    box(slide, tx, y+14, tw, 20, [[(name, {'color':NAVY,'size':sz(15.5),'bold':True,'font':SERIF})]])
    box(slide, tx, y+40, tw, h-50,
        [[('What: ', {'bold':True,'color':NAVY,'size':sz(12)}), (what, {'size':sz(12),'color':INK})],
         [('Why: ', {'bold':True,'color':NAVY,'size':sz(12)}), (why, {'size':sz(12),'color':INK})]],
        line_spacing=1.1, space_after=3)

# =========================================================================
# SLIDE 1 — Revenue upside
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Revenue growth',
       [('Premium already grows ~12% a year, and we have not raised price in five years', {})],
       1)
box(s, 52, 112, 600, 22, [[('Revenue by portfolio tier, 2017\u201321', {'italic':True,'color':GREY,'size':sz(14)})]])
# legend
lx = 1000
rect(s, lx, 152, 14, 14, fill=NAVY); box(s, lx+20, 150, 90, 18, [[('Commodity',{'size':sz(13)})]], anchor=MSO_ANCHOR.MIDDLE)
rect(s, lx+2, 172, 14, 14, fill=PERI); box(s, lx+22, 170, 90, 18, [[('Premium',{'size':sz(13)})]], anchor=MSO_ANCHOR.MIDDLE)
box(s, 52, 172, 400, 20, [[('Revenue by portfolio tier, AED Mn', {'font':SERIF,'bold':True,'size':sz(16),'color':INK})]])
# stacked bars
baseline_y = 612
cols = [
    (78,  '26%','2,000', 237,'1,480', 83,'520'),
    (170, '29%','2,020', 230,'1,435', 94,'585'),
    (262, '37%','2,010', 203,'1,267', 119,'743'),
    (354, '42%','1,960', 182,'1,138', 132,'822'),
    (446, '43%','1,900', 173,'1,083', 131,'817'),
]
years = ['2017','2018','2019','2020','2021']
for i,(cx,pill,tot,ch,cl,ph,pl) in enumerate(cols):
    cy = baseline_y - ch
    rc = rect(s, cx, cy, 68, ch, fill=NAVY)
    shape_text(rc, [[(cl,{'color':WHITE,'size':sz(12),'bold':True})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    py = cy - ph
    rp = rect(s, cx, py, 68, ph, fill=PERI)
    shape_text(rp, [[(pl,{'color':WHITE,'size':sz(12),'bold':True})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, cx-4, py-24, 76, 18, [[(tot,{'size':sz(13),'bold':True,'color':INK})]], align=PP_ALIGN.CENTER)
    pr = rect(s, cx+7, py-52, 54, 24, fill=NAVY, rounded=True, rad=0.5)
    shape_text(pr, [[(pill,{'color':WHITE,'size':sz(13),'bold':True})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(s, cx-4, baseline_y+8, 76, 18, [[(years[i],{'size':sz(13),'bold':True,'color':INK})]], align=PP_ALIGN.CENTER)
hline(s, 78, baseline_y, 440, color=INK)
# CAGR compare block (x base 560, y base 214)
bx = 560
box(s, bx, 220, 140, 16, [[('CAGR 2017\u201321', {'color':GREY,'size':sz(12)})]])
box(s, bx+140, 214, 110, 20, [[('Premium',{'font':SERIF,'bold':True,'size':sz(17),'color':PERI})]], align=PP_ALIGN.CENTER)
box(s, bx+235, 214, 120, 20, [[('Commodity',{'font':SERIF,'bold':True,'size':sz(17),'color':NAVY})]], align=PP_ALIGN.CENTER)
rows = [('Revenue\ngrowth', 70, '+12%','\u22128%'),
        ('Volume\ngrowth', 150, '+11%','\u22128%'),
        ('Price\ngrowth', 230, '0%','0%')]
for lab, top, pv, cv in rows:
    parts = lab.split('\n')
    box(s, bx, 214+top, 140, 40,
        [[(parts[0],{'bold':True,'size':sz(15),'color':INK})],[(parts[1],{'bold':True,'size':sz(15),'color':INK})]],
        line_spacing=1.05)
    box(s, bx+150, 214+top-4, 90, 40, [[(pv,{'size':sz(30),'bold':True,'color':PERI})]], align=PP_ALIGN.CENTER)
    box(s, bx+245, 214+top-4, 95, 40, [[(cv,{'size':sz(30),'bold':True,'color':NAVY})]], align=PP_ALIGN.CENTER)
box(s, bx, 514, 330, 60, [[('Price per SKU is identical in 2017 and 2021 — every dirham of decline is lost volume.',
    {'italic':True,'size':sz(11.5),'color':GREY})]], line_spacing=1.2)
vline(s, 928, 208, 420, color=LINE)
# rail
rail = [
    [('\u2022  ',{'color':NAVY,'bold':True}),('Price frozen for 5 years. ',{'bold':True}),
     ('Every SKU holds its 2017 price; on commodity lines cost inflation cut ',{}),
     ('GP% from 40%\u219230% ',{'color':NAVY,'bold':True}),('— pricing is untapped and pure margin.',{})],
    [('\u2022  ',{'color':NAVY,'bold':True}),('Volume lost to the market. ',{'bold':True}),
     ('Our volume fell while the category grew ~4%/yr — ',{}),
     ('share recovery is the largest pool.',{'bold':True})],
    [('\u2022  ',{'color':NAVY,'bold':True}),('Mix is already winning. ',{'bold':True}),
     ('Premium rose ',{}),('26%\u219243% of revenue ',{'color':PERI,'bold':True}),
     ('at ~+12%/yr and holds 40% GP.',{})],
]
yy = 214
for item in rail:
    tb = box(s, 952, yy, 300, 90, [item], size=sz(13.5), line_spacing=1.15)
    yy += 96
box(s, 52, 652, 1176, 22, [[('Note: Premium = organic milk + flavoured yogurt; Commodity = standard milk, standard yogurt, ice cream. Price = revenue \u00f7 volume per SKU. CAGR = compound annual growth rate 2017\u201321.',
    {'color':GREY,'size':sz(10.5)})]], line_spacing=1.3)
box(s, 52, 686, 1176, 22, [[('Source: Dairyworks product & geography sales and GP (2017\u20132021); Euromonitor UAE retail value (RSP).',
    {'color':GREY,'size':sz(10.5)})]])

# =========================================================================
# SLIDE 2 — Five-lever overview (native table)
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Revenue levers overview',
       [('Five levers rebuild revenue to ~AED 2.7bn by Year 5', {})], 2)
box(s, 52, 112, 1120, 22, [[('Sequenced from the fastest, self-funding levers to longer-horizon growth; impact ranges illustrative',
    {'italic':True,'color':GREY,'size':sz(14)})]])
rows_ov = [
    ('1','Pricing & revenue mgmt','Recover five years of untaken price; price-pack architecture; trade-spend reset','+~AED 200M'),
    ('2','Share recovery','Rebuild UAE route-to-market, reset A&M 0.6%\u2192~3%, win back KSA & Qatar listings','+~AED 250M'),
    ('3','Mix & premiumization','Scale organic milk & flavoured yogurt; premiumize and relaunch ice cream','+~AED 120M'),
    ('4','New categories','Enter plant-based & sour-milk adjacencies on a proven best-practice playbook','+~AED 110M'),
    ('5','New markets','Scale KSA and enter North Africa (Egypt, Morocco) via export / distributor model','+~AED 120M'),
]
tbl_shape = s.shapes.add_table(len(rows_ov)+1, 3, px(52), px(166), px(1176), px(330))
table = tbl_shape.table
table.columns[0].width = px(260); table.columns[1].width = px(766); table.columns[2].width = px(150)
table.first_row = False; table.horz_banding = False
hdr = ['Revenue lever','What we will do','Value captured (Year 5)']
for c, text in enumerate(hdr):
    cell = table.cell(0, c)
    cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = px(12); cell.margin_right = px(12); cell.margin_top = px(6); cell.margin_bottom = px(6)
    p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT if c==2 else PP_ALIGN.LEFT
    r = p.add_run(); r.text = text; r.font.size = sz(13); r.font.bold = True
    r.font.color.rgb = WHITE; r.font.name = SANS
for i,(n,lev,what,val) in enumerate(rows_ov, start=1):
    bg = LGREY if i%2==0 else WHITE
    for c in range(3):
        cell = table.cell(i, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = bg
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = px(12); cell.margin_right = px(12); cell.margin_top = px(6); cell.margin_bottom = px(6)
    c0 = table.cell(i,0).text_frame.paragraphs[0]
    rn = c0.add_run(); rn.text = n+'   '; rn.font.bold=True; rn.font.color.rgb=PERI; rn.font.size=sz(14); rn.font.name=SANS
    rl = c0.add_run(); rl.text = lev; rl.font.size=sz(14); rl.font.color.rgb=INK; rl.font.name=SANS
    c1 = table.cell(i,1).text_frame.paragraphs[0]
    r1 = c1.add_run(); r1.text = what; r1.font.size=sz(14); r1.font.color.rgb=INK; r1.font.name=SANS
    c2 = table.cell(i,2).text_frame.paragraphs[0]; c2.alignment=PP_ALIGN.RIGHT
    r2 = c2.add_run(); r2.text = val; r2.font.size=sz(14); r2.font.bold=True; r2.font.color.rgb=NAVY; r2.font.name=SANS
box(s, 52, 686, 1176, 22, [[('Impact ranges are illustrative, from the team value-creation model. Source: Dairyworks product & geography sales and GP (2017\u20132021); Euromonitor; peer benchmark.',
    {'color':GREY,'size':sz(10.5)})]])

# =========================================================================
# SLIDE 3 — Lever 1 Pricing (solutions / impact)
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Lever 1 of 5 · Pricing & revenue management',
       [('Lever 1 — Price has been flat for five years; a modest rise restores commodity margin', {})], 3)
box(s, 52, 112, 1120, 22, [[('The pricing solutions, and the revenue and margin they unlock',{'italic':True,'color':GREY,'size':sz(14)})]])
hbar2(s, 52, 166, 560, 'The solutions')
solution_card(s, 52, 216, 560, 86, 1, 'Recover list price',
    'Phase modest increases — single-digit to mid-teens — across commodity lines.',
    'Price frozen five years; cost inflation cut commodity GP from 40%\u219230% — pure recoverable margin.')
solution_card(s, 52, 314, 560, 86, 2, 'Price-pack architecture',
    'Entry, core and premium price points; smaller packs at a higher price per kg.',
    'Lifts effective price without sticker shock, and keeps an opening price point for value shoppers.')
solution_card(s, 52, 412, 560, 86, 3, 'Premium price ladders',
    'Raise prices on organic and flavoured lines.',
    'They already grow double-digit at 40% GP — willingness-to-pay is proven, so the headroom is real.')
hbar2(s, 652, 166, 576, 'The impact')
hbar_impact(s, 652, 216, [
    ('Price recovery', NAVY, 340, '~AED 150M'),
    ('Price-pack', PERI, 68, '~AED 30M'),
    ('Premium ladders', PERI2, 45, '~AED 20M'),
])
chip(s, 652, 400, 576, [('Commodity gross margin ',{'size':sz(13)}),
    ('30% \u2192 ~40%',{'size':sz(13),'bold':True,'color':NAVY}),
    (' — nearly all of the price increase drops straight through to profit.',{'size':sz(13)})])
prize(s, 652, 470, 576, '+~AED 200M revenue', '~90% flows to gross profit. Fastest, lowest-capital lever — start in Horizon 1.')
sowhat(s, 'So what:  ', 'Pricing is the fastest win and nearly all margin — flat prices leave ~half the commodity GP erosion on the table.')
box(s, 52, 686, 1176, 22, [[('Source: Dairyworks product & geography sales and GP (2017\u20132021); impact split illustrative, from the value-creation model. Price = revenue \u00f7 volume per SKU.',{'color':GREY,'size':sz(10.5)})]])

# =========================================================================
# SLIDE 4 — Lever 2 Share
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Lever 2 of 5 · Share recovery (distribution & brand)',
       [('Lever 2 — We shrank while the market grew; closing the gap is the biggest prize', {})], 4)
box(s, 52, 112, 1120, 22, [[('We shrank while the market grew — distribution and brand win it back',{'italic':True,'color':GREY,'size':sz(14)})]])
hbar2(s, 52, 166, 560, 'The solutions')
solution_card(s, 52, 216, 560, 86, 1, 'Rebuild route-to-market',
    'Fix on-shelf availability, distribution reach and modern-trade + online execution.',
    'Availability slipped while the market grew — shoppers can\u2019t buy what they can\u2019t find.')
solution_card(s, 52, 314, 560, 86, 2, 'Relaunch the brand',
    'Step up marketing to peer levels and relaunch to lift recognition.',
    'Spend is a fraction of peers and few shoppers recognise us — nothing pulls demand.')
solution_card(s, 52, 412, 560, 86, 3, 'Win back export listings',
    'Regain the KSA & Qatar listings we lost.',
    'We handed shelf — and the shopper relationship — straight to competitors.')
hbar2(s, 652, 166, 576, 'The impact')
hbar_impact(s, 652, 216, [
    ('Distribution & channels', NAVY, 340, '~AED 120M'),
    ('Brand relaunch', PERI, 226, '~AED 80M'),
    ('Export listings', PERI2, 142, '~AED 50M'),
])
chip(s, 652, 400, 576, [('Just growing ',{'size':sz(13)}),
    ('with the market (~4%/yr)',{'size':sz(13),'bold':True,'color':NAVY}),
    (' — not even gaining share — stabilises then recovers share.',{'size':sz(13)})])
prize(s, 652, 470, 576, '+~AED 250M revenue', 'The largest pool — build through Horizons 1\u20132.')
sowhat(s, 'So what:  ', 'Just growing with the market — not even gaining share — wins back the most revenue; distribution and brand are how.')
box(s, 52, 686, 1176, 22, [[('Source: Dairyworks product & geography volumes (2017\u20132021); Euromonitor UAE retail value; 2019 Nielsen brand recognition; peer A&M benchmark.',{'color':GREY,'size':sz(10.5)})]])

# =========================================================================
# SLIDE 5 — Lever 3 Mix
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Lever 3 of 5 · Mix & premiumization',
       [('Lever 3 — Shift the mix to premium; it lifts revenue and margin at once', {})], 5)
box(s, 52, 112, 1120, 22, [[('Premium already grew from 26% to 43% of revenue — push it further',{'italic':True,'color':GREY,'size':sz(14)})]])
hbar2(s, 52, 166, 560, 'The solutions')
solution_card(s, 52, 216, 560, 86, 1, 'Scale the premium winners',
    'Put volume, marketing and shelf behind organic milk & flavoured yogurt.',
    'They grow double-digit at 40% margin — the mix already shifts our way.')
solution_card(s, 52, 314, 560, 86, 2, 'Premiumize & relaunch ice cream',
    'Re-platform our highest-margin category and relaunch it premium.',
    'It earns 40% margin yet is declining fastest — the biggest self-help gap.')
solution_card(s, 52, 412, 560, 86, 3, 'Add premium formats',
    'Launch high-protein, single-serve and gifting packs.',
    'New formats recruit new shoppers at premium price points.')
hbar2(s, 652, 166, 576, 'The impact')
hbar_impact(s, 652, 216, [
    ('Scale winners', NAVY, 308, '~AED 55M'),
    ('Ice-cream relaunch', PERI, 224, '~AED 40M'),
    ('Premium formats', PERI2, 140, '~AED 25M'),
])
chip(s, 652, 400, 576, [('Premium rises ',{'size':sz(13)}),
    ('43% \u2192 >55% of revenue',{'size':sz(13),'bold':True,'color':NAVY}),
    (' — blended gross margin up ',{'size':sz(13)}),('2\u20133pp',{'size':sz(13),'bold':True,'color':NAVY}),('.',{'size':sz(13)})])
prize(s, 652, 470, 576, '+~AED 120M revenue · margin-accretive', 'Compounds over Horizons 2\u20133 as the mix shifts.')
sowhat(s, 'So what:  ', 'Mix is the one lever that lifts revenue and margin at once — and the trend is already with us.')
box(s, 52, 686, 1176, 22, [[('Source: Dairyworks product & geography sales and GP (2017\u20132021); impact split illustrative, from the value-creation model.',{'color':GREY,'size':sz(10.5)})]])

# =========================================================================
# SLIDE 6 — Lever 4 New categories (best practice left / adjacencies+impact right)
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Lever 4 of 5 · New categories',
       [('Lever 4 — Enter fast-growing categories we are missing, using a proven playbook', {})], 6)
box(s, 52, 112, 1120, 22, [[('What has worked for other brands — and the adjacencies to copy it into',{'italic':True,'color':GREY,'size':sz(14)})]])
hbar2(s, 52, 166, 560, 'Best practice — proven by other brands')
def bpcard(slide, x, y, w, h, title, runs):
    rect(slide, x, y, w, h, fill=WHITE, line=LINE, rounded=True, rad=0.05)
    box(slide, x+13, y+9, w-26, 18, [[(title,{'font':SERIF,'bold':True,'size':sz(14),'color':NAVY})]])
    box(slide, x+13, y+30, w-26, h-36, [runs], line_spacing=1.15, size=sz(12))
bpcard(s, 52, 216, 560, 64, 'Oatly — plant-based',
    [('Bold rebrand + taste-led, packaging-as-media \u2192 ',{'size':sz(12)}),
     ('+700% demand, 21% CAGR',{'size':sz(12),'bold':True,'color':PERI}),
     ('. Lesson: lead on ',{'size':sz(12)}),('taste',{'size':sz(12),'bold':True,'color':NAVY}),(', not just health.',{'size':sz(12)})])
bpcard(s, 52, 290, 560, 64, 'Chobani — protein / Greek yogurt',
    [('Omnichannel + sampling \u2192 ',{'size':sz(12)}),
     ('+8pt awareness, 51% new buyers, $10.60 ROAS',{'size':sz(12),'bold':True,'color':PERI}),
     ('. Lesson: recruit ',{'size':sz(12)}),('new households',{'size':sz(12),'bold':True,'color':NAVY}),(' via retail media & trial.',{'size':sz(12)})])
bpcard(s, 52, 364, 560, 64, 'Halo Top — better-for-you ice cream',
    [('Lead-retailer launch + in-store sampling \u2192 ',{'size':sz(12)}),
     ('#3 UK brand within 12 months',{'size':sz(12),'bold':True,'color':PERI}),
     ('. Lesson: anchor on one retailer, drive ',{'size':sz(12)}),('trial',{'size':sz(12),'bold':True,'color':NAVY}),('.',{'size':sz(12)})])
chip(s, 52, 440, 560, [('The playbook for us: ',{'size':sz(12.5),'bold':True,'color':NAVY}),
    ('enter on a clear better-for-you proposition, lead with taste, launch with a lead retailer + sampling, and amplify through online / quick-commerce.',{'size':sz(12.5)})], h=60)
hbar2(s, 652, 166, 576, 'The adjacencies — and the prize')
box(s, 652, 214, 500, 18, [[('Adjacencies we don\u2019t yet play in — UAE market CAGR 2021\u201326E',{'font':SERIF,'bold':True,'size':sz(13),'color':INK})]])
adj = [('Plant-based milk', PERI, 297, '+9.9%/yr'),
       ('Sour-milk products', PERI, 255, '+8.5%/yr'),
       ('Flavoured milk drinks', PERI2, 204, '+6.8%/yr'),
       ('Drinking yogurt', PERI2, 186, '+6.2%/yr')]
ay = 246
for (label, fill, bw, val) in adj:
    box(s, 652, ay+2, 118, 20, [[(label,{'size':sz(13),'bold':True})]], anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 652+126, ay, bw, 22, fill=fill, rounded=True, rad=0.12)
    box(s, 652+126+bw+8, ay, 120, 22, [[(val,{'size':sz(12),'bold':True})]], anchor=MSO_ANCHOR.MIDDLE)
    ay += 36
chip(s, 652, 400, 576, [('All four grow faster than our categories, and we have ',{'size':sz(13)}),
    ('zero presence',{'size':sz(13),'bold':True,'color':NAVY}),
    (' — existing chilled distribution keeps entry low-cost.',{'size':sz(13)})])
prize(s, 652, 470, 576, '+~AED 110M revenue', 'Follow a proven path, not invent one — Horizons 2\u20133.')
sowhat(s, 'So what:  ', 'These categories are large and fast-growing, and the winning formula is known — we follow a proven path, not invent one.')
box(s, 52, 686, 1176, 22, [[('Source: Euromonitor UAE retail value (2021\u201326E). Best-practice results: Oatly / Forsman & Bodenfors; Chobani / Walmart Connect & Snapchat; Halo Top / dunnhumby & Shopkick case studies.',{'color':GREY,'size':sz(10.5)})]])

# =========================================================================
# SLIDE 7 — Lever 5 New markets (markets+flags left / impact right)
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Lever 5 of 5 · New markets',
       [('Lever 5 — Enter Tunisia, Egypt and Morocco first, in that order', {})], 7)
box(s, 52, 112, 1120, 22, [[('Ranked on a 14-factor entry scorecard; KSA, UAE & Qatar already served',{'italic':True,'color':GREY,'size':sz(14)})]])
hbar2(s, 52, 166, 560, 'The priority markets')
def flag_tunisia(slide, x, y):
    rect(slide, x, y, 34, 23, fill=TN_RED)
    rect(slide, x+10, y+4, 15, 15, fill=WHITE, oval=True)
    rect(slide, x+13, y+5.5, 12, 12, fill=TN_RED, oval=True)
    rect(slide, x+16, y+7, 9, 9, fill=WHITE, oval=True)
def flag_egypt(slide, x, y):
    rect(slide, x, y, 34, 7.7, fill=EG_RED)
    rect(slide, x, y+7.7, 34, 7.6, fill=WHITE)
    rect(slide, x, y+15.3, 34, 7.7, fill=BLACK)
    rect(slide, x+13, y+8, 8, 8, fill=GOLD, oval=True)
def flag_morocco(slide, x, y):
    rect(slide, x, y, 34, 23, fill=MA_RED)
    st = slide.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, px(x+8), px(y+4), px(18), px(15))
    st.fill.background(); st.line.color.rgb = GREEN; st.line.width = Pt(1.2); st.shadow.inherit=False
def market_card(slide, y, flag_fn, num, name, score_runs, desc_runs):
    x, w, h = 52, 560, 80
    rect(slide, x, y, w, h, fill=WHITE, line=LINE, rounded=True, rad=0.05)
    flag_fn(slide, x+18, y+16)
    circ = rect(slide, x+62, y+13, 25, 25, fill=NAVY, oval=True)
    shape_text(circ, [[(str(num),{'color':WHITE,'size':sz(13),'bold':True})]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    box(slide, x+96, y+14, 180, 24, [[(name,{'font':SERIF,'bold':True,'size':sz(16.5),'color':NAVY})]], anchor=MSO_ANCHOR.MIDDLE)
    box(slide, x+300, y+14, w-320, 24, [score_runs], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    box(slide, x+18, y+46, w-36, 26, [desc_runs], size=sz(12), line_spacing=1.15)
market_card(s, 216, flag_tunisia, 1, 'Tunisia',
    [('Score ',{'size':sz(11.5),'color':GREY,'bold':True}),('77.3',{'size':sz(11.5),'color':NAVY,'bold':True}),
     (' · Rank ',{'size':sz(11.5),'color':GREY,'bold':True}),('#1',{'size':sz(11.5),'color':NAVY,'bold':True})],
    [('Fastest-growing market (',{'size':sz(12)}),('+11.2%/yr',{'size':sz(12),'bold':True,'color':NAVY}),
     ('). Lead with ',{'size':sz(12)}),('ice cream & flavoured yoghurt',{'size':sz(12),'bold':True,'color':NAVY}),('.',{'size':sz(12)})])
market_card(s, 314, flag_egypt, 2, 'Egypt',
    [('Score ',{'size':sz(11.5),'color':GREY,'bold':True}),('75.4',{'size':sz(11.5),'color':NAVY,'bold':True}),
     (' · Rank ',{'size':sz(11.5),'color':GREY,'bold':True}),('#2',{'size':sz(11.5),'color':NAVY,'bold':True})],
    [('Best size-and-growth balance — largest unpenetrated base (',{'size':sz(12)}),('+7.0%/yr',{'size':sz(12),'bold':True,'color':NAVY}),(').',{'size':sz(12)})])
market_card(s, 412, flag_morocco, 3, 'Morocco',
    [('Score ',{'size':sz(11.5),'color':GREY,'bold':True}),('60.4',{'size':sz(11.5),'color':NAVY,'bold':True}),
     (' · ',{'size':sz(11.5),'color':GREY,'bold':True}),('#3 unpenetrated',{'size':sz(11.5),'color':NAVY,'bold':True})],
    [('Large, steady base (',{'size':sz(12)}),('+6.5%/yr',{'size':sz(12),'bold':True,'color':NAVY}),(') — strong in ice cream & flavoured yoghurt.',{'size':sz(12)})])
hbar2(s, 652, 166, 576, 'The impact')
hbar_impact(s, 652, 216, [
    ('Egypt', NAVY, 308, '~AED 55M'),
    ('Morocco', PERI, 224, '~AED 40M'),
    ('Tunisia', PERI2, 140, '~AED 25M'),
])
chip(s, 652, 400, 576, [('Asset-light',{'size':sz(13),'bold':True,'color':NAVY}),
    (' distributor / export entry off existing plants — sequenced in scorecard order.',{'size':sz(13)})])
prize(s, 652, 470, 576, '+~AED 120M revenue', 'Longer-horizon; sequence after the home-market turnaround (Horizon 3).')
sowhat(s, 'So what:  ', 'Our GCC markets are already served — the next growth comes from North Africa, led by Tunisia and Egypt.')
box(s, 52, 686, 1176, 22, [[('Source: Team market-entry scorecard (14-factor; scores B21:O34, ranking B37:H49) and portfolio-relevant dairy market size & CAGR, 2022\u201326E. KSA, UAE & Qatar excluded as already penetrated; impact split illustrative.',{'color':GREY,'size':sz(10.5)})]])

# =========================================================================
# SLIDE 8 — Implementation roadmap
# =========================================================================
s = add_slide()
chrome(s, 'Value creation  ›  ', 'Implementation roadmap',
       [('A three-phase plan lifts EBITDA margin from 5.8% to ~16.5%, each phase funding the next', {})], 8)
box(s, 52, 112, 1120, 22, [[('Three phases over five years: stop the bleed, build the engine, reach full potential',{'italic':True,'color':GREY,'size':sz(14)})]])
def phase(slide, x, w, k, t):
    r = rect(slide, x, 152, w, 46, fill=NAVY, rounded=True, rad=0.08)
    shape_text(r, [[(k,{'color':WHITE,'size':sz(11),'bold':True})],[(t,{'color':WHITE,'size':sz(14),'bold':True,'font':SERIF})]],
               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
phase(s, 250, 316, 'HORIZON 1', 'Stop the bleed · 0\u201312m')
phase(s, 574, 322, 'HORIZON 2', 'Build the engine · 12\u201336m')
phase(s, 904, 324, 'HORIZON 3', 'Full potential · 36\u201360m')
for sx in (250, 574, 904, 1228):
    vline(s, sx, 152, 392, color=LINE)
def rbar(slide, x, y, w, fill, text):
    r = rect(slide, x, y, w, 32, fill=fill, rounded=True, rad=0.14)
    shape_text(r, [[(text,{'color':WHITE,'size':sz(11.5),'bold':True})]], anchor=MSO_ANCHOR.MIDDLE, ml=12, mr=8)
def wslab(slide, y, l1, l2):
    box(slide, 52, y, 190, 36, [[(l1,{'size':sz(12.5),'bold':True})],[(l2,{'size':sz(12.5),'bold':True})]], line_spacing=1.05)
wslab(s, 214, '1 · Pricing &', 'revenue mgmt')
rbar(s, 254, 208, 308, NAVY, 'List-price recovery + promo reset')
rbar(s, 578, 208, 314, PERI, 'Price-pack architecture')
wslab(s, 266, '2 · Share recovery', '(distribution+brand)')
rbar(s, 254, 260, 308, NAVY, 'Fix availability; KSA & Qatar listings')
rbar(s, 578, 260, 646, PERI, 'Rebuild UAE RTM; A&M reset 0.6%\u2192~3%; relaunch')
wslab(s, 318, '3 · Mix &', 'premiumization')
rbar(s, 578, 312, 314, PERI, 'Scale organic & flavoured; relaunch ice cream')
rbar(s, 908, 312, 316, PERI2, 'Premium mix embedded')
wslab(s, 370, '4 · New', 'categories')
rbar(s, 578, 364, 314, PERI, 'Pilot plant-based & sour milk')
rbar(s, 908, 364, 316, PERI2, 'Scale adjacencies nationally')
wslab(s, 422, '5 · New', 'markets')
rbar(s, 908, 416, 316, PERI2, 'Scale KSA; enter Egypt & Morocco')
def mstone(slide, x, w, head, body):
    r = rect(slide, x, 470, w, 60, fill=LGREY)
    r.line.fill.background()
    shape_text(r, [[(head,{'color':NAVY,'size':sz(10.5),'bold':True})],[(body,{'color':INK,'size':sz(11)})]],
               anchor=MSO_ANCHOR.TOP, ml=10, mr=10, line_spacing=1.2, space_after=2)
mstone(s, 254, 308, 'MILESTONE · YEAR 1', 'Break-even protected; S&D \u22123pp; price recovered on commodity lines')
mstone(s, 578, 314, 'MILESTONE · YEAR 3', 'EBITDA margin ~12%; UAE share stabilised; adjacencies piloted')
mstone(s, 908, 316, 'MILESTONE · YEAR 5', 'Revenue ~AED 2.7bn; EBITDA margin ~16.5% (~AED 445M)')
box(s, 52, 556, 1176, 24,
    [[('EBITDA margin trajectory:   ',{'bold':True,'color':INK,'size':sz(12)}),
      ('5.8%',{'bold':True,'color':NAVY,'size':sz(14)}),('   \u2192   ',{'size':sz(12)}),
      ('~12%',{'bold':True,'color':PERI,'size':sz(14)}),('   \u2192   ',{'size':sz(12)}),
      ('~16.5%',{'bold':True,'color':NAVY,'size':sz(14)}),
      ('     each horizon funds the investment of the next',{'italic':True,'size':sz(12),'color':GREY})]],
    anchor=MSO_ANCHOR.MIDDLE)
box(s, 52, 686, 1176, 22, [[('Source: Team value-creation plan; Dairyworks P&L and peer benchmark; initiative economics from the value-creation model. Timeframes indicative.',{'color':GREY,'size':sz(10.5)})]])

dest = "/workspace/dairyworks-value-creation/Dairyworks-value-creation-roadmap.pptx"
prs.save(dest)
import os
print("saved", dest, os.path.getsize(dest), "bytes;", len(prs.slides._sldIdLst), "slides")
