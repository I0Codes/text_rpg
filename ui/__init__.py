"""UI package — interface, console implementation, progression helpers.

To use the Kivy backend, import it explicitly:
    from ui.kivy_ui import KivyUI
(requires kivy to be installed)
"""
from .base_ui import GameUI
from .console_ui import ConsoleUI
from .progression_ui import ProgressionUI

__all__ = ["GameUI", "ConsoleUI", "ProgressionUI"]
