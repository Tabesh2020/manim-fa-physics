r"""ماژول الکترواستاتیک (Electrostatics)"""

from __future__ import annotations
from typing import Iterable

from manim import normalize, VGroup, Dot, Rectangle, Arc
from manim.constants import ORIGIN, TAU
from manim.mobject.vector_field import ArrowVectorField
from manim.utils.color import BLUE, RED, RED_A, RED_D, color_gradient
import numpy as np

__all__ = ["Charge", "ElectricField"]


class Charge(VGroup):
    """یک جسم بار الکترواستاتیک که یک :class:`~ElectricField` تولید می‌کند."""

    def __init__(
        self,
        magnitude: float = 1,
        point: np.ndarray = ORIGIN,
        add_glow: bool = True,
        **kwargs,
    ) -> None:
        """پارامترها
        ----------
        magnitude
            شدت بار الکترواستاتیک
        point
            موقعیت بار
        add_glow
            آیا افکت درخشندگی اضافه شود. حلقه‌های متنوعی برای شبیه‌سازی نور ایجاد می‌کند.
        kwargs
            پارامترهای اضافی برای VGroup
        """
        VGroup.__init__(self, **kwargs)
        self.magnitude = magnitude
        self.point = point
        self.radius = (abs(magnitude) * 0.4 if abs(magnitude) < 2 else 0.8) * 0.3

        if magnitude > 0:
            label = VGroup(
                Rectangle(width=0.32 * 1.1, height=0.006 * 1.1).set_z_index(1),
                Rectangle(width=0.006 * 1.1, height=0.32 * 1.1).set_z_index(1),
            )
            color = RED
            layer_colors = [RED_D, RED_A]
            layer_radius = 4
        else:
            label = Rectangle(width=0.27, height=0.003)
            color = BLUE
            layer_colors = ["#3399FF", "#66B2FF"]
            layer_radius = 2

        if add_glow:  # استفاده از چندین Arc برای شبیه‌سازی درخشندگی
            layer_num = 80
            color_list = color_gradient(layer_colors, layer_num)
            opacity_func = lambda t: 1500 * (1 - abs(t - 0.009) ** 0.0001)
            rate_func = lambda t: t**2

            for i in range(layer_num):
                self.add(
                    Arc(
                        radius=layer_radius * rate_func((0.5 + i) / layer_num),
                        angle=TAU,
                        color=color_list[i],
                        stroke_width=101 * (rate_func((i + 1) / layer_num) - rate_func(i / layer_num)) * layer_radius,
                        stroke_opacity=opacity_func(rate_func(i / layer_num)),
                    ).shift(point)
                )

        self.add(Dot(point=self.point, radius=self.radius, color=color))
        self.add(label.scale(self.radius / 0.3).shift(point))
        for mob in self:
            mob.set_z_index(1)


class ElectricField(ArrowVectorField):
    """یک میدان الکتریکی."""

    def __init__(self, *charges: Charge, **kwargs) -> None:
        """پارامترها
        ----------
        charges
            تمام بارهایی که میدان الکتریکی را ایجاد می‌کنند
        kwargs
            پارامترهای اضافی برای ArrowVectorField
        """
        self.charges = charges
        positions = []
        magnitudes = []
        for charge in charges:
            positions.append(charge.get_center())
            magnitudes.append(charge.magnitude)

        super().__init__(lambda p: self._field_func(p, positions, magnitudes), **kwargs)

    def _field_func(
        self,
        p: np.ndarray,
        positions: Iterable[np.ndarray],
        magnitudes: Iterable[float],
    ) -> np.ndarray:
        """محاسبه بردار میدان الکتریکی در نقطه p"""
        field_vect = np.zeros(3)
        for p0, mag in zip(positions, magnitudes):
            r = p - p0
            dist = np.linalg.norm(r)
            if dist < 0.1:  # جلوگیری از تقسیم بر صفر
                return np.zeros(3)
            field_vect += mag / dist**2 * normalize(r)
        return field_vect
