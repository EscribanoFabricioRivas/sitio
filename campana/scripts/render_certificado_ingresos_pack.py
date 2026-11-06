#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Pack Estratégico: Certificado Notarial de Ingresos (Migraciones, Independientes y Bancos)
Incluye AMBAS líneas de diseño aprobadas:
1. Línea CON IA (Editorial Arquitectónico 4:5 Carrusel + Reel 9:16 MP4 con tecleo y música):
   - Enfocada en Residencia Legal ante Migraciones + puente hacia radicación/inversión en Punta del Este.
2. Línea SIN IA (Placas Técnicas Tipográficas XXL en Piedra #e9e7e1 y Carbón #111111, 1080x1350):
   - Pieza Técnica A (Piedra): Certificado de ingresos para trabajadores independientes, profesionales y SAS.
   - Pieza Técnica B (Carbón): Certificado de ingresos para apertura de cuenta bancaria y garantía de alquiler.
3. Formato Especial Google Maps / Google Business Profile (700x700):
   - Listo para subir a la ficha de Google Maps que hoy tracciona las consultas directas.
"""

import os
from PIL import Image, ImageDraw
from render_weekly_pack import (
    FONDOS_DIR,
    get_font,
    load_cropped_logo,
    draw_tracked_text,
    render_feed_piece,
    render_vertical_piece,
)
from render_maldonado_express_pack import (
    C_CARBON,
    C_GOLD,
    C_GOLD_LIGHT,
    C_PEARL,
    C_WHITE,
    MUSIC_DIR,
    OUT_MAIN,
    make_architectural_continuation_bg,
    wrap_lines,
    save_multi,
    copy_editorial_to_all,
    render_editorial_carousel_card,
    render_vertical_editorial_slide,
    build_reel_mp4_with_typewriter_and_music,
    draw_dynamic_pill,
)
from render_technical_graphics import render_step_card_xxl


def render_gbp_ingresos_700x700(base_name, bg_path):
    """Genera pieza 700x700 cuadrada oficial para Google Business Profile / Google Maps."""
    W, H = 700, 700
    canvas = make_architectural_continuation_bg(bg_path, W, H, variant=1)
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.rounded_rectangle(
        [(36, 36), (664, 664)],
        radius=22,
        fill=None,
        outline=(196, 173, 122, 130),
        width=2,
    )

    logo = load_cropped_logo(target_height=52)
    canvas.paste(logo, (60, 58), logo)

    f_badge = get_font(15, "demibold")
    draw_dynamic_pill(
        draw,
        x=395,
        y=62,
        text="MIGRACIONES · BANCOS",
        font=f_badge,
        fill_bg=(17, 17, 17, 200),
        outline_col=(196, 173, 122, 160),
        text_col=C_GOLD_LIGHT,
        pad_x=16,
        pad_y=9,
        radius=18,
    )

    f_kicker = get_font(16, "demibold")
    draw_tracked_text(draw, (60, 140), "CERTIFICACIONES · PUNTA DEL ESTE", f_kicker, C_GOLD_LIGHT, tracking=2)

    f_head = get_font(38, "medium")
    y_cur = 172
    for hl in ["Certificado notarial", "de ingresos:", "Migraciones y bancos."]:
        draw.text((60, y_cur), hl, font=f_head, fill=C_WHITE)
        y_cur += 46

    y_cur += 10
    draw.line([(60, y_cur), (140, y_cur)], fill=C_GOLD, width=3)
    y_cur += 16

    f_body = get_font(22, "regular")
    body = "Para residencia legal ante Migraciones, trabajadores independientes, profesionales, empresas, cuentas bancarias y garantías de alquiler."
    for bl in wrap_lines(draw, body, f_body, 575):
        draw.text((60, y_cur), bl, font=f_body, fill=C_PEARL)
        y_cur += 30

    box_y1 = 448
    box_y2 = 548
    draw.rounded_rectangle(
        [(60, box_y1), (640, box_y2)],
        radius=16,
        fill=(26, 24, 20, 225),
        outline=(196, 173, 122, 160),
        width=2,
    )
    draw.rounded_rectangle([(60, box_y1), (68, box_y2)], radius=4, fill=C_GOLD)
    f_box_lbl = get_font(15, "demibold")
    draw_tracked_text(draw, (84, box_y1 + 14), "PRESUPUESTO Y REQUISITOS POR WHATSAPP", f_box_lbl, C_GOLD_LIGHT, tracking=2)
    f_box_txt = get_font(20, "medium")
    draw.text((84, box_y1 + 42), "Escríbenos al +598 99 431 185 indicando", font=f_box_txt, fill=C_WHITE)
    draw.text((84, box_y1 + 68), "para qué organismo o trámite lo necesitas.", font=f_box_txt, fill=C_PEARL)

    y_foot = 582
    draw.line([(60, y_foot - 12), (460, y_foot - 12)], fill=(196, 173, 122, 95), width=1)
    f_f1 = get_font(22, "medium")
    f_f2 = get_font(18, "regular")
    draw.text((60, y_foot), "Fabricio Rivas | Escribano Público", font=f_f1, fill=C_WHITE)
    draw.text((60, y_foot + 28), "Punta del Este · Maldonado · Matrícula 17058/5", font=f_f2, fill=C_GOLD_LIGHT)

    return save_multi(canvas, base_name)


def main():
    bg1 = os.path.join(FONDOS_DIR, "bg1.jpg")
    bg4 = os.path.join(FONDOS_DIR, "bg4.jpg")

    # =========================================================================
    # PIEZA 1 (CON IA · EDITORIAL ARQUITECTÓNICO): RESIDENCIA / MIGRACIONES
    # =========================================================================
    ing_ed_feed = os.path.join(OUT_MAIN, "ingresos_con_ia_01_1080x1350")
    render_feed_piece(
        bg_path=bg1,
        out_base_path=ing_ed_feed,
        kicker="RESIDENCIA Y TRÁMITES · PUNTA DEL ESTE",
        headline_lines=[
            "Certificado notarial",
            "de ingresos para",
            "Migraciones y bancos",
        ],
        subtitle_lines=[
            "Si tramitas tu residencia legal en Uruguay,",
            "eres trabajador independiente o abres cuenta",
            "bancaria en Maldonado, acreditamos tus ingresos",
            "conforme a la pauta de cada institución.",
        ],
        badge_number="01 / 03",
    )
    copy_editorial_to_all("ingresos_con_ia_01_1080x1350", ing_ed_feed)

    render_editorial_carousel_card(
        base_name="ingresos_con_ia_02_1080x1350",
        bg_path=bg1,
        variant=1,
        badge_text="02 / 03",
        step_num="01",
        kicker="DIRECCIÓN NACIONAL DE MIGRACIÓN",
        headline_lines=["Acreditar medios de", "vida lícitos en Uruguay"],
        body_text=(
            "Para residentes del Mercosur y del exterior que se radican en Punta del Este "
            "y perciben ingresos independientes, rentas, dividendos o trabajo remoto."
        ),
        takeaway_label="PUENTE PATRIMONIAL EN URUGUAY",
        takeaway_text="Acompañamos también tu apertura bancaria, contrato de alquiler anual o compra de propiedad.",
    )

    render_editorial_carousel_card(
        base_name="ingresos_con_ia_03_1080x1350",
        bg_path=bg4,
        variant=2,
        badge_text="03 / 03",
        step_num="02",
        kicker="QUÉ ENVIAR POR WHATSAPP",
        headline_lines=["Revisión previa antes", "de venir a firmar"],
        body_text=(
            "1. Organismo o entidad que te pide el certificado.\n"
            "2. Tu actividad (independiente, empresa, rentas o exterior).\n"
            "3. Documento de identidad o pasaporte vigente."
        ),
        takeaway_label="CONSULTA Y PRESUPUESTO",
        takeaway_text="WhatsApp +598 99 431 185 · Atención directa, también a distancia si estás en otro país.",
    )

    # Reel 9:16 MP4 con música y typewriter para Pieza 1
    ing_ed_vert = os.path.join(OUT_MAIN, "ingresos_editorial_story_1080x1920")
    render_vertical_piece(
        bg_path=bg1,
        out_base_path=ing_ed_vert,
        kicker="RESIDENCIA · INDEPENDIENTES · BANCOS",
        headline_lines=[
            "Certificado notarial",
            "de ingresos en",
            "Punta del Este",
        ],
        subtitle_lines=[
            "Para trámites de residencia ante Migraciones,",
            "trabajadores independientes, apertura de cuentas",
            "bancarias y garantías de alquiler en Maldonado.",
            "Revisamos tus recaudos por WhatsApp.",
        ],
        cta_pill_text="Consulta al +598 99 431 185",
    )
    copy_editorial_to_all("ingresos_editorial_story_1080x1920", ing_ed_vert)

    s2_spec = render_vertical_editorial_slide(
        base_name="ingresos_reel_slide2_1080x1920",
        bg_path=bg1,
        variant=1,
        badge_text="MIGRACIONES Y BANCOS",
        step_num="01",
        kicker="TRES CASOS FRECUENTES",
        headline_lines=["Cuándo te piden un", "certificado de ingresos"],
        body_text="1. Residencia legal ante Migraciones.\n2. Trabajadores independientes, unipersonales y SAS.\n3. Bancos y garantías de alquiler.",
        box_label="REVISIÓN DOCUMENTAL PREVIA",
        box_full_text="Verificamos la pauta exacta del organismo antes de emitir el certificado para evitar observaciones.",
        cta_text="WhatsApp +598 99 431 185 · Punta del Este",
    )

    s3_spec = render_vertical_editorial_slide(
        base_name="ingresos_reel_slide3_1080x1920",
        bg_path=bg4,
        variant=2,
        badge_text="PASO A PASO",
        step_num="02",
        kicker="CÓMO COORDINAR HOY",
        headline_lines=["Envía tu consulta", "por WhatsApp"],
        body_text="Indícanos para qué institución necesitas el certificado y cuál es tu actividad para pasarte requisitos y presupuesto.",
        box_label="ATENCIÓN DIRECTA",
        box_full_text="Coordinas el retiro en Punta del Este con toda la documentación revisada de antemano.",
        cta_text="Guía completa en escribanofabriciorivas.com",
    )

    music_path = os.path.join(MUSIC_DIR, "v4_cafe_del_mar_rhodes_sax_con_locucion.mp3")
    build_reel_mp4_with_typewriter_and_music(
        slide1_jpg_path=os.path.join(OUT_MAIN, "ingresos_editorial_story_1080x1920.jpg"),
        slide2_spec=s2_spec,
        slide3_spec=s3_spec,
        out_mp4_name="reel_07_certificado_ingresos_migraciones_1080x1920.mp4",
        music_mp3_path=music_path,
    )

    # =========================================================================
    # PIEZA 2 (SIN IA · TÉCNICA XXL PIEDRA #e9e7e1): TRABAJADORES INDEPENDIENTES
    # =========================================================================
    render_step_card_xxl(
        filename_base="tecnica_05_certificado_ingresos_independientes_1080x1350",
        dark_mode=False,
        badge_text="INDEPENDIENTES",
        step_num="01",
        kicker="Profesionales y empresas",
        headline_lines=[
            "Certificado de ingresos",
            "para independientes.",
        ],
        body_text="Si tienes unipersonal, eres profesional independiente o socio de una SAS, acreditamos tus ingresos ante bancos, garantías u organismos.",
        takeaway_label="QUÉ ENVIAR POR WHATSAPP:",
        takeaway_text="Indica qué entidad lo pide y tu giro en BPS/DGI.",
    )

    # =========================================================================
    # PIEZA 3 (SIN IA · TÉCNICA XXL CARBÓN #111111): MIGRACIONES Y BANCOS
    # =========================================================================
    render_step_card_xxl(
        filename_base="tecnica_06_certificado_ingresos_migraciones_1080x1350",
        dark_mode=True,
        badge_text="MIGRACIONES",
        step_num="UY",
        kicker="Residencia legal y bancos",
        headline_lines=[
            "Medios de vida para",
            "residencia en Uruguay.",
        ],
        body_text="Emitimos el certificado notarial de ingresos exigido por Dirección Nacional de Migración y bancos en Punta del Este y Maldonado.",
        takeaway_label="ATENCIÓN DIRECTA:",
        takeaway_text="Revisión previa al +598 99 431 185.",
    )

    # =========================================================================
    # FORMATO GOOGLE MAPS / GBP 700x700
    # =========================================================================
    render_gbp_ingresos_700x700("ingresos_gbp_700x700", bg1)

    print("✅ Pack Certificado de Ingresos (CON IA + SIN IA + Reel MP4 + GBP 700x700) generado con éxito.")


if __name__ == "__main__":
    main()
