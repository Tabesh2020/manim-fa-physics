# 🎬 manim-fa-physics

افزونه مانیم (مجموعه‌ای از ماژول‌های فیزیک) برای به تصویر کشیدن مفاهیم فیزیک از قبیل مکانیک، نور و الکترومغناطیس نوشته شده است.  
این افزونه یا پلاگین به شما امکان می‌دهد تا با خلق صحنه‌های دینامیک در قالب انیمیشن‌های ویدیویی مفاهیم فیزیک را به صورت بصری  آموزش دهید.

---

## 🔧 نحوه نصب پلاگین


```bash
pip install manim-fa-physics
```
 یا برای نصب محلی (در حالت توسعه):

```bash
pip install -e .
```
---


## 💡 مثال‌های آموزشی

### 🔹 مثال ۱ — حرکت آونگ ساده
```python
from manim import *
from manim_fa_physics import *

class PendulumDemo(SpaceScene):
    def construct(self):
        pend = Pendulum(length=3, initial_theta=0.4)
        self.add(pend)
        self.make_rigid_body(*pend.bobs)
        pend.start_swinging()
        self.add(TracedPath(pend.bobs[-1].get_center, stroke_color=BLUE))
        self.wait(5)

        
```
---
### 🔹 مثال ۲ — انتشار نور در عدسی‌های واگرا 
```python
from manim import *
from manim_fa_physics import *
from manim_fa import FaText

class ConcaveLensExampleDynamic(Scene):
    def construct(self):
        # ساخت عدسی واگرا
        lens = Lens(-4, 1, fill_opacity=0.4, color=BLUE).shift(RIGHT)
        self.play(FadeIn(lens))

        # تعریف پرتوها
        rays = [
            Ray(LEFT * 4 + UP * i, RIGHT, 8, [lens], color=YELLOW)
            for i in [0.6, 0.2, -0.2, -0.6]
        ]

        # نمایش تدریجی پرتوها
        for ray in rays:
            self.play(Create(ray), run_time=1.2)
            self.wait(0.2)

        # نمایش متن فارسی با فونت پیش‌فرض Vazirmatn
        text = FaText(
            "عبور پرتوهای نور از ==عدسی واگرا==",
            font_size=36
        )

        text.to_corner(UL)  # گوشه‌ی بالا چپ
        text.shift(RIGHT * 2 + DOWN * 2)

        # انیمیشن نوشتن متن
        self.play(Write(text))
        self.wait(2)

```
---
### 🔹 مثال ۳ — تغییرات میدان الکتریکی بارها
```python
from manim import *
from manim_fa_physics import *


class DynamicElectricFieldSceneII(Scene):
    

    def construct(self):
        # تعریف دو بار ثابت منفی در دو طرف صحنه
        neg_left = Charge(-1, LEFT * 3 + DOWN)
        neg_right = Charge(-1, RIGHT * 3 + DOWN)

        # تعریف یک بار مثبت متحرک
        pos_charge = Charge(2, ORIGIN + UP * 0.5)

        # ایجاد میدان الکتریکی اولیه بر اساس موقعیت فعلی بارها
        field = ElectricField(neg_left, neg_right, pos_charge)

        # افزودن اجزای صحنه
        self.add(neg_left, neg_right, pos_charge, field)

        # تابع به‌روزرسانی میدان برای هر فریم
        def update_field(field_obj):
            field_obj.become(ElectricField(neg_left, neg_right, pos_charge))

        field.add_updater(lambda f: update_field(f))

        # پویانمایی حرکت بار مثبت
        self.play(
            pos_charge.animate.shift(RIGHT * 4),
            run_time=5,
            rate_func=there_and_back,
        )

        # توقف آپدیت میدان و پایان
        field.remove_updater(lambda f: update_field(f))
        self.wait(2)

```

---
### 🔹 مثال ۴ — موج ایستاده روی تار
```python
from manim import *
from manim_fa_physics import *
from manim_fa import FaText

class StandingWaveExampleScene(Scene):
    def construct(self):
        title = FaText("موج ایستاده در **هارمونیک‌های** مختلف", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        wave1 = StandingWave(1)
        wave2 = StandingWave(2)
        wave3 = StandingWave(3)
        waves = VGroup(wave1, wave2, wave3)
        waves.arrange(DOWN).move_to(ORIGIN)
        self.add(waves)

        for wave in waves:
            wave.start_wave()
        self.wait(4)
```
---
### 🔹 مثال ۵ — میدان مغناطیسی دو آهنربای میله‌ای
```python
from manim import *
from manim_fa_physics import *
from manim_fa import FaText

class BarMagnetExample(Scene):
    def construct(self):
        bar1 = BarMagnet().rotate(PI / 2).shift(LEFT * 3.5)
        bar2 = BarMagnet().rotate(PI / 2).shift(RIGHT * 3.5)

        caption = FaText("خطوط میدان از قطب ==شمال== به قطب ==جنوب==", font_size=30)
        caption.to_edge(DOWN)

        self.add(BarMagneticField(bar1, bar2))
        self.play(FadeIn(bar1), FadeIn(bar2))
        self.play(Write(caption))
        self.wait(2)
```
---

