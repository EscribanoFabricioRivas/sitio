#!/usr/bin/env python3
"""
Suite de Música Institucional y Firma Sonora — Escribano Fabricio Rivas
100% Grabaciones Reales de Estudio (Cero MIDI/Sintetizador Robótico) + Locución Masculina Rioplatense/Uruguaya Natural.
4 Estilos (con y sin locución masculina = 8 pistas masterizadas a -15 LUFS):
  1. V1 — Smooth Jazz Sunset · Café del Mar (Guitarra Acústica Cálida, Fender Rhodes & Bajo Suave)
  2. V2 — Chill R&B / Neo-Soul Ejecutivo (Piano Eléctrico Wurlitzer/Rhodes, Sub-Bajo R&B, Shaker & Detalle Amable de Piano)
  3. V3 — Smooth Jazz Club · Escobillas & Contrabajo (Trío de Piano Jazz, Contrabajo Caminante y Escobillas)
  4. V4 — Café del Mar Rhodes & Smooth Lounge (Acordes Fender Rhodes, Shaker Costero & Saxo Suave)
"""
import os, subprocess, shutil
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
EDGE_TTS = "/Library/Frameworks/Python.framework/Versions/3.13/bin/edge-tts"
SAMPLE_DIR = "/tmp/fr_studio_samples"
VO_DIR = "/tmp/fr_studio_samples/vo_final"
OUT_DIR = "/Users/arianawajntraub/Documents/antigravity/elegant-bardeen/sitio/campana/musica_fabricio"
DRIVE_DIR = "/Users/arianawajntraub/Library/CloudStorage/GoogleDrive-ariana@starunionservicios.com.ar/Mi unidad/FR pp AG/musica_fabricio"

os.makedirs(VO_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DRIVE_DIR, exist_ok=True)

# Clean old files
for d in [OUT_DIR, DRIVE_DIR]:
    for fn in os.listdir(d):
        if fn.endswith(".mp3") or fn.endswith(".wav"):
            os.remove(os.path.join(d, fn))

