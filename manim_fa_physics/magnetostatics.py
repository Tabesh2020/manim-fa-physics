r"""ماژول مغناطیس ایستا (Magnetostatics)"""

from __future__ import annotations
import itertools as it
from typing import Iterable, Tuple

from manim import VMobject, ArrowVectorField, np
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL

__all__ = ["Wire", "MagneticField"]


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
