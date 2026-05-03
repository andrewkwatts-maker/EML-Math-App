"""Constants screen — searchable list of all 136 named EML constants."""
from __future__ import annotations

from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen


class ConstantsScreen(MDScreen):
    list_widget = ObjectProperty(None)
    detail_label = ObjectProperty(None)
    search_field = ObjectProperty(None)
    detail_text = StringProperty("Tap a constant to see its EML datasheet.")

    _all_names: list[str] = []

    def on_pre_enter(self) -> None:
        self._populate()

    def _populate(self, filter_text: str = "") -> None:
        if self.list_widget is None:
            return
        try:
            from eml_math import list_symbols
        except ImportError:
            self.detail_text = "eml-math not installed"
            return

        if not self._all_names:
            try:
                self._all_names = list_symbols()
            except Exception as exc:                  # noqa: BLE001
                self.detail_text = f"list_symbols error: {exc}"
                return

        f = (filter_text or "").strip().lower()
        names = [n for n in self._all_names if f in n.lower()] if f else self._all_names

        self.list_widget.clear_widgets()
        for n in names:
            item = OneLineListItem(text=n)
            item.bind(on_release=lambda _w, name=n: self._show_detail(name))
            self.list_widget.add_widget(item)

    def filter_changed(self, value: str) -> None:
        self._populate(value)

    def _show_detail(self, name: str) -> None:
        try:
            from eml_math import Get
            d = Get(name)
            if not isinstance(d, dict):
                self.detail_text = repr(d)
                return
            lines = [f"Name:        {d.get('name', name)}"]
            v = d.get("value")
            if v is not None:
                lines.append(f"Value:       {v}")
            if "formula" in d:
                lines.append(f"Formula:     {d['formula']}")
            if "complexity" in d:
                lines.append(f"Complexity:  {d['complexity']}")
            if "kind" in d:
                lines.append(f"Kind:        {d['kind']}")
            if "eml_tree" in d:
                lines.append(f"EML tree:    {d['eml_tree']}")
            self.detail_text = "\n".join(lines)
        except Exception as exc:                      # noqa: BLE001
            self.detail_text = f"{type(exc).__name__}: {exc}"
