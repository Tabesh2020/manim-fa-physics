r"""پاندول‌ها.

کلاس‌های :class:`~MultiPendulum` و :class:`~Pendulum` هر دو از ویژگی
:py:mod:`~rigid_mechanics` منشعب شده‌اند.

"""

from __future__ import annotations
from typing import Iterable, Optional
from functools import partial

from manim import VGroup, Mobject, Line, Circle, UP, DOWN, RIGHT, np
from manim.utils.color import ORANGE
import pymunk

from .mechanics import SpaceScene

__all__ = [
    "Pendulum",
    "MultiPendulum",
    "SpaceScene",
]


class MultiPendulum(VGroup):
    def __init__(
        self,
        *bobs: Iterable[np.ndarray],
        pivot_point: np.ndarray = UP * 2,
        rod_style: Optional[dict] = None,
        bob_style: Optional[dict] = None,
        **kwargs,
    ) -> None:
        """یک چندپاندول.

        پارامترها
        ----------
        bobs
            موقعیت توپ‌های پاندول.
        pivot_point
            نقطه اتکا یا محور پاندول.
        rod_style
            پارامترهای مربوط به خطوط اتصال.
        bob_style
            پارامترهای مربوط به توپ‌ها (Circle).
        kwargs
            پارامترهای اضافی برای VGroup.

        مثال
        -------
        .. manim:: MultiPendulumExample
            :quality: low

            from manim_physics import *

            class MultiPendulumExample(SpaceScene):
                def construct(self):
                    p = MultiPendulum(RIGHT, LEFT)
                    self.add(p)
                    self.make_rigid_body(*p.bobs)
                    p.start_swinging()
                    self.add(TracedPath(p.bobs[-1].get_center, stroke_color=BLUE))
                    self.wait(10)
        """
        if rod_style is None:
            rod_style = {}
        if bob_style is None:
            bob_style = {"radius": 0.1, "color": ORANGE, "fill_opacity": 1}

        self.pivot_point = pivot_point
        self.bobs = VGroup(*[Circle(**bob_style).move_to(i) for i in bobs])
        self.pins = [pivot_point] + list(bobs)
        self.rods = VGroup()
        self.rods.add(Line(self.pivot_point, self.bobs[0].get_center(), **rod_style))
        self.rods.add(
            *(
                Line(self.bobs[i].get_center(), self.bobs[i + 1].get_center(), **rod_style)
                for i in range(len(bobs) - 1)
            )
        )

        super().__init__(**kwargs)
        self.add(self.rods, self.bobs)

    def _make_joints(
        self, mob1: Mobject, mob2: Mobject, spacescene: SpaceScene
    ) -> None:
        a = mob1.body
        if isinstance(mob2, np.ndarray):
            b = pymunk.Body(body_type=pymunk.Body.STATIC)
            b.position = mob2[0], mob2[1]
        else:
            b = mob2.body
        joint = pymunk.PinJoint(a, b)
        spacescene.space.space.add(joint)

    def _redraw_rods(self, mob: Line, pins, i):
        try:
            x, y, _ = pins[i]
        except:
            x, y = pins[i].body.position
        x1, y1 = pins[i + 1].body.position
        mob.put_start_and_end_on(
            np.array([x, y, 0]),
            np.array([x1, y1, 0]),
        )

    def start_swinging(self) -> None:
        """شروع حرکت پاندول‌ها."""
        spacescene: SpaceScene = self.bobs[0].spacescene
        pins = [self.pivot_point] + list(self.bobs)

        for i in range(len(pins) - 1):
            self._make_joints(pins[i + 1], pins[i], spacescene)
            # استفاده از partial برای جلوگیری از ارور lambda در حلقه
            self.rods[i].add_updater(partial(self._redraw_rods, pins=pins, i=i))

    def end_swinging(self) -> None:
        """توقف حرکت پاندول‌ها."""
        spacescene = self.bobs[0].spacescene
        spacescene.stop_rigidity(self.bobs)


class Pendulum(MultiPendulum):
    def __init__(
        self,
        length: float = 3.5,
        initial_theta: float = 0.3,
        pivot_point: np.ndarray = UP * 2,
        rod_style: Optional[dict] = None,
        bob_style: Optional[dict] = None,
        **kwargs,
    ):
        """یک پاندول ساده.

        پارامترها
        ----------
        length
            طول پاندول.
        initial_theta
            زاویه اولیه انحراف از محور قائم.
        pivot_point
            نقطه اتکا.
        rod_style
            پارامترهای خطوط اتصال.
        bob_style
            پارامترهای توپ پاندول.
        kwargs
            پارامترهای اضافی VGroup.

        مثال
        -------
        .. manim:: PendulumExample
            :quality: low

            from manim_physics import *
            class PendulumExample(SpaceScene):
                def construct(self):
                    pends = VGroup(*[Pendulum(i) for i in np.linspace(1, 5, 7)])
                    self.add(pends)
                    for p in pends:
                        self.make_rigid_body(*p.bobs)
                        p.start_swinging()
                    self.wait(10)
        """
        if rod_style is None:
            rod_style = {}
        if bob_style is None:
            bob_style = {"radius": 0.25, "color": ORANGE, "fill_opacity": 1}

        self.length = length
        self.pivot_point = pivot_point

        point = self.pivot_point + (
            RIGHT * np.sin(initial_theta) * length
            + DOWN * np.cos(initial_theta) * length
        )
        super().__init__(
            point,
            pivot_point=self.pivot_point,
            rod_style=rod_style,
            bob_style=bob_style,
            **kwargs,
        )
