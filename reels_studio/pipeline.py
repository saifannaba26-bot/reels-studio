"""End-to-end pipeline: raw video/audio -> finished vertical reel."""
from __future__ import annotations

import tempfile
from pathlib import Path

from .audio.beats import detect_beats
from .audio.sfx import plan_sfx
from .captions.renderer import write_captions
from .config import Config
from .editing.compositor import compose
from .editing.timeline import plan_cuts
from .media.keywords import extract_keywords
from .media.stock import fetch_clip
from .transcribe import transcribe
from .utils import ffmpeg as ff
from .voiceover import generate_voiceover


def make_reel(input_media: str, out_path: str = "output/reel.mp4",
              music: str | None = None, script: str | None = None,
              caption_style: str | None = None,
              config: Config | None = None,
              progress=print) -> Path:
    """Build a reel.

    input_media : source video (or audio) file.
    music       : background music track (beat-synced cuts when given).
    script      : text for the AI voiceover; when set, the voiceover replaces
                  the original audio and captions follow the voiceover.
    """
    cfg = config or Config.load()
    style_key = caption_style or cfg.caption_style
    work = Path(tempfile.mkdtemp(prefix="reels_pipeline_"))

    progress("1/6 استخراج الصوت والتفريغ...")
    narration_audio = input_media
    voiceover_path = None
    if script:
        progress("2/6 توليد التعليق الصوتي...")
        voiceover_path = str(work / "voiceover.mp3")
        generate_voiceover(script, voiceover_path, voice=cfg.voiceover_voice)
        narration_audio = voiceover_path

    words = transcribe(narration_audio, language=cfg.language,
                       model_size=cfg.whisper_model)
    if not words:
        raise RuntimeError("مفيش كلام اتكتشف في الملف - جرّب ملف فيه صوت واضح")

    progress("3/6 كشف الإيقاع وتخطيط القطع...")
    total = ff.duration(input_media)
    beats = detect_beats(music) if (music and cfg.beat_sync) else []
    segments = plan_cuts(total, beats)

    progress("4/6 مكتبة الصور والفيديو...")
    overlays = []
    if cfg.stock_enabled and (cfg.pexels_key or cfg.pixabay_key):
        for i, (t, kw) in enumerate(extract_keywords(words)):
            if len(overlays) >= 3:      # cap b-roll inserts per reel
                break
            clip = fetch_clip(kw, work / "stock", i,
                              pexels_key=cfg.pexels_key,
                              pixabay_key=cfg.pixabay_key)
            if clip:
                overlays.append((clip, t, min(3.0, total - t)))

    progress("5/6 الكابشن والمؤثرات...")
    ass = write_captions(words, style_key, work / "captions.ass",
                         cfg.width, cfg.height)
    sfx = plan_sfx([s.start for s in segments],
                   [s.zoom for s in segments], cfg.sfx_dir)

    progress("6/6 التجميع النهائي...")
    out = compose(input_media, segments, out_path,
                  captions_ass=ass, stock_overlays=overlays,
                  music=music, voiceover=voiceover_path,
                  sfx_events=sfx, music_volume=cfg.music_volume,
                  fps=cfg.fps)
    progress(f"تم! الريل جاهز: {out}")
    return out
