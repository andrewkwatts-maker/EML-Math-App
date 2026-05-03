"""Compress screen — beam-search compression with parameter knobs."""
from __future__ import annotations

from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.screen import MDScreen

from eml_math_app.widgets.svg_view import TreeImageView


class CompressScreen(MDScreen):
    expr_field = ObjectProperty(None)
    x_lo_field = ObjectProperty(None)
    x_hi_field = ObjectProperty(None)
    n_points_field = ObjectProperty(None)
    precision_field = ObjectProperty(None)
    max_complexity_field = ObjectProperty(None)
    tree_view: TreeImageView = ObjectProperty(None)
    formula_label = ObjectProperty(None)
    error_label = ObjectProperty(None)
    complexity_label = ObjectProperty(None)
    status = StringProperty("Set the function + sampling window, press Compress")

    def run_compression(self) -> None:               # noqa: D401
        if self.expr_field is None:
            return
        text = (self.expr_field.text or "").strip()
        if not text:
            self.status = "Empty expression"
            return
        try:
            from eml_math import compress_str, decompress
            x_lo = float(self.x_lo_field.text or 0.2)
            x_hi = float(self.x_hi_field.text or 3.0)
            n_pts = int(self.n_points_field.text or 40)
            prec = float(self.precision_field.text or 1e-8)
            max_c = int(self.max_complexity_field.text or 8)
            r = compress_str(
                text, x_lo=x_lo, x_hi=x_hi,
                n_points=n_pts, precision_goal=prec,
                max_complexity=max_c,
            )
            if r is None:
                self.status = "No formula found within budget"
                return
            self.formula_label.text = f"Formula:  {r.formula}"
            self.error_label.text = f"Error:    {r.error:.4e}"
            self.complexity_label.text = f"Complexity: {r.complexity}"
            self.status = "Compress complete"
            try:
                from eml_math import parse_eml_tree
                eml_str = decompress(r, fmt="eml")
                tree = parse_eml_tree(f"EML: {eml_str}", expand_eml=False)
                if self.tree_view is not None:
                    self.tree_view.show_tree(tree)
            except Exception as exc:                  # noqa: BLE001
                self.status = f"Render skipped: {exc}"
        except Exception as exc:                      # noqa: BLE001
            self.status = f"{type(exc).__name__}: {exc}"
