#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador oficial del Pack Multicanal en Inglés (Criterio Notarial · Fabricio Rivas):
'Notarial income certificate in Uruguay: residency, banks and rentals'
Destino: sitio/campana/tanda_3_income_certificate_en/
"""
import os
import subprocess
import tempfile
from collections import deque
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

SITIO_DIR = "/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio"
OUT_DIR = os.path.join(SITIO_DIR, "campana", "tanda_3_income_certificate_en")
LOGO_PATH = os.path.join(SITIO_DIR, "images", "fr logo transparente fondo dorado FR escribano fabricio rivas.png")
PORTRAIT_PATH = os.path.join(SITIO_DIR, "images", "fabricio-real-estate.webp")
MUSIC_MP3 = os.path.join(SITIO_DIR, "campana", "musica_fabricio", "v4_cafe_del_mar_rhodes_sax_instrumental.mp3")
FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"

assert os.path.exists(LOGO_PATH), f"Falta logo: {LOGO_PATH}"
assert os.path.exists(PORTRAIT_PATH), f"Falta retrato: {PORTRAIT_PATH}"
assert os.path.exists(MUSIC_MP3) and "canva" not in MUSIC_MP3.lower() and "instrumental" in MUSIC_MP3.lower(), f"Audio inválido: {MUSIC_MP3}"

os.makedirs(OUT_DIR, exist_ok=True)

C_CARBON = (16, 16, 15)        # #10100f (Matriz 3A)
C_BRONZE = (34, 30, 22)        # #221e16 (Matriz 3B)
C_BOX_BG = (20, 19, 16)
C_BOX_ALT = (26, 23, 18)
C_GOLD = (196, 173, 122)       # #c4ad7a
C_GOLD_BORDER = (118, 105, 76)
C_GOLD_LIGHT = (214, 192, 138)
C_WHITE = (248, 247, 244)      # #f8f7f4
C_PEARL = (214, 210, 202)      # #d6d2ca
C_MUTED = (168, 164, 154)


def get_font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    idx_map = {"bold": 0, "demibold": 2, "medium": 5, "regular": 7}
    return ImageFont.truetype(FONT_PATH, size, index=idx_map.get(weight, 7))


def load_logo(target_height: int = 56) -> Image.Image:
    logo = Image.open(LOGO_PATH).convert("RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    w, h = logo.size
    return logo.resize((int(w * (target_height / h)), target_height), Image.Resampling.LANCZOS)


def make_watermark(size: int = 430) -> Image.Image:
    wm = load_logo(target_height=size)
    r, g, b, a = wm.split()
    return Image.merge("RGBA", (r, g, b, a.point(lambda p: int(p * 0.035))))


def extract_clean_portrait(target_h: int = 565) -> Image.Image:
    im = Image.open(PORTRAIT_PATH).convert("RGB")
    w, h = im.size
    px = im.load()
    visited = bytearray(w * h)
    bg_mask = bytearray(w * h)
    q = deque()

    def is_neutral_studio_bg(rgb):
        r, g, b = rgb
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        chroma = max(r, g, b) - min(r, g, b)
        return lum >= 142 and chroma <= 20

    for x in range(w):
        if is_neutral_studio_bg(px[x, 0]):
            visited[x] = 1
            q.append((x, 0))
    for y in range(h - 40):
        for x in (0, w - 1):
            if is_neutral_studio_bg(px[x, y]):
                idx = y * w + x
                if not visited[idx]:
                    visited[idx] = 1
                    q.append((x, y))

    while q:
        cx, cy = q.popleft()
        bg_mask[cy * w + cx] = 255
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                nidx = ny * w + nx
                if not visited[nidx] and is_neutral_studio_bg(px[nx, ny]):
                    visited[nidx] = 1
                    q.append((nx, ny))

    alpha_img = Image.new("L", (w, h), 255)
    apx = alpha_img.load()
    for y in range(h):
        row_off = y * w
        for x in range(w):
            if bg_mask[row_off + x]:
                apx[x, y] = 0

    alpha_soft = alpha_img.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(radius=2.2))
    fade_top = int(h * 0.78)
    spx = alpha_soft.load()
    for y in range(fade_top, h):
        factor = max(0.0, 1.0 - ((y - fade_top) / max(1, h - fade_top)))
        for x in range(w):
            spx[x, y] = int(spx[x, y] * (factor ** 1.15))

    rgba = im.convert("RGBA")
    rgba.putalpha(alpha_soft)
    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    cw, ch = rgba.size
    return rgba.resize((int(cw * (target_h / ch)), target_h), Image.Resampling.LANCZOS)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split()
        cur = []
        for w in words:
            test = " ".join(cur + [w])
            bb = draw.textbbox((0, 0), test, font=font)
            if (bb[2] - bb[0]) <= max_w or not cur:
                cur.append(w)
            else:
                lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))
    return lines


def draw_tracked(draw, pos, text: str, font, fill, tracking: float = 2.3):
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bb = draw.textbbox((0, 0), ch, font=font)
        x += (bb[2] - bb[0]) + tracking


def draw_base_4x5(bg_color, badge_num: str, logo: Image.Image, watermark: Image.Image) -> Image.Image:
    W, H = 1080, 1350
    canvas = Image.new("RGBA", (W, H), bg_color + (255,))
    canvas.paste(watermark, ((W - watermark.size[0]) // 2, (H - watermark.size[1]) // 2 + 20), watermark)
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rectangle([(48, 48), (W - 48, H - 48)], outline=C_GOLD_BORDER, width=1)
    canvas.paste(logo, (96, 188), logo)

    f_badge = get_font(21, "medium")
    bb = draw.textbbox((0, 0), badge_num, font=f_badge)
    bw = (bb[2] - bb[0]) + 42
    bx1 = W - 96 - bw
    by1 = 196
    draw.rounded_rectangle([(bx1, by1), (W - 96, by1 + 42)], radius=21, fill=bg_color + (235,), outline=C_GOLD_BORDER, width=1)
    draw.text((bx1 + 21, by1 + 8), badge_num, font=f_badge, fill=C_GOLD_LIGHT)
    return canvas


def draw_footer_4x5(draw, subline: str):
    W = 1080
    draw.line([(96, 1054), (W - 96, 1054)], fill=C_GOLD_BORDER, width=1)
    draw.text((96, 1072), "Fabricio Rivas · Escribano Público", font=get_font(27, "medium"), fill=C_WHITE)
    draw.text((96, 1110), subline, font=get_font(21, "regular"), fill=C_MUTED)


def render_carousel(logo: Image.Image, watermark: Image.Image, portrait: Image.Image):
    paths = []

    # 0.jpg · Matriz 3A Portada (fiel al boceto aprobado 01)
    c0 = draw_base_4x5(C_CARBON, "01 / 04", logo, watermark)
    d0 = ImageDraw.Draw(c0, "RGBA")
    draw_tracked(d0, (96, 286), "URUGUAY RESIDENCY · LEGAL & COMPLIANCE", get_font(21, "demibold"), C_GOLD, tracking=2.3)
    f_h1 = get_font(72, "demibold")
    y = 330
    for ln in ["Notarial income", "certificate in Uruguay"]:
        d0.text((96, y), ln, font=f_h1, fill=C_WHITE)
        y += 84
    y += 22
    d0.line([(96, y), (216, y)], fill=C_GOLD, width=3)
    f_body = get_font(39, "regular")
    ty = y + 30
    for ln in wrap_lines(d0, "Official proof of means of support (certificado notarial de ingresos) for residency, local banks, and rental guarantees.", f_body, 888):
        d0.text((96, ty), ln, font=f_body, fill=C_PEARL)
        ty += 52
    box_y1, box_y2 = 776, 996
    d0.rounded_rectangle([(96, box_y1), (984, box_y2)], radius=18, fill=C_BOX_BG + (242,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(d0, (132, box_y1 + 28), "PUNTA DEL ESTE & MALDONADO · LAW 18.250", get_font(19, "demibold"), C_GOLD_LIGHT, tracking=2.2)
    f_box = get_font(36, "medium")
    by = box_y1 + 74
    for ln in wrap_lines(d0, "Service in English and Portuguese. Remote PDF pre-review before your signing appointment.", f_box, 816):
        d0.text((132, by), ln, font=f_box, fill=C_WHITE)
        by += 48
    draw_footer_4x5(d0, "SCJ Reg. 17058/5 · Punta del Este & Maldonado · Swipe for details")
    p0 = os.path.join(OUT_DIR, "0.jpg")
    c0.convert("RGB").save(p0, "JPEG", quality=92, optimize=True)
    paths.append(p0)

    # 1.jpg · Matriz 3A Comparativa (fiel al boceto aprobado 02)
    c1 = draw_base_4x5(C_CARBON, "02 / 04", logo, watermark)
    d1 = ImageDraw.Draw(c1, "RGBA")
    draw_tracked(d1, (96, 286), "SIGNATORY RULES · AVOID DUPLICATE FEES", get_font(21, "demibold"), C_GOLD, tracking=2.3)
    f_h2 = get_font(62, "demibold")
    y = 324
    for ln in ["Who signs your", "income certificate?"]:
        d1.text((96, y), ln, font=f_h2, fill=C_WHITE)
        y += 74
    y += 20
    d1.line([(96, y), (216, y)], fill=C_GOLD, width=3)

    col_y1, col_y2 = 520, 858
    left_x1, left_x2 = 96, 524
    right_x1, right_x2 = 556, 984
    d1.rounded_rectangle([(left_x1, col_y1), (left_x2, col_y2)], radius=18, fill=C_BOX_BG + (242,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(d1, (left_x1 + 28, col_y1 + 24), "RESIDENCY · MIGRACIÓN", get_font(18, "demibold"), C_GOLD_LIGHT, tracking=2.0)
    d1.text((left_x1 + 28, col_y1 + 64), "Escribano Público", font=get_font(37, "demibold"), fill=C_WHITE)
    f_col = get_font(32, "regular")
    cy = col_y1 + 124
    for ln in wrap_lines(d1, "Law 18.250 filings for remote contractors, foreign founders, and retirees.", f_col, 372):
        d1.text((left_x1 + 28, cy), ln, font=f_col, fill=C_PEARL)
        cy += 42

    d1.rounded_rectangle([(right_x1, col_y1), (right_x2, col_y2)], radius=18, fill=C_BOX_ALT + (245,), outline=C_GOLD, width=1)
    draw_tracked(d1, (right_x1 + 28, col_y1 + 24), "RENTALS & BANKS", get_font(18, "demibold"), C_GOLD_LIGHT, tracking=2.0)
    d1.text((right_x1 + 28, col_y1 + 64), "Contador / Escribano", font=get_font(35, "demibold"), fill=C_WHITE)
    cy = col_y1 + 124
    for ln in wrap_lines(d1, "Porto, SURA, MAPFRE, SBI, and banks define the signatory on each checklist.", f_col, 372):
        d1.text((right_x1 + 28, cy), ln, font=f_col, fill=C_PEARL)
        cy += 42

    bar_y1, bar_y2 = 884, 1020
    d1.rounded_rectangle([(96, bar_y1), (984, bar_y2)], radius=16, fill=C_BOX_BG + (242,), outline=C_GOLD_BORDER, width=1)
    f_bar = get_font(31, "medium")
    bar_lines = wrap_lines(d1, "Confirm your written checklist via WhatsApp before ordering.", f_bar, 824)
    by = bar_y1 + max(22, (bar_y2 - bar_y1 - len(bar_lines) * 40) // 2)
    for ln in bar_lines:
        d1.text((128, by), ln, font=f_bar, fill=C_GOLD_LIGHT)
        by += 40
    draw_footer_4x5(d1, "SCJ Reg. 17058/5 · Punta del Este & Maldonado · WhatsApp +598 99 431 185")
    p1 = os.path.join(OUT_DIR, "1.jpg")
    c1.convert("RGB").save(p1, "JPEG", quality=92, optimize=True)
    paths.append(p1)

    # 2.jpg · Matriz 3B Bronce (#221e16)
    c2 = draw_base_4x5(C_BRONZE, "03 / 04", logo, watermark)
    d2 = ImageDraw.Draw(c2, "RGBA")
    draw_tracked(d2, (96, 286), "REMOTE CONTRACTORS & FOREIGN ENTITIES", get_font(20, "demibold"), C_GOLD, tracking=2.2)
    f_h3 = get_font(54, "demibold")
    y = 330
    for ln in wrap_lines(d2, "What we review via WhatsApp in advance", f_h3, 884):
        d2.text((96, y), ln, font=f_h3, fill=C_WHITE)
        y += 66
    y += 14
    d2.line([(96, y), (216, y)], fill=C_GOLD, width=3)
    y += 34

    f_it_t = get_font(31, "demibold")
    f_it_b = get_font(29, "regular")
    items3 = [
        ("01 · Foreign inflows & contracts:", "Bank statements, recurring invoices, consulting agreements, and US LLC or company filings."),
        ("02 · Pre-review in English:", "Clear PDF scans suffice during initial review so we align wording before booking."),
        ("03 · Apostille & Traductor Público:", "We confirm upfront which foreign public exhibits need Apostille and sworn Spanish translation."),
    ]
    for tit, desc in items3:
        d2.text((96, y), tit, font=f_it_t, fill=C_GOLD_LIGHT)
        y += 42
        for ln in wrap_lines(d2, desc, f_it_b, 880):
            d2.text((96, y), ln, font=f_it_b, fill=C_PEARL)
            y += 40
        y += 24
    assert y <= 1036, f"Overflow on plate 2: y={y}"
    draw_footer_4x5(d2, "SCJ Reg. 17058/5 · Punta del Este & Maldonado · Swipe for details")
    p2 = os.path.join(OUT_DIR, "2.jpg")
    c2.convert("RGB").save(p2, "JPEG", quality=92, optimize=True)
    paths.append(p2)

    # 3.jpg · Matriz 2 Retrato + Sans (#10100f)
    c3 = draw_base_4x5(C_CARBON, "04 / 04", logo, watermark)
    pw, ph = portrait.size
    px = 1080 - pw - 52
    py = 1054 - ph
    c3.paste(portrait, (px, py), portrait)
    d3 = ImageDraw.Draw(c3, "RGBA")
    draw_tracked(d3, (96, 310), "DIRECT NOTARIAL PRACTICE · PUNTA DEL ESTE", get_font(19, "demibold"), C_GOLD, tracking=2.2)

    col_w = min(470, px - 96 - 24)
    f_h4 = get_font(46, "demibold")
    y = 368
    for ln in wrap_lines(d3, "Remote PDF review before you sign", f_h4, col_w):
        d3.text((96, y), ln, font=f_h4, fill=C_WHITE)
        y += 58
    y += 16
    d3.line([(96, y), (196, y)], fill=C_GOLD, width=3)
    y += 28
    f_b4 = get_font(28, "regular")
    body4 = (
        "Direct service in Punta del Este and Maldonado, with prior remote coordination.\n\n"
        "Service in English and Portuguese. Read the full guide at the link in bio or message on WhatsApp."
    )
    for ln in wrap_lines(d3, body4, f_b4, col_w):
        if ln == "":
            y += 20
            continue
        d3.text((96, y), ln, font=f_b4, fill=C_PEARL)
        y += 40
    assert y <= 1036, f"Overflow on plate 3: y={y}"
    draw_footer_4x5(d3, "SCJ Reg. 17058/5 · ARTOWER, Punta del Este · WhatsApp +598 99 431 185")
    p3 = os.path.join(OUT_DIR, "3.jpg")
    c3.convert("RGB").save(p3, "JPEG", quality=92, optimize=True)
    paths.append(p3)

    return paths


def draw_9x16_typewriter_frame(logo: Image.Image, watermark: Image.Image, full_body: str, words_to_show: int) -> Image.Image:
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), C_CARBON + (255,))
    canvas.paste(watermark, ((W - watermark.size[0]) // 2, 660), watermark)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Zona segura estricta (REEL_9_16: top>=220, bottom>=420 -> y=304..1436, x=104..924 -> right>=156)
    draw.rectangle([(64, 304), (W - 64, 1436)], outline=C_GOLD_BORDER, width=1)
    canvas.paste(logo, (104, 344), logo)

    draw_tracked(draw, (104, 464), "URUGUAY RESIDENCY · PUNTA DEL ESTE", get_font(20, "demibold"), C_GOLD, tracking=2.3)

    f_h = get_font(56, "demibold")
    y = 516
    for ln in ["Notarial income", "certificate in Uruguay"]:
        draw.text((104, y), ln, font=f_h, fill=C_WHITE)
        y += 70
    y += 18
    draw.line([(104, y), (214, y)], fill=C_GOLD, width=3)

    f_b = get_font(35, "regular")
    wrapped_full = wrap_lines(draw, full_body, f_b, 815)
    ty = y + 36
    remaining = max(0, words_to_show)
    for ln in wrapped_full:
        if remaining <= 0:
            break
        ln_words = ln.split(" ")
        take = ln_words[:remaining]
        draw.text((104, ty), " ".join(take), font=f_b, fill=C_PEARL)
        remaining -= len(take)
        ty += 48

    box_y1, box_y2 = 1056, 1236
    draw.rounded_rectangle([(104, box_y1), (936, box_y2)], radius=18, fill=C_BOX_BG + (240,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(draw, (138, box_y1 + 26), "SERVICE IN ENGLISH & PORTUGUESE", get_font(19, "demibold"), C_GOLD_LIGHT, tracking=2.3)
    f_bt = get_font(28, "medium")
    by = box_y1 + 66
    for ln in wrap_lines(draw, "Send your written checklist via WhatsApp (+598 99 431 185) for remote PDF pre-review.", f_bt, 760):
        draw.text((138, by), ln, font=f_bt, fill=C_WHITE)
        by += 38

    draw.line([(104, 1300), (936, 1300)], fill=C_GOLD_BORDER, width=1)
    draw.text((104, 1320), "Fabricio Rivas · Escribano Público", font=get_font(27, "medium"), fill=C_WHITE)
    draw.text((104, 1358), "SCJ Reg. 17058/5 · ARTOWER, Punta del Este · +598 99 431 185", font=get_font(21, "regular"), fill=C_MUTED)
    return canvas.convert("RGB")


def build_9x16_reel(logo: Image.Image, watermark: Image.Image) -> tuple[str, str, str]:
    full_body = (
        "Relocating to Punta del Este or Maldonado? An Escribano Público certifies "
        "your foreign or remote income for Dirección Nacional de Migración, banks, "
        "and eligible rental guarantees."
    )
    fps = 24
    total_dur = 12.5
    typing_dur = 9.2
    n_frames = int(round(total_dur * fps))
    typing_frames = int(round(typing_dur * fps))
    total_words = len(full_body.split(" "))

    out_mp4 = os.path.join(OUT_DIR, "reel.mp4")
    p3s = os.path.join(OUT_DIR, "preview_reel_3s.jpg")
    p11s = os.path.join(OUT_DIR, "preview_reel_11s.jpg")
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = {}
        for i in range(n_frames):
            wc = total_words if i >= typing_frames else max(1, int(((i + 1) / typing_frames) * total_words))
            if wc not in cache:
                cache[wc] = draw_9x16_typewriter_frame(logo, watermark, full_body, wc)
            cache[wc].save(os.path.join(tmpdir, f"f_{i:04d}.jpg"), "JPEG", quality=92)

        fade_out_start = round(total_dur - 1.8, 2)
        cmd = [
            FFMPEG_BIN, "-y",
            "-framerate", str(fps),
            "-i", os.path.join(tmpdir, "f_%04d.jpg"),
            "-i", MUSIC_MP3,
            "-filter_complex",
            f"[1:a]atrim=0:{total_dur},equalizer=f=350:t=q:w=1:g=2,afade=t=in:st=0:d=0.45,afade=t=out:st={fade_out_start}:d=1.8[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), "-preset", "medium", "-crf", "22",
            "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart",
            out_mp4,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([FFMPEG_BIN, "-y", "-ss", "3.0", "-i", out_mp4, "-vframes", "1", p3s], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([FFMPEG_BIN, "-y", "-ss", "11.0", "-i", out_mp4, "-vframes", "1", p11s], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_mp4, p3s, p11s


def render_special_formats(logo: Image.Image, watermark: Image.Image):
    specials = []

    # 1. Google Business Profile 700x700
    g_w, g_h = 700, 700
    g = Image.new("RGBA", (g_w, g_h), C_CARBON + (255,))
    wm_s = make_watermark(size=280)
    g.paste(wm_s, ((g_w - wm_s.size[0]) // 2, (g_h - wm_s.size[1]) // 2), wm_s)
    dg = ImageDraw.Draw(g, "RGBA")
    dg.rectangle([(24, 24), (g_w - 24, g_h - 24)], outline=C_GOLD_BORDER, width=1)
    logo_s = load_logo(target_height=36)
    g.paste(logo_s, (52, 50), logo_s)
    draw_tracked(dg, (52, 118), "URUGUAY RESIDENCY & COMPLIANCE", get_font(15, "demibold"), C_GOLD, tracking=1.8)
    f_gh = get_font(46, "demibold")
    gy = 152
    for ln in ["Notarial income", "certificate"]:
        dg.text((52, gy), ln, font=f_gh, fill=C_WHITE)
        gy += 54
    gy += 14
    dg.line([(52, gy), (142, gy)], fill=C_GOLD, width=2)
    gy += 22
    f_gb = get_font(26, "regular")
    for ln in wrap_lines(dg, "Residency (Law 18.250), banks & rental guarantees in Punta del Este & Maldonado.", f_gb, 596):
        dg.text((52, gy), ln, font=f_gb, fill=C_PEARL)
        gy += 34
    dg.rounded_rectangle([(52, 464), (648, 566)], radius=14, fill=C_BOX_BG + (242,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(dg, (74, 482), "SERVICE IN ENGLISH & PORTUGUESE", get_font(14, "demibold"), C_GOLD_LIGHT, tracking=1.8)
    dg.text((74, 514), "Remote PDF pre-review via WhatsApp", font=get_font(23, "medium"), fill=C_WHITE)
    dg.line([(52, 592), (648, 592)], fill=C_GOLD_BORDER, width=1)
    dg.text((52, 608), "Fabricio Rivas · Escribano Público (SCJ 17058/5)", font=get_font(18, "medium"), fill=C_WHITE)
    dg.text((52, 636), "ARTOWER, Punta del Este · +598 99 431 185", font=get_font(16, "regular"), fill=C_MUTED)
    p_gbp = os.path.join(OUT_DIR, "gbp_700x700.jpg")
    g.convert("RGB").save(p_gbp, "JPEG", quality=92, optimize=True)
    specials.append(p_gbp)

    # 2. Instagram Story + Link Sticker Zone (1080x1920)
    W, H = 1080, 1920
    s = Image.new("RGBA", (W, H), C_CARBON + (255,))
    s.paste(watermark, ((W - watermark.size[0]) // 2, 660), watermark)
    ds = ImageDraw.Draw(s, "RGBA")
    ds.rectangle([(64, 304), (W - 64, 1436)], outline=C_GOLD_BORDER, width=1)
    s.paste(logo, (104, 344), logo)
    draw_tracked(ds, (104, 464), "NEW GUIDE · FOREIGN CLIENTS", get_font(20, "demibold"), C_GOLD, tracking=2.3)
    f_sh = get_font(56, "demibold")
    sy = 516
    for ln in ["Who signs your income", "certificate in Uruguay?"]:
        ds.text((104, sy), ln, font=f_sh, fill=C_WHITE)
        sy += 70
    sy += 18
    ds.line([(104, sy), (214, sy)], fill=C_GOLD, width=3)
    sy += 34
    f_sb = get_font(34, "regular")
    for ln in wrap_lines(ds, "Escribano Público vs. Contador Público for residency (Migración), local banks, and rental guarantees in Punta del Este & Maldonado.", f_sb, 856):
        ds.text((104, sy), ln, font=f_sb, fill=C_PEARL)
        sy += 48
    # Zona reservada para Sticker de Enlace de Instagram (y=1084..1236)
    ds.rounded_rectangle([(104, 1084), (W - 104, 1236)], radius=20, fill=C_BOX_BG + (210,), outline=C_GOLD, width=1)
    draw_tracked(ds, (268, 1144), "TAP LINK STICKER HERE  ·  READ ENGLISH GUIDE", get_font(20, "demibold"), C_GOLD_LIGHT, tracking=2.0)
    ds.line([(104, 1300), (W - 104, 1300)], fill=C_GOLD_BORDER, width=1)
    ds.text((104, 1320), "Fabricio Rivas · Escribano Público", font=get_font(27, "medium"), fill=C_WHITE)
    ds.text((104, 1358), "SCJ Reg. 17058/5 · Punta del Este & Maldonado · +598 99 431 185", font=get_font(21, "regular"), fill=C_MUTED)
    p_story = os.path.join(OUT_DIR, "story_sticker_1080x1920.jpg")
    s.convert("RGB").save(p_story, "JPEG", quality=92, optimize=True)
    specials.append(p_story)

    # 3. Estado de WhatsApp (1080x1920, Matriz 3B Bronce)
    w_im = Image.new("RGBA", (W, H), C_BRONZE + (255,))
    w_im.paste(watermark, ((W - watermark.size[0]) // 2, 660), watermark)
    dw = ImageDraw.Draw(w_im, "RGBA")
    dw.rectangle([(64, 304), (W - 64, 1436)], outline=C_GOLD_BORDER, width=1)
    w_im.paste(logo, (104, 344), logo)
    draw_tracked(dw, (104, 464), "NOTARIAL PRACTICE · PUNTA DEL ESTE", get_font(20, "demibold"), C_GOLD, tracking=2.3)
    wy = 516
    for ln in ["Notarial income", "certificate in Uruguay"]:
        dw.text((104, wy), ln, font=f_sh, fill=C_WHITE)
        wy += 70
    wy += 18
    dw.line([(104, wy), (214, wy)], fill=C_GOLD, width=3)
    wy += 34
    for ln in wrap_lines(dw, "Residency before Dirección Nacional de Migración, remote contractors, foreign LLCs, banks & rental guarantees.", f_sb, 856):
        dw.text((104, wy), ln, font=f_sb, fill=C_PEARL)
        wy += 48
    dw.rounded_rectangle([(104, 1058), (W - 104, 1236)], radius=18, fill=C_BOX_BG + (238,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(dw, (140, 1086), "SERVICE IN ENGLISH & PORTUGUESE", get_font(19, "demibold"), C_GOLD_LIGHT, tracking=2.3)
    by = 1126
    for ln in wrap_lines(dw, "Send your checklist via WhatsApp (+598 99 431 185) for remote PDF pre-review.", get_font(28, "medium"), 792):
        dw.text((140, by), ln, font=get_font(28, "medium"), fill=C_WHITE)
        by += 38
    dw.line([(104, 1300), (W - 104, 1300)], fill=C_GOLD_BORDER, width=1)
    dw.text((104, 1320), "Fabricio Rivas · Escribano Público", font=get_font(27, "medium"), fill=C_WHITE)
    dw.text((104, 1358), "SCJ Reg. 17058/5 · ARTOWER, Punta del Este · +598 99 431 185", font=get_font(21, "regular"), fill=C_MUTED)
    p_wa = os.path.join(OUT_DIR, "whatsapp_status_1080x1920.jpg")
    w_im.convert("RGB").save(p_wa, "JPEG", quality=92, optimize=True)
    specials.append(p_wa)

    return specials


if __name__ == "__main__":
    logo = load_logo(56)
    wm = make_watermark(430)
    portrait = extract_clean_portrait(565)

    imgs = render_carousel(logo, wm, portrait)
    specials = render_special_formats(logo, wm)
    mp4, p3s, p11s = build_9x16_reel(logo, wm)

    for p in imgs + specials + [p3s, p11s]:
        luma = ImageStat.Stat(Image.open(p).convert("L")).mean[0]
        assert luma <= 39.0, f"Luma > 39 en {p}: {luma:.2f}"
        print(f"OK {os.path.basename(p)} | mean_luma={luma:.2f} | bytes={os.path.getsize(p)}")
    print(f"OK {os.path.basename(mp4)} | bytes={os.path.getsize(mp4)}")
