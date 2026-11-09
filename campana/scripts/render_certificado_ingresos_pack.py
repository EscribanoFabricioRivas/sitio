#!/usr/bin/env python3
"""
Generador XXL de Alta Legibilidad para las 3 Publicaciones de Certificado de Ingresos (Maldonado y Punta del Este).
Regla estricta:
- Zona segura 4:5 (1080x1350): todo texto y logo dentro de y = 185..1145, x = 64..1016.
- Tipografía XXL de alto contraste: títulos 62-66px Bold, bloques centrales 38-42px DemiBold/Bold,
  WhatsApp +598 99 431 185 en 42px Bold dentro de barra sólida de máximo contraste.
- CERO texto dorado pálido sobre fondo Piedra #e9e7e1 (sobre Piedra va siempre Carbón #111111 Bold o Blanco sobre bloque Carbón).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE_SITE = Path("/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio")
OUT_DIR = BASE_SITE / "campana" / "pack_maldonado_en_el_dia"
BG_DIR = BASE_SITE / "campana" / "fondos_ia"
LOGO_PATH = BASE_SITE / "images" / "fr logo transparente fondo dorado FR escribano fabricio rivas.png"

OUT_DIR.mkdir(parents=True, exist_ok=True)

CARBON = (17, 17, 17)         # #111111
CARBON_CARD = (32, 32, 32)    # #202020
PIEDRA = (233, 231, 225)      # #e9e7e1
BLANCO = (255, 255, 255)      # #ffffff
DORADO = (196, 173, 122)      # #c4ad7a

FONT_TTC = "/System/Library/Fonts/Avenir Next.ttc"


def get_font(size: int, style: str = "bold") -> ImageFont.FreeTypeFont:
    idx_map = {
        "bold": 0,
        "demibold": 2,
        "medium": 5,
        "regular": 7,
    }
    idx = idx_map.get(style, 0)
    try:
        return ImageFont.truetype(FONT_TTC, size, index=idx)
    except Exception:
        return ImageFont.load_default()


def load_monogram_transparent(height: int = 80, color_override=None) -> Image.Image:
    raw = Image.open(LOGO_PATH).convert("RGBA")
    new_pixels = []
    for r, g, b, a in raw.getdata():
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        alpha = max(0, min(255, int((lum - 25.0) * 3.2)))
        final_a = min(a, alpha)
        if color_override is not None:
            new_pixels.append((color_override[0], color_override[1], color_override[2], final_a))
        else:
            new_pixels.append((r, g, b, final_a))
    clean = Image.new("RGBA", raw.size)
    clean.putdata(new_pixels)
    bbox = clean.getbbox()
    if bbox:
        clean = clean.crop(bbox)
    w, h = clean.size
    new_w = int(w * (height / h))
    return clean.resize((new_w, height), Image.Resampling.LANCZOS)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = f"{cur} {w}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_multiline(draw: ImageDraw.ImageDraw, lines: list[str], x: int, y: int, font: ImageFont.FreeTypeFont, fill, line_spacing: int = 10) -> int:
    cur_y = y
    for line in lines:
        draw.text((x, cur_y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        cur_y += (bbox[3] - bbox[1]) + line_spacing
    return cur_y


# ==============================================================================
# 1. PUBLICACIÓN 1: CON IA · REVISTA EDITORIAL FOTOGRÁFICA XXL (3 LÁMINAS 4:5)
# ==============================================================================
def render_pub1_con_ia():
    slides = [
        {
            "out": "ingresos_con_ia_01_1080x1350.jpg",
            "bg": BG_DIR / "bg7.jpg",
            "step": "01 / 03",
            "kicker": "RESIDENCIA LEGAL Y BANCOS · PUNTA DEL ESTE",
            "title": "Certificado notarial de ingresos en Maldonado",
            "body": "Acreditamos tus medios de vida ante Migraciones, bancos locales y garantías de alquiler en 24 a 48 h.",
        },
        {
            "out": "ingresos_con_ia_02_1080x1350.jpg",
            "bg": BG_DIR / "bg8.jpg",
            "step": "02 / 03",
            "kicker": "EXTRANJEROS · INDEPENDIENTES · SAS",
            "title": "¿Qué ingresos puedes certificar en Uruguay?",
            "body": "Rentas o dividendos del exterior, facturación de empresas unipersonales, honorarios o utilidades de SAS.",
        },
        {
            "out": "ingresos_con_ia_03_1080x1350.jpg",
            "bg": BG_DIR / "bg4.jpg",
            "step": "03 / 03",
            "kicker": "REVISIÓN PREVIA POR WHATSAPP",
            "title": "Envías tus documentos digitales y pasas a firmar",
            "body": "Revisamos tus comprobantes antes de que concurras al estudio en Punta del Este.",
        },
    ]

    logo_gold = load_monogram_transparent(74, color_override=None)

    for s in slides:
        W, H = 1080, 1350
        canvas = Image.new("RGB", (W, H), CARBON)

        photo_h = 545
        bg_img = Image.open(s["bg"]).convert("RGB")
        photo_crop = ImageOps.fit(bg_img, (W, photo_h), method=Image.Resampling.LANCZOS)
        canvas.paste(photo_crop, (0, 0))

        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        for yy in range(photo_h - 80, photo_h):
            alpha = int(255 * ((yy - (photo_h - 80)) / 80.0))
            odraw.line([(0, yy), (W, yy)], fill=(17, 17, 17, alpha))

        odraw.rounded_rectangle((68, 190, 190, 286), radius=14, fill=(17, 17, 17, 235), outline=DORADO + (220,), width=2)
        odraw.rounded_rectangle((836, 204, 1012, 272), radius=34, fill=(17, 17, 17, 235), outline=DORADO + (220,), width=2)

        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        canvas.paste(logo_gold, (94, 201), logo_gold)

        draw = ImageDraw.Draw(canvas)
        f_step = get_font(30, "bold")
        st_bbox = draw.textbbox((0, 0), s["step"], font=f_step)
        draw.text((836 + (176 - (st_bbox[2] - st_bbox[0])) // 2, 218), s["step"], font=f_step, fill=BLANCO)

        # Gold structural divider
        draw.rectangle((0, photo_h - 5, W, photo_h + 3), fill=DORADO)

        # Editorial block XXL (y = 560..1140)
        f_kicker = get_font(31, "bold")
        draw.text((68, 566), s["kicker"], font=f_kicker, fill=DORADO)

        f_title = get_font(64, "bold")
        t_lines = wrap_text(draw, s["title"], f_title, W - 136)
        cur_y = draw_multiline(draw, t_lines, 68, 612, f_title, BLANCO, line_spacing=6)

        f_body = get_font(44, "bold")
        b_lines = wrap_text(draw, s["body"], f_body, W - 136)
        cur_y = draw_multiline(draw, b_lines, 68, cur_y + 14, f_body, PIEDRA, line_spacing=8)

        # Solid Gold CTA Bar inside safe zone (y = 1012..1140)
        bar_y = 1012
        draw.rounded_rectangle((68, bar_y, W - 68, bar_y + 128), radius=12, fill=DORADO)
        f_cta_top = get_font(28, "bold")
        f_cta_wa = get_font(52, "bold")
        draw.text((96, bar_y + 14), "ESCRIBANO FABRICIO RIVAS · PUNTA DEL ESTE", font=f_cta_top, fill=CARBON)
        draw.text((96, bar_y + 52), "WhatsApp +598 99 431 185", font=f_cta_wa, fill=CARBON)

        out_path = OUT_DIR / s["out"]
        canvas.save(out_path, "JPEG", quality=95)
        print("Saved Pub 1 XXL (CON IA):", out_path.name)


# ==============================================================================
# 2. PUBLICACIÓN 2: SIN IA · GRILLA SUIZA EN PIEDRA #e9e7e1 XXL (3 LÁMINAS 4:5)
#    CERO texto dorado sobre Piedra: todo texto en Carbón #111111 Bold sobre tarjetas
#    blancas de alto contraste + barra inferior Carbón sólida con WhatsApp en 44px Bold.
# ==============================================================================
def render_pub2_sin_ia_piedra():
    logo_carbon = load_monogram_transparent(76, color_override=CARBON)
    W, H = 1080, 1350

    slides = [
        {
            "out": "tecnica_05_certificado_ingresos_independientes_1080x1350.jpg",
            "badge": "INDEPENDIENTES Y SAS · 01/03",
            "title": "Certificado de ingresos para independientes",
            "cards": [
                ("UNIPERSONALES Y PROFESIONALES", "Facturación electrónica y declaraciones juradas DGI / BPS."),
                ("SOCIOS Y DIRECTORES DE SAS", "Estatuto social, actas y certificaciones en 24 a 48 h."),
            ],
        },
        {
            "out": "sin_ia_piedra_02_ingresos_requisitos_1080x1350.jpg",
            "badge": "DOCUMENTACIÓN · 02/03",
            "title": "¿Qué comprobantes envías por WhatsApp?",
            "cards": [
                ("1. DESTINO DEL CERTIFICADO", "Indica si te lo solicita un banco, garantía de alquiler o Migración."),
                ("2. RESPALDO DE ACTIVIDAD", "Últimos 6 a 12 meses de facturación, declaraciones o contratos."),
            ],
        },
        {
            "out": "sin_ia_piedra_03_ingresos_cierre_1080x1350.jpg",
            "badge": "ENTREGA EN 24 A 48 H · 03/03",
            "title": "Revisión digital previa sin moverte de más",
            "cards": [
                ("VERIFICACIÓN POR WHATSAPP", "Validamos tus PDFs antes de que vengas a firmar al estudio."),
                ("ESCRIBANO PÚBLICO HABILITADO", "Fabricio Rivas · Matrícula 17058/5 · ARTOWER Punta del Este."),
            ],
        },
    ]

    for s in slides:
        canvas = Image.new("RGB", (W, H), PIEDRA)
        draw = ImageDraw.Draw(canvas)

        # Top header inside safe zone (y = 190..274)
        canvas.paste(logo_carbon, (68, 190), logo_carbon)

        # High-contrast pill on top right
        f_badge = get_font(26, "bold")
        bb = draw.textbbox((0, 0), s["badge"], font=f_badge)
        bw = (bb[2] - bb[0]) + 48
        draw.rounded_rectangle((W - 68 - bw, 200, W - 68, 264), radius=8, fill=CARBON)
        draw.text((W - 68 - bw + 24, 214), s["badge"], font=f_badge, fill=DORADO)

        # Heavy Swiss divider
        draw.rectangle((68, 284, W - 68, 290), fill=CARBON)

        # Main Headline XXL (68px Bold in solid #111111)
        f_title = get_font(66, "bold")
        t_lines = wrap_text(draw, s["title"], f_title, W - 136)
        cur_y = draw_multiline(draw, t_lines, 68, 310, f_title, CARBON, line_spacing=6)

        # 2 Giant High-Contrast White Cards with solid Carbon typography (34px Bold + 47px Bold)
        card_y = 496
        f_card_lbl = get_font(33, "bold")
        f_card_val = get_font(47, "bold")

        for c_lbl, c_val in s["cards"]:
            card_h = 236
            draw.rectangle((68, card_y, W - 68, card_y + card_h), fill=BLANCO, outline=CARBON, width=4)
            draw.rectangle((68, card_y, 88, card_y + card_h), fill=CARBON)
            draw.text((110, card_y + 18), c_lbl, font=f_card_lbl, fill=CARBON)
            draw.rectangle((110, card_y + 64, W - 96, card_y + 68), fill=DORADO)
            val_lines = wrap_text(draw, c_val, f_card_val, W - 206)
            draw_multiline(draw, val_lines, 110, card_y + 78, f_card_val, CARBON, line_spacing=4)
            card_y += card_h + 20

        # Solid Carbon Footer Block inside safe zone (y = 1010..1140)
        foot_y = 1010
        draw.rectangle((68, foot_y, W - 68, foot_y + 130), fill=CARBON)
        draw.rectangle((68, foot_y, 88, foot_y + 130), fill=DORADO)
        f_foot_top = get_font(28, "bold")
        f_foot_wa = get_font(54, "bold")
        draw.text((110, foot_y + 14), "ESCRIBANO FABRICIO RIVAS · PUNTA DEL ESTE", font=f_foot_top, fill=DORADO)
        draw.text((110, foot_y + 52), "WhatsApp +598 99 431 185", font=f_foot_wa, fill=BLANCO)

        out_path = OUT_DIR / s["out"]
        canvas.save(out_path, "JPEG", quality=95)
        print("Saved Pub 2 XXL (SIN IA Piedra):", out_path.name)


# ==============================================================================
# 3. PUBLICACIÓN 3: SIN IA · GRILLA SUIZA EN CARBÓN #111111 XXL (3 LÁMINAS 4:5)
# ==============================================================================
def render_pub3_sin_ia_carbon():
    logo_gold = load_monogram_transparent(76, color_override=None)
    W, H = 1080, 1350

    slides = [
        {
            "out": "tecnica_06_certificado_ingresos_migraciones_1080x1350.jpg",
            "code": "MIGRACIONES Y BANCOS · 01/03",
            "title": "Medios de vida para residencia en Uruguay",
            "items": [
                ("RENTAS Y DIVIDENDOS DEL EXTERIOR", "Acreditación notarial de ingresos percibidos fuera de Uruguay."),
                ("ACTIVIDAD LOCAL O PROFESIONAL", "Honorarios, contratos vigentes o sociedades en el país."),
            ],
        },
        {
            "out": "sin_ia_carbon_02_bancos_alquileres_1080x1350.jpg",
            "code": "BANCOS Y ALQUILERES · 02/03",
            "title": "Carpetas para bancos y garantías en Maldonado",
            "items": [
                ("GARANTÍAS DE ALQUILER ANUAL", "Certificación de tu ingreso mensual promedio para aseguradoras."),
                ("APERTURA DE CUENTA Y COMPLIANCE", "Respaldo formal de origen de fondos para bancos locales."),
            ],
        },
        {
            "out": "sin_ia_carbon_03_puente_patrimonial_1080x1350.jpg",
            "code": "INVERSIÓN EN PUNTA DEL ESTE · 03/03",
            "title": "De tu residencia legal a tu compra inmobiliaria",
            "items": [
                ("ATENCIÓN DIRECTA Y A DISTANCIA", "Adelantamos toda la revisión documental si estás en otro país."),
                ("ESCRIBANO PÚBLICO HABILITADO", "Fabricio Rivas · Matrícula 17058/5 · Universidad CLAEH · AEU."),
            ],
        },
    ]

    for s in slides:
        canvas = Image.new("RGB", (W, H), CARBON)
        draw = ImageDraw.Draw(canvas)

        # Left vertical gold spine inside safe zone (x=68..82, y=190..1138)
        draw.rectangle((68, 190, 82, 1138), fill=DORADO)

        # Header row
        canvas.paste(logo_gold, (108, 190), logo_gold)

        f_code = get_font(27, "bold")
        cb = draw.textbbox((0, 0), s["code"], font=f_code)
        draw.text((W - 68 - (cb[2] - cb[0]), 212), s["code"], font=f_code, fill=DORADO)

        draw.rectangle((108, 284, W - 68, 288), fill=DORADO)

        # Headline XXL (66px Bold White)
        f_title = get_font(66, "bold")
        t_lines = wrap_text(draw, s["title"], f_title, W - 176)
        cur_y = draw_multiline(draw, t_lines, 108, 310, f_title, BLANCO, line_spacing=6)

        # 2 Giant High-Contrast Cards (33px Bold Gold + 46px Bold White)
        box_y = 496
        f_ih = get_font(33, "bold")
        f_ib = get_font(46, "bold")

        for ih, ib in s["items"]:
            card_h = 236
            draw.rectangle((108, box_y, W - 68, box_y + card_h), fill=CARBON_CARD, outline=DORADO, width=3)
            draw.text((138, box_y + 18), ih, font=f_ih, fill=DORADO)
            ib_lines = wrap_text(draw, ib, f_ib, W - 236)
            draw_multiline(draw, ib_lines, 138, box_y + 72, f_ib, BLANCO, line_spacing=4)
            box_y += card_h + 20

        # Solid Gold Bottom Bar inside safe zone (y = 1010..1140)
        cta_y = 1010
        draw.rectangle((108, cta_y, W - 68, cta_y + 130), fill=DORADO)
        f_cta_top = get_font(28, "bold")
        f_cta_wa = get_font(52, "bold")
        draw.text((138, cta_y + 14), "REVISIÓN DOCUMENTAL PREVIA · PUNTA DEL ESTE", font=f_cta_top, fill=CARBON)
        draw.text((138, cta_y + 52), "WhatsApp +598 99 431 185", font=f_cta_wa, fill=CARBON)

        out_path = OUT_DIR / s["out"]
        canvas.save(out_path, "JPEG", quality=95)
        print("Saved Pub 3 XXL (SIN IA Carbón):", out_path.name)


if __name__ == "__main__":
    render_pub1_con_ia()
    render_pub2_sin_ia_piedra()
    render_pub3_sin_ia_carbon()
