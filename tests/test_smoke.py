"""Smoke tests — pure-import. No display server / Kivy event loop needed."""
from __future__ import annotations

import importlib

import pytest


def test_app_import():
    mod = importlib.import_module("eml_math_app.app")
    assert hasattr(mod, "EMLMathApp")


def test_version_is_string():
    import eml_math_app
    v = eml_math_app.__version__
    assert isinstance(v, str)
    assert v.count(".") >= 2


def test_home_screen_imports():
    from eml_math_app.screens.home import HomeScreen
    assert HomeScreen is not None


def test_widgets_import():
    from eml_math_app.widgets import TreeImageView, LatexPreview
    assert TreeImageView is not None
    assert LatexPreview is not None


def test_services_import():
    from eml_math_app.services import formats, hit_test, latex_renderer, parser
    assert hasattr(parser, "default_parser")
    assert hasattr(formats, "format_all")
    assert hasattr(hit_test, "nearest_node")
    assert hasattr(latex_renderer, "render_latex_png")


def test_app_class_instantiable():
    """Build an app object without calling .run() (no display required)."""
    from eml_math_app.app import EMLMathApp
    app = EMLMathApp()
    assert app.title.startswith("EML-Math-App")
