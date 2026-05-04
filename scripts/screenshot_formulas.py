"""Render every formula in the test corpus through the same pipeline the
app uses, then save the resulting LaTeX-preview PNG and tree PNG side-by-side
into ``screenshots/`` so the response per formula can be eyeballed in CI
artifacts (or just on disk after a manual run).

Run from the project root::

    python scripts/screenshot_formulas.py

Output is one PNG per formula, named ``screenshots/<NN>_<label>.png``,
where each combines:

    ┌────────────────────────────────────────────┐
    │  expression text                            │
    │  rendered LaTeX preview                     │  ← matplotlib mathtext
    │  EML expression tree                        │  ← eml_math.flow_png
    │  one-line status                            │
    └────────────────────────────────────────────┘

Composing the screenshot programmatically (rather than driving the live
Kivy window) keeps the script deterministic and headless — useful for CI
and for sanity-checking the math-app's response after every eml-math
release.
"""
from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

# Make the project's ``tests/`` importable when running from the repo root.
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

# matplotlib must run head-less (no display server in CI).
import matplotlib                      # noqa: E402
matplotlib.use("Agg")
from matplotlib import pyplot as plt   # noqa: E402
from PIL import Image                  # noqa: E402

from eml_math_app.services.latex_renderer import (   # noqa: E402
    render_latex_png,
    to_latex_source,
)
from eml_math_app.services.parser import default_parser   # noqa: E402

# Reuse the test corpus so the screenshot set always matches what's pinned.
from tests.test_formulas import ALL_CASES                # noqa: E402


_OUT = _ROOT / "screenshots"
_OUT.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
def _render_one(expr: str) -> tuple[bytes, bytes, str]:
    """Run the app pipeline and return ``(latex_png, tree_png, status)``."""
    parsed = default_parser().parse(expr)
    if parsed is None:
        return b"", b"", f"Could not parse: {expr!r}"
    latex = to_latex_source(expr, parsed) or ""
    latex_png = render_latex_png(latex, figsize=(7.0, 1.1), dpi=140) or b""
    tree_png = parsed.tree.flow_png(direction="down", width=720, height=320)
    return latex_png, tree_png, parsed.info_line


def _compose(label: str, expr: str, latex_png: bytes, tree_png: bytes,
             status: str) -> Image.Image:
    """Stack the title, the LaTeX render and the tree render onto a card."""
    fig = plt.figure(figsize=(8.0, 6.0), dpi=120)
    fig.patch.set_facecolor("#1c1c20")

    # Title row
    ax_title = fig.add_axes((0.04, 0.88, 0.92, 0.10))
    ax_title.axis("off")
    ax_title.text(
        0.0, 0.7, label.replace("_", " ").title(),
        fontsize=15, fontweight="bold", color="#e8e8ea",
    )
    ax_title.text(
        0.0, 0.15, expr,
        fontfamily="monospace", fontsize=11, color="#9aa0a8",
    )

    # LaTeX preview
    ax_latex = fig.add_axes((0.04, 0.70, 0.92, 0.16))
    ax_latex.axis("off")
    ax_latex.set_facecolor("#26262c")
    if latex_png:
        ax_latex.imshow(Image.open(BytesIO(latex_png)), aspect="auto")
    else:
        ax_latex.text(0.5, 0.5, "(no LaTeX)", ha="center", va="center",
                      color="#777", fontsize=12)

    # Tree render
    ax_tree = fig.add_axes((0.04, 0.10, 0.92, 0.58))
    ax_tree.axis("off")
    if tree_png:
        ax_tree.imshow(Image.open(BytesIO(tree_png)), aspect="auto")
    else:
        ax_tree.text(0.5, 0.5, "(no tree)", ha="center", va="center",
                     color="#777", fontsize=12)

    # Footer / status
    ax_status = fig.add_axes((0.04, 0.02, 0.92, 0.06))
    ax_status.axis("off")
    ax_status.text(
        0.0, 0.5, status,
        fontfamily="monospace", fontsize=9, color="#7a7f88",
    )

    buf = BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


# ---------------------------------------------------------------------------
def main() -> None:
    width = max(len(c[0]) for c in ALL_CASES)
    print(f"Rendering {len(ALL_CASES)} formulas to {_OUT}")
    for idx, (label, expr) in enumerate(ALL_CASES, start=1):
        try:
            latex_png, tree_png, status = _render_one(expr)
            img = _compose(label, expr, latex_png, tree_png, status)
            out_path = _OUT / f"{idx:02d}_{label}.png"
            img.save(out_path, optimize=True)
            print(f"  [{idx:02d}/{len(ALL_CASES)}] {label:<{width}}  "
                  f"{len(latex_png):>6}b latex / {len(tree_png):>6}b tree  -> "
                  f"{out_path.name}")
        except Exception as exc:                         # noqa: BLE001
            print(f"  [{idx:02d}/{len(ALL_CASES)}] {label:<{width}}  "
                  f"FAILED: {type(exc).__name__}: {exc}")
    print("done.")


if __name__ == "__main__":
    main()
