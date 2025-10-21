"""
نمایش میدان الکتریکی ناشی از چند بار مثبت و منفی
سازگار با manim v0.19.0 و نسخه‌ی جدید manim-physics
"""

from manim import *
from manim_fa_physics import *


class ElectricFieldExampleSceneII(Scene):
    """نمایش میدان الکتریکی ناشی از سه بار الکتریکی با علامت‌های مختلف"""
    def construct(self):
        # تعریف سه بار با مقادیر و موقعیت‌های متفاوت
        charge1 = Charge(-1, LEFT + DOWN)   # بار منفی
        charge2 = Charge(2, RIGHT + DOWN)   # بار مثبت قوی‌تر
        charge3 = Charge(-1, UP)            # بار منفی دیگر

        # ساخت میدان الکتریکی با تأثیر این بارها
        field = ElectricField(charge1, charge2, charge3)

        # افزودن بارها و میدان به صحنه
        self.add(charge1, charge2, charge3, field)
