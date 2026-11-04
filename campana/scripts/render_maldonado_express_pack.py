#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Pack Inmediato Pre-Grabación (3 Días de Disparo Ya — Maldonado Ciudad)
Sistema Visual Editorial Unificado + Animación de Tecleo en Reels (.mp4) + Música Café del Mar / Smooth Jazz:
- Coherencia total entre la Placa 1 (CON IA Arquitectónica) y las Placas 2, 3 y 4 (Editorial Arquitectónico con Velo Translúcido, CERO cajas blancas/beige desconectadas).
- Monograma FR 100% transparente y proporcionado (76px), jamás encerrado en un cuadrado negro ni estirado.
- Menos carga de texto (jerarquía aireada de lectura rápida) y ancho dinámico de píldoras para que jamás desborde un borde.
- En los Reels .mp4 (24 fps): el cuadro de resolución notarial ("Acreditamos tu titularidad...") se teclea letra por letra al ritmo de una lectura natural con cursor dorado '|', acompañado de la música Smooth Jazz / Chill R&B de estudio.
"""

import math
import os
import subprocess
import tempfile
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

from render_weekly_pack import (
    FONDOS_DIR,
    get_font,
    load_cropped_logo,
    crop_and_resize,
    apply_editorial_veil,
    draw_tracked_text,
    render_feed_piece,
    render_vertical_piece,
)

C_CARBON = (17, 17, 17)
C_GOLD = (196, 173, 122)
C_GOLD_LIGHT = (218, 193, 127)
C_PEARL = (244, 243, 239)
C_MUTED = (205, 201, 192)
C_WHITE = (255, 255, 255)

MAIN_SITIO = "/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio"
WORKTREE_SITIO = "/Users/arianawajntraub/.gemini/antigravity/worktrees/elegant-bardeen/teamwork_preview_workflow_automation/sitio"
GDRIVE_PACK_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/FR pp AG/pack_maldonado_en_el_dia"
ARTIFACT_DIR = "/Users/arianawajntraub/.gemini/antigravity/brain/8a79030b-f9ee-4ee1-9458-051b87c1cead"
MUSIC_DIR = os.path.join(MAIN_SITIO, "campana", "musica_fabricio")

OUT_MAIN = os.path.join(MAIN_SITIO, "campana", "pack_maldonado_en_el_dia")
OUT_WORKTREE = os.path.join(WORKTREE_SITIO, "campana", "pack_maldonado_en_el_dia")

for d in [OUT_MAIN, OUT_WORKTREE, GDRIVE_PACK_DIR]:
    os.makedirs(d, exist_ok=True)


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


def save_multi(canvas, base_name):
    rgb = canvas.convert("RGB")
    for folder in [OUT_MAIN, OUT_WORKTREE, GDRIVE_PACK_DIR]:
        rgb.save(os.path.join(folder, f"{base_name}.jpg"), "JPEG", quality=90, optimize=True)
        rgb.save(os.path.join(folder, f"{base_name}.png"), "PNG", optimize=True)
    rgb.save(os.path.join(ARTIFACT_DIR, f"{base_name}.jpg"), "JPEG", quality=90, optimize=True)
    return os.path.join(OUT_MAIN, f"{base_name}.jpg")


_BG_CACHE = {}


def make_architectural_continuation_bg(bg_path, w, h, variant=1):
    """
    Crea un fondo que continúa la atmósfera arquitectónica de la Placa 1 (sin ser idéntico):
    encuadre lateral distinto + desenfoque óptico sutil + velo carbón-piedra translúcido profundo
    que deja respirar la luz arquitectónica a la derecha y arriba. Cacheado en memoria para render 24fps instantáneo.
    """
    key = (bg_path, w, h, variant)
    if key in _BG_CACHE:
        return _BG_CACHE[key].copy()

    x_bias = 0.82 if variant % 2 == 1 else 0.22
    y_bias = 0.42 if variant % 2 == 1 else 0.62
    raw_bg = crop_and_resize(bg_path, w, h, x_bias=x_bias, y_bias=y_bias)
    soft_bg = raw_bg.filter(ImageFilter.GaussianBlur(radius=5)).convert("RGBA")

    veil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = veil.load()
    # Tono carbón cálido en impares, tono piedra-obsidiana en pares para ritmo visual sutil
    r_base, g_base, b_base = (16, 16, 15) if variant % 2 == 1 else (23, 21, 18)

    for y in range(h):
        ny = y / h
        ay = 0.04 * math.sin(math.pi * ny)
        for x in range(w):
            nx = x / w
            if nx < 0.42:
                ax = 0.84
            else:
                t = (nx - 0.42) / 0.58
                ax = 0.60 + 0.24 * 0.5 * (1.0 + math.cos(math.pi * t))
            alpha = min(0.88, ax + ay)
            px[x, y] = (r_base, g_base, b_base, int(alpha * 255))

    comp = Image.alpha_composite(soft_bg, veil)
    _BG_CACHE[key] = comp
    return comp.copy()


def draw_dynamic_pill(draw, x, y, text, font, fill_bg, outline_col, text_col, pad_x=28, pad_y=14, radius=26):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    w = tw + pad_x * 2
    h = th + pad_y * 2
    draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=radius, fill=fill_bg, outline=outline_col, width=2)
    draw.text((x + pad_x, y + pad_y - 2), text, font=font, fill=text_col)
    return w, h


def render_editorial_carousel_card(
    base_name,
    bg_path,
    variant,
    badge_text,
    step_num,
    kicker,
    headline_lines,
    body_text,
    takeaway_label,
    takeaway_text,
):
    """
    Lámina 1080x1350 para Carrusel con continuidad visual editorial respecto a la Portada CON IA:
    - Logo FR 100% transparente (74px) sin ningún cuadrado negro detrás.
    - Marco fino arquitectónico en oro apagado.
    - Texto breve y aireado.
    - Recuadro de Criterio Notarial / Resolución con barra lateral dorada.
    """
    W, H = 1080, 1350
    canvas = make_architectural_continuation_bg(bg_path, W, H, variant=variant)
    draw = ImageDraw.Draw(canvas, "RGBA")

    # Marco arquitectónico sutil dentro de la zona segura (transparente para dejar respirar la arquitectura velada)
    draw.rounded_rectangle(
        [(64, 140), (1016, 1195)],
        radius=28,
        fill=None,
        outline=(196, 173, 122, 115),
        width=2,
    )

    # 1. Logo FR 100% transparente (jamás caja opaca detrás)
    logo = load_cropped_logo(target_height=76)
    canvas.paste(logo, (96, 178), logo)

    # 2. Píldora superior derecha (ej. "02 / 05") con ancho dinámico
    if badge_text:
        f_badge = get_font(24, "demibold")
        bb = draw.textbbox((0, 0), badge_text, font=f_badge)
        bw = (bb[2] - bb[0]) + 48
        draw.rounded_rectangle(
            [(984 - bw, 186), (984, 240)],
            radius=27,
            fill=(17, 17, 17, 190),
            outline=(196, 173, 122, 160),
            width=2,
        )
        draw.text((984 - bw + 24, 199), badge_text, font=f_badge, fill=C_GOLD_LIGHT)

    # 3. Indicador de paso + Kicker con tracking
    y_cur = 315
    f_step = get_font(25, "bold")
    sb = draw.textbbox((0, 0), step_num, font=f_step)
    sw = max(68, (sb[2] - sb[0]) + 34)
    draw.rounded_rectangle([(96, y_cur), (96 + sw, y_cur + 46)], radius=12, fill=C_GOLD)
    draw.text((96 + (sw - (sb[2] - sb[0])) // 2, y_cur + 8), step_num, font=f_step, fill=C_CARBON)

    f_kicker = get_font(22, "demibold")
    draw_tracked_text(draw, (96 + sw + 20, y_cur + 11), kicker.upper(), f_kicker, C_GOLD_LIGHT, tracking=3)

    # 4. Titular principal (Avenir Next Medium, blanco puro, 58px, limpio y sin gritar)
    y_cur = 400
    f_head = get_font(56, "medium")
    for hl in headline_lines:
        draw.text((96, y_cur), hl, font=f_head, fill=C_WHITE)
        y_cur += 68

    y_cur += 18
    draw.line([(96, y_cur), (196, y_cur)], fill=C_GOLD, width=3)
    y_cur += 30

    # 5. Cuerpo breve y aireado (37px, máximo 3 líneas)
    f_body = get_font(37, "regular")
    for bl in wrap_lines(draw, body_text, f_body, 860):
        draw.text((96, y_cur), bl, font=f_body, fill=C_PEARL)
        y_cur += 50

    # 6. Cuadro de Criterio Notarial / Resolución (con acento lateral dorado y altura dinámica)
    f_tk_label = get_font(22, "demibold")
    f_tk_text = get_font(34, "medium")
    tk_lines = wrap_lines(draw, takeaway_text, f_tk_text, 810)
    box_h = 68 + len(tk_lines) * 44 + 22
    box_y1 = 815
    box_y2 = box_y1 + box_h

    draw.rounded_rectangle(
        [(96, box_y1), (984, box_y2)],
        radius=20,
        fill=(28, 26, 22, 215),
        outline=(196, 173, 122, 140),
        width=2,
    )
    # Barra vertical dorada a la izquierda del cuadro
    draw.rounded_rectangle([(96, box_y1), (106, box_y2)], radius=5, fill=C_GOLD)
    draw_tracked_text(draw, (132, box_y1 + 22), takeaway_label.upper(), f_tk_label, C_GOLD_LIGHT, tracking=3)

    ty = box_y1 + 60
    for tkl in tk_lines:
        draw.text((132, ty), tkl, font=f_tk_text, fill=C_WHITE)
        ty += 44

    # 7. Firma institucional idéntica a la Placa 1 (en zona segura y=1055..1150)
    y_foot = 1055
    draw.line([(96, y_foot - 22), (680, y_foot - 22)], fill=(196, 173, 122, 100), width=2)
    f_f1 = get_font(33, "medium")
    f_f2 = get_font(26, "regular")
    draw.text((96, y_foot), "Fabricio Rivas | Escribano Público", font=f_f1, fill=C_WHITE)
    draw.text((96, y_foot + 44), "Punta del Este · Maldonado · WhatsApp +598 99 431 185", font=f_f2, fill=C_GOLD_LIGHT)

    return save_multi(canvas, base_name)


def draw_vertical_editorial_slide_canvas(
    bg_path,
    variant,
    badge_text,
    step_num,
    kicker,
    headline_lines,
    body_text,
    box_label,
    typed_box_text,
    show_cursor=False,
    cta_text="WhatsApp +598 99 431 185 · ARTOWER Punta del Este",
    zoom_progress=0.0,
):
    """
    Genera un fotograma (o lámina fija) 1080x1920 para las Placas 2 y 3 del Reel:
    - Misma familia visual que la Placa 1 CON IA (fondo arquitectónico con velo profundo, logo FR transparente 78px).
    - El recuadro de información clave ('typed_box_text') permite renderizar cualquier subcadena parcial + cursor '|'
      para lograr el efecto de tecleo en vivo a velocidad de lectura natural en el video .mp4.
    - La píldora inferior calcula su ancho exacto con textbbox para que jamás se corte ni desborde.
    """
    W, H = 1080, 1920
    base_bg = make_architectural_continuation_bg(bg_path, W, H, variant=variant)
    if zoom_progress > 0:
        scale = 1.0 + 0.028 * zoom_progress
        zw, zh = int(W * scale), int(H * scale)
        resized = base_bg.resize((zw, zh), Image.Resampling.BILINEAR)
        left = (zw - W) // 2
        top = (zh - H) // 2
        canvas = resized.crop((left, top, left + W, top + H))
    else:
        canvas = base_bg

    draw = ImageDraw.Draw(canvas, "RGBA")

    # Marco arquitectónico vertical sutil dentro de la zona segura de Reels (y=300..1430)
    draw.rounded_rectangle(
        [(64, 295), (1016, 1435)],
        radius=30,
        fill=None,
        outline=(196, 173, 122, 115),
        width=2,
    )

    # 1. Logo FR 100% transparente y proporcionado (78px)
    logo = load_cropped_logo(target_height=78)
    canvas.paste(logo, (96, 330), logo)

    # 2. Píldora superior derecha con ancho dinámico
    if badge_text:
        f_badge = get_font(23, "demibold")
        bb = draw.textbbox((0, 0), badge_text, font=f_badge)
        bw = (bb[2] - bb[0]) + 46
        draw.rounded_rectangle(
            [(984 - bw, 340), (984, 394)],
            radius=27,
            fill=(17, 17, 17, 195),
            outline=(196, 173, 122, 165),
            width=2,
        )
        draw.text((984 - bw + 23, 353), badge_text, font=f_badge, fill=C_GOLD_LIGHT)

    # 3. Paso + Kicker
    y_cur = 460
    f_step = get_font(25, "bold")
    sb = draw.textbbox((0, 0), step_num, font=f_step)
    sw = max(68, (sb[2] - sb[0]) + 34)
    draw.rounded_rectangle([(96, y_cur), (96 + sw, y_cur + 46)], radius=12, fill=C_GOLD)
    draw.text((96 + (sw - (sb[2] - sb[0])) // 2, y_cur + 8), step_num, font=f_step, fill=C_CARBON)

    f_kicker = get_font(22, "demibold")
    draw_tracked_text(draw, (96 + sw + 20, y_cur + 11), kicker.upper(), f_kicker, C_GOLD_LIGHT, tracking=3)

    # 4. Titular limpio (Avenir Next Medium, 58px)
    y_cur = 540
    f_head = get_font(58, "medium")
    for hl in headline_lines:
        draw.text((96, y_cur), hl, font=f_head, fill=C_WHITE)
        y_cur += 70

    y_cur += 16
    draw.line([(96, y_cur), (196, y_cur)], fill=C_GOLD, width=3)
    y_cur += 28

    # 5. Subtítulo conciso (2 líneas máx., 37px)
    f_body = get_font(37, "regular")
    for bl in wrap_lines(draw, body_text, f_body, 860):
        draw.text((96, y_cur), bl, font=f_body, fill=C_PEARL)
        y_cur += 50

    # 6. CUADRADO DE INFORMACIÓN CON TECLEO EN VIVO ("Acreditamos tu titularidad...")
    box_y1 = 875
    box_y2 = 1125
    draw.rounded_rectangle(
        [(96, box_y1), (984, box_y2)],
        radius=22,
        fill=(26, 24, 20, 230),
        outline=(196, 173, 122, 185),
        width=2,
    )
    draw.rounded_rectangle([(96, box_y1), (108, box_y2)], radius=6, fill=C_GOLD)

    f_box_lbl = get_font(22, "demibold")
    draw_tracked_text(draw, (134, box_y1 + 24), box_label.upper(), f_box_lbl, C_GOLD_LIGHT, tracking=3)

    f_box_txt = get_font(36, "medium")
    display_txt = typed_box_text + ("|" if show_cursor else "")
    wrapped_box = wrap_lines(draw, display_txt, f_box_txt, 815) if display_txt else []
    ty = box_y1 + 68
    for line in wrapped_box[:3]:
        draw.text((134, ty), line, font=f_box_txt, fill=C_WHITE)
        ty += 48

    # 7. Píldora inferior de contacto con ANCHO 100% DINÁMICO (cero desborde garantizado y contraste 12:1 carbón sobre oro)
    f_cta = get_font(27, "demibold")
    draw_dynamic_pill(
        draw,
        x=96,
        y=1165,
        text=cta_text,
        font=f_cta,
        fill_bg=C_GOLD,
        outline_col=C_GOLD_LIGHT,
        text_col=C_CARBON,
        pad_x=30,
        pad_y=15,
        radius=28,
    )

    # 8. Firma institucional en zona segura vertical (y=1295..1390)
    y_foot = 1295
    draw.line([(96, y_foot - 20), (680, y_foot - 20)], fill=(196, 173, 122, 100), width=2)
    f_name = get_font(33, "medium")
    f_sub = get_font(26, "regular")
    draw.text((96, y_foot), "Fabricio Rivas | Escribano Público", font=f_name, fill=C_WHITE)
    draw.text((96, y_foot + 44), "Punta del Este · Maldonado · Matrícula 17058/5", font=f_sub, fill=C_GOLD_LIGHT)

    return canvas


def render_vertical_editorial_slide(
    base_name,
    bg_path,
    variant,
    badge_text,
    step_num,
    kicker,
    headline_lines,
    body_text,
    box_label,
    box_full_text,
    cta_text="WhatsApp +598 99 431 185 · ARTOWER Punta del Este",
):
    """Guarda la versión estática completa (.jpg/.png) de la placa vertical del Reel."""
    canvas = draw_vertical_editorial_slide_canvas(
        bg_path=bg_path,
        variant=variant,
        badge_text=badge_text,
        step_num=step_num,
        kicker=kicker,
        headline_lines=headline_lines,
        body_text=body_text,
        box_label=box_label,
        typed_box_text=box_full_text,
        show_cursor=False,
        cta_text=cta_text,
        zoom_progress=0.0,
    )
    save_multi(canvas, base_name)
    return {
        "bg_path": bg_path,
        "variant": variant,
        "badge_text": badge_text,
        "step_num": step_num,
        "kicker": kicker,
        "headline_lines": headline_lines,
        "body_text": body_text,
        "box_label": box_label,
        "box_full_text": box_full_text,
        "cta_text": cta_text,
    }


def copy_editorial_to_all(base_name, src_prefix):
    for ext in [".jpg", ".png"]:
        src = src_prefix + ext
        if os.path.exists(src):
            img = Image.open(src)
            for folder in [OUT_MAIN, OUT_WORKTREE, GDRIVE_PACK_DIR]:
                img.save(os.path.join(folder, base_name + ext))
            if ext == ".jpg":
                img.save(os.path.join(ARTIFACT_DIR, base_name + ext))


def build_reel_mp4_with_typewriter_and_music(slide1_jpg_path, slide2_spec, slide3_spec, out_mp4_name, music_mp3_path):
    """
    Genera un Reel .mp4 1080x1920 a 24fps reales donde:
    - Escena 1 (0.0s a 3.6s): Portada CON IA con suave paneo cinematográfico.
    - Escena 2 (3.6s a 8.2s): Placa 2 Editorial Arquitectónica con TECLEO EN VIVO al ritmo de lectura normal
      dentro del cuadro de resolución notarial + cursor dorado '|'.
    - Escena 3 (8.2s a 12.8s): Placa 3 Editorial Arquitectónica con TECLEO EN VIVO al ritmo de lectura normal
      dentro del cuadro de resolución notarial + cursor dorado '|'.
    - Pista de audio: Música Smooth Jazz Sunset / Chill R&B Café del Mar (100% libre de derechos).
    """
    fps = 24
    dur_s1 = 3.6
    dur_s2 = 4.6
    dur_s3 = 4.6
    total_dur = dur_s1 + dur_s2 + dur_s3

    out_main_mp4 = os.path.join(OUT_MAIN, out_mp4_name)

    with tempfile.TemporaryDirectory() as tmpdir:
        frame_idx = 0

        # 1. Fotogramas de Escena 1 (Portada CON IA con suave zoom in)
        s1_img = Image.open(slide1_jpg_path).convert("RGB")
        W, H = 1080, 1920
        n_f1 = int(dur_s1 * fps)
        for i in range(n_f1):
            p = i / max(1, n_f1 - 1)
            scale = 1.0 + 0.025 * p
            zw, zh = int(W * scale), int(H * scale)
            big = s1_img.resize((zw, zh), Image.Resampling.BILINEAR)
            crop = big.crop(((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
            crop.save(os.path.join(tmpdir, f"f_{frame_idx:04d}.jpg"), "JPEG", quality=88)
            frame_idx += 1

        # 2 & 3. Fotogramas de Escena 2 y Escena 3 con tecleo a ritmo de lectura normal (~28 caracteres/seg)
        for spec, dur in [(slide2_spec, dur_s2), (slide3_spec, dur_s3)]:
            n_frames = int(dur * fps)
            full_txt = spec["box_full_text"]
            total_chars = len(full_txt)
            # El tecleo arranca a los 0.25s y termina ~1.2s antes del cierre para que se lea completo con comodidad
            start_f = int(0.25 * fps)
            end_f = int((dur - 1.25) * fps)
            type_span = max(1, end_f - start_f)

            for i in range(n_frames):
                p_zoom = i / max(1, n_frames - 1)
                if i < start_f:
                    sub_txt = ""
                    cursor = True
                elif i <= end_f:
                    chars_now = int(round(((i - start_f) / type_span) * total_chars))
                    sub_txt = full_txt[:chars_now]
                    cursor = True
                else:
                    sub_txt = full_txt
                    # Parpadeo suave del cursor al terminar de escribir
                    cursor = ((i - end_f) // 6) % 2 == 0

                frame_canvas = draw_vertical_editorial_slide_canvas(
                    bg_path=spec["bg_path"],
                    variant=spec["variant"],
                    badge_text=spec["badge_text"],
                    step_num=spec["step_num"],
                    kicker=spec["kicker"],
                    headline_lines=spec["headline_lines"],
                    body_text=spec["body_text"],
                    box_label=spec["box_label"],
                    typed_box_text=sub_txt,
                    show_cursor=cursor,
                    cta_text=spec["cta_text"],
                    zoom_progress=p_zoom,
                )
                frame_canvas.convert("RGB").save(os.path.join(tmpdir, f"f_{frame_idx:04d}.jpg"), "JPEG", quality=88)
                frame_idx += 1

        # Mezclar con la música Smooth Jazz / Chill R&B de estudio
        if os.path.exists(music_mp3_path):
            cmd = [
                FFMPEG_BIN, "-y",
                "-framerate", str(fps),
                "-i", os.path.join(tmpdir, "f_%04d.jpg"),
                "-i", music_mp3_path,
                "-filter_complex",
                f"[1:a]atrim=0:{total_dur},afade=t=in:st=0:d=0.8,afade=t=out:st={total_dur-1.4}:d=1.4,volume=0.85[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), "-preset", "fast", "-crf", "22",
                "-c:a", "aac", "-b:a", "160k",
                "-movflags", "+faststart",
                out_main_mp4,
            ]
        else:
            cmd = [
                FFMPEG_BIN, "-y",
                "-framerate", str(fps),
                "-i", os.path.join(tmpdir, "f_%04d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), "-preset", "fast", "-crf", "22",
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

    # Pista oficial elegida: 4. Café del Mar Rhodes & Smooth Sax
    # Intercalada CON locución de Tomás Barítono (1 sola vez en el segundo 3.0) y SIN locución (instrumental puro)
    music_v4_con_locu = os.path.join(MUSIC_DIR, "v4_cafe_del_mar_rhodes_sax_con_locucion.mp3")
    music_v4_sin_locu = os.path.join(MUSIC_DIR, "v4_cafe_del_mar_rhodes_sax_instrumental.mp3")
    music_1 = music_v4_con_locu  # Día 1: CON locución (1 sola vez en seg 3)
    music_2 = music_v4_sin_locu  # Día 2: SIN locución (Instrumental)
    music_3 = music_v4_con_locu  # Día 5: CON locución (1 sola vez en seg 3)

    # =========================================================================
    # PACK 1 (DÍA 1): DECRETO 4118 IDM — REGULARIZACIÓN DE OBRAS EN MALDONADO
    # =========================================================================
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
            "Plan vigente por 18 meses: suspende el impuesto",
            "a la edificación inapropiada en Maldonado.",
            "Emitimos en 24 h el certificado notarial",
            "de legitimación obligatorio para tu carpeta.",
        ],
        badge_number="01 / 05",
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
            "Aplica a obras y ampliaciones previas",
            "al 31 de diciembre de 2025.",
            "Requisito artículo 3 IDM: certificado",
            "notarial de legitimación en 24 h.",
        ],
        cta_pill_text="Envía tu padrón al +598 99 431 185",
    )
    copy_editorial_to_all("pack1_decreto4118_editorial_story_1080x1920", p1_ed_vert)

    # Carrusel Editorial Unificado (4 láminas que continúan el estilo de la Portada)
    render_editorial_carousel_card(
        base_name="pack1_carrusel_01_1080x1350",
        bg_path=bg2,
        variant=1,
        badge_text="02 / 05",
        step_num="01",
        kicker="Alcance del Decreto 4118/2026",
        headline_lines=["¿Qué obras entran en el", "plan de Maldonado?"],
        body_text="Construcciones, parrilleros techados, cocheras o reformas hechas sin permiso municipal hasta el 31/12/2025.",
        takeaway_label="Beneficio fiscal directo",
        takeaway_text="Suspende el impuesto a la edificación inapropiada y exonera tasas.",
    )
    render_editorial_carousel_card(
        base_name="pack1_carrusel_02_1080x1350",
        bg_path=bg2,
        variant=2,
        badge_text="03 / 05",
        step_num="02",
        kicker="Requisito artículo 3 IDM",
        headline_lines=["El documento obligatorio", "para abrir la carpeta"],
        body_text="La Intendencia exige acreditar la titularidad mediante certificado notarial antes de ingresar los planos.",
        takeaway_label="Resolución notarial en 24 h",
        takeaway_text="Acreditamos tu calidad de propietario, promitente comprador o heredero.",
    )
    render_editorial_carousel_card(
        base_name="pack1_carrusel_03_1080x1350",
        bg_path=bg2,
        variant=1,
        badge_text="04 / 05",
        step_num="03",
        kicker="Valor patrimonial",
        headline_lines=["Deja tu padrón apto", "para banco y venta"],
        body_text="Los metros sin declarar traban créditos hipotecarios. El plazo extraordinario dura solo 18 meses.",
        takeaway_label="Criterio notarial",
        takeaway_text="Aun con sucesión en trámite puedes legitimar el inicio del expediente.",
    )
    render_editorial_carousel_card(
        base_name="pack1_carrusel_04_1080x1350",
        bg_path=bg2,
        variant=2,
        badge_text="05 / 05",
        step_num="04",
        kicker="Gestión en el día",
        headline_lines=["Cómo lo resolvemos", "sin demoras en el estudio"],
        body_text="Envías tu número de padrón y cédula por WhatsApp y entregamos el certificado listo para tu arquitecto.",
        takeaway_label="Contacto directo",
        takeaway_text="WhatsApp +598 99 431 185 · ARTOWER Punta del Este",
    )

    # Slides 2 y 3 del Reel 1 (con tecleo animado en el cuadro de resolución)
    s1_v1 = p1_ed_vert + ".jpg"
    s1_v2_spec = render_vertical_editorial_slide(
        base_name="pack1_reel_slide2_1080x1920",
        bg_path=bg2,
        variant=1,
        badge_text="PASO 1 · DECRETO 4118",
        step_num="01",
        kicker="Obras hasta 31/12/2025",
        headline_lines=["Frena el impuesto a la", "edificación inapropiada"],
        body_text="Para ampliaciones, cocheras o parrilleros en Maldonado sin permiso municipal previo.",
        box_label="Plazo extraordinario IDM",
        box_full_text="18 meses de vigencia con exoneración de tasas y suspensión de multas.",
    )
    s1_v3_spec = render_vertical_editorial_slide(
        base_name="pack1_reel_slide3_1080x1920",
        bg_path=bg2,
        variant=2,
        badge_text="PASO 2 · ARTÍCULO 3 IDM",
        step_num="02",
        kicker="Requisito obligatorio",
        headline_lines=["Certificado notarial", "de legitimación en 24 h"],
        body_text="Con tu número de padrón y cédula por WhatsApp preparamos el documento para tu arquitecto.",
        box_label="Resolución notarial en el día",
        box_full_text="Acreditamos tu titularidad como propietario, promitente comprador o heredero.",
    )
    build_reel_mp4_with_typewriter_and_music(
        s1_v1, s1_v2_spec, s1_v3_spec,
        "reel_01_decreto4118_maldonado_1080x1920.mp4",
        music_1,
    )

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
        badge_number="01 / 03",
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

    render_editorial_carousel_card(
        base_name="pack2_carrusel_01_1080x1350",
        bg_path=bg1,
        variant=1,
        badge_text="02 / 03",
        step_num="01",
        kicker="Si ya entregaste el vehículo",
        headline_lines=["Declaración jurada de", "desvinculación vehicular"],
        body_text="Si vendiste un auto o moto sin transferir y siguen llegando multas a tu nombre en Maldonado.",
        takeaway_label="Efecto directo ante IDM / SUCIVE",
        takeaway_text="Corta la generación futura de multas y patente sobre tu cédula.",
    )
    render_editorial_carousel_card(
        base_name="pack2_carrusel_02_1080x1350",
        bg_path=bg1,
        variant=2,
        badge_text="03 / 03",
        step_num="02",
        kicker="Si vas a vender o comprar hoy",
        headline_lines=["Entrega segura con firma", "en 15 minutos en el estudio"],
        body_text="Envías foto de libreta y cédulas por WhatsApp y pasas únicamente a firmar el documento listo.",
        takeaway_label="Resguardo patrimonial",
        takeaway_text="Deslindas responsabilidad civil, penal y municipal desde ese instante.",
    )

    s2_v1 = p2_ed_vert + ".jpg"
    s2_v2_spec = render_vertical_editorial_slide(
        base_name="pack2_reel_slide2_1080x1920",
        bg_path=bg1,
        variant=1,
        badge_text="RADARES EN MALDONADO",
        step_num="01",
        kicker="Desvinculación IDM / SUCIVE",
        headline_lines=["¿Llegan multas de un", "auto que ya entregaste?"],
        body_text="No dejes que las fotomultas de 45 km/h sigan acumulándose sobre tu cédula de identidad.",
        box_label="Resolución notarial en el día",
        box_full_text="Instrumentamos tu declaración jurada notarial de desvinculación ante la IDM.",
    )
    s2_v3_spec = render_vertical_editorial_slide(
        base_name="pack2_reel_slide3_1080x1920",
        bg_path=bg1,
        variant=2,
        badge_text="FIRMA EN 15 MINUTOS",
        step_num="02",
        kicker="Compraventa y Carta Poder",
        headline_lines=["Envías libreta y cédulas", "y pasas directo a firmar"],
        body_text="Redactamos la transferencia o carta poder antes de tu visita para resolverlo en el acto.",
        box_label="Seguridad total al vender",
        box_full_text="Deslindas responsabilidad civil, penal y municipal desde el momento de la firma.",
    )
    build_reel_mp4_with_typewriter_and_music(
        s2_v1, s2_v2_spec, s2_v3_spec,
        "reel_02_automotores_maldonado_1080x1920.mp4",
        music_2,
    )

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
        badge_number="01 / 03",
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

    render_editorial_carousel_card(
        base_name="pack3_placa_luc_1080x1350",
        bg_path=bg4,
        variant=1,
        badge_text="02 / 03",
        step_num="LUC",
        kicker="Ley 19.889 · Alquiler sin garantía",
        headline_lines=["Por qué un borrador de", "internet no te protege"],
        body_text="Para que rija el desalojo abreviado de la LUC, la ley exige cláusulas expresas y firmas certificadas.",
        takeaway_label="Resolución en 24 horas",
        takeaway_text="Redactamos y certificamos tu contrato con inventario blindado en el día.",
    )
    render_editorial_carousel_card(
        base_name="pack3_placa_permiso_menor_1080x1350",
        bg_path=bg4,
        variant=2,
        badge_text="03 / 03",
        step_num="10'",
        kicker="Viajes al exterior y trámites",
        headline_lines=["Permiso de menor listo", "con 1 mensaje de WhatsApp"],
        body_text="Envías foto de cédulas de los padres y partida de nacimiento; pasas 10 minutos a firmar.",
        takeaway_label="Atención sin fila de espera",
        takeaway_text="Certificados de ingresos, firmas y poderes listos en el día en ARTOWER.",
    )

    s3_v1 = p3_ed_vert + ".jpg"
    s3_v2_spec = render_vertical_editorial_slide(
        base_name="pack3_reel_slide2_1080x1920",
        bg_path=bg4,
        variant=1,
        badge_text="ALQUILERES EN MALDONADO",
        step_num="LUC",
        kicker="Ley 19.889 e Inventario",
        headline_lines=["Alquila con plazos de", "desalojo abreviado reales"],
        body_text="Para propietarios e inquilinos en Maldonado y Punta del Este que buscan seguridad jurídica hoy.",
        box_label="Contrato certificado en 24 h",
        box_full_text="Incluimos las cláusulas expresas de la LUC y certificación notarial de firmas.",
    )
    s3_v3_spec = render_vertical_editorial_slide(
        base_name="pack3_reel_slide3_1080x1920",
        bg_path=bg4,
        variant=2,
        badge_text="PERMISO Y CERTIFICADOS",
        step_num="10'",
        kicker="Trámite sin espera",
        headline_lines=["Envías las cédulas por", "WhatsApp y pasas a firmar"],
        body_text="Preparamos tu documento antes de tu llegada a la oficina para que no pierdas tiempo.",
        box_label="Resolución en el día",
        box_full_text="Permisos de menor, certificados de ingresos para bancos y cartas poder en 10 min.",
    )
    build_reel_mp4_with_typewriter_and_music(
        s3_v1, s3_v2_spec, s3_v3_spec,
        "reel_03_alquiler_luc_y_permiso_menor_1080x1920.mp4",
        music_3,
    )
    print("✅ PACK MALDONADO REDISEÑADO COMPLETO (COHERENCIA EDITORIAL + TECLEO EN VIVO + SMOOTH JAZZ)")


if __name__ == "__main__":
    main()
