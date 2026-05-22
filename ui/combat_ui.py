from ui.base_ui import GameUI


class CombatUI:
    def __init__(self, ui: GameUI):
        self._ui = ui

    def display_combat_status(self, player, enemies) -> None:
        self._ui.show_separator()
        self._ui.show_text("СТАТУС БОЮ:")
        self._ui.show_text(
            f"Гравець: {player.name} | HP: {player.hp}/{player.max_hp} | Рівень: {player.level}"
        )
        self._ui.show_text("Вороги:")
        for i, enemy in enumerate(enemies, 1):
            self._ui.show_text(f"  {i}. {enemy.name} | HP: {enemy.hp}/{enemy.max_hp}")
        self._ui.show_separator()

    def display_combat_actions(self) -> None:
        self._ui.show_actions({
            "1": "Атакувати",
            "2": "Захиститися",
            "3": "Використати предмет",
            "4": "Втекти",
        })

    def display_damage(self, attacker, defender, damage, is_crit=False, is_dodged=False) -> None:
        if is_dodged:
            self._ui.show_text(f"{defender.name} ухилився від атаки {attacker.name}!")
        elif damage > 0:
            crit_text = " (КРИТ!)" if is_crit else ""
            self._ui.show_text(
                f"{attacker.name} атакує {defender.name} на {damage} шкоди{crit_text}!"
            )
        else:
            self._ui.show_text(f"{attacker.name} не завдав шкоди {defender.name}.")

    def display_combat_log(self, log_entries) -> None:
        self._ui.show_text("\nЛОГ БОЮ:")
        for entry in log_entries:
            self._ui.show_text(f"  - {entry}")