## 🌀 فهرست کامل انیمیشن‌های کاربردی 

| نام انیمیشن / کلاس             | ماژول                     | توضیح فارسی                                                | کاربرد آموزشی                                           |
| ------------------------------ | ------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
| `MultiPendulum`                | pendulum.py               | یک سیستم چند نوسانی شامل چند وزنه متصل به هم               | شبیه‌سازی نوسان پیچیده چند وزنه‌ای                      |
| `Pendulum`                     | pendulum.py               | یک پاندول ساده با طول و زاویه اولیه قابل تنظیم             | نمایش حرکت نوسانی پاندول                                |
| `SpaceScene`                   | mechanics.py              | صحنه پایه برای اعمال مکانیک سخت و گرانش                    | ایجاد اشیاء صلب و ثابت، و اعمال نیروهای گرانشی و برخورد |
| `make_rigid_body`              | mechanics.py              | تبدیل یک Mobject به جسم متحرک با گرانش و برخورد            | نمایش حرکت واقعی اشیاء تحت گرانش                        |
| `make_static_body`             | mechanics.py              | تبدیل یک Mobject به جسم ثابت                               | ایجاد موانع و سطوح برخوردی                              |
| `Lens`                         | lenses.py                 | یک عدسی محدب یا مقعر با ضخامت و ضریب شکست مشخص             | شبیه‌سازی شکست نور و رفتار عدسی‌ها                      |
| `Ray`                          | rays.py                   | پرتو نور که می‌تواند از عدسی‌ها عبور کند و شکست شود        | نمایش عبور نور از عدسی‌ها و قوانین شکست نور             |
| `Charge`                       | electrostatics.py         | بار الکتریکی مثبت یا منفی با اثر میدان الکتریکی            | نمایش نقاط بار و تاثیر آن‌ها بر میدان الکتریکی          |
| `ElectricField`                | electrostatics.py         | میدان الکتریکی تولید شده توسط یک یا چند بار                | نمایش خطوط میدان الکتریکی و جهت نیرو                    |
| `Wire`                         | magnetostatics.py         | سیم حامل جریان الکتریکی                                    | شبیه‌سازی منابع میدان مغناطیسی                          |
| `MagneticField`                | magnetostatics.py         | میدان مغناطیسی تولید شده توسط سیم‌ها                       | نمایش خطوط میدان مغناطیسی و جهت نیرو                    |
| `Current`                      | magnetostatics.py         | جریان الکتریکی عمود بر صفحه (به سمت داخل یا بیرون)         | شبیه‌سازی منبع میدان مغناطیسی نقطه‌ای                   |
| `CurrentMagneticField`         | magnetostatics.py         | میدان مغناطیسی حاصل از یک یا چند جریان عمود بر صفحه        | نمایش خطوط میدان حول جریان‌های موازی                    |
| `BarMagnet`                    | magnetostatics.py         | آهنربای میله‌ای با قطب شمال و جنوب                          | نمایش دوقطبی مغناطیسی                                   |
| `BarMagneticField`             | magnetostatics.py         | میدان مغناطیسی حاصل از یک یا چند آهنربای میله‌ای            | نمایش خطوط میدان بین چند آهنربا                         |
| `LinearWave`                   | waves.py                  | موج سه‌بعدی که در یک جهت مشخص حرکت می‌کند                  | شبیه‌سازی انتشار موج تخت                                |
| `RadialWave`                   | waves.py                  | موج سه‌بعدی که به‌صورت شعاعی از یک یا چند منبع منتشر می‌شود | شبیه‌سازی تداخل امواج (مثل امواج آب)                    |
| `StandingWave`                 | waves.py                  | موج ایستاده دوبعدی با هارمونیک قابل تنظیم                  | نمایش هارمونیک‌های تار یا لوله صوتی                     |
| `TwoObjectsFalling`            | examples / mechanics      | سقوط دو جسم با برخورد و گرانش                              | نمایش حرکت آزاد و برخورد اشیاء تحت گرانش                |
| `DynamicElectricFieldAdvanced` | examples / electrostatics | نمایش میدان الکتریکی بارهای مثبت و منفی با آرروهای پویا    | مثال پیشرفته برای رفتار دینامیک میدان‌ها                |
| `DynamicEMFieldScene`          | examples / advanced       | ترکیب میدان‌های الکتریکی و مغناطیسی با حرکت بارها و سیم‌ها | شبیه‌سازی واقع‌گرایانه میدان‌های الکترومغناطیس          |


---


## 🧾 مجوز
این پروژه تحت مجوز **MIT** منتشر می‌شود.  
ساخته‌شده توسط علی تابش برای جامعه‌ی فارسی‌زبان Manim.

---

## 🤝 مشارکت
اگر پیشنهادی برای بهبود پلاگین، کلاس‌ها، تابع‌ها یا سازگاری با نسخه‌های جدید Manim دارید،  
Pull Request بسازید یا در بخش Issues مطرح کنید.
