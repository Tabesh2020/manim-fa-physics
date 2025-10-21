from manim import *
from manim_fa_physics import *

class PendulumDemo(SpaceScene):
    def construct(self):
        pend = Pendulum(length=3, initial_theta=0.4)
        self.add(pend)
        self.make_rigid_body(*pend.bobs)
        pend.start_swinging()
        self.add(TracedPath(pend.bobs[-1].get_center, stroke_color=BLUE))
        self.wait(5)
