"""KivyMD application root for EML-Math-App.

Builds the screen manager, loads every .kv file from ``kv/``, and registers
the seven screens of the app.
"""
from __future__ import annotations

import os
from pathlib import Path

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from eml_math_app import __version__

_KV_DIR = Path(__file__).parent / "kv"


class EMLMathApp(MDApp):
    """Top-level app. Material 3 dark theme by default."""

    title = f"EML-Math-App v{__version__}"

    def build(self):
        # Theme — Material You-ish dark palette, matches the eml-math docs site
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        # Load every .kv in kv/ once. Order: root.kv last so screens are
        # already registered as classes by the time root references them.
        for kv in sorted(_KV_DIR.glob("*.kv"), key=lambda p: p.name == "root.kv"):
            Builder.load_file(str(kv))

        # Import screens AFTER loading kv so factory hooks resolve cleanly
        from eml_math_app.screens.home import HomeScreen
        from eml_math_app.screens.builder import BuilderScreen
        from eml_math_app.screens.convert import ConvertScreen
        from eml_math_app.screens.compress import CompressScreen
        from eml_math_app.screens.constants import ConstantsScreen
        from eml_math_app.screens.export import ExportScreen
        from eml_math_app.screens.about import AboutScreen

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(BuilderScreen(name="builder"))
        sm.add_widget(ConvertScreen(name="convert"))
        sm.add_widget(CompressScreen(name="compress"))
        sm.add_widget(ConstantsScreen(name="constants"))
        sm.add_widget(ExportScreen(name="export"))
        sm.add_widget(AboutScreen(name="about"))
        return sm


def run() -> None:
    """Convenience entry — same as ``python -m eml_math_app``."""
    EMLMathApp().run()


if __name__ == "__main__":
    run()
