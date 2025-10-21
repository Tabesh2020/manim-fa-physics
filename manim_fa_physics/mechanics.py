r"""فضای شبیه‌سازی گرانش.

بیشتر اشیاء می‌توانند به صورت یک جسم صلب (حرکت طبق گرانش و برخورد)
یا یک جسم ساکن (ثابت در صحنه) تعریف شوند.

برای استفاده از این ویژگی، باید از :class:`~SpaceScene` استفاده شود
تا به توابع مخصوص فضای شبیه‌سازی دسترسی داشته باشید.

.. note::
    * این ویژگی از بسته pymunk استفاده می‌کند. اگرچه ضروری نیست،
      اما آشنایی مختصر با نحوه استفاده از آن مفید است.

      `مستندات رسمی <http://www.pymunk.org/en/latest/pymunk.html>`_

      `آموزش یوتیوب <https://youtu.be/pRk---rdrbo>`_

    * نرخ فریم پایین ممکن است باعث شود برخی اشیاء از اشیاء ساکن عبور کنند،
      زیرا برخوردها به اندازه کافی دقیق ثبت نمی‌شوند. افزایش نرخ فریم
      ممکن است این مشکل را حل کند.

مثال
--------
.. manim:: TwoObjectsFalling

    from manim_physics import *
    # استفاده از SpaceScene برای دسترسی به تمام متدهای مکانیک صلب
    class TwoObjectsFalling(SpaceScene):
        def construct(self):
            circle = Circle().shift(UP)
            circle.set_fill(RED, 1)
            circle.shift(DOWN + RIGHT)

            rect = Rectangle().shift(UP)
            rect.rotate(PI / 4)
            rect.set_fill(YELLOW_A, 1)
            rect.shift(UP * 2)
            rect.scale(0.5)

            ground = Line([-4, -3.5, 0], [4, -3.5, 0])
            wall1 = Line([-4, -3.5, 0], [-4, 3.5, 0])
            wall2 = Line([4, -3.5, 0], [4, 3.5, 0])
            walls = VGroup(ground, wall1, wall2)
            self.add(walls)

            self.play(
                DrawBorderThenFill(circle),
                DrawBorderThenFill(rect),
            )
            self.make_rigid_body(rect, circle)  # اشیاء با گرانش حرکت می‌کنند
            self.make_static_body(walls)        # اشیاء در محل ثابت می‌مانند
            self.wait(5)
"""
from __future__ import annotations
import numpy as np
from manim import *
from typing import Tuple

from manim import VGroup, VMobject, Mobject, Circle, Line, Rectangle, Polygon, Polygram, Scene, np
from manim.utils.space_ops import angle_between_vectors
import pymunk

__all__ = [
    "Space",
    "_step",
    "_simulate",
    "get_shape",
    "get_angle",
    "SpaceScene",
]


class Space(Mobject):
    def __init__(self, gravity: Tuple[float, float] = (0, -9.81), **kwargs):
        """یک شی انتزاعی برای گرانش.

        پارامترها
        ----------
        gravity
            جهت و شدت گرانش.
        """
        super().__init__(**kwargs)
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.sleep_time_threshold = 5


class SpaceScene(Scene):
    GRAVITY: Tuple[float, float] = (0, -9.81)

    def __init__(self, renderer=None, **kwargs):
        """صحنه پایه برای تمام اشیاء مکانیک صلب.
        وکتور گرانش با ``self.GRAVITY`` قابل تنظیم است.
        """
        self.space = Space(gravity=self.GRAVITY)
        super().__init__(renderer=renderer, **kwargs)

    def setup(self):
        """استفاده داخلی"""
        self.add(self.space)
        self.space.add_updater(_step)

    def add_body(self, body: Mobject):
        """اضافه کردن جسم به pymunk و اتصال Mobject به آن."""
        if body.body != self.space.space.static_body:
            self.space.space.add(body.body)
        self.space.space.add(body.shape)

    def make_rigid_body(
        self,
        *mobs: Mobject,
        elasticity: float = 0.8,
        density: float = 1,
        friction: float = 0.8,
    ):
        """تبدیل هر Mobject به جسم قابل حرکت توسط گرانش.

        پارامترها
        ----------
        mobs
            اشیاء برای تبدیل به جسم صلب.
        elasticity, density, friction
            ویژگی‌های برخورد و تعامل با اشیاء دیگر.
        """
        for mob in mobs:
            if not hasattr(mob, "body"):
                self.add(mob)
                mob.body = pymunk.Body()
                mob.body.position = mob.get_x(), mob.get_y()
                get_angle(mob)
                if not hasattr(mob, "angle"):
                    mob.angle = 0
                mob.body.angle = mob.angle
                get_shape(mob)
                mob.shape.density = density
                mob.shape.elasticity = elasticity
                mob.shape.friction = friction
                mob.spacescene = self

                self.add_body(mob)
                mob.add_updater(_simulate)
            else:
                if mob.body.is_sleeping:
                    mob.body.activate()

    def make_static_body(
        self, *mobs: Mobject, elasticity: float = 1, friction: float = 0.8
    ) -> None:
        """تبدیل هر Mobject به جسم ساکن برای تعامل با اشیاء صلب."""
        for mob in mobs:
            if isinstance(mob, (VGroup, list)):
                self.make_static_body(*mob)
                continue
            mob.body = self.space.space.static_body
            get_shape(mob)
            mob.shape.elasticity = elasticity
            mob.shape.friction = friction
            self.add_body(mob)

    def stop_rigidity(self, *mobs: Mobject) -> None:
        """توقف حرکت صلب اشیاء."""
        for mob in mobs:
            if isinstance(mob, (VGroup, list)):
                self.stop_rigidity(*mob)
                continue
            if hasattr(mob, "body"):
                mob.body.sleep()


