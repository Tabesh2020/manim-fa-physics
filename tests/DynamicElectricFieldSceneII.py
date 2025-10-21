"""
شبیه‌سازی پویای میدان الکتریکی با حرکت یک بار مثبت
سازگار با manim v0.19.0 و نسخه‌ی جدید manim-physics
"""

from manim import *
from manim_fa_physics import *


class DynamicElectricFieldSceneII(Scene):
    """نمایش میدان الکتریکی متغیر بر اثر حرکت یک بار مثبت در بین دو بار منفی"""

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
