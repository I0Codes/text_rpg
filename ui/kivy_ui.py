import threading
from queue import Queue

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from .base_ui import GameUI


class _GameScreen(BoxLayout):
    """Scrollable text output area + single-line input bar."""

    def __init__(self, input_queue: Queue, **kwargs):
        super().__init__(orientation="vertical", padding=8, spacing=4, **kwargs)
        self._input_queue = input_queue

        self._scroll = ScrollView(size_hint=(1, 0.85))
        self._output = Label(
            text="",
            size_hint_y=None,
            halign="left",
            valign="top",
        )
        self._output.bind(
            width=lambda inst, w: setattr(inst, "text_size", (w, None)),
            texture_size=self._output.setter("size"),
        )
        self._scroll.add_widget(self._output)
        self.add_widget(self._scroll)

        row = BoxLayout(size_hint=(1, 0.15), spacing=4)
        self._entry = TextInput(
            hint_text="Введіть команду...",
            multiline=False,
            size_hint=(0.8, 1),
        )
        self._entry.bind(on_text_validate=self._on_submit)
        btn = Button(text="ОК", size_hint=(0.2, 1))
        btn.bind(on_press=self._on_submit)
        row.add_widget(self._entry)
        row.add_widget(btn)
        self.add_widget(row)

    def _on_submit(self, *_) -> None:
        text = self._entry.text
        self._entry.text = ""
        self._input_queue.put(text)

    def append(self, text: str) -> None:
        self._output.text += text + "\n"
        self._scroll.scroll_y = 0


class _KivyApp(App):
    def __init__(self, input_queue: Queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self.screen: _GameScreen | None = None

    def build(self) -> _GameScreen:
        self.screen = _GameScreen(self._input_queue)
        return self.screen


class KivyUI(GameUI):
    """Kivy-based UI backend.

    The game logic runs in a background thread and calls get_input(), which
    blocks on a Queue.  The Kivy main thread puts the user's text into that
    queue when they press Enter or the OK button, unblocking the game thread.

    Usage:
        ui = KivyUI()
        ui.run(lambda: main_game_loop(ui))
    """

    def __init__(self):
        self._input_queue: Queue[str] = Queue()
        self._app = _KivyApp(self._input_queue)

    # --- GameUI primitives ---

    def show_text(self, text: str) -> None:
        Clock.schedule_once(lambda dt: self._append(text))

    def show_separator(self) -> None:
        self.show_text("=" * 50)

    def get_input(self, prompt: str) -> str:
        if prompt:
            self.show_text(prompt)
        return self._input_queue.get()

    def confirm(self, question: str) -> bool:
        answer = self.get_input(f"{question} (Так/Ні): ").lower()
        return answer in ["так", "т", "yes", "y"]

    # --- App lifecycle ---

    def run(self, game_callable) -> None:
        """Launch the Kivy window and run *game_callable* in a daemon thread."""
        threading.Thread(target=game_callable, daemon=True).start()
        self._app.run()

    # --- Internal ---

    def _append(self, text: str) -> None:
        if self._app.screen is not None:
            self._app.screen.append(text)
