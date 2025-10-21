from manim import *
from manim_fa_physics import *

class ParallelWires(ThreeDScene):
    def construct(self):
        wire1 = Wire(Line(UP*2, DOWN*2).shift(LEFT), current=1)
        wire2 = Wire(Line(UP*2, DOWN*2).shift(RIGHT), current=-1)
        field = MagneticField(wire1, wire2, x_range=[-3, 3], y_range=[-3, 3])
        self.set_camera_orientation(phi=PI/3, theta=PI/3)
        self.add(wire1, wire2, field)
