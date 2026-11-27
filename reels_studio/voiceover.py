"""Professional voiceover via edge-tts neural voices (free, Arabic included)."""
from __future__ import annotations

import asyncio

ARABIC_VOICES = {
    "salma": "ar-EG-SalmaNeural",      # مصرية، هادئة
    "hamed": "ar-SA-HamedNeural",      # سعودي، واثق
    "zariyah": "ar-SA-ZariyahNeural",  # سعودية، دافئة
    "layla": "ar-EG-ShakirNeural",     # مصري
}


def generate_voiceover(script: str, out_path: str, voice: str = "ar-EG-SalmaNeural",
                       rate: str = "+0%", pitch: str = "+0Hz") -> str:
    """Render *script* to an mp3 voiceover file. Returns out_path."""
    import edge_tts

    async def _run() -> None:
        tts = edge_tts.Communicate(script, voice, rate=rate, pitch=pitch)
        await tts.save(out_path)

    asyncio.run(_run())
    return out_path
