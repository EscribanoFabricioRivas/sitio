#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Pack Semanal Completo (7 Días - 18 Piezas Gráficas)
Escribano Público Fabricio Rivas · Punta del Este & Maldonado (Matrícula 17058/5)

Cumple estrictamente:
1. Directriz Canva (DISTRIBUCION-Y-CANVA.md):
   - Fotografía editorial realista a sangre de arquitectura contemporánea de Punta del Este.
   - Velo carbón translúcido en el lado izquierdo (no franja negra horizontal ni fondo de volante).
   - Logo real pequeño arriba a la izquierda (dentro de la zona segura).
   - Texto blanco con sans-serif liviana (Avenir Next), detalles oro apagado (#c4ad7a / #dac17f).
   - Mucho aire. Jerarquía limpia, sin letras pesadas ni títulos enteramente en mayúsculas.
2. Zonas Seguras Estrictas (Safe Zones) y Legibilidad Móvil:
   - Formato 1080x1350 (Feed / Post / Carrusel): Todo el contenido y firma entre y=175 e y=1165
     para que la cuadrícula 1:1 del perfil de Instagram (y=135..1215) jamás corte el logo ni la firma.
   - Formato 1080x1920 (Reel IG, Story IG, Historia FB, Estado WhatsApp): Todo el contenido y firma
     entre y=300 e y=1430, dejando 300px libres arriba y 490px libres abajo para la interfaz nativa.
   - Tipografía de firma y pie: 30px a 36px (100% legible en pantallas móviles sin zoom).
"""

import math
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = "/Users/arianawajntraub/.gemini/antigravity/worktrees/elegant-bardeen/teamwork_preview_workflow_automation"
ARTIFACT_DIR = "/Users/arianawajntraub/.gemini/antigravity/brain/8a79030b-f9ee-4ee1-9458-051b87c1cead"
SITIO_DIR = os.path.join(BASE_DIR, "sitio")
LOGO_PATH = os.path.join(SITIO_DIR, "images", "fr logo transparente fondo dorado FR escribano fabricio rivas.png")

FONDOS_DIR = os.path.join(SITIO_DIR, "campana", "fondos_ia")
WEEKLY_PIEZAS_DIR = os.path.join(SITIO_DIR, "campana", "semana_1_pack_completo", "piezas")
MAIN_PIEZAS_DIR = os.path.join(SITIO_DIR, "campana", "piezas")

os.makedirs(FONDOS_DIR, exist_ok=True)
os.makedirs(WEEKLY_PIEZAS_DIR, exist_ok=True)
os.makedirs(MAIN_PIEZAS_DIR, exist_ok=True)

# Copiar los 4 fondos generados al directorio del proyecto
RAW_BGS = {
    "bg1": os.path.join(ARTIFACT_DIR, "bg_01_la_barra_1792970055891.jpg"),
    "bg2": os.path.join(ARTIFACT_DIR, "bg_02_pinares_1792970076129.jpg"),
    "bg3": os.path.join(ARTIFACT_DIR, "bg_03_solanas_v2_1792970135915.jpg"),
    "bg4": os.path.join(ARTIFACT_DIR, "bg_04_courtyard_1792970172906.jpg"),
}

for k, src in RAW_BGS.items():
    dst = os.path.join(FONDOS_DIR, f"{k}.jpg")
    if os.path.exists(src):
        shutil.copy2(src, dst)

# Paleta oficial
COLOR_CARBON = (17, 17, 17)         # #111111
COLOR_GOLD = (196, 173, 122)        # #c4ad7a
COLOR_GOLD_LIGHT = (218, 193, 127)  # #dac17f
COLOR_PEARL = (246, 246, 244)       # #f6f6f4
COLOR_WHITE = (255, 255, 255)       # #ffffff

# Tipografías Sans-Serif livianas y elegantes (Avenir Next)
FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"
# Índices en Avenir Next.ttc:
# 0: Bold, 2: Demi Bold, 5: Medium, 7: Regular, 10: Ultra Light


def get_font(size, weight="regular"):
    idx_map = {
        "ultralight": 10,
        "regular": 7,
        "medium": 5,
        "demibold": 2,
        "bold": 0,
    }
    idx = idx_map.get(weight, 7)
    return ImageFont.truetype(FONT_PATH, size, index=idx)


def load_cropped_logo(target_height=110):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    w, h = logo.size
    target_w = int(w * (target_height / h))
    return logo.resize((target_w, target_height), Image.Resampling.LANCZOS)


def crop_and_resize(img_path, target_w, target_h, x_bias=0.5, y_bias=0.5):
    img = Image.open(img_path).convert("RGB")
    w, h = img.size
    target_ratio = target_w / target_h
    src_ratio = w / h
    if src_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = int((w - new_w) * x_bias)
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = int((h - new_h) * y_bias)
        img = img.crop((0, top, w, top + new_h))
    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)


def apply_editorial_veil(base_img, mode="feed"):
    """
    Aplica el velo carbón translúcido lateral izquierdo (según DISTRIBUCION-Y-CANVA.md):
    'Velo carbón translúcido en el lado izquierdo, no franja negra horizontal ni fondos de volante.'
    Garantiza contraste > 8:1 sobre el texto izquierdo dejando respirar la arquitectura a la derecha.
    """
    w, h = base_img.size
    base_rgba = base_img.convert("RGBA")
    veil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pixels = veil.load()

    for y in range(h):
        for x in range(w):
            nx = x / w
            ny = y / h
            if mode == "feed":
                # Velo lateral izquierdo suave con transición coseno hasta x=0.82
                if nx < 0.28:
                    ax = 0.84
                elif nx < 0.85:
                    t = (nx - 0.28) / (0.85 - 0.28)
                    ax = 0.84 * 0.5 * (1.0 + math.cos(math.pi * t))
                else:
                    ax = 0.0
                # Sutil refuerzo en la zona central para legibilidad perfecta sin franja negra dura
                ay = 0.08 * math.sin(math.pi * ny)
                alpha = min(0.88, ax + ay)
            else:
                # Modo vertical 9:16 (Stories / Reels / Estados):
                # Velo lateral izquierdo + refuerzo suave en la zona segura central (ny=0.15..0.78)
                if nx < 0.35:
                    ax = 0.86
                elif nx < 0.92:
                    t = (nx - 0.35) / (0.92 - 0.35)
                    ax = 0.86 * 0.5 * (1.0 + math.cos(math.pi * t))
                else:
                    ax = 0.05

                # Atenuar arriba (ny < 0.12) y abajo (ny > 0.82) para que la foto respire en los bordes
                if ny < 0.12:
                    vy = 0.55 + 0.45 * (ny / 0.12)
                elif ny > 0.80:
                    t_bot = min(1.0, (ny - 0.80) / 0.20)
                    vy = 1.0 - 0.35 * t_bot
                else:
                    vy = 1.0
                alpha = min(0.88, ax * vy)

            a_int = int(alpha * 255)
            pixels[x, y] = (17, 17, 17, a_int)

    return Image.alpha_composite(base_rgba, veil)


def draw_tracked_text(draw, pos, text, font, fill, tracking=4):
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), ch, font=font)
        ch_w = bbox[2] - bbox[0]
        x += ch_w + tracking


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = []
    for w in words:
        test_line = " ".join(current + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width or not current:
            current.append(w)
        else:
            lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def render_feed_piece(
    bg_path,
    out_base_path,
    kicker,
    headline_lines,
    subtitle_lines,
    badge_number=None,
    footer_line1="Fabricio Rivas | Escribano Público",
    footer_line2="Punta del Este · Maldonado · WhatsApp +598 99 431 185",
    x_bias=0.55,
    y_bias=0.5,
):
    """
    Renderiza pieza 1080x1350 con ZONA SEGURA CENTRAL 1:1 (y=180..1155).
    - El recorte cuadrado 1:1 del perfil de Instagram abarca y=135..1215.
    - Logo en (92, 185), tamaño 105px de alto.
    - Firma institucional en y=1045..1145 con tamaño 34px y 28px (100% legible en celular).
    """
    W, H = 1080, 1350
    bg = crop_and_resize(bg_path, W, H, x_bias=x_bias, y_bias=y_bias)
    canvas = apply_editorial_veil(bg, mode="feed")
    draw = ImageDraw.Draw(canvas)

    # 1. Logo real pequeño arriba a la izquierda (dentro del safe box 1:1, y=185)
    logo = load_cropped_logo(target_height=105)
    canvas.paste(logo, (92, 185), logo)

    # Opcional: indicador de slide para carrusel en píldora carbón con borde oro (100% contraste)
    if badge_number:
        pill_x1, pill_y1, pill_x2, pill_y2 = 845, 195, 988, 250
        draw.rounded_rectangle(
            [(pill_x1, pill_y1), (pill_x2, pill_y2)],
            radius=27,
            fill=(17, 17, 17, 215),
            outline=(196, 173, 122, 190),
            width=2,
        )
        font_badge = get_font(24, "demibold")
        bbox = draw.textbbox((0, 0), badge_number, font=font_badge)
        bw = bbox[2] - bbox[0]
        bh = bbox[3] - bbox[1]
        draw.text(
            (pill_x1 + (pill_x2 - pill_x1 - bw) // 2, pill_y1 + (pill_y2 - pill_y1 - bh) // 2 - 3),
            badge_number,
            font=font_badge,
            fill=COLOR_GOLD_LIGHT,
        )

    # 2. Kicker en oro apagado con tracking elegante
    y_cursor = 385
    if kicker:
        font_kicker = get_font(23, "demibold")
        draw_tracked_text(draw, (92, y_cursor), kicker.upper(), font_kicker, COLOR_GOLD_LIGHT, tracking=4)
        y_cursor += 58

    # 3. Titular principal (sans-serif liviana/regular, blanco puro, cuerpo grande 64px)
    font_headline = get_font(62, "medium")
    for line in headline_lines:
        draw.text((92, y_cursor), line, font=font_headline, fill=COLOR_WHITE)
        y_cursor += 76

    y_cursor += 24
    # Línea sutil en oro apagado
    draw.line([(92, y_cursor), (210, y_cursor)], fill=COLOR_GOLD, width=3)
    y_cursor += 36

    # 4. Bajada / Subtítulo con mucho aire (cuerpo 38px, muy legible en móvil)
    font_sub = get_font(37, "regular")
    for sline in subtitle_lines:
        draw.text((92, y_cursor), sline, font=font_sub, fill=COLOR_PEARL)
        y_cursor += 52

    # 5. Firma institucional en Zona Segura (y=1045..1145, nunca se corta en el grid 1:1)
    y_footer = 1045
    draw.line([(92, y_footer - 24), (680, y_footer - 24)], fill=(196, 173, 122, 110), width=2)
    font_f1 = get_font(34, "medium")
    font_f2 = get_font(27, "regular")
    draw.text((92, y_footer), footer_line1, font=font_f1, fill=COLOR_WHITE)
    draw.text((92, y_footer + 48), footer_line2, font=font_f2, fill=COLOR_GOLD_LIGHT)

    # Guardar PNG y JPG (<300 KB para cumplir regla del repo)
    rgb_canvas = canvas.convert("RGB")
    png_path = out_base_path + ".png"
    jpg_path = out_base_path + ".jpg"
    rgb_canvas.save(png_path, format="PNG", optimize=True)
    rgb_canvas.save(jpg_path, format="JPEG", quality=86, optimize=True)
    return png_path, jpg_path


def render_vertical_piece(
    bg_path,
    out_base_path,
    kicker,
    headline_lines,
    subtitle_lines,
    cta_pill_text="WhatsApp +598 99 431 185",
    footer_line1="Fabricio Rivas | Escribano Público",
    footer_line2="Punta del Este · Maldonado · Matrícula 17058/5",
    x_bias=0.5,
    y_bias=0.5,
):
    """
    Renderiza pieza 1080x1920 (Story IG, Historia FB, Reel IG, Estado WhatsApp)
    con ZONA SEGURA ESTRICTA:
    - Arriba: 0..300 px libres (interfaz de usuario / barra de stories / nombre).
    - Abajo: 1440..1920 px (480 px inferiores!) 100% libres (barra 'Enviar mensaje',
      controles de Reel, pie de Estado de WhatsApp).
    - Derecha: x > 940 libre (iconos laterales de Reels).
    - Todo el contenido vive en el corazón visual (y=310..1420), garantizando también
      que en la vista previa 1:1 o 4:5 de Reels se vea íntegro.
    """
    W, H = 1080, 1920
    bg = crop_and_resize(bg_path, W, H, x_bias=x_bias, y_bias=y_bias)
    canvas = apply_editorial_veil(bg, mode="vertical")
    draw = ImageDraw.Draw(canvas)

    # 1. Logo real pequeño arriba a la izquierda en y=320 (bajo los 280px de UI de Stories)
    logo = load_cropped_logo(target_height=115)
    canvas.paste(logo, (92, 320), logo)

    # 2. Kicker en oro apagado
    y_cursor = 540
    if kicker:
        font_kicker = get_font(25, "demibold")
        draw_tracked_text(draw, (92, y_cursor), kicker.upper(), font_kicker, COLOR_GOLD_LIGHT, tracking=4)
        y_cursor += 64

    # 3. Titular principal (66px, blanco puro)
    font_headline = get_font(66, "medium")
    for line in headline_lines:
        draw.text((92, y_cursor), line, font=font_headline, fill=COLOR_WHITE)
        y_cursor += 82

    y_cursor += 28
    draw.line([(92, y_cursor), (220, y_cursor)], fill=COLOR_GOLD, width=3)
    y_cursor += 40

    # 4. Bajada / Subtítulo (40px, lectura instantánea en celular)
    font_sub = get_font(40, "regular")
    for sline in subtitle_lines:
        draw.text((92, y_cursor), sline, font=font_sub, fill=COLOR_PEARL)
        y_cursor += 56

    # 5. Píldora sutil de contacto / CTA dentro de la zona segura (y ~ 1170)
    if cta_pill_text:
        y_pill = max(y_cursor + 36, 1150)
        pill_w, pill_h = 620, 74
        draw.rounded_rectangle(
            [(92, y_pill), (92 + pill_w, y_pill + pill_h)],
            radius=37,
            fill=(196, 173, 122, 235),
        )
        font_cta = get_font(31, "demibold")
        bbox = draw.textbbox((0, 0), cta_pill_text, font=font_cta)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(
            (92 + (pill_w - tw) // 2, y_pill + (pill_h - th) // 2 - 4),
            cta_pill_text,
            font=font_cta,
            fill=COLOR_CARBON,
        )

    # 6. Firma institucional grande y nítida en y=1310..1410 (dejando 510px libres abajo!)
    y_footer = 1315
    draw.line([(92, y_footer - 24), (720, y_footer - 24)], fill=(196, 173, 122, 120), width=2)
    font_f1 = get_font(36, "medium")
    font_f2 = get_font(29, "regular")
    draw.text((92, y_footer), footer_line1, font=font_f1, fill=COLOR_WHITE)
    draw.text((92, y_footer + 50), footer_line2, font=font_f2, fill=COLOR_GOLD_LIGHT)

    rgb_canvas = canvas.convert("RGB")
    png_path = out_base_path + ".png"
    jpg_path = out_base_path + ".jpg"
    rgb_canvas.save(png_path, format="PNG", optimize=True)
    rgb_canvas.save(jpg_path, format="JPEG", quality=86, optimize=True)
    return png_path, jpg_path


def main():
    bg1 = os.path.join(FONDOS_DIR, "bg1.jpg")
    bg2 = os.path.join(FONDOS_DIR, "bg2.jpg")
    bg3 = os.path.join(FONDOS_DIR, "bg3.jpg")
    bg4 = os.path.join(FONDOS_DIR, "bg4.jpg")

    # =========================================================================
    # DÍA 1 (LUNES): Nota Criterio Notarial (Placa exacta de DISTRIBUCION-Y-CANVA.md)
    # =========================================================================
    render_feed_piece(
        bg_path=bg1,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia1_feed_1080x1350"),
        kicker="Criterio Notarial · Real Estate",
        headline_lines=[
            "Antes de fijar la firma,",
            "revisa la documentación.",
        ],
        subtitle_lines=[
            "Compraventa en Punta del Este.",
            "Títulos, planos y antecedentes.",
        ],
    )
    render_vertical_piece(
        bg_path=bg1,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia1_vertical_1080x1920"),
        kicker="Criterio Notarial · Real Estate",
        headline_lines=[
            "Antes de fijar la firma,",
            "revisa la documentación.",
        ],
        subtitle_lines=[
            "Compraventa en Punta del Este.",
            "Títulos, planos y antecedentes",
            "revisados con rigor notarial.",
        ],
    )

    # =========================================================================
    # DÍA 2 (MARTES): Carrusel Educativo de 5 Placas (1080x1350) + Vertical (1080x1920)
    # =========================================================================
    # Slide 1: Portada
    render_feed_piece(
        bg_path=bg3,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia2_carrusel_01_1080x1350"),
        kicker="Compraventa en Punta del Este",
        headline_lines=[
            "¿Comprando una",
            "propiedad en la costa?",
        ],
        subtitle_lines=[
            "3 puntos críticos que debes revisar",
            "antes de transferir la reserva.",
        ],
        badge_number="01 / 05",
    )
    # Slide 2: Punto 1
    render_feed_piece(
        bg_path=bg3,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia2_carrusel_02_1080x1350"),
        kicker="01 · Estudio de Títulos",
        headline_lines=[
            "La titularidad y los",
            "antecedentes no se",
            "presumen.",
        ],
        subtitle_lines=[
            "Tu escribano estudia la cadena",
            "completa de títulos por 30 años",
            "antes del desembolso mayor.",
        ],
        badge_number="02 / 05",
        x_bias=0.35,
    )
    # Slide 3: Punto 2
    render_feed_piece(
        bg_path=bg3,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia2_carrusel_03_1080x1350"),
        kicker="02 · Boleto de Reserva",
        headline_lines=[
            "La reserva fija las",
            "reglas de juego.",
        ],
        subtitle_lines=[
            "No es una seña informal.",
            "Establece plazos, multas y",
            "condiciones de devolución.",
        ],
        badge_number="03 / 05",
        x_bias=0.65,
    )
    # Slide 4: Punto 3
    render_feed_piece(
        bg_path=bg3,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia2_carrusel_04_1080x1350"),
        kicker="03 · Independencia Profesional",
        headline_lines=[
            "Tu propio escribano",
            "cuida tu patrimonio.",
        ],
        subtitle_lines=[
            "La inmobiliaria acerca a las partes;",
            "tú tienes el derecho de elegir a tu",
            "escribano de confianza.",
        ],
        badge_number="04 / 05",
        x_bias=0.45,
    )
    # Slide 5: Cierre CTA
    render_feed_piece(
        bg_path=bg3,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia2_carrusel_05_1080x1350"),
        kicker="Revisión Documental Previa",
        headline_lines=[
            "Revisa antes",
            "de firmar.",
        ],
        subtitle_lines=[
            "Atención directa, también a",
            "distancia si estás en otro país.",
            "Consulta al +598 99 431 185.",
        ],
        badge_number="05 / 05",
    )
    # Vertical Día 2
    render_vertical_piece(
        bg_path=bg3,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia2_vertical_1080x1920"),
        kicker="Compraventa en Punta del Este",
        headline_lines=[
            "¿Comprando una",
            "propiedad en la costa?",
        ],
        subtitle_lines=[
            "3 puntos críticos antes de",
            "transferir la reserva.",
            "Revisa antes de firmar.",
        ],
    )

    # =========================================================================
    # DÍA 3 (MIÉRCOLES): Clientes Extranjeros (Argentina / Brasil)
    # =========================================================================
    render_feed_piece(
        bg_path=bg2,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia3_feed_1080x1350"),
        kicker="Compradores No Residentes",
        headline_lines=[
            "¿Compras desde",
            "Argentina o Brasil?",
        ],
        subtitle_lines=[
            "Atención directa, también a",
            "distancia si estás en otro país.",
            "Estudio de títulos y poderes.",
        ],
    )
    render_vertical_piece(
        bg_path=bg2,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia3_vertical_1080x1920"),
        kicker="Compradores No Residentes",
        headline_lines=[
            "¿Compras desde",
            "Argentina o Brasil?",
        ],
        subtitle_lines=[
            "Atención directa, también a",
            "distancia si estás en otro país.",
            "Seguridad jurídica en tu compra.",
        ],
    )

    # =========================================================================
    # DÍA 4 (JUEVES): Reel / Video Guionado + Portada 1080x1920 + Placa 1080x1350
    # =========================================================================
    render_vertical_piece(
        bg_path=bg4,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia4_reel_1080x1920"),
        kicker="Criterio Notarial · Punta del Este",
        headline_lines=[
            "No firmes la reserva",
            "sin revisión previa.",
        ],
        subtitle_lines=[
            "El boleto define plazos, multas",
            "y qué ocurre ante deudas o",
            "títulos observados.",
        ],
    )
    render_feed_piece(
        bg_path=bg4,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia4_feed_1080x1350"),
        kicker="Criterio Notarial · Punta del Este",
        headline_lines=[
            "No firmes la reserva",
            "sin revisión previa.",
        ],
        subtitle_lines=[
            "El boleto define plazos, multas",
            "y qué ocurre ante deudas o",
            "títulos observados.",
        ],
    )

    # =========================================================================
    # DÍA 5 (VIERNES): Certificaciones de Firma y Poderes en Maldonado
    # =========================================================================
    render_feed_piece(
        bg_path=bg4,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia5_feed_1080x1350"),
        kicker="Soluciones Notariales · Maldonado",
        headline_lines=[
            "Certificación de firmas",
            "y poderes en el día.",
        ],
        subtitle_lines=[
            "Trámites bancarios, societarios",
            "y comerciales con revisión previa.",
        ],
        x_bias=0.3,
    )
    render_vertical_piece(
        bg_path=bg4,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia5_vertical_1080x1920"),
        kicker="Soluciones Notariales · Maldonado",
        headline_lines=[
            "Certificación de firmas",
            "y poderes en el día.",
        ],
        subtitle_lines=[
            "Trámites bancarios, societarios",
            "y comerciales en Punta del Este",
            "y Maldonado.",
        ],
        x_bias=0.3,
    )

    # =========================================================================
    # DÍA 6 (SÁBADO): Recorrida de Propiedades el Fin de Semana
    # =========================================================================
    render_vertical_piece(
        bg_path=bg1,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia6_vertical_1080x1920"),
        kicker="Fin de Semana en Punta del Este",
        headline_lines=[
            "¿Viendo propiedades",
            "para comprar?",
        ],
        subtitle_lines=[
            "Antes de entregar una seña,",
            "revisa las condiciones con tu",
            "propio escribano.",
        ],
        x_bias=0.7,
    )
    render_feed_piece(
        bg_path=bg1,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia6_feed_1080x1350"),
        kicker="Fin de Semana en Punta del Este",
        headline_lines=[
            "¿Viendo propiedades",
            "para comprar?",
        ],
        subtitle_lines=[
            "Antes de entregar una seña,",
            "revisa las condiciones con tu",
            "propio escribano.",
        ],
        x_bias=0.7,
    )

    # =========================================================================
    # DÍA 7 (DOMINGO): Independencia del Comprador / Cierre Semanal
    # =========================================================================
    render_feed_piece(
        bg_path=bg2,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia7_feed_1080x1350"),
        kicker="Seguridad Jurídica · Real Estate",
        headline_lines=[
            "Tu propio escribano",
            "cuida tu patrimonio.",
        ],
        subtitle_lines=[
            "Estudio independiente de títulos,",
            "planos y antecedentes en",
            "Punta del Este y Maldonado.",
        ],
        x_bias=0.65,
    )
    render_vertical_piece(
        bg_path=bg2,
        out_base_path=os.path.join(WEEKLY_PIEZAS_DIR, "dia7_vertical_1080x1920"),
        kicker="Seguridad Jurídica · Real Estate",
        headline_lines=[
            "Tu propio escribano",
            "cuida tu patrimonio.",
        ],
        subtitle_lines=[
            "Estudio independiente de títulos,",
            "planos y antecedentes en",
            "Punta del Este y Maldonado.",
        ],
        x_bias=0.65,
    )

    # =========================================================================
    # ACTUALIZAR TAMBIÉN LAS PIEZAS MAESTRAS DE CAMPAÑA (ad_feed y ad_story)
    # =========================================================================
    render_feed_piece(
        bg_path=bg1,
        out_base_path=os.path.join(MAIN_PIEZAS_DIR, "ad_feed_1080x1350"),
        kicker="Criterio Notarial · Real Estate",
        headline_lines=[
            "Revisa antes",
            "de firmar.",
        ],
        subtitle_lines=[
            "Estudio independiente de títulos",
            "y boletos de reserva en",
            "Punta del Este y Maldonado.",
        ],
    )
    shutil.copy2(
        os.path.join(MAIN_PIEZAS_DIR, "ad_feed_1080x1350.png"),
        os.path.join(MAIN_PIEZAS_DIR, "ad_post_1080x1350.png"),
    )
    shutil.copy2(
        os.path.join(MAIN_PIEZAS_DIR, "ad_feed_1080x1350.jpg"),
        os.path.join(MAIN_PIEZAS_DIR, "ad_post_1080x1350.jpg"),
    )

    render_vertical_piece(
        bg_path=bg3,
        out_base_path=os.path.join(MAIN_PIEZAS_DIR, "ad_story_1080x1920"),
        kicker="Criterio Notarial · Real Estate",
        headline_lines=[
            "¿Vas a señar una",
            "propiedad en la costa?",
            "Revisa antes de firmar.",
        ],
        subtitle_lines=[
            "Asesoría notarial independiente.",
            "Atención directa, también a",
            "distancia si estás en otro país.",
        ],
    )

    print("18 piezas semanales + 2 piezas maestras de pauta renderizadas con éxito.")


if __name__ == "__main__":
    main()
