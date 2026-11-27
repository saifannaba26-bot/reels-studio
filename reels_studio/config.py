"""Configuration loading for Reels Studio."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DEFAULTS = {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "language": "ar",
    "caption_style": "hormozi",
    "zoom_style": "mixed",          # mixed | punch | slow | shake | none
    "beat_sync": True,
    "stock_enabled": True,
    "stock_provider": "pexels",     # pexels | pixabay
    "voiceover_voice": "ar-EG-SalmaNeural",
    "music_volume": 0.18,
    "sfx_volume": 0.5,
    "whisper_model": "small",
    "fonts_dir": "assets/fonts",
    "sfx_dir": "assets/sfx",
}


@dataclass
class Config:
    values: dict = field(default_factory=lambda: dict(DEFAULTS))

    @classmethod
    def load(cls, path: str | os.PathLike | None = None) -> "Config":
        values = dict(DEFAULTS)
        if path and Path(path).exists():
            with open(path, "r", encoding="utf-8") as fh:
                user = yaml.safe_load(fh) or {}
            values.update(user)
        return cls(values)

    def __getattr__(self, item):
        try:
            return self.values[item]
        except KeyError as exc:
            raise AttributeError(item) from exc

    @property
    def pexels_key(self) -> str | None:
        return os.environ.get("PEXELS_API_KEY")

    @property
    def pixabay_key(self) -> str | None:
        return os.environ.get("PIXABAY_API_KEY")
