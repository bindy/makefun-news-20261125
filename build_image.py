#!/usr/bin/env python3
"""Draw the 25 Nov 2026 world-news image: 30 stories on a 5 by 6 grid.

Pillow draws the whole page, so every headline stays legible. Each story
gets a card with a region tag, a short headline and one line of detail.
The stories are the ones reported on 25 Nov 2026, gathered from Reuters,
AP and other roundups on 26 Nov 2026. Nothing from the 20, 21 or 22 Nov
entries is repeated: the day's own developments lead (Riyadh, the Gulf,
Ukraine's grid, the Shanghai probe).
"""
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
PAPER_RGB = (255, 255, 255)
INK_RGB = (17, 24, 39)
SOFT_RGB = (75, 85, 99)
HEADER_PX = 88
FOOTER_PX = 28
PAD = 12
GUTTER = 8
COLS = 5
ROWS = 6
CARD_BG = (248, 250, 252)
CARD_LINE = (226, 232, 240)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

TAG_COLORS = dict([
    ("MIDDLE EAST", (190, 24, 93)),
    ("UKRAINE", (202, 138, 4)),
    ("EUROPE", (37, 99, 235)),
    ("AMERICAS", (220, 38, 38)),
    ("ASIA", (5, 150, 105)),
    ("TECH", (2, 132, 199)),
    ("HEALTH", (219, 39, 119)),
    ("WORLD", (71, 85, 105)),
])

NEWS = [
    ("MIDDLE EAST", "Houthi drone hits Riyadh tower", "11 people injured in strike on the capital's tallest tower"),
    ("MIDDLE EAST", "Houthis claim Saudi refinery hit", "Group says it struck a Saudi oil refinery and Riyadh finance hub"),
    ("MIDDLE EAST", "Israeli strike kills Hamas official", "Senior Hamas security chief and seven others dead in Gaza"),
    ("UKRAINE", "Russian strikes hit power grid", "Energy sites in five regions damaged; at least five killed"),
    ("UKRAINE", "Putin warns revenge is 'inevitable'", "Says Kyiv's attacks on Russian refineries will draw a reply"),
    ("UKRAINE", "Ukraine hits five Russian jets", "MiG-31 and Su-34 aircraft struck at Savasleyka airbase"),
    ("EUROPE", "NATO calls urgent meeting", "Allies gather as tensions with Russia keep rising"),
    ("EUROPE", "Merz: Europe will show its limits", "German leader says Russia will be shown where the line is"),
    ("EUROPE", "EU weighs new Russia sanctions", "Next round would target Russian energy and banking"),
    ("EUROPE", "EU curbs Chinese cars", "Visa bans and quotas imposed on Chinese car imports"),
    ("AMERICAS", "US weighs new strikes on Iran", "Washington considers further action as Gulf tensions grow"),
    ("AMERICAS", "US readies tariffs on 16 economies", "China and Europe among targets of new tariff plan"),
    ("AMERICAS", "Trump-Putin talks loom", "Allies coordinate ahead of Ukraine talks"),
    ("AMERICAS", "US spy agencies breached", "Unclassified information exposed in agency breach"),
    ("AMERICAS", "Thanksgiving travel crush", "Airports packed nationwide as holiday travel peaks"),
    ("AMERICAS", "Turkey prices climb", "Turkey and potato prices up for Thanksgiving"),
    ("AMERICAS", "Army to detonate explosives", "Toxic lead azide stockpile to be destroyed in Iowa"),
    ("AMERICAS", "Wrongly deported man lands in Spain", "Migrant's long legal battle ends with arrival in Spain"),
    ("AMERICAS", "Thomas Markle indicted", "Meghan Markle's father, 82, charged in US federal case"),
    ("ASIA", "China probes Shanghai party chief", "Graft inquiry into Chen Jining surprises analysts"),
    ("ASIA", "China sentences spy to death", "Official given death sentence in espionage case"),
    ("ASIA", "Huawei convicted of fraud", "Beijing accuses US of 'suppressing' Chinese firms"),
    ("ASIA", "Pakistani boards Tiangong station", "Zeeshan Ali is first foreign astronaut on China's station"),
    ("ASIA", "Seoul rewards AI-cheating tipsters", "Students who report exam AI cheating to be rewarded"),
    ("ASIA", "Malaysia to return migrants", "Government plans to send migrants back home"),
    ("TECH", "OpenAI apologises to Australia", "Sorry over unauthorised access to government files"),
    ("TECH", "AI stocks sell off in Asia", "Sell-off spreads across Asian markets on investor fears"),
    ("TECH", "Huang apologises to Nvidia staff", "CEO sorry as Trump floats idea of a potential pardon"),
    ("HEALTH", "Bird flu kills US dairy worker", "First death after exposure to infected dairy cattle"),
    ("WORLD", "25 hostages taken in Colombia", "Gunmen seize supermarket hostages in Cartagena"),
]


