"""KivyMD application root for EML-Math-App.

Single-page calculator + EML renderer. No ScreenManager — the whole UI is
``HomeScreen``, loaded from ``kv/home.kv`` (with shared rules in ``root.kv``).
"""
from __future__ import annotations

from pathlib import Path

from kivy.lang import Builder
from kivymd.app import MDApp

from eml_math_app import __version__
# Eager imports so the Factory knows the custom widgets before kv parses.
from eml_math_app.widgets.copy_chip import CopyChip  # noqa: F401
from eml_math_app.widgets.expr_input import ExprInput  # noqa: F401
from eml_math_app.widgets.latex_preview import LatexPreview  # noqa: F401
from eml_math_app.widgets.svg_view import TreeImageView  # noqa: F401

_KV_DIR = Path(__file__).parent / "kv"


class EMLMathApp(MDApp):
    title = f"EML-Math-App v{__version__}"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"

        # root.kv first (defines shared rules), then home.kv.
        Builder.load_file(str(_KV_DIR / "root.kv"))
        Builder.load_file(str(_KV_DIR / "home.kv"))

        from eml_math_app.screens.home import HomeScreen
        return HomeScreen()


def run() -> None:
    EMLMathApp().run()


if __name__ == "__main__":
    run()
