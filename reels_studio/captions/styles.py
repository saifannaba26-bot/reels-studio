"""The 7 Arabic caption styles.

Each style is an ASS style block plus rendering hints. libass shapes and
orders Arabic correctly, so we pass logical-order Unicode text.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CaptionStyle:
    key: str
    name_ar: str
    font: str = "Cairo"
    font_size: int = 64
    primary: str = "&H00FFFFFF"     # ASS BGR
    highlight: str = "&H0000D7FF"   # word-by-word highlight color
    outline: str = "&H00000000"
    outline_w: float = 3.0
    shadow: float = 1.0
    bold: bool = True
    alignment: int = 2              # 2 = bottom-center, 8 = top-center, 5 = mid
    margin_v: int = 220
    karaoke: bool = False           # word-by-word sweep highlight
    pop_in: bool = False            # scale-in animation per group
    uppercase_latin: bool = False
    behind_person: bool = False     # needs person mask; falls back gracefully
    numbers_mode: bool = False      # big animated numbers for lists
    notes: str = ""


STYLES: dict[str, CaptionStyle] = {
    # 1) هورموزي: كلمات كبيرة، تلوين كلمة-بكلمة، منتصف الشاشة
    "hormozi": CaptionStyle(
        key="hormozi", name_ar="هورموزي", font_size=84, alignment=5, margin_v=0,
        karaoke=True, pop_in=True, outline_w=4.0,
        notes="كلمة-بكلمة في نص الشاشة مع هايلايت أصفر",
    ),
    # 2) ميستر بيست: سميك جداً، حدود ضخمة، ألوان صارخة
    "mrbeast": CaptionStyle(
        key="mrbeast", name_ar="ميستر بيست", font_size=92, alignment=5, margin_v=0,
        primary="&H0000D7FF", highlight="&H000000FF", outline_w=7.0, shadow=2.0,
        karaoke=True, pop_in=True,
        notes="أصفر بحدود سوداء ضخمة وهايلايت أحمر",
    ),
    # 3) نص ورا الشخص: يحتاج ماسك للشخص (اختياري عبر rembg)
    "behind_person": CaptionStyle(
        key="behind_person", name_ar="نص ورا الشخص", font_size=78, alignment=5,
        margin_v=0, behind_person=True, outline_w=3.5,
        notes="الكابشن يظهر خلف الشخص (يحتاج rembg، وإلا يرجع لستايل عادي)",
    ),
    # 4) بودكاست: سطرين هادئين أسفل الشاشة
    "podcast": CaptionStyle(
        key="podcast", name_ar="بودكاست", font_size=54, alignment=2, margin_v=180,
        karaoke=False, pop_in=False, bold=False, outline_w=2.0,
        notes="هادئ وواضح لمحتوى البودكاست",
    ),
    # 5) سينمائي: خط رفيع، مسافات، أسفل مثل الترجمة السينمائية
    "cinematic": CaptionStyle(
        key="cinematic", name_ar="سينمائي", font="Amiri", font_size=50,
        alignment=2, margin_v=140, bold=False, outline_w=1.2, shadow=0.0,
        primary="&H00F0F0F0",
        notes="إحساس ترجمة الأفلام",
    ),
    # 6) موشن 3D: دخول بحركة وتكبير (محاكاة ثلاثية الأبعاد)
    "motion3d": CaptionStyle(
        key="motion3d", name_ar="موشن 3D", font_size=88, alignment=5, margin_v=0,
        karaoke=True, pop_in=True, outline_w=5.0,
        primary="&H00FFFFFF", highlight="&H00FFAA00",
        notes="دخول بحركة سينمائية ودوران خفيف",
    ),
    # 7) أرقام: أرقام قوائم كبيرة متحركة
    "numbers": CaptionStyle(
        key="numbers", name_ar="أرقام", font_size=80, alignment=5, margin_v=0,
        karaoke=False, pop_in=True, numbers_mode=True,
        highlight="&H0000D7FF",
        notes="يكبّر الأرقام في الكلام (٣ نصائح، رقم ١...)",
    ),
}

STYLE_ORDER = ["hormozi", "mrbeast", "behind_person", "podcast",
               "cinematic", "motion3d", "numbers"]
