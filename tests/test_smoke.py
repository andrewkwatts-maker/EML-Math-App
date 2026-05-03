"""Smoke tests — import every public surface, instantiate the App without
opening a window, and verify each screen class loads cleanly.

Pure-import; never enters Kivy's event loop (no display server needed for CI).
"""
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


@pytest.mark.parametrize("name", [
    "home", "builder", "convert", "compress", "constants", "export", "about",
])
def test_screen_classes_import(name):
    mod = importlib.import_module(f"eml_math_app.screens.{name}")
    expected = {
        "home": "HomeScreen", "builder": "BuilderScreen", "convert": "ConvertScreen",
        "compress": "CompressScreen", "constants": "ConstantsScreen",
        "export": "ExportScreen", "about": "AboutScreen",
    }[name]
    assert hasattr(mod, expected), f"{name} module missing {expected}"


def test_widgets_import():
    from eml_math_app.widgets import TreeImageView, FormulaInput
    assert TreeImageView is not None
    assert FormulaInput is not None


def test_app_class_instantiable():
    """Build an app object without calling .run() (no display required)."""
    from eml_math_app.app import EMLMathApp
    app = EMLMathApp()
    assert app.title.startswith("EML-Math-App")
