# EML-Math-App

**v1.3.1** — KivyMD visual explorer for the [`eml-math`](https://pypi.org/project/eml-math/) PyPI library.

[![CI](https://github.com/andrewkwatts-maker/EML-Math-App/actions/workflows/ci.yml/badge.svg)](https://github.com/andrewkwatts-maker/EML-Math-App/actions/workflows/ci.yml)

A cross-platform GUI (Windows / Linux / macOS / Android) for working with the **EML Sheffer operator** `eml(x, y) = exp(x) − ln(y)`. Build expressions, see the binary tree render live, convert between LaTeX / MathJax / EML / Python, browse the 136 named-constants registry, run beam-search compression, and export to SVG / HTML / PNG / PDF.

The app owns no math — every screen wires UI controls directly to the `eml-math` public API.

---

## Screens

| Screen | What it does | eml-math API used |
|---|---|---|
| **Builder** | Type an expression, see the binary tree render live; pick direction (down/up/left/right) and edge style (straight/curve/spline) | `parse_eml_tree`, `EMLTreeNode.flow_png` |
| **Convert** | Three live-linked panes — LaTeX ↔ Python ↔ EML | `compress_str`, `compress_latex`, `decompress(fmt=…)`, `get` |
| **Compress** | Sample a function, beam-search for the minimal EML formula; visualise the result | `compress_str(precision_goal=…, max_complexity=…, x_lo=…, x_hi=…)` |
| **Constants** | Filterable list of all 136 named constants with EML datasheets | `list_symbols`, `Get(name)` |
| **Export** | Save the active expression to SVG / HTML / PNG / PDF | `flow_svg`, `flow_html`, `flow_png`, `flow_pdf` |

---

## Installation

```bash
pip install eml-math-app           # then: eml-math-app
# OR run from the repo:
git clone https://github.com/andrewkwatts-maker/EML-Math-App.git
cd EML-Math-App
pip install -e .
python -m eml_math_app
```

Required dependencies (pulled in automatically): `kivy>=2.3`, `kivymd>=1.2`, `Pillow>=10`, `eml-math>=1.3.1`.

---

## Building binaries

### Windows `.exe` (single-file)

```bat
build_exe.bat
.\dist\EML-Math-App.exe
```

Uses PyInstaller. First run takes ~3 minutes; output is a single ~50 MB `.exe` bundling Python + Kivy + KivyMD + eml-math.

### Android `.apk` (debug)

```bat
build_apk.bat
adb install -r .\bin\eml-math-app-1.3.1-debug.apk
```

Buildozer is Linux-only, so `build_apk.bat` shells into WSL2 (default distro `Ubuntu`; override with `set WSL_DISTRO=Ubuntu-22.04`). One-time WSL setup is documented at the top of `build_apk.bat`.

---

## Project layout

```
EML-Math-App/
├─ pyproject.toml
├─ buildozer.spec               # Android packaging config
├─ build_exe.bat                # Windows executable
├─ build_apk.bat                # Android APK (via WSL2)
├─ src/eml_math_app/
│  ├─ __init__.py               # __version__ = "1.3.1"
│  ├─ __main__.py               # python -m eml_math_app
│  ├─ app.py                    # MDApp + ScreenManager
│  ├─ kv/                       # one .kv per screen
│  ├─ screens/                  # one .py per screen
│  └─ widgets/                  # TreeImageView, FormulaInput
└─ tests/test_smoke.py
```

## Versioning

Lockstep with the EML stack: `eml-math 1.3.1`, `eml-spectral 1.3.1`, `metaphysica 1.3.1`, `periodica 1.3.1`. Bump in sync with library releases.

## License

MIT — © Andrew K Watts.
