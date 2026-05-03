"""Convert screen — three-pane LaTeX ↔ EML ↔ Python live converter."""
from __future__ import annotations

from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.screen import MDScreen


class ConvertScreen(MDScreen):
    latex_field = ObjectProperty(None)
    python_field = ObjectProperty(None)
    eml_field = ObjectProperty(None)
    status = StringProperty("Edit any pane to derive the others")

    _suppress = False
    _pending = None

    def on_kv_post(self, base_widget) -> None:        # noqa: D401
        for f in (self.latex_field, self.python_field, self.eml_field):
            if f is None:
                continue
            f.bind(text=lambda inst, val, src=f: self._on_change(src, val))

    def _on_change(self, source, text: str) -> None:
        if self._suppress:
            return
        if self._pending is not None:
            self._pending.cancel()
        self._pending = Clock.schedule_once(
            lambda *_: self._derive(source, text), 0.25
        )

    def _derive(self, source, text: str) -> None:
        text = (text or "").strip()
        if not text:
            self.status = "(empty)"
            return
        try:
            from eml_math import (
                compress_str, compress_latex, decompress, get,
            )
            # Determine which pane was edited
            if source is self.latex_field:
                # Direct shortcut: a bare named symbol like "pi"
                r = get(text)
                if r is None:
                    r = compress_latex(text)
            elif source is self.python_field:
                r = get(text)
                if r is None:
                    r = compress_str(text)
            else:  # eml_field
                r = get(text) or compress_str(text)
            if r is None:
                self.status = f"Could not parse: {text!r}"
                return

            self._suppress = True
            try:
                if source is not self.latex_field and self.latex_field is not None:
                    self.latex_field.text = decompress(r, fmt="latex")
                if source is not self.python_field and self.python_field is not None:
                    self.python_field.text = decompress(r, fmt="python")
                if source is not self.eml_field and self.eml_field is not None:
                    self.eml_field.text = decompress(r, fmt="eml")
            finally:
                self._suppress = False
            self.status = f"OK — formula: {r.formula}    error: {r.error:.2e}"
        except Exception as exc:                      # noqa: BLE001
            self.status = f"{type(exc).__name__}: {exc}"
