from manim import *
from manim_fa_physics import *

class TwoObjectsFalling(SpaceScene):
    """
    این صحنه دو جسم را در محیط فیزیکی (با گرانش) رها می‌کند.
    - دایره (قرمز) و مربع (زرد) هر دو جسم صلب هستند.
    - زمین و دیواره‌ها به‌صورت ثابت تعریف شده‌اند.
    """

    def construct(self):
        # ساخت زمین و دیواره‌ها
        ground = Line([-4, -3.5, 0], [4, -3.5, 0])
        wall_left = Line([-4, -3.5, 0], [-4, 3.5, 0])
        wall_right = Line([4, -3.5, 0], [4, 3.5, 0])
        walls = VGroup(ground, wall_left, wall_right)
        self.add(walls)

        # ایجاد یک دایره قرمز (جسم متحرک)
        circle = Circle(radius=0.5, color=RED)
        circle.set_fill(RED, opacity=1)
        circle.move_to(RIGHT + UP)

        # ایجاد یک مربع زرد (جسم متحرک)
        rect = Square(side_length=1, color=YELLOW)
        rect.rotate(PI / 4)
        rect.set_fill(YELLOW_A, opacity=1)
        rect.move_to(UP * 2)

        # نمایش اولیهٔ اجسام با انیمیشن ترسیم
        self.play(DrawBorderThenFill(circle), DrawBorderThenFill(rect))
        self.wait(0.5)

        # تعریف اجسام متحرک و ثابت برای شبیه‌سازی فیزیکی
        self.make_rigid_body(circle, rect)  # این اجسام با گرانش حرکت خواهند کرد
        self.make_static_body(walls)        # این اجسام ثابت خواهند ماند (زمین و دیواره‌ها)

        # اجرای شبیه‌سازی فیزیکی برای چند ثانیه
        self.wait(5)
