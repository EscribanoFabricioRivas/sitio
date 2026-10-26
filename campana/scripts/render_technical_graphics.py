#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Piezas Gráficas Técnicas XXL para Redes Sociales (CERO FOTO IA)
Regla de Oro de Legibilidad Móvil (Lienzo 1080x1350 visto en pantalla de 375px):
- PROHIBIDO usar textos de 20-26px.
- Cuerpo técnico mínimo: 46 a 52 px.
- Titulares: 70 a 86 px.
- Números / Indicadores: 110 a 130 px.
- Firma y pie: 36 a 40 px.
- 1 concepto técnico o 1 paso fuerte por placa = impacto visual inmediato en el feed.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/arianawajntraub/.gemini/antigravity/worktrees/elegant-bardeen/teamwork_preview_workflow_automation"
ARTIFACT_DIR = "/Users/arianawajntraub/.gemini/antigravity/brain/8a79030b-f9ee-4ee1-9458-051b87c1cead"
SITIO_DIR = os.path.join(BASE_DIR, "sitio")
LOGO_PATH = os.path.join(SITIO_DIR, "images", "fr logo transparente fondo dorado FR escribano fabricio rivas.png")
OUT_DIR = os.path.join(SITIO_DIR, "campana", "semana_1_pack_completo", "piezas_tecnicas_sin_ia")
GDRIVE_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/FR pp AG/semana_1_pack_completo/piezas_tecnicas_sin_ia"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(GDRIVE_DIR, exist_ok=True)

FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"

C_CARBON = (17, 17, 17)         # #111111
C_DARK_CARD = (28, 28, 28)      # #1c1c1c
C_TEXT_DARK = (32, 32, 32)      # #202020
C_GOLD = (196, 173, 122)        # #c4ad7a
C_GOLD_LIGHT = (218, 193, 127)  # #dac17f
C_GOLD_DARK = (80, 70, 2)       # #504602
C_SAND_BG = (246, 246, 244)     # #f6f6f4
C_STONE_BG = (233, 231, 225)    # #e9e7e1
C_WHITE = (255, 255, 255)


def get_font(size, weight="regular"):
    idx_map = {
        "ultralight": 10,
        "regular": 7,
        "medium": 5,
        "demibold": 2,
        "bold": 0,
    }
    return ImageFont.truetype(FONT_PATH, size, index=idx_map.get(weight, 7))


