"""Export screen — write the active expression to SVG / HTML / PNG / PDF."""
from __future__ import annotations

from pathlib import Path

from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.screen import MDScreen


class ExportScreen(MDScreen):
    expr_field = ObjectProperty(None)
    out_dir_field = ObjectProperty(None)
    status = StringProperty("Type an expression and pick a format")

    def _build_tree(self):
        text = (self.expr_field.text or "").strip() if self.expr_field else ""
        if not text:
            return None
        from eml_math import parse_eml_tree
        if not text.startswith("EML:"):
            text = f"EML: {text}"
        return parse_eml_tree(text, expand_eml=True)

    def _resolve_dir(self) -> Path:
        raw = (self.out_dir_field.text or "").strip() if self.out_dir_field else ""
        if not raw:
            raw = str(Path.cwd())
        p = Path(raw).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p

    def _slug(self, text: str) -> str:
        s = "".join(c if c.isalnum() else "_" for c in (text or "expression"))
        return s.strip("_")[:40] or "expression"

    def export(self, fmt: str) -> None:
        try:
            tree = self._build_tree()
            if tree is None:
                self.status = "Empty expression"
                return
            out_dir = self._resolve_dir()
            stem = self._slug(self.expr_field.text)
            ext = {"svg": "svg", "html": "html", "png": "png", "pdf": "pdf"}.get(fmt)
            if ext is None:
                self.status = f"Unknown format: {fmt!r}"
                return
            target = out_dir / f"{stem}.{ext}"
            if fmt == "svg":
                target.write_text(tree.flow_svg(), encoding="utf-8")
            elif fmt == "html":
                target.write_text(tree.flow_html(), encoding="utf-8")
            elif fmt == "png":
                target.write_bytes(tree.flow_png())
            elif fmt == "pdf":
                target.write_bytes(tree.flow_pdf())
            self.status = f"Wrote {target}"
        except Exception as exc:                      # noqa: BLE001
            self.status = f"{type(exc).__name__}: {exc}"
