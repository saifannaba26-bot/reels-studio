# 🎬 استوديو ريلز (Reels Studio)

مونتاج ريلز عربي تلقائي بالكامل — من غير ما تكتب ولا سطر كود.

ارفع فيديو، اختار ستايل الكابشن، واستلم ريل عمودي جاهز للنشر.

## المميزات

- 🥁 **مونتاج على الإيقاع**: القطع بينزل على ضربات الموسيقى، مع زوم متنوع (بانش، زوم بطيء، شيك) ومؤثرات صوتية عند كل قطع.
- ✍️ **٧ ستايلات كابشن عربي**: هورموزي، ميستر بيست، نص ورا الشخص، بودكاست، سينمائي، موشن 3D، وأرقام.
- 🎨 **موشن جرافيك**: لور ثيرد متحرك، شريط تقدم، ولمسات عمق ثلاثي الأبعاد.
- 🖼️ **مكتبة صور وفيديوهات**: بتركّب لقطات من Pexels/Pixabay وقت ما الكلام يحتاجها تلقائياً.
- 🔊 **تعليق صوتي احترافي**: اكتب النص والاستوديو يولّده بصوت عربي طبيعي (مجاناً عبر edge-tts).
- 🗣️ **تفريغ كلام تلقائي**: Whisper بيطلّع توقيت كل كلمة عشان الكابشن يتحرك كلمة-بكلمة.

## التشغيل (أسهل طريقة - Docker)

```bash
docker compose up --build
```

وافتح http://localhost:7860 — واجهة عربية كاملة، ارفع واختار واستلم.

## التشغيل بدون Docker

```bash
pip install -r requirements.txt
bash scripts/download_assets.sh     # خطوط عربي + مؤثرات صوتية
python -m reels_studio.app          # الواجهة
```

أو من سطر الأوامر:

```bash
python -m reels_studio.cli video.mp4 --music beat.mp3 --style hormozi -o output/reel.mp4
python -m reels_studio.cli video.mp4 --script "النص بتاعك هنا" --style numbers
```

## مكتبة الصور والفيديو (اختياري)

سجّل مجاناً في [Pexels](https://www.pexels.com/api/) أو [Pixabay](https://pixabay.com/api/docs/) وحط المفتاح:

```bash
export PEXELS_API_KEY=مفتاحك
```

من غير مفتاح الاستوديو شغال عادي، بس من غير لقطات إضافية.

## ستايلات الكابشن السبعة

| الستايل | الوصف |
|---|---|
| `hormozi` | كلمات كبيرة في نص الشاشة، هايلايت كلمة-بكلمة |
| `mrbeast` | أصفر بحدود سوداء ضخمة وطاقة عالية |
| `behind_person` | النص يظهر خلف الشخص (يحتاج `pip install rembg`) |
| `podcast` | سطرين هادئين أسفل الشاشة |
| `cinematic` | إحساس ترجمة الأفلام بخط أميري |
| `motion3d` | دخول بحركة ودوران خفيف |
| `numbers` | يكبّر الأرقام في الكلام للقوائم |

التفاصيل في [docs/CAPTION_STYLES.md](docs/CAPTION_STYLES.md).

## إعدادات

انسخ `config.example.yaml` لـ `config.yaml` وعدّل براحتك (الأبعاد، الصوت، الستايل الافتراضي...).

## بنية المشروع

```
reels_studio/
  pipeline.py        # الخط الكامل من الفيديو الخام للريل
  transcribe.py      # تفريغ Whisper بتوقيت الكلمات
  voiceover.py       # تعليق صوتي عربي
  audio/beats.py     # كشف الإيقاع
  audio/sfx.py       # المؤثرات الصوتية
  captions/styles.py # الـ ٧ ستايلات
  captions/renderer.py
  editing/timeline.py  # خطة القطع على الإيقاع
  editing/zoom.py      # الزومات
  editing/compositor.py# تجميع ffmpeg
  media/stock.py     # مكتبة Pexels/Pixabay
  media/keywords.py  # استخراج الكلمات المفتاحية من الكلام
  graphics/          # موشن جرافيك ولمسات 3D
```

## ملاحظات

- العربي بيترندر صح (RTL + تشكيل) عبر libass وخطوط Cairo/Amiri.
- المؤثرات الصوتية المرفقة مولّدة كبداية — حط باكدجك في `assets/sfx/` بنفس الأسماء.
- كل المونتاج بيتم بـ ffmpeg، مفيش خدمات مدفوعة إلا لو حبيت مكتبة ستوك.

## English

Arabic-first automatic Reels studio: beat-synced cuts, 7 Arabic caption styles, stock b-roll, AI voiceover, motion graphics. Docker or `python -m reels_studio.app` for the UI. MIT licensed.
