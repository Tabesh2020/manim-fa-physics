from manim import *
from manim_fa_physics import *

class CollisionTest(SpaceScene):
    def construct(self):
        ball1 = Circle(radius=0.3, color=BLUE, fill_opacity=1).shift(LEFT)
        ball2 = Circle(radius=0.3, color=GREEN, fill_opacity=1).shift(RIGHT)
        self.make_rigid_body(ball1, ball2)
        ball1.body.apply_impulse_at_local_point((200, 0))
        self.add(ball1, ball2)
        self.wait(5)
