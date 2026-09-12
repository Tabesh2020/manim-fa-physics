r"""ماژول مغناطیس ایستا (Magnetostatics)"""

from __future__ import annotations
import itertools as it
from typing import Iterable, Sequence, Tuple

from manim import (
    VMobject,
    VGroup,
    ArrowVectorField,
    Circle,
    Dot,
    Line,
    Rectangle,
    Tex,
    Vector,
    ORIGIN,
    OUT,
    IN,
    UP,
    DOWN,
    UR,
    UL,
    WHITE,
    RED,
    BLUE,
    PI,
    np,
)
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL
from manim.utils.space_ops import angle_of_vector

__all__ = [
    "Wire",
    "MagneticField",
    "Current",
    "CurrentMagneticField",
    "BarMagnet",
    "BarMagneticField",
]


class Wire(VMobject, metaclass=ConvertToOpenGL):
    """کلاس انتزاعی برای نمایش یک سیم حامل جریان
    که یک :class:`~MagneticField` تولید می‌کند.

    پارامترها
    ----------
    stroke
        VMobject اصلی سیم. سیم خروجی فرم آن را می‌گیرد.
    current
        مقدار جریان عبوری از سیم.
    samples
        تعداد قطعات سیم برای ایجاد :class:`~MagneticField`.
    kwargs
        پارامترهای اضافی برای VMobject.

    .. note::
        برای مثال، به :class:`~MagneticField` مراجعه کنید.
    """

    def __init__(
        self,
        stroke: VMobject,
        current: float = 1,
        samples: int = 16,
        **kwargs,
    ):
        self.current = current
        self.samples = samples
        super().__init__(**kwargs)
        self.set_points(stroke.points)


class MagneticField(ArrowVectorField):
    """یک میدان مغناطیسی.

    پارامترها
    ----------
    wires
        تمام سیم‌هایی که در تولید میدان نقش دارند.
    kwargs
        پارامترهای اضافی برای ArrowVectorField.

    مثال
    -------
    .. manim:: MagneticFieldExample
        :save_last_frame:

        from manim_physics import *

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
    """

    def __init__(self, *wires: Wire, **kwargs):
        dls = []
        currents = []
        for wire in wires:
            points = [
                wire.point_from_proportion(i)
                for i in np.linspace(0, 1, wire.samples + 1)
            ]
            dls.append(list(zip(points, points[1:])))
            currents.append(wire.current)

        super().__init__(
            lambda p: MagneticField._field_func(p, dls, currents),
            **kwargs
        )

    @staticmethod
    def _field_func(
        p: np.ndarray,
        dls: Iterable[Tuple[np.ndarray, np.ndarray]],
        currents: Iterable[float],
    ):
        """محاسبه بردار میدان مغناطیسی در نقطه p"""
        B_field = np.zeros(3)
        for dl in dls:
            for (r0, r1), I in it.product(dl, currents):
                dr = r1 - r0
                r = p - r0
                dist = np.linalg.norm(r)
                if dist < 0.1:  # جلوگیری از تقسیم بر صفر
                    return np.zeros(3)
                B_field += np.cross(dr, r) * I / dist**4
        return B_field


class Current(VGroup):
    """یک جریان الکتریکی عمود بر صفحه که یک :class:`~CurrentMagneticField` تولید می‌کند.

    پارامترها
    ----------
    point
        موقعیت جریان.
    magnitude
        شدت جریان.
    direction
        جهت جریان؛ فقط ``OUT`` (به سمت بیرون صفحه) یا ``IN`` (به سمت داخل صفحه) پذیرفته می‌شود.
    kwargs
        پارامترهای اضافی برای VGroup.

    .. note::
        برای مثال، به :class:`~CurrentMagneticField` مراجعه کنید.
    """

    def __init__(
        self,
        point: Sequence[float] = ORIGIN,
        magnitude: float = 1,
        direction: Sequence[float] = OUT,
        **kwargs,
    ) -> None:
        if np.all(direction == OUT) or np.all(direction == IN):
            self.direction = direction
        else:
            raise ValueError("فقط جهت‌های IN و OUT پشتیبانی می‌شوند.")

        self.magnitude = magnitude
        if np.all(direction == IN):
            # نماد ضربدر برای جریان به سمت داخل صفحه
            label = VGroup(
                Line(ORIGIN, UR).move_to(ORIGIN),
                Line(ORIGIN, UL).move_to(ORIGIN),
            )
            self.magnitude *= -1
        else:
            # نماد نقطه برای جریان به سمت بیرون صفحه
            label = Dot(radius=0.2)

        super().__init__(**kwargs)
        self.add(Circle(color=WHITE), label).scale(0.2).shift(point)


