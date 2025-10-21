from manim import *
from manim_fa_physics import *

class CircularWireField(ThreeDScene):
    def construct(self):
        wire = Wire(Circle(2).rotate(PI/2, UP))
        field = MagneticField(wire, x_range=[-3, 3], y_range=[-3, 3])
        self.set_camera_orientation(phi=PI/3, theta=PI/4)
        self.add(wire, field)
