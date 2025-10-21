"""
نمایش تغییر میدان مغناطیسی در اثر حرکت یک سیم راست حامل جریان
سازگار با manim v0.19.0 و manim_physics جدید
"""

from manim import *
from manim_fa_physics import *


class DynamicMagneticFieldSceneII(ThreeDScene):
    """سیم حامل جریان حرکت می‌کند و میدان مغناطیسی به‌صورت زنده تغییر می‌کند"""

    def construct(self):
        # تعریف یک سیم راست حامل جریان
        wire = Wire(Line(LEFT * 3, RIGHT * 3), current=2.0)

        # ایجاد میدان اولیه
        field = MagneticField(
            wire,
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 0, 1],
            colors=[BLUE, GREEN, YELLOW],
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(wire, field)

        # تابع برای به‌روزرسانی میدان در هر فریم
        def update_field(field_obj):
            field_obj.become(
                MagneticField(
                    wire,
                    x_range=[-5, 5, 1],
                    y_range=[-3, 3, 1],
                    z_range=[0, 0, 1],
                    colors=[BLUE, GREEN, YELLOW],
                )
            )

        field.add_updater(lambda f: update_field(f))

        # حرکت سیم در محور y برای شبیه‌سازی تغییر میدان
        self.play(wire.animate.shift(UP * 2), run_time=3)
        self.play(wire.animate.shift(DOWN * 4), run_time=3)
        self.play(wire.animate.shift(UP * 2), run_time=3)

        # حذف آپدیت و پایان
        field.remove_updater(lambda f: update_field(f))
        self.wait(2)
