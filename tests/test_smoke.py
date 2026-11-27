"""Smoke tests that need no heavy dependencies."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reels_studio.transcribe import Word
from reels_studio.captions.renderer import write_captions
from reels_studio.captions.styles import STYLE_ORDER, STYLES
from reels_studio.editing.timeline import plan_cuts
from reels_studio.editing.zoom import zoom_filter
from reels_studio.media.keywords import extract_keywords
from reels_studio.config import Config


def test_all_seven_styles_render(tmp_path):
    words = [Word("كلمة", i * 0.4, i * 0.4 + 0.35) for i in range(9)]
    for key in STYLE_ORDER:
        out = write_captions(words, key, tmp_path / f"{key}.ass")
        assert "Dialogue" in out.read_text(encoding="utf-8")
    assert len(STYLE_ORDER) == 7


def test_plan_cuts_on_beats():
    beats = [0.8, 1.6, 2.4, 3.2, 4.0, 5.0, 6.0, 7.0, 8.0]
    segs = plan_cuts(9.0, beats)
    assert segs[0].start == 0.0
    assert abs(segs[-1].end - 9.0) < 0.01
    assert all(s.end > s.start for s in segs)


def test_zoom_filters():
    for kind in ["punch", "slow_in", "slow_out", "shake", "still"]:
        assert "zoompan" in zoom_filter(kind, 60)


def test_keywords_skip_stopwords():
    words = [Word("في", 0, 0.2), Word("المونتاج", 0.2, 0.6), Word("على", 0.6, 0.8)]
    pairs = extract_keywords(words, per_window=3)
    assert pairs and pairs[0][1] == "المونتاج"


def test_config_defaults():
    cfg = Config.load()
    assert cfg.width == 1080 and cfg.height == 1920 and cfg.language == "ar"
