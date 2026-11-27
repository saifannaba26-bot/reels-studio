"""Stock image/video library: Pexels and Pixabay, inserted when the speech needs it."""
from __future__ import annotations

import os
from pathlib import Path

import requests

PEXELS_SEARCH = "https://api.pexels.com/videos/search"
PIXABAY_SEARCH = "https://pixabay.com/api/videos/"


def _pexels(query: str, key: str) -> str | None:
    r = requests.get(PEXELS_SEARCH, headers={"Authorization": key},
                     params={"query": query, "per_page": 3, "orientation": "portrait"},
                     timeout=20)
    r.raise_for_status()
    videos = r.json().get("videos", [])
    if not videos:
        return None
    files = sorted(videos[0]["video_files"], key=lambda f: abs(f.get("height", 0) - 1920))
    return files[0]["link"]


def _pixabay(query: str, key: str) -> str | None:
    r = requests.get(PIXABAY_SEARCH,
                     params={"key": key, "q": query, "per_page": 3, "orientation": "vertical"},
                     timeout=20)
    r.raise_for_status()
    hits = r.json().get("hits", [])
    if not hits:
        return None
    videos = hits[0]["videos"]
    best = videos.get("large") or videos.get("medium") or videos.get("small")
    return best["url"] if best else None


def fetch_clip(query: str, out_dir: str | Path, index: int,
               pexels_key: str | None = None, pixabay_key: str | None = None) -> Path | None:
    """Download one stock clip for *query*. Returns the file path or None."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    url = None
    if pexels_key:
        try:
            url = _pexels(query, pexels_key)
        except requests.RequestException:
            url = None
    if url is None and pixabay_key:
        try:
            url = _pixabay(query, pixabay_key)
        except requests.RequestException:
            url = None
    if url is None:
        return None
    out = out_dir / f"stock_{index:03d}.mp4"
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out, "wb") as fh:
            for chunk in r.iter_content(1 << 20):
                fh.write(chunk)
    return out
