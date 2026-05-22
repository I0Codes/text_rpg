"""Combat screen widget for the Kivy backend.

Renders the current encounter as:
  - a large enemy "portrait" (PNG from assets/enemies/<name>.png or a coloured
    placeholder drawn on canvas)
  - flash overlays for hit / miss / crit feedback
  - a scrolling combat log
  - HP bars for the active target and the player
  - a row of action buttons (Атака / Захист / Предмет / Втеча) plus a text
    input field for sub-prompts (item selection, etc.)
"""

from __future__ import annotations

import os
from queue import Queue

from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


_ASSET_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "enemies"
)
_MAX_LOG_LINES = 400  # Keep Label texture below the GPU's ~16K-px limit.


def _enemy_image_path(enemy_name: str) -> str | None:
    """Return path to enemy art if it exists, else None."""
    for ext in (".png", ".jpg", ".jpeg"):
        path = os.path.join(_ASSET_DIR, enemy_name.lower() + ext)
        if os.path.isfile(path):
            return path
    return None


def _skull_image_path() -> str | None:
    for ext in (".png", ".jpg", ".jpeg"):
        path = os.path.join(_ASSET_DIR, "skull" + ext)
        if os.path.isfile(path):
            return path
    return None


# Pleasant fallback tints so a placeholder still feels enemy-specific.
_ENEMY_TINTS: dict[str, tuple[float, float, float]] = {
    "goblin": (0.30, 0.55, 0.25),
    "wolf":   (0.45, 0.40, 0.35),
    "bandit": (0.55, 0.35, 0.25),
    "orc":    (0.35, 0.50, 0.30),
    "troll":  (0.40, 0.45, 0.30),
    "dragon": (0.65, 0.20, 0.20),
}


