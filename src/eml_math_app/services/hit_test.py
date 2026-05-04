"""Hit-testing for an eml-math layout dict.

Pure logic — no Kivy import, no widget state. The renderer widget tells us
which canvas point the mouse maps to (after scaling / letterboxing) and we
return the nearest node, or None if nothing is close enough. Keeping this
in its own module means it can be unit-tested without spinning up a Kivy
window, and reused by any other renderer that produces the same layout
schema (SRP + SOLID's "depend on abstractions": the GUI depends on this
function, not on raw geometry math).
"""
from __future__ import annotations

from typing import Any, Dict, Optional


# Maximum cursor distance from a node centre, in layout units, that still
# counts as "hovered". Roughly one glyph radius in eml-math's renderers.
DEFAULT_HIT_RADIUS = 40.0


def nearest_node(
    layout: Optional[Dict[str, Any]],
    canvas_x: float,
    canvas_y: float,
    hit_radius: float = DEFAULT_HIT_RADIUS,
) -> Optional[Dict[str, Any]]:
    """Return the layout node closest to ``(canvas_x, canvas_y)``.

    ``layout`` must be a dict in eml-math's ``eml-layout/v1`` schema (the
    return value of ``EMLTreeNode.layout()``). Returns ``None`` when the
    layout is empty or no node sits within ``hit_radius``.
    """
    if not layout:
        return None
    nodes = layout.get("nodes") or ()
    if not nodes:
        return None
    best: Optional[Dict[str, Any]] = None
    best_d2 = hit_radius * hit_radius
    for n in nodes:
        dx = float(n["x"]) - canvas_x
        dy = float(n["y"]) - canvas_y
        d2 = dx * dx + dy * dy
        if d2 < best_d2:
            best_d2 = d2
            best = n
    return best


def project_widget_to_canvas(
    layout: Optional[Dict[str, Any]],
    image_x: float,
    image_y: float,
    image_w: float,
    image_h: float,
) -> Optional[tuple]:
    """Map a point inside the displayed image to the layout's canvas space.

    Returns ``(cx, cy)`` or ``None`` when ``layout`` lacks canvas info or
    the image rect is degenerate.
    """
    if not layout or image_w <= 0 or image_h <= 0:
        return None
    canvas = layout.get("canvas") or {}
    cw = float(canvas.get("width") or 0.0)
    ch = float(canvas.get("height") or 0.0)
    if cw <= 0.0 or ch <= 0.0:
        return None
    return image_x / image_w * cw, image_y / image_h * ch
