from entities.enemies import Enemy
from ui import ProgressionUI
from ui.base_ui import GameUI
from ui.menus import InventoryMenu
from world.locations import Location
from world.events import ChoiceEvent

from .combat import Combat
from .game_engine import GameEngine


class Game:
    def __init__(self, player, start_location, ui: GameUI):
        self.player = player
        self.current_location = start_location
        self.is_running = True
        self._ui = ui
        self._combat = Combat(player, ui)
        self._progression_ui = ProgressionUI(ui)
        self.current_event = None

    def show_status(self):
        self._ui.show_separator()
        exp_summary = self.player.experience_manager.get_summary()
        progress = exp_summary["progress_percentage"]
        totals = GameEngine.calculate_total_stats(self.player)
        status = (
            f"Персонаж: {self.player.name}\n"
            f"Рівень: {self.player.level}\n"
            f"HP: {self.player.hp}/{self.player.max_hp}\n"
            f"Досвід: {exp_summary['total_experience']}/{exp_summary['experience_to_next_level']}"
            f" ({progress:.1f}%)\n"
            f"Макс HP: {totals['max_hp']}  Crit: {totals['crit_chance']:.1%}"
            f"  Dodge: {totals['dodge_chance']:.1%}\n"
            f"Фізичне ураження: {totals['physical_damage']:.1f}"
            f"  Магічне ураження: {totals['magical_damage']:.1f}\n"
            f"Локація: {self.current_location.name}"
        )
        self._ui.show_status(status)
        self._ui.show_separator()

    def show_actions(self):
        self._ui.show_actions(self.current_location.get_actions())

    def handle_action(self, choice):
        if self.current_event is not None:
            self._handle_choice_event(choice)
            return

        choice = choice.strip()
        choice_lower = choice.lower()

        if choice_lower == "вийти":
            if self._ui.confirm("Ви впевнені що хочете вийти з гри?"):
                self.is_running = False
                self._ui.show_text("\nВи залишаєте гру...")
            return

        if choice_lower in ["статус", "status", "листок", "sheet"]:
            self._progression_ui.display_character_sheet(self.player)
            return

        if choice_lower in ["атрибути", "attributes", "attribute"]:
            available_points = getattr(self.player.leveling_system, "attribute_points", 0)
            self._progression_ui.display_attribute_menu(self.player, available_points)
            return

        if choice_lower == "i":
            InventoryMenu(self._ui).show(self.player)
            return

        if choice_lower == "s":
            self.show_status()
            return

        result = self.current_location.handle_action(choice, self.player)

        if isinstance(result, ChoiceEvent):
            self.current_event = result
            result.trigger(self.player)
            result.show_choices()
        elif isinstance(result, Enemy):
            self._combat.run([result])
        elif isinstance(result, Location):
            self.current_location = result
            self._ui.show_text(f"\n⇨ Ви перемістилися до {self.current_location.name}")

    def _handle_choice_event(self, choice):
        try:
            choice_index = int(choice.strip())
            if 1 <= choice_index <= len(self.current_event.choices):
                self.current_event.resolve(self.player, choice_index)
                self.current_event = None
            else:
                self._ui.show_text(
                    f"⚠️ Невірний вибір. Введіть число від 1 до {len(self.current_event.choices)}."
                )
                self.current_event.show_choices()
        except ValueError:
            self._ui.show_text("⚠️ Будь ласка, введіть число.")
            self.current_event.show_choices()

    def check_game_over(self):
        if not self.player.is_alive():
            self._ui.show_text("\n💀 Ваш персонаж загинув.")
            self.is_running = False

    def run(self):
        self._ui.show_text("\n🌲 Гра розпочалась!")
        self._ui.show_text("Системні команди: вийти, статус, атрибути")

        while self.is_running:
            if self.current_event is not None:
                choice = self._ui.get_input("\nВаш вибір (введіть номер): ")
            else:
                self.show_status()
                self.show_actions()
                choice = self._ui.get_input("\nВаш вибір: ")

            self.handle_action(choice)
            self.check_game_over()

        self._ui.show_text("\n🎮 Гру завершено.")
