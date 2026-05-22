import threading
from queue import Queue

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from .base_ui import GameUI
from .kivy_combat_screen import CombatScreen


_MAX_LOG_LINES = 400  # Keep Label texture below the GPU's ~16K-px limit.


class _MainScreen(Screen):
    """Scrollable text output area + single-line input bar (the default view)."""

    def __init__(self, input_queue: Queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue

        root = BoxLayout(orientation="vertical", padding=8, spacing=4)
        self.add_widget(root)

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
        root.add_widget(self._scroll)

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
        root.add_widget(row)

    def _on_submit(self, *_) -> None:
        text = self._entry.text
        self._entry.text = ""
        self._input_queue.put(text)

    def append(self, text: str) -> None:
        new_text = self._output.text + text + "\n"
        # Drop the oldest lines so the underlying GPU texture stays small
        # enough to render. Without this, very long sessions silently end up
        # with an empty Label once the texture exceeds GL_MAX_TEXTURE_SIZE.
        lines = new_text.split("\n")
        if len(lines) > _MAX_LOG_LINES:
            lines = lines[-_MAX_LOG_LINES:]
            new_text = "\n".join(lines)
        self._output.text = new_text
        self._scroll.scroll_y = 0


class _RootManager(ScreenManager):
    def __init__(self, input_queue: Queue, **kwargs):
        super().__init__(transition=NoTransition(), **kwargs)
        self.main_screen = _MainScreen(input_queue, name="main")
        self.combat_screen = CombatScreen(input_queue, name="combat")
        self.add_widget(self.main_screen)
        self.add_widget(self.combat_screen)


class _KivyApp(App):
    def __init__(self, input_queue: Queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self.root_manager: _RootManager | None = None

    def build(self) -> _RootManager:
        self.root_manager = _RootManager(self._input_queue)
        return self.root_manager


class KivyUI(GameUI):
    """Kivy-based UI backend with a dedicated combat screen.

    The game logic runs in a background thread and calls get_input(), which
    blocks on a Queue. The Kivy main thread puts the user's text into that
    queue when they press Enter, click ОК, or tap an action button. Combat
    rendering switches to a separate screen (enemy art, HP bars, animated
    flash overlays, skull on death).

    Usage:
        ui = KivyUI()
        ui.run(lambda: main_game_loop(ui))
    """

    def __init__(self):
        self._input_queue: Queue[str] = Queue()
        self._app = _KivyApp(self._input_queue)
        self._in_combat = False

    # ------------------------------------------------------------------
    # GameUI primitives
    # ------------------------------------------------------------------

    def show_text(self, text: str) -> None:
        if self._in_combat:
            Clock.schedule_once(lambda dt: self._append_combat(text))
        else:
            Clock.schedule_once(lambda dt: self._append_main(text))

    def show_separator(self) -> None:
        self.show_text("=" * 50)

    def get_input(self, prompt: str) -> str:
        if prompt:
            self.show_text(prompt)
        return self._input_queue.get()

    def confirm(self, question: str) -> bool:
        answer = self.get_input(f"{question} (Так/Ні): ").lower()
        return answer in ["так", "т", "yes", "y"]

    # ------------------------------------------------------------------
    # Combat hooks (called from the game thread; marshalled via Clock)
    # ------------------------------------------------------------------

    def enter_combat(self, player, enemies) -> None:
        self._in_combat = True
        Clock.schedule_once(lambda dt: self._enter_combat(player, enemies))

    def exit_combat(self) -> None:
        Clock.schedule_once(lambda dt: self._exit_combat())
        self._in_combat = False

    def update_combat_state(self, player, enemies) -> None:
        Clock.schedule_once(lambda dt: self._update_combat_state(player, enemies))

    def show_combat_log(self, text: str) -> None:
        Clock.schedule_once(lambda dt: self._append_combat(text))

    def animate_player_attack(self, target_index: int, outcome: str) -> None:
        Clock.schedule_once(
            lambda dt: self._app.root_manager.combat_screen.flash_enemy(
                target_index, outcome
            )
        )

    def animate_enemy_attack(self, enemy_index: int, outcome: str) -> None:
        Clock.schedule_once(
            lambda dt: self._app.root_manager.combat_screen.flash_player(outcome)
        )

    def mark_enemy_dead(self, enemy_index: int) -> None:
        Clock.schedule_once(
            lambda dt: self._app.root_manager.combat_screen.mark_dead(enemy_index)
        )

    # ------------------------------------------------------------------
    # App lifecycle
    # ------------------------------------------------------------------

    def run(self, game_callable) -> None:
        """Launch the Kivy window and run *game_callable* in a daemon thread."""
        threading.Thread(target=game_callable, daemon=True).start()
        self._app.run()

    # ------------------------------------------------------------------
    # Internal (Kivy thread only)
    # ------------------------------------------------------------------

    def _append_main(self, text: str) -> None:
        rm = self._app.root_manager
        if rm is not None:
            rm.main_screen.append(text)

    def _append_combat(self, text: str) -> None:
        rm = self._app.root_manager
        if rm is None:
            return
        rm.combat_screen.append_log(text)

    def _enter_combat(self, player, enemies) -> None:
        rm = self._app.root_manager
        if rm is None:
            return
        rm.combat_screen.clear_log()
        rm.combat_screen.set_state(player, enemies)
        rm.current = "combat"

    def _exit_combat(self) -> None:
        rm = self._app.root_manager
        if rm is None:
            return
        rm.current = "main"

    def _update_combat_state(self, player, enemies) -> None:
        rm = self._app.root_manager
        if rm is None:
            return
        rm.combat_screen.set_state(player, enemies)