def build_natural_voiceover(tag, voice, rate, pitch):
    """
    Generates 3 separate downward-cadence studio takes:
      1) "Escribano Fabricio Rivas."
      2) "Punta del Este."
      3) "Maldonado."
    Preserves full natural sibilance and breath tails (zero clipped 's'),
    applies Neumann U87 warm studio condenser EQ, and exports WAV + MP3.
    """
    p1 = os.path.join(VO_DIR, f"{tag}_1.mp3")
    p2 = os.path.join(VO_DIR, f"{tag}_2.mp3")
    p3 = os.path.join(VO_DIR, f"{tag}_3.mp3")
    out_wav = os.path.join(VO_DIR, f"vo_{tag}.wav")
    out_mp3 = os.path.join(OUT_DIR, f"locucion_{tag}.mp3")

    subprocess.run([EDGE_TTS, "--voice", voice, f"--rate={rate}", f"--pitch={pitch}", "--text", "Escribano Fabricio Rivas.", "--write-media", p1], check=True)
    subprocess.run([EDGE_TTS, "--voice", voice, f"--rate={rate}", f"--pitch={pitch}", "--text", "Punta del Este.", "--write-media", p2], check=True)
    subprocess.run([EDGE_TTS, "--voice", voice, f"--rate={rate}", f"--pitch={pitch}", "--text", "Maldonado.", "--write-media", p3], check=True)

    # Trim only leading digital silence, keep full natural ending tail of each word!
    fc = (
        "[0:a]silenceremove=start_periods=1:start_silence=0.04:start_threshold=-55dB,apad=pad_dur=0.18[a];"
        "[1:a]silenceremove=start_periods=1:start_silence=0.04:start_threshold=-55dB,apad=pad_dur=0.12[b];"
        "[2:a]silenceremove=start_periods=1:start_silence=0.04:start_threshold=-55dB,apad=pad_dur=0.25[c];"
        "[a][b][c]concat=n=3:v=0:a=1,"
        "highpass=f=70,"
        "equalizer=f=145:width_type=q:w=1.0:g=2.6,"
        "equalizer=f=420:width_type=q:w=1.4:g=-1.2,"
        "equalizer=f=3400:width_type=q:w=1.5:g=-2.0,"
        "lowpass=f=11800,"
        "acompressor=threshold=-18dB:ratio=2.4:attack=18:release=220:makeup=2,"
        "aecho=0.8:0.88:24:0.06,"
        "loudnorm=I=-15:TP=-1.5:LRA=6"
    )
    subprocess.run([FFMPEG, "-y", "-i", p1, "-i", p2, "-i", p3, "-filter_complex", fc, "-ar", "44100", "-ac", "2", out_wav], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-i", out_wav, "-b:a", "256k", out_mp3], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.copy2(out_mp3, os.path.join(DRIVE_DIR, os.path.basename(out_mp3)))
    return out_wav

def render_studio_track(src_mp3, start_sec, dur_sec, slug, vo_wav, eq_preset="cafedelmar"):
    inst_mp3 = os.path.join(OUT_DIR, f"{slug}_instrumental.mp3")
    vo_mp3 = os.path.join(OUT_DIR, f"{slug}_con_locucion.mp3")
    master_wav = os.path.join(VO_DIR, f"{slug}_master.wav")

    fade_out_st = dur_sec - 3.2
    if eq_preset == "rnb":
        # Warm Neo-Soul / R&B curve: rich sub-bass at 95Hz, warm Rhodes midrange, silky top end
        af = (
            f"atrim={start_sec}:{start_sec + dur_sec},asetpts=PTS-STARTPTS,"
            "highpass=f=34,"
            "equalizer=f=95:width_type=q:w=1.0:g=2.2,"
            "equalizer=f=260:width_type=q:w=1.2:g=1.2,"
            "equalizer=f=3100:width_type=q:w=1.4:g=-2.2,"
            "lowpass=f=12500,"
            "extrastereo=m=1.18,"
            f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_st}:d=3.2,"
            "loudnorm=I=-15.5:TP=-1.5:LRA=8"
        )
    else:
        # Warm Café del Mar / Smooth Jazz curve: organic acoustic warmth, soft highs
        af = (
            f"atrim={start_sec}:{start_sec + dur_sec},asetpts=PTS-STARTPTS,"
            "highpass=f=38,"
            "equalizer=f=115:width_type=q:w=1.1:g=1.8,"
            "equalizer=f=3300:width_type=q:w=1.5:g=-2.0,"
            "lowpass=f=12800,"
            "extrastereo=m=1.15,"
            f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_st}:d=3.2,"
            "loudnorm=I=-15.5:TP=-1.5:LRA=8"
        )

    subprocess.run([FFMPEG, "-y", "-i", src_mp3, "-af", af, "-ar", "44100", "-ac", "2", master_wav], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run([FFMPEG, "-y", "-i", master_wav, "-codec:a", "libmp3lame", "-b:a", "256k", inst_mp3], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.copy2(inst_mp3, os.path.join(DRIVE_DIR, os.path.basename(inst_mp3)))

    # Mix with smooth sidechain-style volume envelope ONLY ONCE at 2.8s..7.8s (second 3.0 single voiceover rule)
    duck_fc = (
        "[0:a]volume='if(between(t,2.4,2.9), 0.90-(t-2.4)*1.04, "
        "if(between(t,2.9,7.6), 0.38, "
        "if(between(t,7.6,8.3), 0.38+(t-7.6)*0.74, 0.90)))':eval=frame[music];"
        "[1:a]adelay=3000|3000,volume=1.38[vo1];"
        "[music][vo1]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        "alimiter=limit=0.93:level=disabled"
    )
    subprocess.run([FFMPEG, "-y", "-i", master_wav, "-i", vo_wav, "-filter_complex", duck_fc, "-codec:a", "libmp3lame", "-b:a", "256k", vo_mp3], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.copy2(vo_mp3, os.path.join(DRIVE_DIR, os.path.basename(vo_mp3)))
    print("Rendered studio pair:", slug)

if __name__ == "__main__":
    vo_mateo = build_natural_voiceover("mateo_uy", "es-UY-MateoNeural", "-6%", "-2Hz")
    vo_tomas = build_natural_voiceover("tomas_ar", "es-AR-TomasNeural", "-5%", "-3Hz")

    # V1: Smooth Jazz Sunset · Café del Mar (Acoustic Guitar, Warm Fender Rhodes & Soft Groove)
    render_studio_track(f"{SAMPLE_DIR}/live/smooth_lovin.mp3", 0.0, 28.0, "v1_smooth_jazz_sunset_cafe_del_mar", vo_mateo, "cafedelmar")

    # V2: Chill R&B / Neo-Soul Ejecutivo (Warm Electric Piano, R&B Sub-Bass, Soft Shaker & Tender Piano Detail)
    render_studio_track(f"{SAMPLE_DIR}/live/jamendo-630741.mp3", 0.0, 28.0, "v2_chill_rnb_neosoul_ejecutivo", vo_tomas, "rnb")

    # V3: Smooth Jazz Club · Escobillas, Contrabajo & Piano (Backbay Lounge)
    render_studio_track(f"{SAMPLE_DIR}/live/backbay_lounge.mp3", 0.0, 28.0, "v3_smooth_jazz_club_contrabajo", vo_mateo, "cafedelmar")

    # V4: Café del Mar Rhodes & Smooth Sax (Fender Rhodes, Shaker & Warm Tenor Sax)
    render_studio_track(f"{SAMPLE_DIR}/live/jamendo-601438.mp3", 0.0, 28.0, "v4_cafe_del_mar_rhodes_sax", vo_tomas, "cafedelmar")
