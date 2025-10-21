from manim import *
from manim_fa_physics import *

class MultipleCharges(Scene):
    def construct(self):
        charges = [
            Charge(2, UP * 2),
            Charge(-1, DOWN),
            Charge(1.5, LEFT * 2),
        ]
        field = ElectricField(*charges)
        self.add(*charges, field)
