
from manim import *
from manim_fa_physics import *
from manim_fa import FaText

class DynamicMagneticFieldWithText(Scene):
    def construct(self):
        # سیم عمودی در مرکز
        wire = Line(UP * 2, DOWN * 2, color=BLUE, stroke_width=4)
        self.add(wire)

        # تابع تولید میدان مغناطیسی
        def create_field():
            field = VGroup()
            for r in np.arange(0.5, 2.5, 0.5):
                circle = Circle(radius=r, color=YELLOW)
                field.add(circle)
            return field

        field = create_field()
        field.move_to(wire.get_center())
        self.add(field)

        # آپدیتور برای چرخش سیم
        def rotate_wire(mob, dt):
            mob.rotate(0.5 * dt)  # سرعت چرخش سیم

        wire.add_updater(rotate_wire)

        # آپدیتور برای به‌روزرسانی میدان مغناطیسی
        def update_field(mob, dt):
            mob.become(create_field())
            mob.move_to(wire.get_center())

        field.add_updater(update_field)

        # اضافه کردن متن فارسی با فونت IRLotus
        text = FaText(
            "میدان مغناطیسی حول سیم جریان‌دار",
            font="IRLotus",
            font_size=36
        ).to_edge(DOWN)
        self.add(text)

        # اجرای صحنه 8 ثانیه
        self.wait(8)
