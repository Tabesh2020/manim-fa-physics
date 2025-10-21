from manim import *
from manim_fa_physics import *

class DipoleExample(Scene):
    def construct(self):
        q1 = Charge(1, LEFT)
        q2 = Charge(-1, RIGHT)
        q3 = Charge(-2, UP)
        field = ElectricField(q1, q2, q3)
        self.add(q1, q2, q3, field)
