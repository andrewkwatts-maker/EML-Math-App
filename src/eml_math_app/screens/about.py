"""About screen — version + links."""
from __future__ import annotations

from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen

from eml_math_app import __version__


class AboutScreen(MDScreen):
    version = StringProperty(__version__)
    eml_version = StringProperty("?")

    def on_pre_enter(self) -> None:
        try:
            import eml_math
            self.eml_version = getattr(eml_math, "__version__", "?")
        except ImportError:
            self.eml_version = "(not installed)"
