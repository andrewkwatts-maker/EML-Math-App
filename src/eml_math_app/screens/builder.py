"""Builder screen — type an expression, see the EML tree render live."""
from __future__ import annotations

from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.screen import MDScreen

from eml_math_app.widgets.formula_input import FormulaInput
from eml_math_app.widgets.svg_view import TreeImageView


class BuilderScreen(MDScreen):
    formula_field: FormulaInput = ObjectProperty(None)
    tree_view: TreeImageView = ObjectProperty(None)
    direction = StringProperty("down")
    edge_style = StringProperty("curve")
    status = StringProperty("Type an expression — try `eml(1, 1)` or `sin(x)*cos(x)`")

    def on_kv_post(self, base_widget) -> None:        # noqa: D401
        if self.formula_field is not None:
            self.formula_field.bind_parsed(self._on_parsed)

    def _on_parsed(self, tree, error_str: str) -> None:
        if error_str:
            self.status = f"Parse error: {error_str}"
            if self.tree_view is not None:
                self.tree_view.show_tree(None)
            return
        if tree is None:
            self.status = "Empty expression"
            if self.tree_view is not None:
                self.tree_view.show_tree(None)
            return
        self.status = "Tree built"
        if self.tree_view is not None:
            self.tree_view.direction = self.direction
            self.tree_view.edge_style = self.edge_style
            try:
                self.tree_view.show_tree(tree)
            except Exception as exc:                  # noqa: BLE001
                self.status = f"Render error: {exc}"

    def set_direction(self, value: str) -> None:
        self.direction = value
        # re-render with the existing tree
        if self.tree_view is not None and self.tree_view.last_tree is not None:
            self.tree_view.direction = value
            self.tree_view.show_tree(self.tree_view.last_tree)

    def set_edge_style(self, value: str) -> None:
        self.edge_style = value
        if self.tree_view is not None and self.tree_view.last_tree is not None:
            self.tree_view.edge_style = value
            self.tree_view.show_tree(self.tree_view.last_tree)