class CurrentMagneticField(ArrowVectorField):
    """میدان مغناطیسی حاصل از یک یا چند جریان عمود بر صفحه.

    پارامترها
    ----------
    currents
        تمام جریان‌هایی که در تولید میدان نقش دارند.
    kwargs
        پارامترهای اضافی برای ArrowVectorField.

    مثال
    -------
    .. manim:: MagnetismExample
        :save_last_frame:

        from manim_fa_physics import *

        class MagnetismExample(Scene):
            def construct(self):
                current1 = Current(LEFT * 2.5)
                current2 = Current(RIGHT * 2.5, direction=IN)
                field = CurrentMagneticField(current1, current2)
                self.add(field, current1, current2)
    """

    def __init__(self, *currents: Current, **kwargs) -> None:
        super().__init__(lambda p: self._field_func(p, *currents), **kwargs)

    def _field_func(self, p: np.ndarray, *currents: Current) -> np.ndarray:
        """محاسبه بردار میدان مغناطیسی در نقطه p"""
        direction = np.zeros(3)
        x, y, _ = p
        for current in currents:
            x0, y0, _ = current.get_center()
            mag = current.magnitude
            dist_sq = (x - x0) ** 2 + (y - y0) ** 2
            if dist_sq > 0.01:  # جلوگیری از تقسیم بر صفر نزدیک خود جریان
                direction += mag * np.array([-(y - y0), (x - x0), 0]) / dist_sq**1.5
        return direction


class BarMagnet(VGroup):
    """یک آهنربای میله‌ای با قطب شمال (N) و جنوب (S) که یک :class:`~BarMagneticField` تولید می‌کند.

    پارامترها
    ----------
    north
        موقعیت قطب شمال.
    south
        موقعیت قطب جنوب.
    height
        ارتفاع آهنربا.
    width
        عرض آهنربا (باید کمتر از ارتفاع باشد).
    kwargs
        پارامترهای اضافی برای VGroup.

    مثال
    -------
    .. manim:: BarMagnetExample
        :save_last_frame:

        from manim_fa_physics import *

        class BarMagnetExample(Scene):
            def construct(self):
                bar1 = BarMagnet().rotate(PI / 2).shift(LEFT * 3.5)
                bar2 = BarMagnet().rotate(PI / 2).shift(RIGHT * 3.5)
                self.add(BarMagneticField(bar1, bar2))
                self.add(bar1, bar2)
    """

    def __init__(
        self,
        north: Sequence[float] = UP,
        south: Sequence[float] = DOWN,
        height: float = 2,
        width: float = 1,
        **kwargs,
    ) -> None:
        self.length = np.linalg.norm(np.array(north) - np.array(south))
        super().__init__(**kwargs)
        if width > height:
            raise ValueError("عرض آهنربای میله‌ای باید کمتر از ارتفاع آن باشد.")

        self.magnet_width = width
        self.bar = VGroup(
            Rectangle(
                height=height / 2, width=width, fill_opacity=1, color=RED
            ).next_to(ORIGIN, UP, 0),
            Rectangle(
                height=height / 2, width=width, fill_opacity=1, color=BLUE
            ).next_to(ORIGIN, DOWN, 0),
        )
        self.north_label = Tex("N").shift(UP * (self.length / 2 - 0.5))
        self.south_label = Tex("S").shift(UP * -(self.length / 2 - 0.5))
        self.add(self.bar, self.north_label, self.south_label)
        self.rotate(-PI / 2 + angle_of_vector(self.get_south_to_north()))

    def get_south_to_north(self) -> np.ndarray:
        """بردار واحد از قطب جنوب به سمت قطب شمال."""
        return Vector(
            self.north_label.get_center() - self.south_label.get_center()
        ).get_vector()


class BarMagneticField(CurrentMagneticField):
    """میدان مغناطیسی حاصل از یک یا چند آهنربای میله‌ای، با شبیه‌سازی آن به کمک جریان‌های معادل.

    پارامترها
    ----------
    bars
        تمام آهنرباهایی که در تولید میدان نقش دارند.
    kwargs
        پارامترهای اضافی برای ArrowVectorField.

    .. note::
        برای مثال، به :class:`~BarMagnet` مراجعه کنید.
    """

    def __init__(self, *bars: BarMagnet, **kwargs) -> None:
        currents = []
        for bar in bars:
            currents_ = []
            currents_ += [
                Current(magnitude=-1).move_to(i)
                for i in np.linspace(
                    [bar.magnet_width / 2, bar.length / 2, 0],
                    [bar.magnet_width / 2, -bar.length / 2, 0],
                    10,
                )
            ]
            currents_ += [
                Current(magnitude=1).move_to(i)
                for i in np.linspace(
                    [-bar.magnet_width / 2, bar.length / 2, 0],
                    [-bar.magnet_width / 2, -bar.length / 2, 0],
                    10,
                )
            ]
            VGroup(*currents_).rotate(
                -PI / 2 + angle_of_vector(bar.get_south_to_north())
            ).shift(bar.get_center())
            currents += currents_

        super().__init__(*currents, **kwargs)
