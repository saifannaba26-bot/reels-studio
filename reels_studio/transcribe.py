"""Speech-to-text with word-level timestamps (faster-whisper)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Word:
    text: str
    start: float
    end: float


def transcribe(media_path: str, language: str = "ar", model_size: str = "small") -> list[Word]:
    """Return word-level timestamps for the speech in *media_path*."""
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="auto", compute_type="auto")
    segments, _ = model.transcribe(media_path, language=language, word_timestamps=True)
    words: list[Word] = []
    for seg in segments:
        for w in seg.words or []:
            words.append(Word(text=w.word.strip(), start=float(w.start), end=float(w.end)))
    return [w for w in words if w.text]


def group_words(words: list[Word], max_words: int = 3, max_gap: float = 0.6) -> list[list[Word]]:
    """Group words into short caption phrases, breaking on pauses."""
    groups: list[list[Word]] = []
    current: list[Word] = []
    for w in words:
        if current and (len(current) >= max_words or w.start - current[-1].end > max_gap):
            groups.append(current)
            current = []
        current.append(w)
    if current:
        groups.append(current)
    return groups
