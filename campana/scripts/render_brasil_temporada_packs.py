#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador oficial de los 2 Packs Multicanal en Portugués (Temporada Brasil · Fabricio Rivas):
1) tanda_4_brasil_imovel_pt: Comprar imóvel em Punta del Este (Tabelião, sinal e procuração)
2) tanda_5_brasil_cartorio_pt: Cartório em Punta del Este para brasileiros na temporada
"""
import os
import sys
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageStat

sys.path.insert(0, os.path.dirname(__file__))
import render_criterio_en_income_pack as base

SITIO_DIR = base.SITIO_DIR
FFMPEG_BIN = base.FFMPEG_BIN
MUSIC_MP3 = base.MUSIC_MP3
C_CARBON = base.C_CARBON
C_BRONZE = base.C_BRONZE
C_BOX_BG = base.C_BOX_BG
C_BOX_ALT = base.C_BOX_ALT
C_GOLD = base.C_GOLD
C_GOLD_BORDER = base.C_GOLD_BORDER
C_GOLD_LIGHT = base.C_GOLD_LIGHT
C_WHITE = base.C_WHITE
C_PEARL = base.C_PEARL
C_MUTED = base.C_MUTED
get_font = base.get_font
load_logo = base.load_logo
make_watermark = base.make_watermark
extract_clean_portrait = base.extract_clean_portrait
draw_tracked = base.draw_tracked
wrap_lines = base.wrap_lines
draw_base_4x5 = base.draw_base_4x5
draw_footer_4x5 = base.draw_footer_4x5


def render_pack(cfg: dict, logo: Image.Image, watermark: Image.Image, portrait: Image.Image):
    out_dir = os.path.join(SITIO_DIR, "campana", cfg["folder"])
    os.makedirs(out_dir, exist_ok=True)
    generated = []

    # 0.jpg · Matriz 3A Carbón (#10100f)
    c0 = draw_base_4x5(C_CARBON, "01 / 04", logo, watermark)
    d0 = ImageDraw.Draw(c0, "RGBA")
    draw_tracked(d0, (96, 294), cfg["s1_kicker"], get_font(20, "demibold"), C_GOLD, tracking=2.2)
    f_h1 = get_font(62, "demibold")
    y = 342
    for ln in wrap_lines(d0, cfg["s1_title"], f_h1, 884):
        d0.text((96, y), ln, font=f_h1, fill=C_WHITE)
        y += 74
    y += 18
    d0.line([(96, y), (224, y)], fill=C_GOLD, width=3)
    y += 38
    f_b1 = get_font(34, "regular")
    for ln in wrap_lines(d0, cfg["s1_sub"], f_b1, 880):
        d0.text((96, y), ln, font=f_b1, fill=C_PEARL)
        y += 48
    d0.rounded_rectangle([(96, 860), (984, 1002)], radius=18, fill=C_BOX_BG + (238,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(d0, (128, 886), cfg["s1_box_kicker"], get_font(18, "demibold"), C_GOLD_LIGHT, tracking=2.1)
    d0.text((128, 924), cfg["s1_box_text"], font=get_font(28, "medium"), fill=C_WHITE)
    draw_footer_4x5(d0, "Matrícula SCJ 17058/5 · Punta del Este e Maldonado · Deslize para ver mais")
    p0 = os.path.join(out_dir, "0.jpg")
    c0.convert("RGB").save(p0, "JPEG", quality=92, optimize=True)
    generated.append(p0)

    # 1.jpg · Matriz 3A Carbón
    c1 = draw_base_4x5(C_CARBON, "02 / 04", logo, watermark)
    d1 = ImageDraw.Draw(c1, "RGBA")
    draw_tracked(d1, (96, 286), cfg["s2_kicker"], get_font(20, "demibold"), C_GOLD, tracking=2.2)
    f_h2 = get_font(54, "demibold")
    y = 330
    for ln in wrap_lines(d1, cfg["s2_title"], f_h2, 884):
        d1.text((96, y), ln, font=f_h2, fill=C_WHITE)
        y += 66
    y += 14
    d1.line([(96, y), (216, y)], fill=C_GOLD, width=3)
    y += 34
    for box_title, box_body in cfg["s2_boxes"]:
        d1.rounded_rectangle([(96, y), (984, y + 188)], radius=18, fill=C_BOX_BG + (240,), outline=C_GOLD_BORDER, width=1)
        d1.text((128, y + 24), box_title, font=get_font(30, "demibold"), fill=C_GOLD_LIGHT)
        by = y + 72
        for ln in wrap_lines(d1, box_body, get_font(28, "regular"), 820):
            d1.text((128, by), ln, font=get_font(28, "regular"), fill=C_PEARL)
            by += 38
        y += 212
    assert y <= 1044, f"Overflow slide 1 in {cfg['folder']}: {y}"
    draw_footer_4x5(d1, "Atendimento em português · Punta del Este e Maldonado · Deslize para ver mais")
    p1 = os.path.join(out_dir, "1.jpg")
    c1.convert("RGB").save(p1, "JPEG", quality=92, optimize=True)
    generated.append(p1)

    # 2.jpg · Matriz 3B Bronce (#221e16)
    c2 = draw_base_4x5(C_BRONZE, "03 / 04", logo, watermark)
    d2 = ImageDraw.Draw(c2, "RGBA")
    draw_tracked(d2, (96, 286), cfg["s3_kicker"], get_font(20, "demibold"), C_GOLD, tracking=2.2)
    f_h3 = get_font(54, "demibold")
    y = 330
    for ln in wrap_lines(d2, cfg["s3_title"], f_h3, 884):
        d2.text((96, y), ln, font=f_h3, fill=C_WHITE)
        y += 66
    y += 14
    d2.line([(96, y), (216, y)], fill=C_GOLD, width=3)
    y += 34
    f_it_t = get_font(30, "demibold")
    f_it_b = get_font(28, "regular")
    for tit, desc in cfg["s3_items"]:
        d2.text((96, y), tit, font=f_it_t, fill=C_GOLD_LIGHT)
        y += 40
        for ln in wrap_lines(d2, desc, f_it_b, 880):
            d2.text((96, y), ln, font=f_it_b, fill=C_PEARL)
            y += 38
        y += 22
    assert y <= 1044, f"Overflow slide 2 in {cfg['folder']}: {y}"
    draw_footer_4x5(d2, "Matrícula SCJ 17058/5 · Punta del Este e Maldonado · Deslize para ver mais")
    p2 = os.path.join(out_dir, "2.jpg")
    c2.convert("RGB").save(p2, "JPEG", quality=92, optimize=True)
    generated.append(p2)

    # 3.jpg · Matriz 2 Retrato + Sans (#10100f)
    c3 = draw_base_4x5(C_CARBON, "04 / 04", logo, watermark)
    pw, ph = portrait.size
    px = 1080 - pw - 52
    py = 1054 - ph
    c3.paste(portrait, (px, py), portrait)
    d3 = ImageDraw.Draw(c3, "RGBA")
    draw_tracked(d3, (96, 306), "ATENDIMENTO EM PORTUGUÊS · PUNTA DEL ESTE", get_font(18, "demibold"), C_GOLD, tracking=2.0)
    col_w = min(475, px - 96 - 24)
    f_h4 = get_font(44, "demibold")
    y = 362
    for ln in wrap_lines(d3, cfg["s4_title"], f_h4, col_w):
        d3.text((96, y), ln, font=f_h4, fill=C_WHITE)
        y += 56
    y += 14
    d3.line([(96, y), (196, y)], fill=C_GOLD, width=3)
    y += 28
    f_b4 = get_font(27, "regular")
    for ln in wrap_lines(d3, cfg["s4_body"], f_b4, col_w):
        if ln == "":
            y += 18
            continue
        d3.text((96, y), ln, font=f_b4, fill=C_PEARL)
        y += 38
    assert y <= 1040, f"Overflow slide 3 in {cfg['folder']}: {y}"
    draw_footer_4x5(d3, "Matrícula SCJ 17058/5 · Punta del Este e Maldonado · WhatsApp +598 99 431 185")
    p3 = os.path.join(out_dir, "3.jpg")
    c3.convert("RGB").save(p3, "JPEG", quality=92, optimize=True)
    generated.append(p3)

    # GBP 700x700
    g_w, g_h = 700, 700
    g = Image.new("RGBA", (g_w, g_h), C_CARBON + (255,))
    wm_s = make_watermark(size=280)
    g.paste(wm_s, ((g_w - wm_s.size[0]) // 2, (g_h - wm_s.size[1]) // 2), wm_s)
    dg = ImageDraw.Draw(g, "RGBA")
    dg.rectangle([(24, 24), (g_w - 24, g_h - 24)], outline=C_GOLD_BORDER, width=1)
    logo_s = load_logo(target_height=36)
    g.paste(logo_s, (52, 48), logo_s)
    draw_tracked(dg, (52, 114), cfg["gbp_kicker"], get_font(15, "demibold"), C_GOLD, tracking=1.8)
    f_gh = get_font(42, "demibold")
    gy = 148
    for ln in wrap_lines(dg, cfg["gbp_title"], f_gh, 596):
        dg.text((52, gy), ln, font=f_gh, fill=C_WHITE)
        gy += 50
    gy += 12
    dg.line([(52, gy), (142, gy)], fill=C_GOLD, width=2)
    gy += 20
    f_gb = get_font(25, "regular")
    for ln in wrap_lines(dg, cfg["gbp_body"], f_gb, 596):
        dg.text((52, gy), ln, font=f_gb, fill=C_PEARL)
        gy += 33
    dg.rounded_rectangle([(52, 464), (648, 566)], radius=14, fill=C_BOX_BG + (242,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(dg, (74, 482), "ATENDIMENTO EM PORTUGUÊS", get_font(14, "demibold"), C_GOLD_LIGHT, tracking=1.8)
    dg.text((74, 514), "Coordenação prévia pelo WhatsApp", font=get_font(23, "medium"), fill=C_WHITE)
    dg.line([(52, 592), (648, 592)], fill=C_GOLD_BORDER, width=1)
    dg.text((52, 608), "Fabricio Rivas · Escribano Público (SCJ 17058/5)", font=get_font(18, "medium"), fill=C_WHITE)
    dg.text((52, 636), "Punta del Este e Maldonado · +598 99 431 185", font=get_font(16, "regular"), fill=C_MUTED)
    p_gbp = os.path.join(out_dir, "gbp_700x700.jpg")
    g.convert("RGB").save(p_gbp, "JPEG", quality=92, optimize=True)
    generated.append(p_gbp)

    # Story 9:16 + Sticker Zone
    W, H = 1080, 1920
    s = Image.new("RGBA", (W, H), C_CARBON + (255,))
    s.paste(watermark, ((W - watermark.size[0]) // 2, 660), watermark)
    ds = ImageDraw.Draw(s, "RGBA")
    ds.rectangle([(64, 304), (W - 64, 1436)], outline=C_GOLD_BORDER, width=1)
    s.paste(logo, (104, 344), logo)
    draw_tracked(ds, (104, 464), cfg["story_kicker"], get_font(20, "demibold"), C_GOLD, tracking=2.2)
    f_sh = get_font(54, "demibold")
    sy = 516
    for ln in wrap_lines(ds, cfg["story_title"], f_sh, 856):
        ds.text((104, sy), ln, font=f_sh, fill=C_WHITE)
        sy += 66
    sy += 16
    ds.line([(104, sy), (214, sy)], fill=C_GOLD, width=3)
    sy += 32
    f_sb = get_font(33, "regular")
    for ln in wrap_lines(ds, cfg["story_body"], f_sb, 856):
        ds.text((104, sy), ln, font=f_sb, fill=C_PEARL)
        sy += 46
    ds.rounded_rectangle([(104, 1084), (W - 104, 1236)], radius=20, fill=C_BOX_BG + (210,), outline=C_GOLD, width=1)
    draw_tracked(ds, (236, 1144), cfg["story_sticker_hint"], get_font(20, "demibold"), C_GOLD_LIGHT, tracking=1.9)
    ds.line([(104, 1300), (W - 104, 1300)], fill=C_GOLD_BORDER, width=1)
    ds.text((104, 1320), "Fabricio Rivas · Escribano Público", font=get_font(27, "medium"), fill=C_WHITE)
    ds.text((104, 1358), "Matrícula SCJ 17058/5 · Punta del Este · +598 99 431 185", font=get_font(21, "regular"), fill=C_MUTED)
    p_story = os.path.join(out_dir, "story_sticker_1080x1920.jpg")
    s.convert("RGB").save(p_story, "JPEG", quality=92, optimize=True)
    generated.append(p_story)

    # WhatsApp Status 9:16 (Matriz 3B Bronce)
    w_im = Image.new("RGBA", (W, H), C_BRONZE + (255,))
    w_im.paste(watermark, ((W - watermark.size[0]) // 2, 660), watermark)
    dw = ImageDraw.Draw(w_im, "RGBA")
    dw.rectangle([(64, 304), (W - 64, 1436)], outline=C_GOLD_BORDER, width=1)
    w_im.paste(logo, (104, 344), logo)
    draw_tracked(dw, (104, 464), "TABELIÃO · PUNTA DEL ESTE", get_font(20, "demibold"), C_GOLD, tracking=2.2)
    wy = 516
    for ln in wrap_lines(dw, cfg["wa_title"], f_sh, 856):
        dw.text((104, wy), ln, font=f_sh, fill=C_WHITE)
        wy += 66
    wy += 16
    dw.line([(104, wy), (214, wy)], fill=C_GOLD, width=3)
    wy += 32
    for ln in wrap_lines(dw, cfg["wa_body"], f_sb, 856):
        dw.text((104, wy), ln, font=f_sb, fill=C_PEARL)
        wy += 46
    dw.rounded_rectangle([(104, 1058), (W - 104, 1236)], radius=18, fill=C_BOX_BG + (238,), outline=C_GOLD_BORDER, width=1)
    draw_tracked(dw, (140, 1086), "ATENDIMENTO EM PORTUGUÊS", get_font(19, "demibold"), C_GOLD_LIGHT, tracking=2.1)
    by = 1126
    for ln in wrap_lines(dw, "Envie seu documento pelo WhatsApp (+598 99 431 185) para conferência prévia.", get_font(27, "medium"), 792):
        dw.text((140, by), ln, font=get_font(27, "medium"), fill=C_WHITE)
        by += 37
    dw.line([(104, 1300), (W - 104, 1300)], fill=C_GOLD_BORDER, width=1)
    dw.text((104, 1320), "Fabricio Rivas · Escribano Público", font=get_font(27, "medium"), fill=C_WHITE)
    dw.text((104, 1358), "Matrícula SCJ 17058/5 · Punta del Este · +598 99 431 185", font=get_font(21, "regular"), fill=C_MUTED)
    p_wa = os.path.join(out_dir, "whatsapp_status_1080x1920.jpg")
    w_im.convert("RGB").save(p_wa, "JPEG", quality=92, optimize=True)
    generated.append(p_wa)

    # Reel 9:16 Typewriter + Audio V4 Instrumental + fade
    fps = 24
    total_dur = 12.5
    typing_dur = 9.2
    n_frames = int(round(total_dur * fps))
    typing_frames = int(round(typing_dur * fps))
    full_body = cfg["reel_body"]
    total_words = len(full_body.split(" "))
    out_mp4 = os.path.join(out_dir, "reel.mp4")
    p3s = os.path.join(out_dir, "preview_reel_3s.jpg")
    p11s = os.path.join(out_dir, "preview_reel_11s.jpg")

    def draw_reel_frame(wc: int) -> Image.Image:
        canvas = Image.new("RGBA", (W, H), C_CARBON + (255,))
        canvas.paste(watermark, ((W - watermark.size[0]) // 2, 660), watermark)
        draw = ImageDraw.Draw(canvas, "RGBA")
        draw.rectangle([(64, 304), (W - 64, 1436)], outline=C_GOLD_BORDER, width=1)
        canvas.paste(logo, (104, 344), logo)
        draw_tracked(draw, (104, 464), cfg["reel_kicker"], get_font(20, "demibold"), C_GOLD, tracking=2.1)
        f_rh = get_font(52, "demibold")
        ry = 516
        for ln in wrap_lines(draw, cfg["reel_title"], f_rh, 830):
            draw.text((104, ry), ln, font=f_rh, fill=C_WHITE)
            ry += 64
        ry += 16
        draw.line([(104, ry), (214, ry)], fill=C_GOLD, width=3)
        f_rb = get_font(34, "regular")
        wrapped = wrap_lines(draw, full_body, f_rb, 815)
        ty = ry + 34
        rem = max(0, wc)
        for ln in wrapped:
            if rem <= 0:
                break
            words = ln.split(" ")
            take = words[:rem]
            draw.text((104, ty), " ".join(take), font=f_rb, fill=C_PEARL)
            rem -= len(take)
            ty += 46
        box_y1, box_y2 = 1056, 1236
        draw.rounded_rectangle([(104, box_y1), (936, box_y2)], radius=18, fill=C_BOX_BG + (240,), outline=C_GOLD_BORDER, width=1)
        draw_tracked(draw, (138, box_y1 + 26), "ATENDIMENTO EM PORTUGUÊS", get_font(19, "demibold"), C_GOLD_LIGHT, tracking=2.1)
        by = box_y1 + 66
        for ln in wrap_lines(draw, "Envie o documento antes pelo WhatsApp (+598 99 431 185) para conferência.", get_font(27, "medium"), 760):
            draw.text((138, by), ln, font=get_font(27, "medium"), fill=C_WHITE)
            by += 37
        draw.line([(104, 1300), (936, 1300)], fill=C_GOLD_BORDER, width=1)
        draw.text((104, 1320), "Fabricio Rivas · Escribano Público", font=get_font(27, "medium"), fill=C_WHITE)
        draw.text((104, 1358), "Matrícula SCJ 17058/5 · Punta del Este · +598 99 431 185", font=get_font(21, "regular"), fill=C_MUTED)
        return canvas.convert("RGB")

    with tempfile.TemporaryDirectory() as tmpdir:
        cache = {}
        for i in range(n_frames):
            wc = total_words if i >= typing_frames else max(1, int(((i + 1) / typing_frames) * total_words))
            if wc not in cache:
                cache[wc] = draw_reel_frame(wc)
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

    generated.extend([p3s, p11s])
    for p in generated:
        luma = ImageStat.Stat(Image.open(p).convert("L")).mean[0]
        assert luma <= 39.0, f"Luma > 39 em {p}: {luma:.2f}"
        print(f"OK {cfg['folder']}/{os.path.basename(p)} | mean_luma={luma:.2f} | bytes={os.path.getsize(p)}")
    print(f"OK {cfg['folder']}/reel.mp4 | bytes={os.path.getsize(out_mp4)}")


PACKS = [
    {
        "folder": "tanda_4_brasil_imovel_pt",
        "s1_kicker": "CLIENTES BRASILEIROS · PUNTA DEL ESTE",
        "s1_title": "Vai comprar imóvel em Punta del Este?",
        "s1_sub": "Proteja o sinal na reserva e agilize a escritura antes do voo de volta ao Brasil.",
        "s1_box_kicker": "TABELIÃO NO URUGUAI (ESCRIBANO PÚBLICO)",
        "s1_box_text": "No Uruguai, o comprador escolhe o seu Tabelião.",
        "s2_kicker": "SEGURANÇA ANTES DE TRANSFERIR O SINAL",
        "s2_title": "Reserva e custódia de sinal (escrow)",
        "s2_boxes": [
            ("01 · Contrato de reserva revisado", "Cláusulas de prazo, forma de pagamento e devolução caso surja pendência no imóvel."),
            ("02 · Custódia de sinal com o Tabelião", "O valor fica protegido sob guarda notarial até a conferência completa dos registros."),
        ],
        "s3_kicker": "DUE DILIGENCE E PROCURAÇÃO NO URUGUAI",
        "s3_title": "Estudo de títulos antes da escritura",
        "s3_items": [
            ("01 · Títulos e registros públicos:", "Cadeia de escrituras, certidões em Maldonado e Montevidéu e ausência de ônus."),
            ("02 · Regularidade fiscal e de obra:", "Imposto municipal, despesas comuns, imposto primário, Catastro e BPS."),
            ("03 · Procuração antes do voo de volta:", "Lavrada no protocolo uruguaio: dispensa cartório BR, Apostila e tradução."),
        ],
        "s4_title": "Procuração assinada no Uruguai",
        "s4_body": "Poupa cartório brasileiro, Apostila de Haia e tradução pública.\n\nAtendimento em português. Coordenação prévia pelo WhatsApp no link da bio.",
        "gbp_kicker": "IMÓVEIS · PUNTA DEL ESTE",
        "gbp_title": "Comprar imóvel em Punta del Este",
        "gbp_body": "Reserva, custódia de sinal (escrow), estudo de títulos e procuração antes do voo de volta ao Brasil.",
        "story_kicker": "GUIA EM PORTUGUÊS · IMÓVEIS",
        "story_title": "Imóvel em Punta del Este",
        "story_body": "Proteja o sinal na reserva e deixe a procuração assinada no Uruguai antes do voo de volta ao Brasil.",
        "story_sticker_hint": "TOQUE NO LINK  ·  LER GUIA COMPLETO",
        "wa_title": "Vai comprar em Punta del Este?",
        "wa_body": "Revise o contrato de reserva, proteja o sinal em custódia e assine a procuração antes de voltar ao Brasil.",
        "reel_kicker": "IMÓVEIS · CLIENTES BRASILEIROS",
        "reel_title": "Vai comprar imóvel em Punta del Este?",
        "reel_body": "No Uruguai, o comprador escolhe o seu Tabelião. Revisamos o contrato de reserva, protegemos o sinal em custódia e lavramos sua procuração antes do voo de volta ao Brasil.",
    },
    {
        "folder": "tanda_5_brasil_cartorio_pt",
        "s1_kicker": "CARTÓRIO EM PUNTA DEL ESTE · TEMPORADA",
        "s1_title": "Precisa de Cartório em Punta del Este?",
        "s1_sub": "Reconhecimento de firma no mesmo dia, procurações, locação, autorização de menor, renda DNM e veículos.",
        "s1_box_kicker": "ATENDIMENTO EM PORTUGUÊS",
        "s1_box_text": "Coordenação prévia pelo WhatsApp em português.",
        "s2_kicker": "DOCUMENTOS PRÁTICOS NA TEMPORADA",
        "s2_title": "Firma no mesmo dia e procuração",
        "s2_boxes": [
            ("01 · Reconhecimento de firma no mesmo dia", "Mediante envio prévio do documento pelo WhatsApp para conferência antes da assinatura."),
            ("02 · Procurações e cartas poder", "Instrumentos ajustados à legislação uruguaia para bancos, imóveis e condomínios."),
        ],
        "s3_kicker": "LOCAÇÃO, FAMÍLIA, RESIDÊNCIA E BENS",
        "s3_title": "Outros atos para brasileiros",
        "s3_items": [
            ("01 · Locação e viagem de menor:", "Contratos de temporada ou anuais em Maldonado e autorização de viagem de menor."),
            ("02 · Certidão notarial de renda:", "Aceita na DNM e em bancos; conferimos antes o critério de seguradoras."),
            ("03 · Veículos e embarcações:", "Carta poder para circulação ou transferência definitiva com certidões."),
        ],
        "s4_title": "Conferência prévia pelo WhatsApp",
        "s4_body": "Atendimento direto em Punta del Este, com coordenação documental prévia à distância.\n\nAtendimento em português. Acesse o link na bio.",
        "gbp_kicker": "CARTÓRIO NO URUGUAI · PUNTA DEL ESTE",
        "gbp_title": "Cartório em Punta del Este",
        "gbp_body": "Reconhecimento de firma no mesmo dia, procuração, locação, viagem de menor, renda DNM e veículos.",
        "story_kicker": "GUIA EM PORTUGUÊS · TEMPORADA",
        "story_title": "Cartório em Punta del Este",
        "story_body": "Reconhecimento de firma no mesmo dia, procurações, contratos de locação, autorização de menor, renda e veículos.",
        "story_sticker_hint": "TOQUE NO LINK  ·  VER SERVIÇOS E GUIA",
        "wa_title": "Documentação em Punta del Este?",
        "wa_body": "Reconhecimento de firma no mesmo dia, procuração, locação, viagem de menor, renda DNM e veículos.",
        "reel_kicker": "CARTÓRIO EM PUNTA DEL ESTE",
        "reel_title": "Precisa de Cartório em Punta del Este?",
        "reel_body": "Reconhecimento de firma no mesmo dia, procuração, contrato de locação, autorização de viagem de menor, certidão notarial de renda para a DNM e transferência de veículos ou embarcações.",
    },
]


if __name__ == "__main__":
    logo = load_logo(56)
    wm = make_watermark(430)
    portrait = extract_clean_portrait(565)
    for cfg in PACKS:
        render_pack(cfg, logo, wm, portrait)
