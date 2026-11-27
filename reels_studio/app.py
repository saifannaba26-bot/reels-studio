"""Web UI for non-coders: upload a video, pick a style, get a reel.

Run:  python -m reels_studio.app   then open http://localhost:7860
"""
from __future__ import annotations

import gradio as gr

from .captions.styles import STYLES, STYLE_ORDER
from .config import Config
from .pipeline import make_reel


def build(video, music, script, style_key, beat_sync, stock_on):
    if video is None:
        raise gr.Error("ارفع فيديو الأول")
    cfg = Config.load()
    cfg.values["beat_sync"] = bool(beat_sync)
    cfg.values["stock_enabled"] = bool(stock_on)
    logs: list[str] = []
    out = make_reel(video, out_path="output/reel_ui.mp4",
                    music=music or None, script=script or None,
                    caption_style=style_key, config=cfg,
                    progress=lambda m: logs.append(m))
    return str(out), "\n".join(logs)


style_choices = [(f"{STYLES[k].name_ar} - {STYLES[k].notes}", k) for k in STYLE_ORDER]

RTL_CSS = """
.gradio-container { direction: rtl; text-align: right; }
.gradio-container textarea, .gradio-container input[type=text] { direction: rtl; text-align: right; }
"""

with gr.Blocks(title="استوديو ريلز", css=RTL_CSS) as demo:
    gr.Markdown("# 🎬 استوديو ريلز\nارفع الفيديو، اختار ستايل الكابشن، واستلم الريل جاهز.")
    with gr.Row():
        with gr.Column():
            video = gr.Video(label="الفيديو الأساسي")
            music = gr.Audio(label="موسيقى خلفية (اختياري - القطع على الإيقاع)", type="filepath")
            script = gr.Textbox(label="نص التعليق الصوتي (اختياري - صوت AI احترافي)",
                                lines=4, placeholder="اكتب النص هنا لو عايز تعليق صوتي...")
            style = gr.Radio(choices=style_choices, value="hormozi", label="ستايل الكابشن")
            with gr.Row():
                beat = gr.Checkbox(value=True, label="قطع على الإيقاع 🥁")
                stock = gr.Checkbox(value=True, label="صور وفيديوهات من المكتبة 🖼️")
            go = gr.Button("🚀 اعمل الريل", variant="primary")
        with gr.Column():
            result = gr.Video(label="الريل الجاهز")
            log = gr.Textbox(label="الخطوات", lines=8, interactive=False)
    go.click(build, inputs=[video, music, script, style, beat, stock],
             outputs=[result, log])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
