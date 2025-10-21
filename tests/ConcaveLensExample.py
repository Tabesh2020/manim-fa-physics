from manim import *
from manim_fa_physics import *

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
            self.play(Create(ray), run_time=1.5)
            self.wait(0.3)

        # افزودن متن برای توضیح
        text = Tex("عبور پرتوهای نور از عدسی واگرا", font_size=36).to_edge(DOWN)
        self.play(Write(text))

        # کمی مکث برای مشاهده نتیجه
        self.wait(2)
