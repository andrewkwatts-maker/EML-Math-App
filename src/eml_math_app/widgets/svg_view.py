"""TreeImageView — render an EML expression tree to a Kivy texture.

Path: ``EMLTreeNode → eml_math.flow_png(tree) → PNG bytes →
kivy.core.image.CoreImage → texture → kivy.uix.image.Image``.

Pillow is required (PNG path of eml-math). The widget pins it as a hard
dependency of the GUI even though it's optional in eml-math itself.
"""
from __future__ import annotations

from io import BytesIO
from typing import Any, Optional

from kivy.core.image import Image as CoreImage
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.image import Image as KivyImage


class TreeImageView(KivyImage):
    """A Kivy ``Image`` widget that displays an EML expression tree.

    Attributes
    ----------
    direction : str
        ``"down" | "up" | "left" | "right"`` (forwarded to ``flow_png``).
    edge_style : str
        ``"straight" | "curve" | "spline"`` (forwarded via ``layout_opts``
        when the new render package is used; legacy ``flow_png`` ignores).
    width_px / height_px : int
        Rendered canvas pixel dimensions (Kivy scales to widget).
    """

    direction = StringProperty("down")
    edge_style = StringProperty("curve")
    width_px = NumericProperty(720)
    height_px = NumericProperty(440)

    _last_tree: Optional[Any] = None
    _last_png: Optional[bytes] = None

    def show_tree(self, tree: Any, **flow_opts: Any) -> None:
        """Render *tree* (an EMLTreeNode or any object exposing
        ``flow_png(...)`` returning bytes) and display it.

        Extra ``flow_opts`` are forwarded straight to ``flow_png`` —
        e.g. ``palette=DEFAULT_PALETTE``, ``inline_constants=True``,
        ``edge_width=4.0``.
        """
        if tree is None:
            self.texture = None
            self._last_tree = None
            self._last_png = None
            return
        png = tree.flow_png(
            direction=self.direction,
            width=int(self.width_px),
            height=int(self.height_px),
            **flow_opts,
        )
        self._last_tree = tree
        self._last_png = png
        cimg = CoreImage(BytesIO(png), ext="png")
        self.texture = cimg.texture

    def show_png_bytes(self, png: bytes) -> None:
        """Display arbitrary PNG bytes directly (e.g. from a Renderer)."""
        self._last_png = png
        if not png:
            self.texture = None
            return
        cimg = CoreImage(BytesIO(png), ext="png")
        self.texture = cimg.texture

    @property
    def last_png(self) -> Optional[bytes]:
        """Most-recent rendered PNG bytes — used by the Export screen."""
        return self._last_png

    @property
    def last_tree(self):
        return self._last_tree
