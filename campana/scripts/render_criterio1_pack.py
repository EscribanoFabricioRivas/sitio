#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Pack Semanal Criterio Notarial #1 (26/10 — Publicada el 06/11):
'¿Certificación de firma o certificado notarial? Cuál te están pidiendo (BPS y DGI)'
Genera:
1. Carrusel 5 láminas 1080x1350 (4:5)
2. Reel MP4 1080x1920 (9:16) con tecleo en vivo + música Café del Mar Rhodes & Sax
3. Formatos especiales del desplegable del Panel 360:
   - Google Maps / Google Business Profile 700x700 (criterio1_gbp_700x700.jpg)
   - Instagram Story con espacio para Sticker de URL 1080x1920 (criterio1_story_sticker_1080x1920.jpg)
   - Estado de WhatsApp 1080x1920 (criterio1_whatsapp_estado_1080x1920.jpg)
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


def render_gbp_700x700(base_name, bg_path):
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

    f_badge = get_font(16, "demibold")
    draw_dynamic_pill(
        draw,
        x=445,
        y=62,
        text="BPS · DGI · BANCOS",
        font=f_badge,
        fill_bg=(17, 17, 17, 200),
        outline_col=(196, 173, 122, 160),
        text_col=C_GOLD_LIGHT,
        pad_x=18,
        pad_y=9,
        radius=18,
    )

    f_kicker = get_font(16, "demibold")
    draw_tracked_text(draw, (60, 142), "CRITERIO NOTARIAL · PUNTA DEL ESTE", f_kicker, C_GOLD_LIGHT, tracking=2)

    f_head = get_font(38, "medium")
    y_cur = 176
    for hl in ["¿Certificación de firma", "o certificado notarial?", "Cuál te están pidiendo."]:
        draw.text((60, y_cur), hl, font=f_head, fill=C_WHITE)
        y_cur += 46

    y_cur += 10
    draw.line([(60, y_cur), (140, y_cur)], fill=C_GOLD, width=3)
    y_cur += 18

    f_body = get_font(23, "regular")
    body = "Firma certificada: tu firma en un documento ya listo. Certificado notarial: un hecho o dato acreditado por el escribano."
    for bl in wrap_lines(draw, body, f_body, 575):
        draw.text((60, y_cur), bl, font=f_body, fill=C_PEARL)
        y_cur += 31

    # Box inferior
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
    draw_tracked_text(draw, (84, box_y1 + 14), "CONSULTA DIRECTA POR WHATSAPP", f_box_lbl, C_GOLD_LIGHT, tracking=2)
    f_box_txt = get_font(21, "medium")
    draw.text((84, box_y1 + 42), "Envía foto del requisito al +598 99 431 185", font=f_box_txt, fill=C_WHITE)
    draw.text((84, box_y1 + 68), "y te confirmamos qué acto corresponde.", font=f_box_txt, fill=C_PEARL)

    y_foot = 582
    draw.line([(60, y_foot - 12), (460, y_foot - 12)], fill=(196, 173, 122, 95), width=1)
    f_f1 = get_font(22, "medium")
    f_f2 = get_font(18, "regular")
    draw.text((60, y_foot), "Fabricio Rivas | Escribano Público", font=f_f1, fill=C_WHITE)
    draw.text((60, y_foot + 28), "Punta del Este · Maldonado · Matrícula 17058/5", font=f_f2, fill=C_GOLD_LIGHT)

    return save_multi(canvas, base_name)


