from manim import *
from manim_fa_physics import *

class MagneticFieldExample(ThreeDScene):
    def construct(self):
        wire = Wire(Circle(2).rotate(PI / 2, UP))
        mag_field = MagneticField(
            wire,
            x_range=[-4, 4],
            y_range=[-4, 4],
        )
        self.set_camera_orientation(PI / 3, PI / 4)
        self.add(wire, mag_field)
