"""
نمایش میدان مغناطیسی یک سیم دایروی حامل جریان ثابت
سازگار با manim v0.19.0 و manim_physics جدید
"""

from manim import *
from manim_fa_physics import *


class StaticMagneticFieldExample(ThreeDScene):
    """نمایش میدان مغناطیسی اطراف یک حلقه سیم"""

    def construct(self):
        # تعریف یک سیم دایروی که در جهت محور Z قرار دارد
        wire = Wire(Circle(radius=2).rotate(PI / 2, UP), current=1.5)

        # تعریف میدان مغناطیسی بر اساس موقعیت سیم
        field = MagneticField(
            wire,
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[0, 0, 1],  # دو‌بعدی روی صفحه xy
            length_func=lambda norm: 0.3 * np.tanh(norm),
            colors=[BLUE, GREEN, YELLOW],
        )

        # تنظیم زاویه دوربین برای دید سه‌بعدی
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        # افزودن سیم و میدان
        self.add(wire, field)

        # نمایش انیمیشن چرخش میدان
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(2)