class EnemyPortrait(FloatLayout):
    """Single enemy art slot with hp bar, name and a flash overlay."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background colour block (also acts as placeholder art).
        with self.canvas.before:
            self._bg_color = Color(0.15, 0.15, 0.20, 1)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync_rects, size=self._sync_rects)

        # Image (only used when a real PNG exists).
        self._image = Image(
            fit_mode="contain",
            size_hint=(0.9, 0.75),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
        )
        self.add_widget(self._image)

        # Large fallback glyph centred behind the image (visible only when no
        # PNG is loaded).
        self._glyph = Label(
            text="",
            font_size="96sp",
            color=(1, 1, 1, 0.85),
            size_hint=(1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
        )
        self.add_widget(self._glyph)

        # Name + HP labels at the top.
        self._name_label = Label(
            text="",
            font_size="20sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.12),
            pos_hint={"center_x": 0.5, "top": 1},
        )
        self.add_widget(self._name_label)

        # HP bar pinned to the bottom.
        self._hp_bar = ProgressBar(
            max=100,
            value=100,
            size_hint=(0.9, 0.04),
            pos_hint={"center_x": 0.5, "y": 0.02},
        )
        self.add_widget(self._hp_bar)
        self._hp_label = Label(
            text="",
            font_size="14sp",
            color=(1, 1, 1, 1),
            size_hint=(0.9, 0.06),
            pos_hint={"center_x": 0.5, "y": 0.06},
        )
        self.add_widget(self._hp_label)

        # Flash overlay (drawn on canvas.after so it sits on top of everything).
        with self.canvas.after:
            self._flash_color = Color(1, 0, 0, 0)
            self._flash_rect = Rectangle(pos=self.pos, size=self.size)

        self._dead = False
        self._enemy_name = ""
        self._enemy_level = 1

    def _sync_rects(self, *_):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._flash_rect.pos = self.pos
        self._flash_rect.size = self.size

    def set_enemy(self, enemy) -> None:
        self._dead = False
        name = getattr(enemy, "name", "?")
        level = getattr(enemy, "level", 1)
        self._enemy_name = name
        self._enemy_level = level
        self._name_label.text = f"{name}  (рів. {level})"
        self._name_label.color = (1, 1, 1, 1)

        tint = _ENEMY_TINTS.get(name.lower(), (0.30, 0.30, 0.40))
        self._bg_color.rgba = (*tint, 1.0)

        path = _enemy_image_path(name)
        if path:
            self._image.source = path
            self._image.opacity = 1
            self._glyph.text = ""
        else:
            self._image.source = ""
            self._image.opacity = 0
            self._glyph.text = self._fallback_glyph(name)
            self._glyph.color = (1, 1, 1, 0.92)

        self._hp_bar.opacity = 1
        self._hp_label.opacity = 1
        self.update_hp(enemy)

    def update_hp(self, enemy) -> None:
        if self._dead:
            return
        hp = max(0, getattr(enemy, "hp", 0))
        max_hp = max(1, getattr(enemy, "max_hp", 1))
        pct = hp / max_hp
        self._hp_bar.max = max_hp
        self._hp_bar.value = hp
        self._hp_label.text = f"HP: {hp}/{max_hp}"

    def show_skull(self) -> None:
        self._dead = True
        path = _skull_image_path()
        if path:
            self._image.source = path
            self._image.opacity = 1
            self._glyph.text = ""
        else:
            self._image.source = ""
            self._image.opacity = 0
            self._glyph.text = "💀"
            self._glyph.color = (0.85, 0.85, 0.85, 1)
        self._bg_color.rgba = (0.08, 0.08, 0.10, 1.0)
        name = self._enemy_name or "Ворог"
        self._name_label.text = f"{name}  — повалений"
        self._name_label.color = (0.7, 0.7, 0.7, 1)
        self._hp_bar.opacity = 0
        self._hp_label.opacity = 0

    def flash(self, rgb: tuple[float, float, float], peak_alpha: float = 0.55,
              duration: float = 0.35) -> None:
        # Snap to peak, then fade out.
        Animation.cancel_all(self._flash_color)
        self._flash_color.rgba = (*rgb, peak_alpha)
        Animation(a=0.0, duration=duration, t="out_quad").start(self._flash_color)

    @staticmethod
    def _fallback_glyph(name: str) -> str:
        mapping = {
            "goblin": "👺",
            "wolf": "🐺",
            "bandit": "🗡",
            "orc": "👹",
            "troll": "🧌",
            "dragon": "🐲",
        }
        return mapping.get(name.lower(), name[:1].upper() if name else "?")


class CombatScreen(Screen):
    """Full combat view: enemies on top, log + HP bars in the middle, controls
    at the bottom."""

    def __init__(self, input_queue: Queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self._portraits: list[EnemyPortrait] = []
        self._portrait_box: BoxLayout | None = None

        root = BoxLayout(orientation="vertical", padding=6, spacing=6)
        self.add_widget(root)

        # --- Enemies row ---
        self._portrait_box = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.42),
            spacing=6,
        )
        root.add_widget(self._portrait_box)

        # --- Combat log ---
        self._log_scroll = ScrollView(size_hint=(1, 0.28))
        self._log = Label(
            text="",
            size_hint_y=None,
            halign="left",
            valign="top",
            color=(1, 1, 1, 1),
        )
        self._log.bind(
            width=lambda inst, w: setattr(inst, "text_size", (w, None)),
            texture_size=self._log.setter("size"),
        )
        self._log_scroll.add_widget(self._log)
        root.add_widget(self._log_scroll)

        # --- Player status with flash overlay ---
        self._player_box = FloatLayout(size_hint=(1, 0.12))
        root.add_widget(self._player_box)

        inner = BoxLayout(orientation="vertical", spacing=2,
                          size_hint=(1, 1), pos_hint={"x": 0, "y": 0})
        self._player_box.add_widget(inner)

        self._player_label = Label(
            text="",
            font_size="16sp",
            color=(1, 1, 1, 1),
            size_hint=(1, 0.5),
            halign="left",
            valign="middle",
        )
        self._player_label.bind(
            size=lambda inst, val: setattr(inst, "text_size", val),
        )
        inner.add_widget(self._player_label)

        self._player_hp_bar = ProgressBar(max=100, value=100, size_hint=(1, 0.5))
        inner.add_widget(self._player_hp_bar)

        # Player flash overlay (on the player_box).
        with self._player_box.canvas.after:
            self._player_flash_color = Color(1, 0, 0, 0)
            self._player_flash_rect = Rectangle(
                pos=self._player_box.pos, size=self._player_box.size,
            )
        self._player_box.bind(pos=self._sync_player_flash,
                              size=self._sync_player_flash)

        # --- Actions row ---
        actions = BoxLayout(orientation="horizontal",
                            size_hint=(1, 0.10), spacing=4)
        for label, value in [
            ("⚔ Атака (1)", "1"),
            ("🛡 Захист (2)", "2"),
            ("🧪 Предмет (3)", "3"),
            ("🏃 Втеча (4)", "4"),
        ]:
            btn = Button(text=label)
            btn.bind(on_press=lambda _b, v=value: self._submit(v))
            actions.add_widget(btn)
        root.add_widget(actions)

        # --- Free-form input row (for item picks etc.) ---
        entry_row = BoxLayout(orientation="horizontal",
                              size_hint=(1, 0.08), spacing=4)
        self._entry = TextInput(
            hint_text="Введіть команду або номер...",
            multiline=False,
            size_hint=(0.8, 1),
        )
        self._entry.bind(on_text_validate=lambda *_: self._submit_entry())
        ok_btn = Button(text="ОК", size_hint=(0.2, 1))
        ok_btn.bind(on_press=lambda *_: self._submit_entry())
        entry_row.add_widget(self._entry)
        entry_row.add_widget(ok_btn)
        root.add_widget(entry_row)

    # ----- submission helpers -----

    def _submit(self, text: str) -> None:
        self._input_queue.put(text)

    def _submit_entry(self) -> None:
        text = self._entry.text
        self._entry.text = ""
        self._input_queue.put(text)

    def _sync_player_flash(self, *_):
        self._player_flash_rect.pos = self._player_box.pos
        self._player_flash_rect.size = self._player_box.size

    # ----- public API used by KivyUI -----

    def set_state(self, player, enemies) -> None:
        """Sync portraits and HP bars with the current encounter."""
        self._ensure_portraits(len(enemies))
        for portrait, enemy in zip(self._portraits, enemies):
            enemy_name = getattr(enemy, "name", "")
            is_alive = getattr(enemy, "is_alive", lambda: True)()
            if not is_alive:
                # Already-dead enemy: ensure portrait holds this enemy's name
                # before flipping to the skull, and don't re-flip if already shown.
                if portrait._enemy_name != enemy_name:
                    portrait.set_enemy(enemy)
                if not portrait._dead:
                    portrait.show_skull()
                continue
            # Live enemy: re-init only on slot change; otherwise just refresh HP.
            if portrait._enemy_name != enemy_name or portrait._dead:
                portrait.set_enemy(enemy)
            else:
                portrait.update_hp(enemy)
        self._update_player(player)

    def _ensure_portraits(self, n: int) -> None:
        if n == len(self._portraits):
            return
        self._portrait_box.clear_widgets()
        self._portraits = []
        for _ in range(max(1, n)):
            p = EnemyPortrait()
            self._portraits.append(p)
            self._portrait_box.add_widget(p)

    def _update_player(self, player) -> None:
        hp = max(0, getattr(player, "hp", 0))
        max_hp = max(1, getattr(player, "max_hp", 1))
        name = getattr(player, "name", "Гравець")
        level = getattr(player, "level", 1)
        self._player_label.text = (
            f"{name}  (рів. {level})    HP: {hp}/{max_hp}"
        )
        self._player_hp_bar.max = max_hp
        self._player_hp_bar.value = hp

    def append_log(self, text: str) -> None:
        if not text:
            return
        new_text = self._log.text + text + "\n"
        lines = new_text.split("\n")
        if len(lines) > _MAX_LOG_LINES:
            lines = lines[-_MAX_LOG_LINES:]
            new_text = "\n".join(lines)
        self._log.text = new_text
        self._log_scroll.scroll_y = 0

    def clear_log(self) -> None:
        self._log.text = ""

    def flash_enemy(self, index: int, outcome: str) -> None:
        if not self._portraits:
            return
        idx = max(0, min(index, len(self._portraits) - 1))
        color, alpha, dur = self._outcome_style(outcome, hostile_to_enemy=True)
        self._portraits[idx].flash(color, peak_alpha=alpha, duration=dur)

    def flash_player(self, outcome: str) -> None:
        color, alpha, dur = self._outcome_style(outcome, hostile_to_enemy=False)
        Animation.cancel_all(self._player_flash_color)
        self._player_flash_color.rgba = (*color, alpha)
        Animation(a=0.0, duration=dur, t="out_quad").start(self._player_flash_color)

    def mark_dead(self, index: int) -> None:
        if not self._portraits:
            return
        idx = max(0, min(index, len(self._portraits) - 1))
        self._portraits[idx].show_skull()

    @staticmethod
    def _outcome_style(outcome: str, hostile_to_enemy: bool):
        # (rgb, peak alpha, duration)
        if outcome == "crit":
            return (1.0, 0.15, 0.15), 0.75, 0.55
        if outcome == "hit":
            return (1.0, 0.10, 0.10), 0.55, 0.35
        if outcome in ("miss", "dodge"):
            return (1.0, 1.0, 1.0), 0.55, 0.30
        if outcome == "blocked":
            return (0.20, 0.55, 1.0), 0.45, 0.35
        return (1.0, 1.0, 1.0), 0.35, 0.25
