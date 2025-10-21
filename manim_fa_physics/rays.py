r"""لنزها برای شکست پرتوها (Rays)."""

from __future__ import annotations
from typing import Iterable, Tuple

from manim import config, VMobject, VectorizedPoint, Circle, Square
from manim import Difference

from manim.utils.color import WHITE
import numpy as np
from shapely import geometry as gm

__all__ = ["Lens"]

try:
    # برای manim < 0.15.0
    from manim.mobject.opengl_compatibility import ConvertToOpenGL
except ModuleNotFoundError:
    # برای manim >= 0.15.0
    from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL


def intersection(vmob1: VMobject, vmob2: VMobject) -> np.ndarray:
    """نقاط تقاطع دو منحنی"""
    a = gm.LineString(vmob1.points)
    b = gm.LineString(vmob2.points)
    intersects: gm.GeometryCollection = a.intersection(b)
    try:  # اگر چندین تقاطع وجود داشته باشد
        return np.array(
            [[[x, y, z] for x, y, z in m.coords][0] for m in intersects.geoms]
        )
    except:  # در غیر این صورت
        return np.array([[x, y, z] for x, y, z in intersects.coords])


def snell(i_ang: float, n: float) -> float:
    """قانون اسنل برای شکست نور
    ورودی و خروجی بر حسب رادیان
    """
    return np.arcsin(np.sin(i_ang) / n)


def antisnell(r_ang: float, n: float) -> float:
    """قانون معکوس اسنل
    ورودی و خروجی بر حسب رادیان
    """
    return np.arcsin(np.sin(r_ang) * n)


class Lens(VMobject, metaclass=ConvertToOpenGL):
    def __init__(self, f: float, d: float, n: float = 1.52, **kwargs) -> None:
        """یک لنز. معمولاً همراه با :class:`~Ray` استفاده می‌شود.

        پارامترها
        ----------
        f
            فاصله کانونی. با مقدار مثبت لنز محدب، با مقدار منفی لنز مقعر.
            توجه: مقدار f دقیقاً با نقطه کانونی همخوانی ندارد (مشکل شناخته شده).
        d
            ضخامت لنز
        n
            ضریب شکست. پیش‌فرض برای شیشه.
        kwargs
            پارامترهای اضافی برای VMobject
        """
        super().__init__(**kwargs)
        self.f = f
        f *= 50 / 7 * f if f > 0 else -50 / 7 * f  # روش غیرمعمول اما کار می‌کند
        if f > 0:
            r = ((n - 1) ** 2 * f * d / n) ** 0.5
        else:
            r = ((n - 1) ** 2 * -f * d / n) ** 0.5
        self.d = d
        self.n = n
        self.r = r

        # ساخت هندسه لنز
        if f > 0:
            self.set_points(
                Intersection(
                    a := Circle(r).shift(np.array([r - d / 2, 0, 0])),
                    b := Circle(r).shift(np.array([-(r - d / 2), 0, 0])),
                )
                .insert_n_curves(50)
                .points
            )
        else:
            self.set_points(
                Difference(
                    Difference(
                        Square(2 * 0.7 * r),
                        a := Circle(r).shift(np.array([-(r + d / 2), 0, 0])),
                    ),
                    b := Circle(r).shift(np.array([r + d / 2, 0, 0])),
                )
                .insert_n_curves(50)
                .points
            )

        # افزودن نقاط مرکزی هندسه برای محاسبات بعدی
        self.add(VectorizedPoint(a.get_center()), VectorizedPoint(b.get_center()))

    @property
    def C(self) -> Tuple[np.ndarray, np.ndarray]:
        """بازگرداندن دو نقطه متناظر با مراکز انحنای لنز"""
        i = 0
        i += 1 if config.renderer != "opengl" else 0
        return self[i].points[0], self[i + 1].points[0]  # این کمی گیج‌کننده است
