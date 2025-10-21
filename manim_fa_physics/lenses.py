r"""پرتوهای نور که توسط لنزها (Lens) شکست داده می‌شوند."""

from __future__ import annotations
from typing import Iterable


import numpy as np
from manim import *
from shapely import geometry as gm

from manim_fa_physics.rays import intersection
from manim_fa_physics.mechanics import snell, antisnell, rotate_vector, angle_of_vector

from manim import config, Line
from manim.utils.space_ops import angle_of_vector, rotate_vector
import numpy as np


__all__ = ["Ray"]


class Ray(Line):
    def __init__(
        self,
        start: Iterable[float],
        direction: Iterable[float],
        init_length: float = 5,
        propagate: Iterable[Lens] | None = None,
        **kwargs,
    ) -> None:
        """یک پرتو نور.

        پارامترها
        ----------
        start
            نقطه شروع پرتو
        direction
            جهت پرتو
        init_length
            طول اولیه پرتو. پس از عبور از لنزها، طول پرتو برای نمایش شکست تغییر می‌کند.
        propagate
            لیستی از لنزها که پرتو باید از آن‌ها عبور کند.

        مثال
        -------
        .. manim:: RayExampleScene
            :save_last_frame:

            from manim_physics import *

            class RayExampleScene(Scene):
                def construct(self):
                    lens_style = {"fill_opacity": 0.5, "color": BLUE}
                    a = Lens(-5, 1, **lens_style).shift(LEFT)
                    a2 = Lens(5, 1, **lens_style).shift(RIGHT)
                    b = [
                        Ray(LEFT * 5 + UP * i, RIGHT, 8, [a, a2], color=RED)
                        for i in np.linspace(-2, 2, 10)
                    ]
                    self.add(a, a2, *b)
        """
        self.init_length = init_length
        self.propagated = False
        super().__init__(start, np.array(start) + np.array(direction) * init_length, **kwargs)
        if propagate:
            self.propagate(*propagate)

    def propagate(self, *lenses: Lens) -> None:
        """عبور پرتو از لیست لنزهای داده شده.

        پارامترها
        ----------
        lenses
            تمام لنزهایی که پرتو باید از آن‌ها عبور کند.
        """
        sorted_lens = self._sort_lens(lenses)
        for lens in sorted_lens:
            intersects = intersection(lens, self)
            if len(intersects) == 0:
                continue
            intersects = self._sort_intersections(intersects)
            if not self.propagated:
                self.put_start_and_end_on(self.start, intersects[1])
            else:
                nppcc = self.n_points_per_cubic_curve if config.renderer != "opengl" else self.n_points_per_curve
                self.points = self.points[:-nppcc]
                self.add_line_to(intersects[1])
            self.end = intersects[1]

            # زاویه تابش و شکست
            i_ang = angle_of_vector(self.end - lens.C[0])
            i_ang -= angle_of_vector(self.start - self.end)
            r_ang = snell(i_ang, lens.n)
            r_ang *= -1 if lens.f > 0 else 1

            ref_ray = rotate_vector(lens.C[0] - self.end, r_ang)
            intersects = intersection(
                lens,
                Line(self.end - ref_ray * self.init_length, self.end + ref_ray * self.init_length)
            )
            intersects = self._sort_intersections(intersects)
            self.add_line_to(intersects[1])

            self.start = self.end
            self.end = intersects[1]

            # برخورد با سطح دوم لنز
            i_ang = angle_of_vector(self.end - lens.C[1])
            i_ang -= angle_of_vector(self.start - self.end)
            if np.abs(np.sin(i_ang)) < 1 / lens.n:
                r_ang = antisnell(i_ang, lens.n)
                r_ang *= -1 if lens.f < 0 else 1
                ref_ray = rotate_vector(lens.C[1] - self.end, r_ang)
                ref_ray *= -1 if lens.f > 0 else 1
                self.add_line_to(self.end + ref_ray * self.init_length)
                self.start = self.end
                self.end = self.get_end()

            self.propagated = True

    def _sort_lens(self, lenses: Iterable[Lens]) -> Iterable[Lens]:
        """مرتب‌سازی لنزها بر اساس فاصله از نقطه شروع پرتو"""
        dists = []
        for lens in lenses:
            try:
                dists += [[np.linalg.norm(intersection(self, lens)[0] - self.start), lens]]
            except:
                dists += [[np.inf, lens]]
        dists.sort(key=lambda x: x[0])
        return np.array(dists, dtype=object)[:, 1]

    def _sort_intersections(self, intersections: Iterable[Iterable[float]]) -> Iterable[Iterable[float]]:
        """مرتب‌سازی نقاط تقاطع بر اساس فاصله تا انتهای پرتو"""
        result = []
        for inters in intersections:
            result.append([np.linalg.norm(inters - self.end), inters])
        result.sort(key=lambda x: x[0])
        return np.array(result, dtype=object)[:, 1]
