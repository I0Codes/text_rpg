"""UI package — import the interface and the console implementation.

To use the Kivy backend, import it explicitly:
    from ui.kivy_ui import KivyUI
(requires kivy to be installed)
"""
from .base_ui import GameUI
from .console_ui import ConsoleUI

__all__ = ["GameUI", "ConsoleUI"]