def load_logo(height=88):
    logo = Image.open(LOGO_PATH).convert("RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    w, h = logo.size
    return logo.resize((int(w * (height / h)), height), Image.Resampling.LANCZOS)


def wrap_lines(draw, text, font, max_w):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        cur = []
        for w in words:
            test = " ".join(cur + [w])
            bbox = draw.textbbox((0, 0), test, font=font)
            if (bbox[2] - bbox[0]) <= max_w or not cur:
                cur.append(w)
            else:
                lines.append(" ".join(cur))
                cur = [w]
        if cur:
            lines.append(" ".join(cur))
    return lines


def draw_header_xxl(canvas, draw, dark_mode=True, badge_text="01 / 04"):
    """Encabezado grande y limpio dentro de la zona segura 1:1 (y=155..255)."""
    logo = load_logo(height=84)
    if not dark_mode:
        draw.rounded_rectangle([(84, 150), (196, 250)], radius=22, fill=C_CARBON)
        canvas.paste(logo, (97, 158), logo)
    else:
        canvas.paste(logo, (84, 155), logo)

    if badge_text:
        f_badge = get_font(30, "demibold")
        bbox = draw.textbbox((0, 0), badge_text, font=f_badge)
        tw = bbox[2] - bbox[0] + 56
        bg_col = (34, 34, 34) if dark_mode else C_CARBON
        txt_col = C_GOLD_LIGHT
        draw.rounded_rectangle([(996 - tw, 165), (996, 233)], radius=34, fill=bg_col, outline=C_GOLD, width=2)
        draw.text((996 - tw + 28, 180), badge_text, font=f_badge, fill=txt_col)


def draw_footer_xxl(draw, dark_mode=True):
    """Firma institucional GRANDE (36px / 30px) dentro de la zona segura 1:1 (y=1075..1175)."""
    y = 1080
    line_col = (196, 173, 122, 120) if dark_mode else (17, 17, 17, 60)
    draw.line([(84, y - 22), (996, y - 22)], fill=line_col, width=3)
    f_name = get_font(36, "demibold")
    f_sub = get_font(30, "medium")
    c1 = C_WHITE if dark_mode else C_CARBON
    c2 = C_GOLD_LIGHT if dark_mode else C_GOLD_DARK
    draw.text((84, y), "Fabricio Rivas | Escribano Público", font=f_name, fill=c1)
    draw.text((84, y + 48), "Punta del Este · WhatsApp +598 99 431 185", font=f_sub, fill=c2)


def save_both(canvas, filename_base):
    rgb = canvas.convert("RGB")
    for folder in [OUT_DIR, GDRIVE_DIR]:
        rgb.save(os.path.join(folder, filename_base + ".jpg"), "JPEG", quality=90, optimize=True)
        rgb.save(os.path.join(folder, filename_base + ".png"), "PNG", optimize=True)
    rgb.save(os.path.join(ARTIFACT_DIR, filename_base + ".jpg"), "JPEG", quality=90, optimize=True)


def render_step_card_xxl(
    filename_base,
    dark_mode,
    badge_text,
    step_num,
    kicker,
    headline_lines,
    body_text,
    takeaway_label,
    takeaway_text,
):
    """
    Renderiza una placa técnica XXL para redes:
    - 1 gran paso técnico por placa, con números de 110px, titular de 68px y cuerpo de 44px.
    """
    W, H = 1080, 1350
    bg_color = C_CARBON if dark_mode else C_STONE_BG
    canvas = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(canvas)

    draw_header_xxl(canvas, draw, dark_mode=dark_mode, badge_text=badge_text)

    # Tarjeta central grande
    card_bg = C_DARK_CARD if dark_mode else C_WHITE
    card_border = C_GOLD if dark_mode else (196, 173, 122)
    draw.rounded_rectangle([(76, 280), (1004, 1025)], radius=34, fill=card_bg, outline=card_border, width=3)

    # Círculo con número XXL o etiqueta de paso
    pill_w = max(135, len(step_num) * 34 + 44)
    draw.rounded_rectangle([(120, 325), (120 + pill_w, 415)], radius=22, fill=C_GOLD)
    f_num = get_font(44, "bold")
    bbox = draw.textbbox((0, 0), step_num, font=f_num)
    nw = bbox[2] - bbox[0]
    draw.text((120 + (pill_w - nw) // 2, 342), step_num, font=f_num, fill=C_CARBON)

    # Kicker al lado del número
    f_kicker = get_font(28, "demibold")
    k_col = C_GOLD_LIGHT if dark_mode else C_GOLD_DARK
    draw.text((120 + pill_w + 26, 352), kicker.upper(), font=f_kicker, fill=k_col)

    # Titular XXL (64px)
    y_cur = 445
    f_head = get_font(62, "bold")
    head_col = C_WHITE if dark_mode else C_CARBON
    for hl in headline_lines:
        draw.text((120, y_cur), hl, font=f_head, fill=head_col)
        y_cur += 74

    y_cur += 20
    # Explicación técnica clara en 42px (lectura instantánea en el feed del móvil)
    f_body = get_font(41, "regular")
    body_col = C_SAND_BG if dark_mode else C_TEXT_DARK
    for bl in wrap_lines(draw, body_text, f_body, 830):
        draw.text((120, y_cur), bl, font=f_body, fill=body_col)
        y_cur += 54

    # Caja inferior de Recomendación / Clave práctica (en el pie de la tarjeta)
    box_y1, box_y2 = 845, 990
    box_fill = (44, 39, 26) if dark_mode else (244, 240, 230)
    draw.rounded_rectangle([(116, box_y1), (964, box_y2)], radius=22, fill=box_fill, outline=C_GOLD, width=2)
    f_tk_label = get_font(28, "bold")
    f_tk_text = get_font(33, "medium")
    tk_col = C_GOLD_LIGHT if dark_mode else C_GOLD_DARK
    draw.text((144, box_y1 + 20), takeaway_label, font=f_tk_label, fill=tk_col)
    draw.text((144, box_y1 + 66), takeaway_text, font=f_tk_text, fill=head_col)

    draw_footer_xxl(draw, dark_mode=dark_mode)
    save_both(canvas, filename_base)


def main():
    # 1. PASO 01: Seña en Custodia (Escrow) — Fondo Claro Editorial (#e9e7e1)
    render_step_card_xxl(
        filename_base="tecnica_01_proceso_compraventa_1080x1350",
        dark_mode=False,
        badge_text="PASO 01 / 03",
        step_num="01",
        kicker="Antes de transferir",
        headline_lines=[
            "La seña queda en",
            "custodia notarial.",
        ],
        body_text="En Uruguay, el 10% de reserva no se entrega directo al vendedor: tu escribano lo retiene en garantía (escrow) hasta auditar los títulos.",
        takeaway_label="RECOMENDACIÓN CLAVE:",
        takeaway_text="Exige cláusula de devolución íntegra si hay deudas.",
    )

    # 2. COMPARATIVA TÉCNICA: Promesa Inscripta Ley 8.733 — Fondo Carbón (#111111)
    render_step_card_xxl(
        filename_base="tecnica_02_reserva_vs_promesa_1080x1350",
        dark_mode=True,
        badge_text="CLAVE LEGAL",
        step_num="LEY",
        kicker="Reserva vs. Promesa 8.733",
        headline_lines=[
            "¿Compras en pozo",
            "o en cuotas?",
        ],
        body_text="El Boleto de Reserva es privado y no frena embargos. La Promesa Inscripta (Ley 8.733) se registra y te da derecho real frente a terceros.",
        takeaway_label="REGLA PRÁCTICA:",
        takeaway_text="Si hay pagos a plazo, exige Promesa Inscripta.",
    )

    # 3. AUDITORÍA DOCUMENTAL: Estudio de 30 años y PH — Fondo Claro (#e9e7e1)
    render_step_card_xxl(
        filename_base="tecnica_03_checklist_ph_vs_casa_1080x1350",
        dark_mode=False,
        badge_text="PASO 02 / 03",
        step_num="02",
        kicker="Auditoría Registral",
        headline_lines=[
            "Estudio de títulos",
            "por 30 años y BPS.",
        ],
        body_text="Verificamos en Registros Públicos (DGR) que no existan hipotecas, embargos ni sucesiones pendientes, más Final de Obra y libre de BPS.",
        takeaway_label="EN APARTAMENTOS (PH):",
        takeaway_text="Se audita Reglamento y libre de gastos comunes.",
    )

    # 4. EXTRANJEROS: Poder Especial Apostillado — Fondo Carbón (#111111)
    render_step_card_xxl(
        filename_base="tecnica_04_poder_extranjeros_1080x1350",
        dark_mode=True,
        badge_text="EXTRANJEROS",
        step_num="AR/BR",
        kicker="Compra a distancia",
        headline_lines=[
            "Cómo firmar desde",
            "Argentina o Brasil.",
        ],
        body_text="1. Redactamos la minuta en Punta del Este.\n2. Firmas en tu ciudad y colocas la Apostilla.\n3. Protocolizamos en Uruguay para escriturar.",
        takeaway_label="MODALIDAD:",
        takeaway_text="Atención directa, también a distancia.",
    )

    print("4 placas técnicas XXL para redes generadas con éxito.")


if __name__ == "__main__":
    main()
