from manim import *
from manim_fa_physics import *

class MultiPendulumDemo(SpaceScene):
    def construct(self):
        p = MultiPendulum(RIGHT, LEFT, RIGHT * 0.5)
        self.add(p)
        self.make_rigid_body(*p.bobs)
        p.start_swinging()
        self.wait(6)
