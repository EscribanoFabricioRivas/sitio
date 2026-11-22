#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador oficial del Pack Redes Criterio Notarial #2 (Cuenta Aprobalo Fabricio Rivas):
'¿Declaración jurada o certificación de firma? Qué exige cada trámite en Maldonado'
Pieza Aprobalo: 1a1a3e97-6831-4faf-a799-33f2c436beac

Cumple estrictamente con `sitio/campana/SISTEMA_REDES_OFICIAL_FR.md` y reglas D1:
1. Garantía lumínica obligatoria: mean_luma <= 39 en todas las placas (bases #10100f y #221e16).
2. Tipografía Sans Geométrica (`Avenir Next DemiBold / Medium / Regular`) estrictamente en caja alta y baja.
3. Matrices oficiales rotadas: 3A (Carbón), 3A (Carbón), 3B (Bronce), 2 (Retrato + Sans).
4. Zonas seguras estrictas:
   - 4:5 (1080x1350): todo texto y logo dentro de y = 185..1145.
   - 9:16 (1080x1920): todo texto y logo dentro de y = 300..1440.
5. Video Reel MP4: placas/títulos/marco 100% fijos (0px de movimiento), typewriter suave en cuerpo,
   audio `oficial_cuenta_fabricio_canva.mp3` con afade in 0.45s / out 1.8s y refuerzo >300Hz.
"""

import os
import subprocess
import tempfile
from collections import deque
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

SITIO_DIR = "/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio"
OUT_DIR = os.path.join(SITIO_DIR, "campana", "tanda_2_declaracion_jurada")
LOGO_PATH = os.path.join(SITIO_DIR, "images", "fr logo transparente fondo dorado FR escribano fabricio rivas.png")
PORTRAIT_PATH = os.path.join(SITIO_DIR, "images", "fabricio-real-estate.webp")
MUSIC_MP3 = os.path.join(SITIO_DIR, "campana", "musica_fabricio", "oficial_cuenta_fabricio_canva.mp3")
FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"

os.makedirs(OUT_DIR, exist_ok=True)

C_CARBON = (16, 16, 15)        # #10100f (Matriz 3A)
C_BRONZE = (34, 30, 22)        # #221e16 (Matriz 3B)
C_BOX_BG = (20, 19, 16)        # Caja interna oscura
C_GOLD = (196, 173, 122)       # #c4ad7a
C_GOLD_BORDER = (118, 105, 76) # Filete fino 1px
C_GOLD_LIGHT = (214, 192, 138)
C_WHITE = (248, 247, 244)      # #f8f7f4
C_PEARL = (214, 210, 202)      # #d6d2ca
C_MUTED = (168, 164, 154)


def get_font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    idx_map = {
        "bold": 0,
        "demibold": 2,
        "medium": 5,
        "regular": 7,
    }
    return ImageFont.truetype(FONT_PATH, size, index=idx_map.get(weight, 7))


def load_logo(target_height: int = 58) -> Image.Image:
    logo = Image.open(LOGO_PATH).convert("RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    w, h = logo.size
    target_w = int(w * (target_height / h))
    return logo.resize((target_w, target_height), Image.Resampling.LANCZOS)


def make_subtle_watermark(size: int = 420) -> Image.Image:
    wm = load_logo(target_height=size)
    r, g, b, a = wm.split()
    # Sutil marca de agua al ~3.5% sobre carbón/bronce para riqueza visual sin romper luma
    a_soft = a.point(lambda p: int(p * 0.035))
    return Image.merge("RGBA", (r, g, b, a_soft))


def extract_clean_portrait(target_h: int = 620) -> Image.Image:
    """
    Extrae a Fabricio desde fabricio-real-estate.webp usando BFS floodfill conectado
    únicamente desde los bordes exteriores (izquierda/arriba/derecha) sobre el fondo neutro.
    Cero huecos dentro de la camisa ni bordes serrucho sobre carbón #10100f.
    """
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

    # Semillas solo en bordes laterales y superior (jamás desde el borde inferior del traje)
    for x in range(w):
        if is_neutral_studio_bg(px[x, 0]):
            idx = x
            visited[idx] = 1
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

    # Contraer levemente 2px y suavizar para eliminar halo claro de estudio sobre #10100f
    alpha_eroded = alpha_img.filter(ImageFilter.MinFilter(3))
    alpha_soft = alpha_eroded.filter(ImageFilter.GaussianBlur(radius=2.2))

    # Desvanecimiento suave inferior para integración limpia sin corte duro
    fade_top = int(h * 0.78)
    spx = alpha_soft.load()
    for y in range(fade_top, h):
        factor = max(0.0, 1.0 - ((y - fade_top) / max(1, h - fade_top)))
        for x in range(w):
            spx[x, y] = int(spx[x, y] * (factor ** 1.15))

    # Recorte ajustado horizontalmente alrededor de la silueta centrada
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha_soft)
    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)

    cw, ch = rgba.size
    new_w = int(cw * (target_h / ch))
    return rgba.resize((new_w, target_h), Image.Resampling.LANCZOS)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int):
    lines = []
    for paragraph in text.split("\n"):
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


def draw_tracked_text(draw, pos, text, font, fill, tracking=2.5):
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bb = draw.textbbox((0, 0), ch, font=font)
        x += (bb[2] - bb[0]) + tracking


def draw_base_card_4x5(bg_color, badge_num: str, logo: Image.Image, watermark: Image.Image) -> Image.Image:
    W, H = 1080, 1350
    canvas = Image.new("RGBA", (W, H), bg_color + (255,))
    # Marca de agua FR centrada y muy sutil
    wx = (W - watermark.size[0]) // 2
    wy = (H - watermark.size[1]) // 2 + 20
    canvas.paste(watermark, (wx, wy), watermark)

    draw = ImageDraw.Draw(canvas, "RGBA")
    # Filete de oro fino 1px alrededor (dentro del lienzo, como tanda_1_reserva)
    draw.rectangle([(48, 48), (W - 48, H - 48)], outline=C_GOLD_BORDER, width=1)

    # Logo superior izquierdo dentro de zona segura y=185..1145 (y=188..246)
    canvas.paste(logo, (96, 188), logo)

    # Píldora de número arriba a la derecha (01 / 04 .. 04 / 04)
    f_badge = get_font(21, "medium")
    bb = draw.textbbox((0, 0), badge_num, font=f_badge)
    bw = (bb[2] - bb[0]) + 42
    bh = 42
    bx1 = W - 96 - bw
    by1 = 196
    draw.rounded_rectangle([(bx1, by1), (W - 96, by1 + bh)], radius=21, fill=bg_color + (235,), outline=C_GOLD_BORDER, width=1)
    draw.text((bx1 + 21, by1 + 8), badge_num, font=f_badge, fill=C_GOLD_LIGHT)

    return canvas


def draw_footer_4x5(draw, subline: str):
    W = 1080
    # Línea fina de pie dentro de zona segura y <= 1145
    y_line = 1054
    draw.line([(96, y_line), (W - 96, y_line)], fill=C_GOLD_BORDER, width=1)
    f_f1 = get_font(27, "medium")
    f_f2 = get_font(21, "regular")
    draw.text((96, 1074), "Fabricio Rivas · Escribano Público", font=f_f1, fill=C_WHITE)
    draw.text((96, 1112), subline, font=f_f2, fill=C_MUTED)


def render_4x5_carousel():
    logo = load_logo(target_height=56)
    watermark = make_subtle_watermark(size=430)
    portrait = extract_clean_portrait(target_h=565)

    # ------------------------------------------------------------------
    # PLACA 01 · Matriz 3A (Carbón Profundo #10100f)
    # ------------------------------------------------------------------
    c1 = draw_base_card_4x5(C_CARBON, "01 / 04", logo, watermark)
    d1 = ImageDraw.Draw(c1, "RGBA")
    f_kicker = get_font(20, "demibold")
    draw_tracked_text(d1, (96, 318), "CRITERIO NOTARIAL · CERTIFICACIONES", f_kicker, C_GOLD, tracking=2.6)

    f_h1 = get_font(60, "demibold")
    h1_lines = wrap_lines(
        d1,
        "Declaración jurada con firma certificada: tú declaras, el escribano certifica tu firma.",
        f_h1,
        884,
    )
    y = 374
    for ln in h1_lines:
        d1.text((96, y), ln, font=f_h1, fill=C_WHITE)
        y += 74

    y += 20
    d1.line([(96, y), (226, y)], fill=C_GOLD, width=3)
    y += 34

    f_body = get_font(33, "regular")
    body1 = (
        "En trámites ante organismos públicos, bancos o registros en Maldonado, "
        "son dos responsabilidades distintas que se unen en un mismo documento."
    )
    for ln in wrap_lines(d1, body1, f_body, 880):
        d1.text((96, y), ln, font=f_body, fill=C_PEARL)
        y += 48

    draw_footer_4x5(d1, "Matrícula SCJ 17058/5 · Punta del Este · Desliza para ver más")
    p1_path = os.path.join(OUT_DIR, "0.jpg")
    c1.convert("RGB").save(p1_path, "JPEG", quality=92, optimize=True)

    # ------------------------------------------------------------------
    # PLACA 02 · Matriz 3A (Carbón Profundo #10100f)
    # ------------------------------------------------------------------
    c2 = draw_base_card_4x5(C_CARBON, "02 / 04", logo, watermark)
    d2 = ImageDraw.Draw(c2, "RGBA")
    draw_tracked_text(d2, (96, 318), "QUÉ HACE CADA PARTE · ALCANCE LEGAL", f_kicker, C_GOLD, tracking=2.6)

    f_h2 = get_font(54, "demibold")
    y = 372
    for ln in wrap_lines(d2, "Qué declaras tú y qué acredita la actuación notarial:", f_h2, 884):
        d2.text((96, y), ln, font=f_h2, fill=C_WHITE)
        y += 66

    y += 14
    d2.line([(96, y), (226, y)], fill=C_GOLD, width=3)
    y += 34

    f_it_title = get_font(30, "demibold")
    f_it_body = get_font(28, "regular")
    items2 = [
        ("01 · Tu declaración:", "Manifiestas un hecho o dato personal bajo tu responsabilidad ante quien te lo solicita."),
        ("02 · La certificación notarial:", "El escribano verifica tu identidad y da fe de que la firma fue puesta en su presencia."),
        ("03 · Si firmas por una empresa:", "Se controla además la representación vigente (estatuto, contrato social o poder)."),
    ]
    for it_t, it_b in items2:
        d2.text((96, y), it_t, font=f_it_title, fill=C_GOLD_LIGHT)
        y += 40
        for ln in wrap_lines(d2, it_b, f_it_body, 880):
            d2.text((96, y), ln, font=f_it_body, fill=C_PEARL)
            y += 38
        y += 22

    draw_footer_4x5(d2, "Matrícula SCJ 17058/5 · Punta del Este · Desliza para ver más")
    p2_path = os.path.join(OUT_DIR, "1.jpg")
    c2.convert("RGB").save(p2_path, "JPEG", quality=92, optimize=True)

    # ------------------------------------------------------------------
    # PLACA 03 · Matriz 3B (Bronce / Oro Apagado #221e16)
    # ------------------------------------------------------------------
    c3 = draw_base_card_4x5(C_BRONZE, "03 / 04", logo, watermark)
    d3 = ImageDraw.Draw(c3, "RGBA")
    draw_tracked_text(d3, (96, 318), "REGLA PRÁCTICA ANTES DE FIRMAR", f_kicker, C_GOLD, tracking=2.6)

    y = 372
    for ln in wrap_lines(d3, "Tres recaudos para resolver el trámite en una sola visita:", f_h2, 884):
        d3.text((96, y), ln, font=f_h2, fill=C_WHITE)
        y += 66

    y += 14
    d3.line([(96, y), (226, y)], fill=C_GOLD, width=3)
    y += 32

    body3 = (
        "Envía antes por WhatsApp el modelo o instructivo del organismo, "
        "la foto del requisito exacto y tu documento de identidad vigente "
        "para preparar el texto."
    )
    for ln in wrap_lines(d3, body3, f_body, 880):
        d3.text((96, y), ln, font=f_body, fill=C_PEARL)
        y += 46

    # Recuadro interno Criterio de Seguridad: ancho contenido x = 96..984 (0 desbordes)
    f_box_lbl = get_font(19, "demibold")
    f_box_txt = get_font(30, "medium")
    box_txt = "Primero se revisa qué te pide el organismo; después se redacta y se certifica la firma."
    box_lines = wrap_lines(d3, box_txt, f_box_txt, 808)
    box_y1 = 790
    box_h = 68 + len(box_lines) * 42 + 28
    box_y2 = box_y1 + box_h
    d3.rounded_rectangle([(96, box_y1), (984, box_y2)], radius=18, fill=C_BOX_BG + (240,), outline=C_GOLD_BORDER, width=1)
    draw_tracked_text(d3, (132, box_y1 + 26), "CRITERIO DE SEGURIDAD", f_box_lbl, C_GOLD_LIGHT, tracking=2.5)
    by = box_y1 + 66
    for ln in box_lines:
        d3.text((132, by), ln, font=f_box_txt, fill=C_WHITE)
        by += 42

    draw_footer_4x5(d3, "Matrícula SCJ 17058/5 · Punta del Este · Desliza para ver más")
    p3_path = os.path.join(OUT_DIR, "2.jpg")
    c3.convert("RGB").save(p3_path, "JPEG", quality=92, optimize=True)

    # ------------------------------------------------------------------
    # PLACA 04 · Matriz 2 (Retrato + Sans sobre Carbón #10100f)
    # ------------------------------------------------------------------
    c4 = draw_base_card_4x5(C_CARBON, "04 / 04", logo, watermark)
    # Posicionar retrato limpiamente a la derecha arriba de la línea de pie (y_line=1054)
    pw, ph = portrait.size
    px = 1080 - pw - 52
    py = 1054 - ph
    c4.paste(portrait, (px, py), portrait)

    d4 = ImageDraw.Draw(c4, "RGBA")
    draw_tracked_text(d4, (96, 318), "ATENCIÓN NOTARIAL DIRECTA", f_kicker, C_GOLD, tracking=2.6)

    # Columna izquierda acotada a max_w = 485px para no superponerse jamás al retrato
    f_h4 = get_font(46, "demibold")
    y = 374
    for ln in wrap_lines(d4, "¿Te pidieron una declaración jurada con firma certificada?", f_h4, 490):
        d4.text((96, y), ln, font=f_h4, fill=C_WHITE)
        y += 58

    y += 16
    d4.line([(96, y), (196, y)], fill=C_GOLD, width=3)
    y += 28

    f_b4 = get_font(28, "regular")
    body4 = (
        "Atención directa en Punta del Este y Maldonado, también con coordinación previa a distancia.\n\n"
        "Consulta la guía en el enlace de la bio o envía el requisito por WhatsApp."
    )
    for ln in wrap_lines(d4, body4, f_b4, 480):
        d4.text((96, y), ln, font=f_b4, fill=C_PEARL)
        y += 40

    draw_footer_4x5(d4, "Matrícula SCJ 17058/5 · Punta del Este y Maldonado · WhatsApp +598 99 431 185")
    p4_path = os.path.join(OUT_DIR, "3.jpg")
    c4.convert("RGB").save(p4_path, "JPEG", quality=92, optimize=True)

    return [p1_path, p2_path, p3_path, p4_path]


def draw_9x16_scene(
    bg_color,
    logo: Image.Image,
    watermark: Image.Image,
    badge: str,
    kicker: str,
    headline: str,
    typed_txt: str,
    show_cursor: bool,
    box_mode: bool,
    box_label: str = "",
    portrait: Image.Image | None = None,
) -> Image.Image:
    """
    Lienzo 1080x1920 para Reel MP4 con marco, títulos y retrato 100% fijos (0px de movimiento)
    y zona segura estricta y = 300..1440.
    """
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), bg_color + (255,))
    canvas.paste(watermark, ((W - watermark.size[0]) // 2, 660), watermark)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Marco fino fijo dentro de la zona segura vertical
    draw.rectangle([(64, 304), (W - 64, 1436)], outline=C_GOLD_BORDER, width=1)
    canvas.paste(logo, (104, 344), logo)

    f_badge = get_font(21, "medium")
    bb = draw.textbbox((0, 0), badge, font=f_badge)
    bw = (bb[2] - bb[0]) + 40
    draw.rounded_rectangle([(W - 104 - bw, 350), (W - 104, 392)], radius=21, fill=bg_color + (235,), outline=C_GOLD_BORDER, width=1)
    draw.text((W - 104 - bw + 20, 358), badge, font=f_badge, fill=C_GOLD_LIGHT)

    f_kicker = get_font(20, "demibold")
    draw_tracked_text(draw, (104, 468), kicker, f_kicker, C_GOLD, tracking=2.5)

    if portrait is not None:
        # Escena de cierre 4 (Matriz 2) con retrato fijo a la derecha sobre la línea de pie
        pw, ph = portrait.size
        canvas.paste(portrait, (W - pw - 76, 1300 - ph), portrait)
        draw = ImageDraw.Draw(canvas, "RGBA")
        f_h = get_font(48, "demibold")
        y = 524
        for ln in wrap_lines(draw, headline, f_h, 465):
            draw.text((104, y), ln, font=f_h, fill=C_WHITE)
            y += 60
        y += 16
        draw.line([(104, y), (204, y)], fill=C_GOLD, width=3)
        y += 28
        f_b = get_font(30, "regular")
        for ln in wrap_lines(draw, typed_txt, f_b, 465):
            draw.text((104, y), ln, font=f_b, fill=C_PEARL)
            y += 42
    else:
        f_h = get_font(56, "demibold")
        y = 524
        for ln in wrap_lines(draw, headline, f_h, 860):
            draw.text((104, y), ln, font=f_h, fill=C_WHITE)
            y += 70
        y += 18
        draw.line([(104, y), (224, y)], fill=C_GOLD, width=3)

        display = typed_txt + ("|" if show_cursor else "")
        if box_mode:
            box_y1 = 830
            box_y2 = 1130
            draw.rounded_rectangle([(104, box_y1), (W - 104, box_y2)], radius=20, fill=C_BOX_BG + (238,), outline=C_GOLD_BORDER, width=1)
            f_bl = get_font(19, "demibold")
            draw_tracked_text(draw, (140, box_y1 + 28), box_label, f_bl, C_GOLD_LIGHT, tracking=2.5)
            f_bt = get_font(35, "medium")
            ty = box_y1 + 74
            for ln in wrap_lines(draw, display, f_bt, 792):
                draw.text((140, ty), ln, font=f_bt, fill=C_WHITE)
                ty += 48
        else:
            f_b = get_font(38, "regular")
            ty = y + 36
            for ln in wrap_lines(draw, display, f_b, 860):
                draw.text((104, ty), ln, font=f_b, fill=C_PEARL)
                ty += 52

    # Pie fijo en y = 1300..1400 (100% dentro de y = 300..1440)
    draw.line([(104, 1300), (W - 104, 1300)], fill=C_GOLD_BORDER, width=1)
    f_f1 = get_font(27, "medium")
    f_f2 = get_font(21, "regular")
    draw.text((104, 1320), "Fabricio Rivas · Escribano Público", font=f_f1, fill=C_WHITE)
    draw.text((104, 1358), "Matrícula SCJ 17058/5 · Punta del Este y Maldonado · +598 99 431 185", font=f_f2, fill=C_MUTED)
    return canvas.convert("RGB")


def build_9x16_reel():
    logo = load_logo(target_height=56)
    watermark = make_subtle_watermark(size=440)
    portrait = extract_clean_portrait(target_h=540)
    fps = 24
    # 12.0s totales (288 cuadros): lectura cómoda, cero zoompan en placas editoriales
    scenes = [
        {
            "bg": C_CARBON,
            "badge": "01 / 04",
            "kicker": "CRITERIO NOTARIAL · CERTIFICACIONES",
            "headline": "Declaración jurada con firma certificada:",
            "full_text": "Tú declaras bajo tu responsabilidad. El escribano acredita tu identidad y firma.",
            "box_mode": False,
            "box_label": "",
            "portrait": None,
            "dur": 2.9,
        },
        {
            "bg": C_CARBON,
            "badge": "02 / 04",
            "kicker": "ALCANCE DE CADA PARTE",
            "headline": "Cómo se divide el documento ante un organismo:",
            "full_text": "Tu afirmación define el contenido; la certificación notarial valida quién firmó.",
            "box_mode": True,
            "box_label": "CRITERIO NOTARIAL",
            "portrait": None,
            "dur": 3.2,
        },
        {
            "bg": C_BRONZE,
            "badge": "03 / 04",
            "kicker": "QUÉ ENVIAR ANTES POR WHATSAPP",
            "headline": "Resuelve el trámite en una sola visita:",
            "full_text": "Foto del requisito exacto, texto o modelo recibido y tu cédula vigente.",
            "box_mode": True,
            "box_label": "RECAUDOS PREVIOS",
            "portrait": None,
            "dur": 3.1,
        },
        {
            "bg": C_CARBON,
            "badge": "04 / 04",
            "kicker": "ATENCIÓN NOTARIAL DIRECTA",
            "headline": "¿Te pidieron firma certificada en Maldonado?",
            "full_text": "Atención directa en Punta del Este, también con coordinación previa a distancia.\n\nConsulta el enlace en bio o escribe por WhatsApp.",
            "box_mode": False,
            "box_label": "",
            "portrait": portrait,
            "dur": 2.8,
        },
    ]

    out_mp4 = os.path.join(OUT_DIR, "reel.mp4")
    with tempfile.TemporaryDirectory() as tmpdir:
        f_idx = 0
        for sc in scenes:
            n_frames = int(round(sc["dur"] * fps))
            if sc["portrait"] is not None:
                # Escena final estática y limpia (sin tipeo)
                im_final = draw_9x16_scene(
                    bg_color=sc["bg"],
                    logo=logo,
                    watermark=watermark,
                    badge=sc["badge"],
                    kicker=sc["kicker"],
                    headline=sc["headline"],
                    typed_txt=sc["full_text"],
                    show_cursor=False,
                    box_mode=False,
                    portrait=sc["portrait"],
                )
                for _ in range(n_frames):
                    im_final.save(os.path.join(tmpdir, f"f_{f_idx:04d}.jpg"), "JPEG", quality=90)
                    f_idx += 1
            else:
                txt = sc["full_text"]
                start_f = int(0.15 * fps)
                end_f = int((sc["dur"] - 0.85) * fps)
                span = max(1, end_f - start_f)
                cache_frames = {}
                for i in range(n_frames):
                    if i < start_f:
                        sub, cur = "", True
                    elif i <= end_f:
                        chars = int(round(((i - start_f) / span) * len(txt)))
                        sub, cur = txt[:chars], True
                    else:
                        sub = txt
                        cur = ((i - end_f) // 6) % 2 == 0
                    key = (sub, cur)
                    if key not in cache_frames:
                        cache_frames[key] = draw_9x16_scene(
                            bg_color=sc["bg"],
                            logo=logo,
                            watermark=watermark,
                            badge=sc["badge"],
                            kicker=sc["kicker"],
                            headline=sc["headline"],
                            typed_txt=sub,
                            show_cursor=cur,
                            box_mode=sc["box_mode"],
                            box_label=sc["box_label"],
                        )
                    cache_frames[key].save(os.path.join(tmpdir, f"f_{f_idx:04d}.jpg"), "JPEG", quality=90)
                    f_idx += 1

        total_dur = sum(s["dur"] for s in scenes)
        fade_out_start = round(total_dur - 1.8, 2)
        cmd = [
            FFMPEG_BIN, "-y",
            "-framerate", str(fps),
            "-i", os.path.join(tmpdir, "f_%04d.jpg"),
            "-i", MUSIC_MP3,
            "-filter_complex",
            f"[1:a]atrim=0:{total_dur},equalizer=f=350:t=q:w=1:g=2,afade=t=in:st=0:d=0.45,afade=t=out:st={fade_out_start}:d=1.8[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), "-preset", "medium", "-crf", "23",
            "-c:a", "aac", "-b:a", "160k",
            "-movflags", "+faststart",
            out_mp4,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Extraer un frame de prueba para inspección visual de zona segura
        subprocess.run(
            [FFMPEG_BIN, "-y", "-ss", "10.0", "-i", out_mp4, "-vframes", "1", os.path.join(OUT_DIR, "preview_reel_s4.jpg")],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    return out_mp4


if __name__ == "__main__":
    imgs = render_4x5_carousel()
    for p in imgs:
        luma = ImageStat.Stat(Image.open(p).convert("L")).mean[0]
        assert luma <= 39.0, f"Fallo Garantía Lumínica en {p}: {luma:.2f} > 39"
        print(f"OK {os.path.basename(p)}: mean_luma = {luma:.2f} (<= 39)")
    mp4 = build_9x16_reel()
    print(f"OK {os.path.basename(mp4)}: {os.path.getsize(mp4)} bytes")