def get_font(points, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), points)


def fit_text(draw, text, face, limit):
    words = text.split(" ")
    lines = []
    line = ""
    for word in words:
        trial = line + " " + word if line else word
        if draw.textlength(trial, font=face) <= limit:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def paint_story(draw, num, tag, head, sub, sx, sy, sw, sh):
    colour = TAG_COLORS[tag]
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill=CARD_BG, outline=CARD_LINE)
    draw.rounded_rectangle([sx, sy, sx + sw, sy + 5], radius=3, fill=colour)
    draw.text((sx + 8, sy + 11), tag, font=get_font(10, True), fill=colour)
    draw.text((sx + sw - 8, sy + 11), "{:02d}".format(num), font=get_font(10, True), fill=colour, anchor="ra")
    draw.line([sx + 8, sy + 26, sx + sw - 8, sy + 26], fill=CARD_LINE)
    head_lines = fit_text(draw, head, get_font(14, True), sw - 16)[:3]
    ty = sy + 30
    for ln in head_lines:
        draw.text((sx + 8, ty), ln, font=get_font(14, True), fill=INK_RGB)
        ty += 18
    sub_lines = fit_text(draw, sub, get_font(11), sw - 16)[:2]
    for ln in sub_lines:
        draw.text((sx + 8, ty + 2), ln, font=get_font(11), fill=SOFT_RGB)
        ty += 14


def build():
    assert len(NEWS) == 30
    image = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER_RGB)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, CANVAS_W, HEADER_PX], fill=(15, 23, 42))
    draw.text((16, 12), "THE WORLD IN ONE PICTURE", font=get_font(30, True), fill=(255, 255, 255))
    draw.text((16, 52), "WEDNESDAY, 25 NOVEMBER 2026  •  30 STORIES  •  8 SECTIONS", font=get_font(17), fill=(191, 219, 254))
    draw.text((CANVAS_W - 16, 52), "make.fun", font=get_font(17, True), fill=(147, 197, 253), anchor="ra")
    cell_w = (CANVAS_W - PAD * 2 - GUTTER * (COLS - 1)) // COLS
    cell_h = (CANVAS_H - HEADER_PX - FOOTER_PX - PAD - GUTTER * (ROWS - 1)) // ROWS
    grid_top = HEADER_PX + 10
    for pos, (tag, head, sub) in enumerate(NEWS):
        r, c = divmod(pos, COLS)
        paint_story(draw, pos + 1, tag, head, sub,
                    PAD + c * (cell_w + GUTTER), grid_top + r * (cell_h + GUTTER),
                    cell_w, cell_h)
    draw.text((16, CANVAS_H - 22), "Sources: Reuters, AP, AFP, Al Jazeera  •  Headlines as reported on 25 Nov 2026", font=get_font(11), fill=SOFT_RGB)
    path = os.path.expanduser("~/workspace/makefun-news-20261125/entry.png")
    image.save(path, "PNG")
    print("wrote", path, image.size)


if __name__ == "__main__":
    build()