def main():
    bg3 = os.path.join(FONDOS_DIR, "bg3.jpg")
    bg2 = os.path.join(FONDOS_DIR, "bg2.jpg")

    # 1. Portada 4:5 (Lámina 1 del Carrusel)
    c1_ed_feed = os.path.join(OUT_MAIN, "criterio1_carrusel_01_1080x1350")
    render_feed_piece(
        bg_path=bg3,
        out_base_path=c1_ed_feed,
        kicker="CRITERIO NOTARIAL · BPS, DGI Y BANCOS",
        headline_lines=[
            "¿Certificación de firma",
            "o certificado notarial?",
            "Cuál te están pidiendo",
        ],
        subtitle_lines=[
            "Los nombres se parecen, pero son dos actos distintos.",
            "Uno da fe de tu firma en un texto ya preparado;",
            "el otro acredita un hecho o dato a partir de",
            "documentos o registros.",
        ],
        badge_number="01 / 05",
    )
    copy_editorial_to_all("criterio1_carrusel_01_1080x1350", c1_ed_feed)

    # 2. Láminas 2 a 5 del Carrusel 4:5 (1080x1350)
    render_editorial_carousel_card(
        base_name="criterio1_carrusel_02_1080x1350",
        bg_path=bg3,
        variant=1,
        badge_text="02 / 05",
        step_num="01",
        kicker="CERTIFICACIÓN DE FIRMA",
        headline_lines=["Tu firma puesta en un", "documento que ya existe"],
        body_text=(
            "El escribano identifica a quien firma y certifica la firma puesta "
            "en su presencia sobre un formulario, contrato, autorización o carta poder."
        ),
        takeaway_label="RESOLUCIÓN EN EL DÍA",
        takeaway_text="Con el documento ya redactado y tu documento de identidad vigente, coordinas horario y pasas directo a firmar.",
    )

    render_editorial_carousel_card(
        base_name="criterio1_carrusel_03_1080x1350",
        bg_path=bg3,
        variant=2,
        badge_text="03 / 05",
        step_num="02",
        kicker="CERTIFICADO NOTARIAL",
        headline_lines=["Un hecho o situación", "acreditado por escribano"],
        body_text=(
            "Aquí el documento lo redacta el escribano tras verificar documentos "
            "o registros: quién representa a una empresa, su vigencia o titularidad."
        ),
        takeaway_label="CONTROL PREVIO DE DOCUMENTACIÓN",
        takeaway_text="Conviene enviar antes los antecedentes por WhatsApp para verificar registros y tener el certificado listo.",
    )

    render_editorial_carousel_card(
        base_name="criterio1_carrusel_04_1080x1350",
        bg_path=bg2,
        variant=1,
        badge_text="04 / 05",
        step_num="03",
        kicker="TRÁMITES ANTE BPS Y DGI",
        headline_lines=["Manda siempre el texto", "literal del requisito"],
        body_text=(
            "Según el trámite, BPS o DGI pueden pedirte firma certificada en un formulario, "
            "un certificado de representación o vigencia societaria, o un poder."
        ),
        takeaway_label="QUÉ TENER A MANO ANTES DE VENIR",
        takeaway_text="Foto del requisito del organismo, documento de identidad vigente y, si es por una empresa, sus datos.",
    )

    render_editorial_carousel_card(
        base_name="criterio1_carrusel_05_1080x1350",
        bg_path=bg3,
        variant=2,
        badge_text="05 / 05",
        step_num="04",
        kicker="PROCESO EN 3 PASOS",
        headline_lines=["Cómo lo coordinamos", "por WhatsApp"],
        body_text=(
            "1. Envías foto de lo que te pidieron y para qué trámite es.\n"
            "2. Confirmamos qué acto corresponde y qué documentos llevar.\n"
            "3. Acordamos la firma en Punta del Este o Maldonado."
        ),
        takeaway_label="ATENCIÓN DIRECTA",
        takeaway_text="WhatsApp +598 99 431 185 · Atención directa, también a distancia si estás en otro país, según el acto.",
    )

    # 3. Portada 9:16 (Story / Reel Portada / Estado WhatsApp)
    c1_ed_vert = os.path.join(OUT_MAIN, "criterio1_editorial_story_1080x1920")
    render_vertical_piece(
        bg_path=bg3,
        out_base_path=c1_ed_vert,
        kicker="CRITERIO NOTARIAL · BPS Y DGI",
        headline_lines=[
            "¿Certificación de",
            "firma o certificado",
            "notarial?",
        ],
        subtitle_lines=[
            "Uno da fe de tu firma en un formulario o contrato;",
            "el otro acredita un hecho o dato a partir de registros.",
            "Envía foto del requisito y te confirmamos",
            "cuál corresponde antes de coordinar.",
        ],
        cta_pill_text="Envía tu requisito al +598 99 431 185",
    )
    copy_editorial_to_all("criterio1_editorial_story_1080x1920", c1_ed_vert)

    # 4. Placas 2 y 3 del Reel 9:16 + Compilación del Reel MP4 con Tecleo y Música
    s2_spec = render_vertical_editorial_slide(
        base_name="criterio1_reel_slide2_1080x1920",
        bg_path=bg3,
        variant=1,
        badge_text="DIFERENCIA CLAVE",
        step_num="01",
        kicker="FIRMA VS. CERTIFICADO",
        headline_lines=["Dos actos distintos", "con nombres parecidos"],
        body_text="En la certificación das fe de tu firma en un texto ya listo; en el certificado el escribano acredita un dato o situación.",
        box_label="RESOLUCIÓN EN EL ESTUDIO",
        box_full_text="En certificaciones sobre documento ya redactado, coordinas por WhatsApp y firmas en el día.",
        cta_text="WhatsApp +598 99 431 185 · Punta del Este",
    )

    s3_spec = render_vertical_editorial_slide(
        base_name="criterio1_reel_slide3_1080x1920",
        bg_path=bg3,
        variant=2,
        badge_text="BPS · DGI · BANCOS",
        step_num="02",
        kicker="ANTES DE COORDINAR",
        headline_lines=["Envía una foto del", "requisito por WhatsApp"],
        body_text="Con el texto literal del pedido de BPS, DGI o el banco definimos qué acto corresponde.",
        box_label="ATENCIÓN DIRECTA",
        box_full_text="Te confirmamos en el primer mensaje qué documento corresponde y qué llevar para evitar una segunda visita.",
        cta_text="Nota completa en escribanofabriciorivas.com",
    )

    music_con_locu = os.path.join(MUSIC_DIR, "v4_cafe_del_mar_rhodes_sax_con_locucion.mp3")
    build_reel_mp4_with_typewriter_and_music(
        slide1_jpg_path=os.path.join(OUT_MAIN, "criterio1_editorial_story_1080x1920.jpg"),
        slide2_spec=s2_spec,
        slide3_spec=s3_spec,
        out_mp4_name="reel_06_criterio1_firma_vs_certificado_1080x1920.mp4",
        music_mp3_path=music_con_locu,
    )

    # 5. Formatos Especiales del Desplegable del Panel 360 (Google Maps 700x700 + Story Sticker + Estado WhatsApp)
    render_gbp_700x700("criterio1_gbp_700x700", bg3)

    render_vertical_editorial_slide(
        base_name="criterio1_story_sticker_1080x1920",
        bg_path=bg3,
        variant=1,
        badge_text="NUEVA NOTA EN LA WEB",
        step_num="01",
        kicker="CRITERIO NOTARIAL · BPS Y DGI",
        headline_lines=["¿Certificación de firma", "o certificado notarial?"],
        body_text="Cómo distinguir cuál te están pidiendo en BPS, DGI o el banco y qué tener a mano antes de coordinar.",
        box_label="TOCA EL ENLACE DE ESTA HISTORIA",
        box_full_text="Lee la nota completa en escribanofabriciorivas.com o envíanos foto del requisito por WhatsApp.",
        cta_text="Toca el enlace para leer la nota completa",
    )

    render_vertical_editorial_slide(
        base_name="criterio1_whatsapp_estado_1080x1920",
        bg_path=bg2,
        variant=2,
        badge_text="ESTADO DE WHATSAPP",
        step_num="01",
        kicker="CRITERIO NOTARIAL · MALDONADO",
        headline_lines=["¿Te pidieron firma", "certificada o certificado?"],
        body_text="Responde a este estado con una foto del requisito de BPS, DGI o el banco y te confirmamos cuál corresponde.",
        box_label="RESPUESTA DIRECTA POR WHATSAPP",
        box_full_text="Evita reunir papeles de más: revisamos el requisito antes de coordinar tu firma en Punta del Este.",
        cta_text="Responde a este estado o entra a la nota",
    )

    print("✅ Pack Criterio Notarial #1 completo generado con éxito.")


if __name__ == "__main__":
    main()
