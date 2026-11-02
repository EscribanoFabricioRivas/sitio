#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Pack Inmediato Pre-Grabación (3 Días de Disparo Ya — Maldonado Ciudad)
Combina el Esquema Actual de Fabricio Rivas:
- Motor A (CON IA): Fotografía arquitectónica de Maldonado/Punta del Este con velo carbón izquierdo y tipografía Avenir Next.
- Motor B (SIN IA - Técnico XXL): Placas e infografías de alto impacto (Carbón #111111, Piedra #e9e7e1, Dorado #c4ad7a) con cuerpo 41-62px.
- Motor C (Video Reels .mp4 1080x1920 con música institucional vía ffmpeg): Para publicar ya mientras Fabricio graba en 3 días.
"""

import os
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

from render_weekly_pack import (
    FONDOS_DIR,
    render_feed_piece,
    render_vertical_piece,
)
from render_technical_graphics import (
    C_CARBON,
    C_DARK_CARD,
    C_TEXT_DARK,
    C_GOLD,
    C_GOLD_LIGHT,
    C_GOLD_DARK,
    C_SAND_BG,
    C_STONE_BG,
    C_WHITE,
    get_font,
    wrap_lines,
    draw_header_xxl,
    draw_footer_xxl,
    load_logo,
)

MAIN_SITIO = "/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio"
WORKTREE_SITIO = "/Users/arianawajntraub/.gemini/antigravity/worktrees/elegant-bardeen/teamwork_preview_workflow_automation/sitio"
GDRIVE_PACK_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/FR pp AG/pack_maldonado_en_el_dia"
ARTIFACT_DIR = "/Users/arianawajntraub/.gemini/antigravity/brain/8a79030b-f9ee-4ee1-9458-051b87c1cead"

OUT_MAIN = os.path.join(MAIN_SITIO, "campana", "pack_maldonado_en_el_dia")
OUT_WORKTREE = os.path.join(WORKTREE_SITIO, "campana", "pack_maldonado_en_el_dia")

for d in [OUT_MAIN, OUT_WORKTREE, GDRIVE_PACK_DIR]:
    os.makedirs(d, exist_ok=True)


def save_multi(canvas, base_name):
    rgb = canvas.convert("RGB")
    for folder in [OUT_MAIN, OUT_WORKTREE, GDRIVE_PACK_DIR]:
        rgb.save(os.path.join(folder, f"{base_name}.jpg"), "JPEG", quality=90, optimize=True)
        rgb.save(os.path.join(folder, f"{base_name}.png"), "PNG", optimize=True)
    rgb.save(os.path.join(ARTIFACT_DIR, f"{base_name}.jpg"), "JPEG", quality=90, optimize=True)
    return os.path.join(OUT_MAIN, f"{base_name}.jpg")


def render_xxl_card_multi(
    base_name,
    dark_mode,
    badge_text,
    step_num,
    kicker,
    headline_lines,
    body_text,
    takeaway_label,
    takeaway_text,
):
    W, H = 1080, 1350
    bg_color = C_CARBON if dark_mode else C_STONE_BG
    canvas = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(canvas)

    draw_header_xxl(canvas, draw, dark_mode=dark_mode, badge_text=badge_text)

    card_bg = C_DARK_CARD if dark_mode else C_WHITE
    card_border = C_GOLD
    draw.rounded_rectangle([(76, 280), (1004, 1025)], radius=34, fill=card_bg, outline=card_border, width=3)

    pill_w = max(135, len(step_num) * 34 + 44)
    draw.rounded_rectangle([(120, 325), (120 + pill_w, 415)], radius=22, fill=C_GOLD)
    f_num = get_font(44, "bold")
    bbox = draw.textbbox((0, 0), step_num, font=f_num)
    nw = bbox[2] - bbox[0]
    draw.text((120 + (pill_w - nw) // 2, 342), step_num, font=f_num, fill=C_CARBON)

    f_kicker = get_font(26, "demibold")
    k_col = C_GOLD_LIGHT if dark_mode else C_GOLD_DARK
    draw.text((120 + pill_w + 26, 354), kicker.upper(), font=f_kicker, fill=k_col)

    y_cur = 445
    f_head = get_font(58, "bold")
    head_col = C_WHITE if dark_mode else C_CARBON
    for hl in headline_lines:
        draw.text((120, y_cur), hl, font=f_head, fill=head_col)
        y_cur += 70

    y_cur += 18
    f_body = get_font(40, "regular")
    body_col = C_SAND_BG if dark_mode else C_TEXT_DARK
    for bl in wrap_lines(draw, body_text, f_body, 830):
        draw.text((120, y_cur), bl, font=f_body, fill=body_col)
        y_cur += 52

    box_y1, box_y2 = 845, 990
    box_fill = (44, 39, 26) if dark_mode else (244, 240, 230)
    draw.rounded_rectangle([(116, box_y1), (964, box_y2)], radius=22, fill=box_fill, outline=C_GOLD, width=2)
    f_tk_label = get_font(26, "bold")
    f_tk_text = get_font(32, "medium")
    tk_col = C_GOLD_LIGHT if dark_mode else C_GOLD_DARK
    draw.text((146, box_y1 + 22), takeaway_label.upper(), font=f_tk_label, fill=tk_col)
    draw.text((146, box_y1 + 66), takeaway_text, font=f_tk_text, fill=head_col)

    draw_footer_xxl(draw, dark_mode=dark_mode)
    return save_multi(canvas, base_name)


def render_vertical_xxl_slide(
    base_name,
    dark_mode,
    badge_text,
    step_num,
    kicker,
    headline_lines,
    body_text,
    cta_text="WhatsApp +598 99 431 185 · ARTOWER Punta del Este",
):
    """Renderiza slide 1080x1920 SIN IA (Técnico XXL) con zona segura estricta (y=310..1410)."""
    W, H = 1080, 1920
    bg_color = C_CARBON if dark_mode else C_STONE_BG
    canvas = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(canvas)

    logo = load_logo(height=92)
    if not dark_mode:
        draw.rounded_rectangle([(84, 315), (206, 420)], radius=22, fill=C_CARBON)
        canvas.paste(logo, (98, 322), logo)
    else:
        canvas.paste(logo, (84, 320), logo)

    f_badge = get_font(28, "demibold")
    bbox = draw.textbbox((0, 0), badge_text, font=f_badge)
    tw = bbox[2] - bbox[0] + 54
    bg_col = (34, 34, 34) if dark_mode else C_CARBON
    draw.rounded_rectangle([(996 - tw, 332), (996, 398)], radius=32, fill=bg_col, outline=C_GOLD, width=2)
    draw.text((996 - tw + 27, 346), badge_text, font=f_badge, fill=C_GOLD_LIGHT)

    card_bg = C_DARK_CARD if dark_mode else C_WHITE
    draw.rounded_rectangle([(76, 455), (1004, 1265)], radius=36, fill=card_bg, outline=C_GOLD, width=3)

    pill_w = max(140, len(step_num) * 34 + 48)
    draw.rounded_rectangle([(120, 510), (120 + pill_w, 600)], radius=22, fill=C_GOLD)
    f_num = get_font(44, "bold")
    nb = draw.textbbox((0, 0), step_num, font=f_num)
    draw.text((120 + (pill_w - (nb[2] - nb[0])) // 2, 527), step_num, font=f_num, fill=C_CARBON)

    f_kicker = get_font(27, "demibold")
    k_col = C_GOLD_LIGHT if dark_mode else C_GOLD_DARK
    draw.text((120 + pill_w + 26, 540), kicker.upper(), font=f_kicker, fill=k_col)

    y_cur = 640
    f_head = get_font(62, "bold")
    head_col = C_WHITE if dark_mode else C_CARBON
    for hl in headline_lines:
        draw.text((120, y_cur), hl, font=f_head, fill=head_col)
        y_cur += 74

    y_cur += 24
    f_body = get_font(42, "regular")
    body_col = C_SAND_BG if dark_mode else C_TEXT_DARK
    for bl in wrap_lines(draw, body_text, f_body, 830):
        draw.text((120, y_cur), bl, font=f_body, fill=body_col)
        y_cur += 56

    box_y1, box_y2 = 1090, 1215
    box_fill = (44, 39, 26) if dark_mode else (244, 240, 230)
    draw.rounded_rectangle([(116, box_y1), (964, box_y2)], radius=22, fill=box_fill, outline=C_GOLD, width=2)
    f_cta = get_font(32, "demibold")
    draw.text((146, box_y1 + 42), cta_text, font=f_cta, fill=head_col)

    # Firma en zona segura vertical (y=1310..1405)
    y_foot = 1315
    line_col = (196, 173, 122, 120) if dark_mode else (17, 17, 17, 60)
    draw.line([(84, y_foot - 20), (996, y_foot - 20)], fill=line_col, width=3)
    f_name = get_font(36, "demibold")
    f_sub = get_font(29, "medium")
    c1 = C_WHITE if dark_mode else C_CARBON
    c2 = C_GOLD_LIGHT if dark_mode else C_GOLD_DARK
    draw.text((84, y_foot), "Fabricio Rivas | Escribano Público · Mat. 17058/5", font=f_name, fill=c1)
    draw.text((84, y_foot + 48), "Atención directa en Punta del Este y Maldonado", font=f_sub, fill=c2)

    return save_multi(canvas, base_name)


def copy_editorial_to_all(base_name, src_prefix):
    for ext in [".jpg", ".png"]:
        src = src_prefix + ext
        if os.path.exists(src):
            img = Image.open(src)
            for folder in [OUT_MAIN, OUT_WORKTREE, GDRIVE_PACK_DIR]:
                img.save(os.path.join(folder, base_name + ext))
            if ext == ".jpg":
                img.save(os.path.join(ARTIFACT_DIR, base_name + ext))


def build_reel_mp4_with_music(slide_paths, out_mp4_name, seconds_per_slide=4.0):
    """
    Crea un Reel .mp4 1080x1920 a 30fps uniendo las placas verticales con zoom suave
    y una pista de audio ambiental institucional generada con sintesis armónica limpia en ffmpeg.
    """
    total_dur = len(slide_paths) * seconds_per_slide
    out_main_mp4 = os.path.join(OUT_MAIN, out_mp4_name)

    inputs = []
    filter_parts = []
    for i, sp in enumerate(slide_paths):
        inputs.extend(["-loop", "1", "-t", str(seconds_per_slide), "-i", sp])
        filter_parts.append(
            f"[{i}:v]scale=1080:1920,format=yuv420p,fade=t=in:st=0:d=0.35,fade=t=out:st={seconds_per_slide-0.35}:d=0.35[v{i}]"
        )

    concat_v = "".join(f"[v{i}]" for i in range(len(slide_paths))) + f"concat=n={len(slide_paths)}:v=1:a=0[vout]"
    # Audio institucional sobrio (acorde cálido Do Mayor 7 suave, volumen discreto -18dB con fade in/out)
    audio_filter = (
        f"aevalsrc='0.045*sin(2*PI*261.63*t)+0.035*sin(2*PI*329.63*t)+0.03*sin(2*PI*392.00*t)+0.02*sin(2*PI*493.88*t)':s=44100:d={total_dur},"
        f"afade=t=in:st=0:d=1.2,afade=t=out:st={total_dur-1.5}:d=1.5[aout]"
    )
    full_filter = ";".join(filter_parts + [concat_v, audio_filter])

    cmd = [
        FFMPEG_BIN, "-y",
        *inputs,
        "-filter_complex", full_filter,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        out_main_mp4,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for folder in [OUT_WORKTREE, GDRIVE_PACK_DIR, ARTIFACT_DIR]:
        dst = os.path.join(folder, out_mp4_name)
        if os.path.abspath(out_main_mp4) != os.path.abspath(dst):
            with open(out_main_mp4, "rb") as fsrc, open(dst, "wb") as fdst:
                fdst.write(fsrc.read())
    return out_main_mp4


def main():
    bg1 = os.path.join(FONDOS_DIR, "bg1.jpg")
    bg2 = os.path.join(FONDOS_DIR, "bg2.jpg")
    bg3 = os.path.join(FONDOS_DIR, "bg3.jpg")
    bg4 = os.path.join(FONDOS_DIR, "bg4.jpg")

    # =========================================================================
    # PACK 1 (DÍA 1): DECRETO 4118 IDM — REGULARIZACIÓN DE OBRAS EN MALDONADO
    # =========================================================================
    # 1A. Placa Editorial CON IA (1080x1350 + 1080x1920)
    p1_ed_feed = os.path.join(OUT_MAIN, "pack1_decreto4118_editorial_feed_1080x1350")
    render_feed_piece(
        bg_path=bg2,
        out_base_path=p1_ed_feed,
        kicker="DECRETO 4118/2026 · INTENDENCIA DE MALDONADO",
        headline_lines=[
            "¿Ampliaste tu casa",
            "o parrillero en",
            "Maldonado sin plano?",
        ],
        subtitle_lines=[
            "La Intendencia abrió por 18 meses el plan que",
            "suspende el impuesto a la edificación inapropiada.",
            "Preparamos en 24 h el certificado notarial",
            "de legitimación obligatorio para tu carpeta.",
        ],
        badge_number=None,
    )
    copy_editorial_to_all("pack1_decreto4118_editorial_feed_1080x1350", p1_ed_feed)

    p1_ed_vert = os.path.join(OUT_MAIN, "pack1_decreto4118_editorial_story_1080x1920")
    render_vertical_piece(
        bg_path=bg2,
        out_base_path=p1_ed_vert,
        kicker="DECRETO 4118/2026 · MALDONADO CIUDAD",
        headline_lines=[
            "Regularización de",
            "obras sin permiso",
            "en Maldonado.",
        ],
        subtitle_lines=[
            "Aplica a obras y ampliaciones hechas",
            "hasta el 31 de diciembre de 2025.",
            "Requisito artículo 3 IDM: certificado",
            "notarial de legitimación en el día.",
        ],
        cta_pill_text="Envía tu padrón al +598 99 431 185",
    )
    copy_editorial_to_all("pack1_decreto4118_editorial_story_1080x1920", p1_ed_vert)

    # 1B. Carrusel Técnico XXL SIN IA (4 placas 1080x1350)
    render_xxl_card_multi(
        base_name="pack1_carrusel_01_1080x1350",
        dark_mode=True,
        badge_text="01 / 04",
        step_num="01",
        kicker="Decreto 4118/2026 IDM",
        headline_lines=["¿Qué obras entran en el", "plan de Maldonado?"],
        body_text="Construcciones, parrilleros techados, cocheras o ampliaciones hechas sin permiso municipal hasta el 31 de diciembre de 2025 en todo el departamento.",
        takeaway_label="Beneficio directo",
        takeaway_text="Suspende el impuesto a la edificación inapropiada.",
    )
    render_xxl_card_multi(
        base_name="pack1_carrusel_02_1080x1350",
        dark_mode=False,
        badge_text="02 / 04",
        step_num="02",
        kicker="Requisito artículo 3 IDM",
        headline_lines=["El documento obligatorio", "para abrir la carpeta"],
        body_text="Para iniciar el trámite, la Intendencia exige un certificado notarial de legitimación que acredite tu calidad de propietario, promitente comprador o heredero.",
        takeaway_label="En propiedad horizontal",
        takeaway_text="Se suma el certificado de anuencia de copropiedad.",
    )
    render_xxl_card_multi(
        base_name="pack1_carrusel_03_1080x1350",
        dark_mode=True,
        badge_text="03 / 04",
        step_num="03",
        kicker="Por qué regularizar hoy",
        headline_lines=["Deja tu padrón apto", "para banco y venta"],
        body_text="Un padrón con metros sin declarar frena créditos hipotecarios y baja el precio de venta. El régimen extraordinario dura solo 18 meses.",
        takeaway_label="Criterio notarial",
        takeaway_text="Aun con sucesión en trámite puedes legitimar el inicio.",
    )
    render_xxl_card_multi(
        base_name="pack1_carrusel_04_1080x1350",
        dark_mode=False,
        badge_text="04 / 04",
        step_num="04",
        kicker="Resolución en 24 horas",
        headline_lines=["Cómo lo resolvemos", "sin demoras en el estudio"],
        body_text="Nos envías por WhatsApp tu número de padrón y cédula. Verificamos la titulación registral y emitimos el certificado listo para tu arquitecto.",
        takeaway_label="Contacto directo",
        takeaway_text="WhatsApp +598 99 431 185 · ARTOWER Punta del Este",
    )

    # Slides verticales para el Reel MP4 del Pack 1
    s1_v1 = p1_ed_vert + ".jpg"
    s1_v2 = render_vertical_xxl_slide(
        "pack1_reel_slide2_1080x1920", True, "PASO 1 · DECRETO 4118", "01", "Obras hasta 31/12/2025",
        ["Frena el impuesto a la", "edificación inapropiada"],
        "Si ampliaste tu vivienda o cerraste un parrillero en Maldonado sin permiso, tienes 18 meses para regularizar con exoneración de tasas.",
    )
    s1_v3 = render_vertical_xxl_slide(
        "pack1_reel_slide3_1080x1920", False, "PASO 2 · REQUISITO IDM", "02", "Artículo 3 reglamentación",
        ["Certificado notarial", "de legitimación en 24 h"],
        "Acreditamos tu titularidad como propietario, promitente comprador o heredero para que tu arquitecto ingrese la carpeta sin trabas.",
    )
    build_reel_mp4_with_music([s1_v1, s1_v2, s1_v3], "reel_01_decreto4118_maldonado_1080x1920.mp4")

    # =========================================================================
    # PACK 2 (DÍA 2): AUTOMOTORES MALDONADO — RADARES 45 KM/H Y DESVINCULACIÓN
    # =========================================================================
    p2_ed_feed = os.path.join(OUT_MAIN, "pack2_automotores_editorial_feed_1080x1350")
    render_feed_piece(
        bg_path=bg1,
        out_base_path=p2_ed_feed,
        kicker="VEHÍCULOS Y RADARES EN MALDONADO · SUCIVE / IDM",
        headline_lines=[
            "¿Vendiste tu auto",
            "de palabra y te caen",
            "multas de radar?",
        ],
        subtitle_lines=[
            "Con los radares de 45 km/h en Maldonado, entregar",
            "un vehículo sin firma certificada compromete tu cédula.",
            "Resolvemos desvinculaciones, compraventas",
            "y cartas poder automotor en el día.",
        ],
        badge_number=None,
    )
    copy_editorial_to_all("pack2_automotores_editorial_feed_1080x1350", p2_ed_feed)

    p2_ed_vert = os.path.join(OUT_MAIN, "pack2_automotores_editorial_story_1080x1920")
    render_vertical_piece(
        bg_path=bg1,
        out_base_path=p2_ed_vert,
        kicker="TRÁMITE AUTOMOTOR EN EL DÍA · MALDONADO",
        headline_lines=[
            "No entregues las llaves",
            "sin desvincular tu",
            "responsabilidad.",
        ],
        subtitle_lines=[
            "1. Declaración jurada de desvinculación IDM.",
            "2. Compraventa con firma certificada en 15 min.",
            "3. Carta poder para reempadronar en el Campus.",
        ],
        cta_pill_text="Agenda en el día: +598 99 431 185",
    )
    copy_editorial_to_all("pack2_automotores_editorial_story_1080x1920", p2_ed_vert)

    render_xxl_card_multi(
        base_name="pack2_carrusel_01_1080x1350",
        dark_mode=True,
        badge_text="CASO 1",
        step_num="01",
        kicker="Ya entregaste el vehículo",
        headline_lines=["Declaración jurada de", "desvinculación vehicular"],
        body_text="Si vendiste un auto o una moto hace tiempo sin transferir y siguen llegando multas o patente a tu nombre, instrumentamos la declaración jurada notarial ante la IDM.",
        takeaway_label="Efecto inmediato",
        takeaway_text="Corta la generación futura de deuda sobre tu cédula.",
    )
    render_xxl_card_multi(
        base_name="pack2_carrusel_02_1080x1350",
        dark_mode=False,
        badge_text="CASO 2",
        step_num="02",
        kicker="Vas a vender o comprar hoy",
        headline_lines=["Entrega segura en", "15 minutos en el estudio"],
        body_text="Nos envías foto de libreta y cédulas por WhatsApp. Cuando llegan comprador y vendedor al estudio, el documento ya está redactado y listo para firmar.",
        takeaway_label="Seguridad jurídica",
        takeaway_text="Deslindas responsabilidad civil, penal y municipal desde esa hora.",
    )

    s2_v1 = p2_ed_vert + ".jpg"
    s2_v2 = render_vertical_xxl_slide(
        "pack2_reel_slide2_1080x1920", True, "RADARES EN MALDONADO", "01", "Desvinculación IDM / SUCIVE",
        ["¿Siguen llegando multas", "de un auto que ya vendiste?"],
        "Confeccionamos en el día la declaración jurada notarial con firma certificada para desvincular tu cédula en la Intendencia de Maldonado.",
    )
    s2_v3 = render_vertical_xxl_slide(
        "pack2_reel_slide3_1080x1920", False, "FIRMA EN 15 MINUTOS", "02", "Compraventa y Carta Poder",
        ["Envías libreta y cédulas", "por WhatsApp y pasas a firmar"],
        "Preparamos tu transferencia, compromiso o carta poder para reempadronar en el Campus antes de que llegues a la oficina.",
    )
    build_reel_mp4_with_music([s2_v1, s2_v2, s2_v3], "reel_02_automotores_maldonado_1080x1920.mp4")

    # =========================================================================
    # PACK 3 (DÍA 3): ALQUILERES LUC EN 24 H + PERMISO DE MENOR EN 10 MINUTOS
    # =========================================================================
    p3_ed_feed = os.path.join(OUT_MAIN, "pack3_alquiler_permiso_editorial_feed_1080x1350")
    render_feed_piece(
        bg_path=bg4,
        out_base_path=p3_ed_feed,
        kicker="GESTIONES EN EL DÍA · MALDONADO Y PUNTA DEL ESTE",
        headline_lines=[
            "Contratos de alquiler",
            "por LUC y permisos de",
            "menor sin esperas.",
        ],
        subtitle_lines=[
            "Enviando la documentación por WhatsApp a la mañana,",
            "redactamos el documento antes de tu visita para que",
            "pases por ARTOWER únicamente 10 minutos a firmar.",
        ],
        badge_number=None,
    )
    copy_editorial_to_all("pack3_alquiler_permiso_editorial_feed_1080x1350", p3_ed_feed)

    p3_ed_vert = os.path.join(OUT_MAIN, "pack3_alquiler_permiso_editorial_story_1080x1920")
    render_vertical_piece(
        bg_path=bg4,
        out_base_path=p3_ed_vert,
        kicker="TRÁMITES EXPRESS · MALDONADO CIUDAD",
        headline_lines=[
            "Envías por WhatsApp,",
            "pasas solo 10 minutos",
            "a firmar.",
        ],
        subtitle_lines=[
            "• Alquiler anual por LUC (Ley 19.889) o temporada.",
            "• Permiso de menor para viajes al exterior.",
            "• Cartas poder para BPS, DGI, bancos e IDM.",
        ],
        cta_pill_text="WhatsApp +598 99 431 185",
    )
    copy_editorial_to_all("pack3_alquiler_permiso_editorial_story_1080x1920", p3_ed_vert)

    render_xxl_card_multi(
        base_name="pack3_placa_luc_1080x1350",
        dark_mode=True,
        badge_text="ALQUILER LUC",
        step_num="LUC",
        kicker="Ley 19.889 · Alquiler sin garantía",
        headline_lines=["Por qué un contrato de", "internet no te protege"],
        body_text="Para que rija el desalojo abreviado de la LUC en un alquiler sin garantía en Maldonado, la ley exige cláusulas expresas y certificación notarial de firmas.",
        takeaway_label="Resolución en 24 horas",
        takeaway_text="Contrato blindado + inventario certificado en el día.",
    )
    render_xxl_card_multi(
        base_name="pack3_placa_permiso_menor_1080x1350",
        dark_mode=False,
        badge_text="EN EL DÍA",
        step_num="10'",
        kicker="Viajes de fin de año y vacaciones",
        headline_lines=["Permiso de menor listo", "con 1 mensaje de WhatsApp"],
        body_text="Nos envías foto de las cédulas de los padres, del menor y partida de nacimiento. Cuando pasas por el estudio, el permiso ya está impreso para firmar.",
        takeaway_label="Cero fila de espera",
        takeaway_text="WhatsApp +598 99 431 185 · ARTOWER Punta del Este",
    )

    s3_v1 = p3_ed_vert + ".jpg"
    s3_v2 = render_vertical_xxl_slide(
        "pack3_reel_slide2_1080x1920", True, "ALQUILERES EN MALDONADO", "LUC", "Ley 19.889 e Inventario",
        ["Alquila con plazos de", "desalojo abreviado reales"],
        "No uses un borrador genérico de internet: redactamos y certificamos tu contrato de alquiler anual o de temporada en 24 horas.",
    )
    s3_v3 = render_vertical_xxl_slide(
        "pack3_reel_slide3_1080x1920", False, "PERMISO DE MENOR", "10'", "Trámite sin espera",
        ["Envías las cédulas por", "WhatsApp y pasas a firmar"],
        "Permisos de menor para viajar, cartas poder para bancos, BPS, DGI y certificaciones de firma en el día en Punta del Este y Maldonado.",
    )
    build_reel_mp4_with_music([s3_v1, s3_v2, s3_v3], "reel_03_alquiler_luc_y_permiso_menor_1080x1920.mp4")
    print("✅ PACK MALDONADO EN EL DÍA GENERADO COMPLETO (CON IA + SIN IA XXL + 3 REELS MP4)")


if __name__ == "__main__":
    main()
