from ui.base_ui import GameUI


class CombatUI:
    """Combat presentation helper.

    Always writes a text log line so any backend stays readable. When the
    backend supports the graphical combat-screen hooks (see GameUI), this
    also triggers HP-bar refreshes and hit/miss flash animations.
    """

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
        self._ui.update_combat_state(player, enemies)

    def display_combat_actions(self) -> None:
        self._ui.show_actions({
            "1": "Атакувати",
            "2": "Захиститися",
            "3": "Використати предмет",
            "4": "Втекти",
        })

    def display_damage(self, attacker, defender, damage, is_crit=False,
                       is_dodged=False, target_index=0, attacker_is_player=True) -> None:
        if is_dodged:
            self._ui.show_text(f"{defender.name} ухилився від атаки {attacker.name}!")
            outcome = "dodge"
        elif damage > 0:
            crit_text = " (КРИТ!)" if is_crit else ""
            self._ui.show_text(
                f"{attacker.name} атакує {defender.name} на {damage} шкоди{crit_text}!"
            )
            outcome = "crit" if is_crit else "hit"
        else:
            self._ui.show_text(f"{attacker.name} не завдав шкоди {defender.name}.")
            outcome = "blocked"

        if attacker_is_player:
            self._ui.animate_player_attack(target_index, outcome)
        else:
            self._ui.animate_enemy_attack(target_index, outcome)

    def display_combat_log(self, log_entries) -> None:
        self._ui.show_text("\nЛОГ БОЮ:")
        for entry in log_entries:
            self._ui.show_text(f"  - {entry}")
