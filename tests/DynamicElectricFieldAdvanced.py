from manim import *
from manim_fa_physics import Charge
import numpy as np

class DynamicElectricFieldAdvanced(Scene):
    """
    نمایش میدان الکتریکی بارهای مثبت و منفی با حرکت،
    با آرروهای پویا و روان.
    """

    def construct(self):
        # تعریف بارها
        charges = [
            Charge(-1, LEFT + DOWN),
            Charge(2, RIGHT + DOWN),
            Charge(-1, UP)
        ]

        # نمایش بارها
        for charge in charges:
            self.add(charge)

        # grid نقاط آرروها
        x_range = np.linspace(-5, 5, 25)
        y_range = np.linspace(-3, 3, 18)
        field_points = np.array([[x, y, 0] for x in x_range for y in y_range])

        # ایجاد آرروها
        arrows = VGroup()
        for p in field_points:
            arr = Arrow(start=p, end=p + 0.1 * RIGHT, buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.3)
            arrows.add(arr)
        self.add(arrows)

        # تابع به‌روزرسانی آرروها
        def update_field(arrows, dt):
            for i, arr in enumerate(arrows):
                p = field_points[i]
                v = np.zeros(3)
                for charge in charges:
                    r = p - charge.get_center()
                    dist = np.linalg.norm(r)
                    if dist < 0.1:  # جلوگیری از تقسیم بر صفر
                        continue
                    v += charge.magnitude / dist**2 * (r / dist)
                # طول آررو حداقل 0.05 برای جلوگیری از لرزش
                if np.linalg.norm(v) > 1e-6:
                    arr.put_start_and_end_on(p, p + 0.3 * normalize(v))
                else:
                    arr.put_start_and_end_on(p, p + 0.05 * RIGHT)

        # اضافه کردن آپدیت کننده آرروها
        arrows.add_updater(update_field)

        # حرکت بارها و همزمان به‌روزرسانی آرروها
        def move_charges(dt):
            for charge in charges:
                # حرکت همزمان به سمت راست و بالا/پایین برای مثال
                charge.shift(0.3 * dt * RIGHT + 0.2 * dt * UP)

        self.add_updater(move_charges)

        # اجرای صحنه برای 3 ثانیه
        self.wait(3)
