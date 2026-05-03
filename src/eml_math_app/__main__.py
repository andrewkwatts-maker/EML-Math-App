"""Entry point: ``python -m eml_math_app`` or via the ``eml-math-app`` script."""
from __future__ import annotations


def main() -> None:
    from eml_math_app.app import EMLMathApp
    EMLMathApp().run()


if __name__ == "__main__":
    main()
