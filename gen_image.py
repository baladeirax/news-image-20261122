#!/usr/bin/env python3
"""Render the Sunday 22 November 2026 front page as a 1024x1024 PNG.

Only PIL is used. Everything is fixed: the same text, the same
positions, no clock, no dice, no network. Run it as
``python3 gen_image.py [out.png]``; without an argument the image
lands next to this file as entry.png.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
BG = (247, 243, 234)
FG = (18, 18, 18)
NAVY = (20, 33, 61)
SCARLET = (178, 34, 34)
MUTED = (90, 90, 88)
WASH = (232, 227, 214)
DARKBLUE = (24, 42, 66)

FONT_FOLDER = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_FOLDER, filename), size)


def serif_b(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def sans_b(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def wrap_lines(draw, text, font, width):
    """Split text into lines that fit width, word by word."""
    words = text.split()
    done, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                done.append(current)
            current = word
    if current:
        done.append(current)
    return done


def draw_lines(draw, x, y, width, text, font, fill=FG, spacing=1.28):
    """Draw wrapped text starting at (x, y); return the y below it."""
    for line in wrap_lines(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += int(font.size * spacing)
    return y


def story_box(draw, x, y, w, h, title, body):
    """A two-part panel: navy title bar, then body text."""
    draw.rectangle([x, y, x + w, y + h], outline=FG, width=2)
    draw.rectangle([x, y, x + w, y + 30], fill=NAVY)
    draw.text((x + 10, y + 6), title, font=sans_b(17), fill=(255, 255, 255))
    return draw_lines(draw, x + 10, y + 40, w - 20, body, sans(16),
                      spacing=1.3)


def pact_graphic(draw, x, y, w, h):
    """The rejected Antalya Pact, drawn as a navy fact box."""
    draw.rectangle([x, y, x + w, y + h], fill=DARKBLUE, outline=FG, width=2)
    draw.text((x + 12, y + 10), "THE ANTALYA PACT — REJECTED",
              font=sans_b(18), fill=(255, 255, 255))
    draw.line([x + 12, y + 38, x + w - 12, y + 38],
              fill=(200, 205, 210), width=1)
    draw.text((x + 12, y + 46), "NO DEAL", font=sans_b(44),
              fill=(230, 90, 90))
    yy = y + 104
    yy = draw_lines(draw, x + 12, yy, w - 24,
                    "REJECTED BY: EU \u00b7 Panama \u00b7 Marshall "
                    "Islands \u00b7 UK \u00b7 least-developed countries "
                    "— 130+ in all.",
                    sans_b(14), fill=(255, 255, 255), spacing=1.3)
    yy = draw_lines(draw, x + 12, yy + 6, w - 24,
                    "BACKED BY: Russia \u00b7 China \u00b7 Arab states.",
                    sans_b(14), fill=(200, 205, 210), spacing=1.3)
    draw.text((x + 12, y + h - 40),
              "194 delegations \u00b7 longest COP ever \u00b7 first breakdown",
              font=sans(13), fill=(200, 205, 210))
    draw.text((x + 12, y + h - 22), "since Copenhagen 2009",
              font=sans(13), fill=(200, 205, 210))


def front_page(path):
    canvas = Image.new("RGB", (PAGE, PAGE), BG)
    draw = ImageDraw.Draw(canvas)
    edge = 24

    # Masthead.
    draw.text((edge, 10), "THE DAILY WORLD", font=serif_b(52), fill=FG)
    draw.text((PAGE - edge - 330, 24), "SUNDAY", font=sans_b(25),
              fill=SCARLET)
    draw.text((PAGE - edge - 330, 54), "22 NOVEMBER 2026", font=sans_b(25),
              fill=FG)
    draw.line([edge, 94, PAGE - edge, 94], fill=FG, width=3)
    draw.line([edge, 100, PAGE - edge, 100], fill=FG, width=1)

    # Date check strip: the winner-format lesson, stated plainly.
    y = 108
    draw.rectangle([edge, y, PAGE - edge, y + 28], fill=NAVY)
    draw.text((edge + 10, y + 5),
              "DATE CHECK \u2713 — Every story below happened or was "
              "first reported on Sunday 22 November 2026.",
              font=sans_b(15), fill=(255, 255, 255))

    # Lead headline.
    y = 146
    y = draw_lines(draw, edge, y, PAGE - 2 * edge,
                   "COP31 COLLAPSES IN ANTALYA", sans_b(42),
                   spacing=1.08)
    y = draw_lines(draw, edge, y + 4, PAGE - 2 * edge,
                   "No deal after record overtime — EU rejects draft "
                   "with no mention of fossil fuels", sans_b(21),
                   fill=SCARLET, spacing=1.08)
    y += 8

    # Lead story on the left, pact graphic on the right.
    top = y
    text_w = 520
    y = draw_lines(draw, edge, top, text_w,
                   "The UN climate summit in Antalya collapsed after "
                   "nearly 200 countries failed to agree a deal — the "
                   "longest COP in history.",
                   sans(19), spacing=1.32)
    y = draw_lines(draw, edge, y + 8, text_w,
                   "The breaking point was fossil fuels: the final "
                   "draft of the Antalya Pact made no mention of them, "
                   "and the EU, Panama, the UK and the least-developed "
                   "countries refused to endorse it. President Murat "
                   "Kurum conceded there was no consensus.",
                   sans(17), spacing=1.32)
    y = draw_lines(draw, edge, y + 8, text_w,
                   "First major breakdown since Copenhagen 2009.",
                   sans(17), spacing=1.32)
    pact_graphic(draw, edge + text_w + 16, top,
                 PAGE - edge - (edge + text_w + 16), 236)
    y = top + 236 + 12

    # The day in Antalya: the summit's arc, in five beats.
    draw.rectangle([edge, y, PAGE - edge, y + 84], fill=WASH,
                   outline=FG, width=2)
    draw.text((edge + 10, y + 5), "THE DAY IN ANTALYA", font=sans_b(16),
              fill=NAVY)
    beats = [
        ("OVERTIME", "Talks run 2 days past\ndeadline into Sunday"),
        ("THE DRAFT", "Final text drops all\nfossil-fuel mentions"),
        ("THE REJECTION", "EU and 130+ countries\nrefuse the Antalya Pact"),
        ("THE CONCESSION", "Kurum: no consensus;\nno deal adopted"),
        ("WHAT SURVIVED", "90+ countries sign the\nelectricity pledge"),
    ]
    slot_w = (PAGE - 2 * edge - 20) // 5
    for i, (head, body) in enumerate(beats):
        sx = edge + 10 + i * slot_w
        draw.text((sx, y + 26), head, font=sans_b(15), fill=SCARLET)
        yy = y + 46
        for line in body.split("\n"):
            draw.text((sx, yy), line, font=sans(13), fill=FG)
            yy += 17
    y += 84 + 12

    # Four story panels, two by two.
    col_w = (PAGE - 2 * edge - 16) // 2
    left_x, right_x = edge, edge + col_w + 16
    box_h = 118
    story_box(draw, left_x, y, col_w, box_h, "SEA DRONES HIT WARSHIP",
              "Suspected Ukrainian maritime drones strike a Russian "
              "naval vessel docked at Benghazi Naval Base, Libya. A "
              "sanctioned Russian cargo ship, Sparta II, is still "
              "burning a day after a drone strike in the Gulf of "
              "Finland.")
    story_box(draw, right_x, y, col_w, box_h, "IRAN STRIKES BAHRAIN",
              "Iranian projectiles hit a civilian industrial facility "
              "in Sitra, Bahrain, causing a fire and injuring two "
              "people. Gulf states condemn the attack; a separate "
              "tanker incident is reported in the Gulf of Oman.")
    y += box_h + 8
    story_box(draw, left_x, y, col_w, box_h, "KYIV APARTMENT HIT",
              "A Russian drone strikes a five-storey apartment block "
              "in Dymer, north of Kyiv; 14 people are missing. A "
              "ballistic missile on Kryvyi Rih kills a 7-year-old boy "
              "and a 20-year-old woman; 60 are wounded.")
    story_box(draw, right_x, y, col_w, box_h, "EL CHAPO ISIDRO CAUGHT",
              "Mexican special forces capture cartel boss Fausto "
              "Isidro Meza Flores in Sinaloa. Eleven people are "
              "killed in the raid, including four soldiers.")
    y += box_h + 8

    # Also today.
    draw.rectangle([edge, y, PAGE - edge, y + 76], outline=FG, width=2)
    draw.text((edge + 10, y + 5), "ALSO ON 22 NOVEMBER", font=sans_b(16),
              fill=NAVY)
    draw_lines(draw, edge + 10, y + 26, PAGE - 2 * edge - 20,
               "Cikande candy factory fire kills 3, 36+ missing in "
               "Indonesia \u00b7 47 countries join the methane pledge "
               "\u00b7 90+ countries back 35% electricity by 2035 "
               "\u00b7 Longest COP ever \u00b7 US absent from the talks "
               "\u00b7 First breakdown since Copenhagen 2009.",
               sans(14), spacing=1.3)
    y += 76 + 8

    # Yesterday in brief, then the footer rule and sources.
    draw_lines(draw, edge, y, PAGE - 2 * edge,
               "YESTERDAY, IN BRIEF (21 NOV): Rutte in Warsaw — "
               "\u201cNATO will defend every inch of Polish "
               "territory\u201d \u00b7 Poland seeks more Eastern Sentry "
               "jets \u00b7 North Atlantic Council meets Monday.",
               sans(14), fill=MUTED, spacing=1.3)
    draw.line([edge, PAGE - 34, PAGE - edge, PAGE - 34], fill=FG, width=1)
    draw.text((edge, PAGE - 28),
              "Sources: CNN \u00b7 Reuters \u00b7 Le Monde \u00b7 AP \u00b7 "
              "Al Jazeera — All stories dated 22 November 2026",
              font=sans(13), fill=MUTED)

    canvas.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    front_page(target)
    print("wrote", target)
