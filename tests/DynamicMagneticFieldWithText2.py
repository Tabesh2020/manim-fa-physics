
from manim import *
from manim_fa_physics import *
from manim_fa import FaText


class DynamicMagneticFieldWithText(Scene):
    def construct(self):
        # ایجاد سیم به شکل خط
        wire = Line(LEFT*2, RIGHT*2, color=RED)
        self.add(wire)

        # ایجاد میدان مغناطیسی ثابت
        field = Rectangle(width=6, height=4, color=BLUE, fill_opacity=0.2)
        self.add(field)

        # تعریف updater سیم (چرخش)
        def rotate_wire(mobject, dt):
            mobject.rotate(0.5 * dt)

        wire.add_updater(rotate_wire)

        # اضافه کردن متن فارسی
        text = FaText(
            "سیم در میدان مغناطیسی در حال چرخش است",
            font="IRLotus",
            font_size=36
        ).to_edge(DOWN)
        self.add(text)

        # صحنه را برای 8 ثانیه نگه دارید تا انیمیشن دیده شود
        self.wait(8)

