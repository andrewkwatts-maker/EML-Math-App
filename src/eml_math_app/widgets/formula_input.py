"""FormulaInput — debounced MDTextField with parse-error indicator.

Fires ``on_parsed(tree, error_str)`` 200 ms after the user stops typing.
Wraps ``eml_math.parse_eml_tree`` and surfaces parse errors as a one-line
hint underneath the field.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.textfield import MDTextField

DEBOUNCE_S = 0.2


class FormulaInput(MDTextField):
    """Single-line MDTextField that parses every change after a debounce."""

    debounce = NumericProperty(DEBOUNCE_S)
    last_error = StringProperty("")
    expand_eml = StringProperty("auto")  # "auto" | "true" | "false"

    _parse_event: Any = None
    _on_parsed_cb: Optional[Callable[[Any, str], None]] = None

    def bind_parsed(self, callback: Callable[[Any, str], None]) -> None:
        """Register the listener invoked after each successful debounced parse.

        The callback receives ``(tree, error_str)``. Either one will be
        truthy at a time: ``tree`` set on success (``error_str == ""``),
        or ``error_str`` set on failure (``tree is None``).
        """
        self._on_parsed_cb = callback

    def on_text(self, _instance, value: str) -> None:  # noqa: D401
        if self._parse_event is not None:
            self._parse_event.cancel()
        self._parse_event = Clock.schedule_once(
            lambda *_: self._parse_now(value), self.debounce
        )

    def _parse_now(self, raw: str) -> None:
        text = (raw or "").strip()
        tree = None
        err = ""
        if not text:
            self.last_error = ""
            self.helper_text = ""
            self.error = False
        else:
            try:
                from eml_math import parse_eml_tree
                # Accept either "EML: …" or bare expressions
                if not text.startswith("EML:"):
                    text = f"EML: {text}"
                expand = (
                    True if self.expand_eml == "true"
                    else False if self.expand_eml == "false"
                    else True   # "auto" — default to expanded form
                )
                tree = parse_eml_tree(text, expand_eml=expand)
            except Exception as exc:                         # noqa: BLE001
                err = f"{type(exc).__name__}: {exc}"
                self.last_error = err
                self.helper_text = err
                self.helper_text_mode = "on_error"
                self.error = True
            else:
                self.last_error = ""
                self.helper_text = ""
                self.error = False

        if self._on_parsed_cb is not None:
            self._on_parsed_cb(tree, err)
