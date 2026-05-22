"""Tiny indirection so legacy print() call sites can route into the active
GameUI without threading a UI argument through every method signature.

Falls back to ``print`` when no UI is registered, so unit tests that read
stdout (via ``capsys``) and the console-only entrypoint keep working.
"""
from __future__ import annotations

from typing import Optional

from ui.base_ui import GameUI

_ui: Optional[GameUI] = None


def register_ui(ui: GameUI) -> None:
    global _ui
    _ui = ui


def output(text: str = "") -> None:
    if _ui is not None:
        _ui.show_text(text)
    else:
        print(text)