def _step(space, dt):
    """به‌روزرسانی گام فیزیکی"""
    space.space.step(dt)


def _simulate(b):
    """به‌روزرسانی موقعیت و زاویه Mobject طبق pymunk Body"""
    x, y = b.body.position
    b.move_to(np.array([x, y, 0]))
    b.rotate(b.body.angle - getattr(b, "angle", 0))
    b.angle = b.body.angle


def get_shape(mob: VMobject) -> None:
    """دریافت شکل جسم از Mobject"""
    if isinstance(mob, Circle):
        mob.shape = pymunk.Circle(body=mob.body, radius=mob.radius)
    elif isinstance(mob, Line):
        mob.shape = pymunk.Segment(
            mob.body,
            (mob.get_start()[0], mob.get_start()[1]),
            (mob.get_end()[0], mob.get_end()[1]),
            mob.stroke_width - 3.95,
        )
    elif isinstance(mob, Rectangle):
        width = np.linalg.norm(mob.get_vertices()[1] - mob.get_vertices()[0])
        height = np.linalg.norm(mob.get_vertices()[2] - mob.get_vertices()[1])
        mob.shape = pymunk.Poly.create_box(mob.body, (width, height))
    elif isinstance(mob, Polygram):
        vertices = [(a, b) for a, b, _ in mob.get_vertices() - mob.get_center()]
        mob.shape = pymunk.Poly(mob.body, vertices)
    elif isinstance(mob, Polygon):
        width = np.linalg.norm(mob.get_vertices()[1] - mob.get_vertices()[0])
        height = np.linalg.norm(mob.get_vertices()[2] - mob.get_vertices()[1])
        mob.shape = pymunk.Poly.create_box(mob.body, (width, height))
    else:
        mob.shape = pymunk.Poly.create_box(mob.body, (mob.width, mob.height))


def get_angle(mob: VMobject) -> None:
    """دریافت زاویه جسم از Mobject، استفاده داخلی برای Updaterها"""
    if isinstance(mob, Polygon):
        vec1 = mob.get_vertices()[0] - mob.get_vertices()[1]
        vec2 = type(mob)().get_vertices()[0] - type(mob)().get_vertices()[1]
        mob.angle = angle_between_vectors(vec1, vec2)
    elif isinstance(mob, Line):
        mob.angle = mob.get_angle()
def snell(i_ang, n):
    """
    قانون اسنل: زاویه شکست را بر اساس زاویه تابش و ضریب شکست لنز محاسبه می‌کند.
    i_ang : زاویه تابش (به رادیان)
    n : ضریب شکست
    """
    # اگر مقدار خیلی نزدیک صفر باشد (برای جلوگیری از خطای ریاضی)
    if abs(np.sin(i_ang)) < 1e-6:
        return 0
    try:
        return np.arcsin(np.sin(i_ang) / n)
    except ValueError:
        # اگر سینوس از محدوده مجاز خارج شد
        return 0


def antisnell(i_ang, n):
    """
    حالت معکوس قانون اسنل (از لنز به هوا)
    """
    if abs(np.sin(i_ang)) < 1e-6:
        return 0
    try:
        return np.arcsin(np.sin(i_ang) * n)
    except ValueError:
        return 0