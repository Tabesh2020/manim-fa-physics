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

        # نمایش متن فارسی با فونت IRLotus
        text = FaText(
            "عبور پرتوهای نور از عدسی واگرا",
            font="IRLotus",
            font_size=36
        )

        text.to_corner(UL)  # گوشه‌ی بالا چپ
        text.shift(RIGHT * 2 + DOWN * 2)

        # انیمیشن نوشتن متن
        self.play(Write(text))
        self.wait(2)
