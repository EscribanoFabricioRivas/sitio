#!/usr/bin/env python3
"""
Generador de las 3 Publicaciones Diferenciadas para Certificado de Ingresos (Maldonado y Punta del Este):
1. PUBLICACIÓN 1 (CON IA · Revista Editorial Fotográfica 4:5 — 3 láminas + Reel MP4):
   - Layout editorial de revista arquitectónica (bloque fotográfico superior limpio + bloque editorial inferior sólido #111111 sin recuadros repetitivos).
2. PUBLICACIÓN 2 (SIN IA · Grilla Tipográfica Suiza en Piedra #e9e7e1 — 3 láminas 4:5):
   - 100% tipográfico editorial suizo sobre Piedra #e9e7e1 con monograma FR en Carbón #111111 100% transparente (CERO cuadrado negro detrás del logo, CERO marco redondeado viejo).
3. PUBLICACIÓN 3 (SIN IA · Grilla Tipográfica Suiza en Carbón #111111 — 3 láminas 4:5 + Google Maps 700x700):
   - 100% tipográfico de alto contraste sobre Carbón #111111 con columna vertebral dorada #c4ad7a y filas estructuradas de requisitos.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE_SITE = Path("/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio")
OUT_DIR = BASE_SITE / "campana" / "pack_maldonado_en_el_dia"
BG_DIR = BASE_SITE / "campana" / "fondos_ia"
LOGO_PATH = BASE_SITE / "images" / "fr logo transparente fondo dorado FR escribano fabricio rivas.png"

OUT_DIR.mkdir(parents=True, exist_ok=True)

CARBON = (17, 17, 17)         # #111111
CARBON_SOFT = (28, 28, 28)    # #1c1c1c
PIEDRA = (233, 231, 225)      # #e9e7e1
PIEDRA_DARK = (216, 212, 202) # #d8d4ca
DORADO = (196, 173, 122)      # #c4ad7a
DORADO_DARK = (142, 118, 68)
BLANCO = (255, 255, 255)
GRIS_TXT = (85, 82, 76)

FONT_TTC = "/System/Library/Fonts/Avenir Next.ttc"


def get_font(size: int, style: str = "regular") -> ImageFont.FreeTypeFont:
    idx_map = {
        "bold": 0,
        "demibold": 2,
        "medium": 5,
        "regular": 7,
        "ultralight": 9,
    }
    idx = idx_map.get(style, 7)
    try:
        return ImageFont.truetype(FONT_TTC, size, index=idx)
    except Exception:
        return ImageFont.load_default()


def load_monogram_transparent(height: int = 86, color_override=None) -> Image.Image:
    """
    Extrae el monograma FR 100% transparente (elimina por completo cualquier fondo negro).
    Si color_override=(17,17,17), pinta el monograma en Carbón puro para fondos claros (#e9e7e1)
    sin jamás ponerle un parche negro detrás.
    """
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


def draw_multiline(draw: ImageDraw.ImageDraw, lines: list[str], x: int, y: int, font: ImageFont.FreeTypeFont, fill, line_spacing: int = 12) -> int:
    cur_y = y
    for line in lines:
        draw.text((x, cur_y), line, font=font, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        cur_y += (bbox[3] - bbox[1]) + line_spacing
    return cur_y


# ==============================================================================
# 1. PUBLICACIÓN 1: CON IA · REVISTA EDITORIAL FOTOGRÁFICA (3 LÁMINAS 4:5)
#    (Mitad superior foto arquitectónica limpia sin velo marrón encima +
#     Mitad inferior bloque editorial sólido #111111 con filete dorado #c4ad7a)
# ==============================================================================
def render_pub1_con_ia():
    slides = [
        {
            "out": "ingresos_con_ia_01_1080x1350.jpg",
            "bg": BG_DIR / "bg4.jpg",
            "step": "01 / 03",
            "kicker": "RESIDENCIA LEGAL Y BANCOS · PUNTA DEL ESTE",
            "title": "Certificado notarial de ingresos en Maldonado",
            "body": "Acreditación formal de tus medios de vida para Dirección Nacional de Migración, apertura de cuentas bancarias y garantías de alquiler.",
            "pill": "REVISIÓN DOCUMENTAL PREVIA POR WHATSAPP · +598 99 431 185",
        },
        {
            "out": "ingresos_con_ia_02_1080x1350.jpg",
            "bg": BG_DIR / "bg2.jpg",
            "step": "02 / 03",
            "kicker": "EXTRANJEROS, PROFESIONALES Y EMPRESAS",
            "title": "¿Qué ingresos se pueden certificar en Uruguay?",
            "body": "Rentas o dividendos del exterior, honorarios profesionales independientes, facturación de unipersonales o participación en sociedades SAS.",
            "pill": "CRITERIO AJUSTADO A LA ENTIDAD RECEPTORA EN 24 A 48 H",
        },
        {
            "out": "ingresos_con_ia_03_1080x1350.jpg",
            "bg": BG_DIR / "bg1.jpg",
            "step": "03 / 03",
            "kicker": "GESTIÓN ÁGIL SIN MOVERTE DE MÁS",
            "title": "Envías tus comprobantes digitales y pasas a firmar",
            "body": "Indícanos por WhatsApp qué organismo te solicita el certificado y tu actividad principal para indicarte los recaudos exactos en el día.",
            "pill": "ESCRIBANO FABRICIO RIVAS · MAT. 17058/5 · +598 99 431 185",
        },
    ]

    logo_gold = load_monogram_transparent(72, color_override=None)

    for s in slides:
        W, H = 1080, 1350
        canvas = Image.new("RGB", (W, H), CARBON)

        # Top photo zone: y = 0..660 (100% clean architectural image)
        photo_h = 660
        bg_img = Image.open(s["bg"]).convert("RGB")
        photo_crop = ImageOps.fit(bg_img, (W, photo_h), method=Image.Resampling.LANCZOS)
        canvas.paste(photo_crop, (0, 0))

        # Subtle top header bar inside safe zone (y=190) with dark pill for monogram & step
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        # Soft gradient only at the bottom 90px of the photo to transition into the solid editorial block
        for yy in range(photo_h - 90, photo_h):
            alpha = int(255 * ((yy - (photo_h - 90)) / 90.0))
            odraw.line([(0, yy), (W, yy)], fill=(17, 17, 17, alpha))

        # Top badge pill on photo (inside safe zone y=195)
        odraw.rounded_rectangle((84, 192, 200, 286), radius=14, fill=(17, 17, 17, 215), outline=DORADO + (180,), width=1)
        odraw.rounded_rectangle((860, 212, 996, 266), radius=27, fill=(17, 17, 17, 215), outline=DORADO + (200,), width=1)

        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        canvas.paste(logo_gold, (108, 203), logo_gold)

        draw = ImageDraw.Draw(canvas)
        f_step = get_font(22, "demibold")
        st_bbox = draw.textbbox((0, 0), s["step"], font=f_step)
        draw.text((860 + (136 - (st_bbox[2] - st_bbox[0])) // 2, 224), s["step"], font=f_step, fill=PIEDRA)

        # Gold structural divider at y = 660
        draw.rectangle((0, photo_h - 4, W, photo_h + 2), fill=DORADO)

        # Editorial bottom block: y = 662..1350 (Safe zone bottom = 1145)
        f_kicker = get_font(21, "demibold")
        draw.text((88, 692), s["kicker"], font=f_kicker, fill=DORADO)

        f_title = get_font(52, "bold")
        t_lines = wrap_text(draw, s["title"], f_title, W - 176)
        cur_y = draw_multiline(draw, t_lines, 88, 732, f_title, BLANCO, line_spacing=8)

        f_body = get_font(30, "regular")
        b_lines = wrap_text(draw, s["body"], f_body, W - 176)
        cur_y = draw_multiline(draw, b_lines, 88, cur_y + 18, f_body, PIEDRA, line_spacing=10)

        # Bottom highlight strip inside safe zone (y <= 1135)
        bar_y = 1048
        draw.rounded_rectangle((88, bar_y, W - 88, bar_y + 74), radius=10, fill=CARBON_SOFT, outline=DORADO, width=2)
        f_pill = get_font(22, "demibold")
        draw.text((114, bar_y + 23), s["pill"], font=f_pill, fill=DORADO)

        out_path = OUT_DIR / s["out"]
        canvas.save(out_path, "JPEG", quality=94)
        print("Saved Pub 1 (CON IA):", out_path.name)


# ==============================================================================
# 2. PUBLICACIÓN 2: SIN IA · GRILLA TIPOGRÁFICA SUIZA EN PIEDRA #e9e7e1 (3 LÁMINAS 4:5)
#    (100% Tipográfico Puro · Monograma FR en Carbón #111111 SIN cuadrado negro ·
#     Grilla editorial suiza con líneas sólidas y bloques de datos)
# ==============================================================================
def render_pub2_sin_ia_piedra():
    logo_carbon = load_monogram_transparent(74, color_override=CARBON)
    W, H = 1080, 1350

    slides = [
        {
            "out": "tecnica_05_certificado_ingresos_independientes_1080x1350.jpg",
            "num": "01",
            "tag": "TRABAJADORES INDEPENDIENTES · UNIPERSONALES · SAS",
            "title": "Certificado notarial de ingresos para independientes.",
            "lead": "Si facturas como profesional universitario, titular de empresa unipersonal o socio de una SAS en Maldonado, acreditamos tus ingresos mensuales ante bancos y organismos.",
            "rows": [
                ("UNIPERSONALES Y SERVICIOS", "Facturación electrónica y declaraciones juradas DGI / BPS."),
                ("SOCIOS Y DIRECTORES DE SAS", "Estatuto social, actas de distribución o remuneraciones."),
                ("PLAZO DE EMISIÓN", "Revisión por WhatsApp y retiro en 24 a 48 horas hábiles."),
            ],
        },
        {
            "out": "sin_ia_piedra_02_ingresos_requisitos_1080x1350.jpg",
            "num": "02",
            "tag": "CHECKLIST DOCUMENTAL · REVISIÓN DIGITAL PREVIA",
            "title": "¿Qué comprobantes necesitas enviar por WhatsApp?",
            "lead": "Antes de que vengas al estudio en Punta del Este, verificamos los documentos en PDF para que el certificado cumpla con el formato exacto de la entidad:",
            "rows": [
                ("1. ENTIDAD RECEPTORA", "Indica si es para banco, garantía de alquiler, Migración o licitación."),
                ("2. RESPALDO DE INGRESOS", "Últimos 6 a 12 meses de facturación, declaraciones o contratos."),
                ("3. IDENTIDAD Y GIRO", "Cédula o pasaporte vigente y constancia de inscripción en DGI/BPS."),
            ],
        },
        {
            "out": "sin_ia_piedra_03_ingresos_cierre_1080x1350.jpg",
            "num": "03",
            "tag": "ATENCIÓN DIRECTA · PUNTA DEL ESTE Y MALDONADO",
            "title": "Coordina tu certificado hoy por WhatsApp.",
            "lead": "Recibimos tu documentación de respaldo a distancia y coordinamos día y hora de firma o entrega en Punta del Este.",
            "rows": [
                ("WHATSAPP DIRECTO", "+598 99 431 185 · Respuesta ágil en el día."),
                ("ESCRIBANO HABILITADO", "Fabricio Rivas · Matrícula SCJ N.º 17058/5 · CLAEH · AEU."),
                ("UBICACIÓN DEL ESTUDIO", "ARTOWER, Francisco Salazar y Chiverta, Punta del Este."),
            ],
        },
    ]

    for idx, s in enumerate(slides, 1):
        canvas = Image.new("RGB", (W, H), PIEDRA)
        draw = ImageDraw.Draw(canvas)

        # Top Swiss header inside safe zone (y = 195..285)
        canvas.paste(logo_carbon, (88, 195), logo_carbon)

        # Big editorial number on the right (Swiss style)
        f_big_num = get_font(68, "bold")
        nb = draw.textbbox((0, 0), s["num"], font=f_big_num)
        draw.text((W - 88 - (nb[2] - nb[0]), 182), s["num"], font=f_big_num, fill=DORADO_DARK)

        f_sub_idx = get_font(18, "demibold")
        draw.text((W - 88 - (nb[2] - nb[0]), 258), f"LÁMINA 0{idx} / 03", font=f_sub_idx, fill=CARBON)

        # Structural horizontal rule #1
        draw.rectangle((88, 292, W - 88, 295), fill=CARBON)
        draw.rectangle((88, 295, 290, 300), fill=DORADO_DARK)

        # Tagline
        f_tag = get_font(21, "demibold")
        draw.text((88, 322), s["tag"], font=f_tag, fill=DORADO_DARK)

        # Main Typographic Headline XXL
        f_title = get_font(56, "bold")
        t_lines = wrap_text(draw, s["title"], f_title, W - 176)
        cur_y = draw_multiline(draw, t_lines, 88, 364, f_title, CARBON, line_spacing=8)

        # Lead paragraph
        f_lead = get_font(29, "regular")
        l_lines = wrap_text(draw, s["lead"], f_lead, W - 176)
        cur_y = draw_multiline(draw, l_lines, 88, cur_y + 16, f_lead, GRIS_TXT, line_spacing=9)

        # Swiss table of 3 structured rows
        row_y = max(cur_y + 28, 725)
        f_row_lbl = get_font(20, "bold")
        f_row_val = get_font(25, "medium")

        for r_lbl, r_val in s["rows"]:
            draw.rectangle((88, row_y, W - 88, row_y + 96), fill=PIEDRA_DARK)
            draw.rectangle((88, row_y, 96, row_y + 96), fill=CARBON)
            draw.text((118, row_y + 16), r_lbl, font=f_row_lbl, fill=DORADO_DARK)
            draw.text((118, row_y + 46), r_val, font=f_row_val, fill=CARBON)
            row_y += 108

        # Footer rule inside safe zone (y <= 1135)
        foot_y = 1078
        draw.rectangle((88, foot_y, W - 88, foot_y + 2), fill=CARBON)
        f_foot_b = get_font(23, "bold")
        f_foot_r = get_font(22, "medium")
        draw.text((88, foot_y + 16), "Fabricio Rivas | Escribano Público", font=f_foot_b, fill=CARBON)
        w_txt = "WhatsApp +598 99 431 185"
        wb = draw.textbbox((0, 0), w_txt, font=f_foot_r)
        draw.text((W - 88 - (wb[2] - wb[0]), foot_y + 17), w_txt, font=f_foot_r, fill=DORADO_DARK)

        out_path = OUT_DIR / s["out"]
        canvas.save(out_path, "JPEG", quality=94)
        print("Saved Pub 2 (SIN IA Piedra):", out_path.name)


# ==============================================================================
# 3. PUBLICACIÓN 3: SIN IA · GRILLA TIPOGRÁFICA SUIZA EN CARBÓN #111111 (3 LÁMINAS 4:5)
#    (100% Tipográfico Alto Contraste · Cero foto borrosa · Cero marco redondeado viejo ·
#     Columna lateral dorada + tabla jurídica limpia)
# ==============================================================================
def render_pub3_sin_ia_carbon():
    logo_gold = load_monogram_transparent(74, color_override=None)
    W, H = 1080, 1350

    slides = [
        {
            "out": "tecnica_06_certificado_ingresos_migraciones_1080x1350.jpg",
            "code": "MIGRACIONES · BANCOS",
            "title": "Medios de vida para residencia legal en Uruguay.",
            "lead": "La Dirección Nacional de Migración y los bancos locales exigen acreditar el origen lícito, el monto mensual y la regularidad de tus ingresos mediante certificado notarial.",
            "items": [
                ("RENTAS Y DIVIDENDOS DEL EXTERIOR", "Acreditación de ingresos percibidos fuera de Uruguay con documentación respaldante."),
                ("ACTIVIDAD LOCAL O REMOTA", "Honorarios profesionales, contratos vigentes o sociedades en Uruguay."),
            ],
            "cta": "REVISIÓN PREVIA POR WHATSAPP · +598 99 431 185",
        },
        {
            "out": "sin_ia_carbon_02_bancos_alquileres_1080x1350.jpg",
            "code": "GARANTÍAS · APERTURA BANCARIA",
            "title": "Carpeta para bancos y garantías de alquiler en Maldonado.",
            "lead": "Si alquilas vivienda anual o abres cuenta patrimonial en Punta del Este, las aseguradoras y oficiales de cumplimiento piden certificación contable o notarial de ingresos.",
            "items": [
                ("ASEGURADORAS Y GARANTÍAS", "Certificación del flujo mensual promedio para contratos de alquiler anual."),
                ("CUMPLIMIENTO BANCARIO (COMPLIANCE)", "Acreditación documental del origen de fondos para compra o apertura de cuenta."),
            ],
            "cta": "EMISIÓN EN 24 A 48 HORAS HÁBILES · PUNTA DEL ESTE",
        },
        {
            "out": "sin_ia_carbon_03_puente_patrimonial_1080x1350.jpg",
            "code": "RADICACIÓN EN PUNTA DEL ESTE",
            "title": "De tu residencia legal a tu compra inmobiliaria o SAS.",
            "lead": "Acompañamos cada etapa jurídica de quienes se radican o invierten en Maldonado: desde el certificado de ingresos y el alquiler anual hasta la compraventa inmobiliaria.",
            "items": [
                ("ATENCIÓN DIRECTA Y A DISTANCIA", "Adelantamos la revisión documental por WhatsApp aunque estés en otro país."),
                ("ESCRIBANO PÚBLICO HABILITADO", "Fabricio Rivas · Matrícula SCJ 17058/5 · Universidad CLAEH · AEU."),
            ],
            "cta": "CONSULTA DIRECTA · WHATSAPP +598 99 431 185",
        },
    ]

    for idx, s in enumerate(slides, 1):
        canvas = Image.new("RGB", (W, H), CARBON)
        draw = ImageDraw.Draw(canvas)

        # Left vertical architectural gold spine inside safe zone (x=88..96, y=195..1130)
        draw.rectangle((88, 195, 96, 1130), fill=DORADO)

        # Header row (x=126..992, y=195)
        canvas.paste(logo_gold, (126, 195), logo_gold)

        f_code = get_font(20, "demibold")
        cb = draw.textbbox((0, 0), f"{s['code']}  ·  0{idx}/03", font=f_code)
        draw.text((W - 88 - (cb[2] - cb[0]), 220), f"{s['code']}  ·  0{idx}/03", font=f_code, fill=DORADO)

        # Horizontal divider
        draw.rectangle((126, 290, W - 88, 292), fill=(60, 56, 48))

        # Big Headline XXL
        f_title = get_font(56, "bold")
        t_lines = wrap_text(draw, s["title"], f_title, W - 214)
        cur_y = draw_multiline(draw, t_lines, 126, 322, f_title, PIEDRA, line_spacing=8)

        # Lead text
        f_lead = get_font(29, "regular")
        l_lines = wrap_text(draw, s["lead"], f_lead, W - 214)
        cur_y = draw_multiline(draw, l_lines, 126, cur_y + 18, f_lead, (200, 196, 188), line_spacing=10)

        # Two structured dark-stone cards
        box_y = max(cur_y + 28, 720)
        f_ih = get_font(21, "bold")
        f_ib = get_font(25, "regular")

        for ih, ib in s["items"]:
            draw.rectangle((126, box_y, W - 88, box_y + 126), fill=CARBON_SOFT, outline=(68, 62, 48), width=1)
            draw.text((152, box_y + 18), ih, font=f_ih, fill=DORADO)
            ib_lines = wrap_text(draw, ib, f_ib, W - 266)
            draw_multiline(draw, ib_lines, 152, box_y + 50, f_ib, BLANCO, line_spacing=6)
            box_y += 142

        # Bottom solid gold bar inside safe zone (y <= 1130)
        cta_y = 1054
        draw.rectangle((126, cta_y, W - 88, cta_y + 76), fill=DORADO)
        f_cta = get_font(23, "bold")
        draw.text((152, cta_y + 24), s["cta"], font=f_cta, fill=CARBON)

        out_path = OUT_DIR / s["out"]
        canvas.save(out_path, "JPEG", quality=94)
        print("Saved Pub 3 (SIN IA Carbón):", out_path.name)


if __name__ == "__main__":
    render_pub1_con_ia()
    render_pub2_sin_ia_piedra()
    render_pub3_sin_ia_carbon()
