from ui.base_ui import GameUI
from ui.menus import InventoryMenu
from world.locations import Location

from .combat import Combat


class Game:
    def __init__(self, player, start_location, ui: GameUI):
        self.player = player
        self.current_location = start_location
        self.is_running = True
        self._ui = ui
        self._combat = Combat(player, ui)

    def show_status(self):
        self._ui.show_separator()
        exp_summary = self.player.experience_manager.get_summary()
        progress = exp_summary["progress_percentage"]
        status = (
            f"Персонаж: {self.player.name}\n"
            f"Рівень: {self.player.level}\n"
            f"HP: {self.player.hp}/{self.player.max_hp}\n"
            f"Досвід: {exp_summary['total_experience']}/{exp_summary['experience_to_next_level']}"
            f" ({progress:.1f}%)\n"
            f"Локація: {self.current_location.name}"
        )
        self._ui.show_status(status)
        self._ui.show_separator()

    def show_actions(self):
        self._ui.show_actions(self.current_location.get_actions())

    def handle_action(self, choice):
        choice = choice.strip()
        choice_lower = choice.lower()

        if choice_lower == "вийти":
            if self._ui.confirm("Ви впевнені що хочете вийти з гри?"):
                self.is_running = False
                self._ui.show_text("\nВи залишаєте гру...")
            return

        if choice_lower == "i":
            InventoryMenu(self._ui).show(self.player)
            return

        if choice_lower == "s":
            self.show_status()
            return

    def check_game_over(self):
        if not self.player.is_alive():
            self._ui.show_text("\n💀 Ваш персонаж загинув.")
            self.is_running = False

    def run(self):
        self._ui.show_text("\n🌲 Гра розпочалась!")
        self._ui.show_text("Системні команди: вийти")

        while self.is_running:
            self.show_status()
            self.show_actions()
            choice = self._ui.get_input("\nВаш вибір: ")
            self.handle_action(choice)
            self.check_game_over()

        self._ui.show_text("\n🎮 Гру завершено.")
