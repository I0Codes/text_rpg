try:
    from config.settings import LUCK_BONUS_MULTIPLIER
except ImportError:
    LUCK_BONUS_MULTIPLIER = 0.003

from ui.base_ui import GameUI


class ProgressionUI:
    def __init__(self, ui: GameUI):
        self._ui = ui

    def display_level_up(self, character, new_level: int) -> None:
        self._ui.show_separator()
        self._ui.show_text("  ★  ПІДНЯТТЯ РІВНЯ  ★")
        self._ui.show_text(f"  {character.name}")
        self._ui.show_text(f"  Рівень: {new_level - 1} → {new_level}")
        self._ui.show_text("  ✨ +3 очок атрибутів")
        self._ui.show_text("  Класові бонуси застосовані!")
        exp_summary = character.experience_manager.get_summary()
        self._ui.show_text(
            f"  До рівня {new_level + 1}: {exp_summary['experience_to_next_level']} досвіду"
        )
        self._ui.show_separator()

    def display_character_sheet(self, character) -> None:
        self._ui.show_separator()
        self._ui.show_text(f"  ★  {character.name.upper()}  ★")
        self._ui.show_text(f"  Рівень: {character.level}")
        self._ui.show_text(f"  Здоров'я: {character.hp}/{character.max_hp}")
        self._ui.show_text(f"  Мана: {character.mana}/{character.max_mana}")
        self._ui.show_text(f"  Витривалість: {character.stamina}/{character.max_stamina}")

        exp_summary = character.experience_manager.get_summary()
        self._ui.show_text(
            f"  Досвід: {character.experience_manager.total_experience}"
            f"/{character.experience_manager.experience_to_next_level}"
        )
        filled = int((exp_summary["progress_percentage"] / 100) * 40)
        bar = "█" * filled + "░" * (40 - filled)
        self._ui.show_text(f"  [{bar}] {exp_summary['progress_percentage']:.1f}%")

        attrs = character.attributes
        self._ui.show_text("\n  АТРИБУТИ:")
        self._ui.show_text(
            f"  Сила: {attrs.strength}"
            f" (+{attrs.get_physical_damage_bonus():.1f} шкода, +{attrs.get_hp_bonus():.1f} HP)"
        )
        self._ui.show_text(
            f"  Інтелект: {attrs.intelligence}"
            f" (+{attrs.get_magic_damage_bonus():.1f} магія, +{attrs.get_mana_bonus():.1f} мана)"
        )
        self._ui.show_text(
            f"  Ловкість: {attrs.agility}"
            f" (Крит: {attrs.get_crit_chance():.1%}, Ухил: {attrs.get_dodge_chance():.1%})"
        )
        self._ui.show_text(
            f"  Удача: {attrs.luck}"
            f" (Бонус: {LUCK_BONUS_MULTIPLIER * attrs.luck:.1%})"
        )
        self._ui.show_text(f"  Золото: {character.gold}")
        self._ui.show_text(
            f"  Інвентар: {len(character.inventory.items)}/{character.inventory.max_capacity}"
        )
        self._ui.show_separator()

    def display_attribute_menu(self, character, available_points: int) -> None:
        self._ui.show_separator()
        self._ui.show_text("  РОЗПОДІЛ ОЧОК АТРИБУТІВ")
        self._ui.show_text(f"  Доступні очки: {available_points}")

        attrs = character.attributes
        for key, name, current, bonus in [
            ("1", "Сила (Strength)", attrs.strength, "+1.5 до фізичної шкоди, +2 до HP"),
            ("2", "Інтелект (Intelligence)", attrs.intelligence, "+2 до магічної шкоди, +2 до мани"),
            ("3", "Ловкість (Agility)", attrs.agility, "+0.5% до крита, +1% до ухилення"),
            ("4", "Удача (Luck)", attrs.luck, "+0.3% до крита та ухилення"),
        ]:
            self._ui.show_text(f"\n  {key}. {name}")
            self._ui.show_text(f"     Поточно: {current}")
            self._ui.show_text(f"     Бонус: {bonus}")

        self._ui.show_separator()
        self._ui.show_text("  Введіть номер атрибута (1-4) або 0 для скасування")

    def display_experience_gain(self, amount: int, source: str, progress_percent: float) -> None:
        self._ui.show_text(f"\n✨ +{amount} досвіду від {source}!")
        filled = int((progress_percent / 100) * 40)
        bar = "█" * filled + "░" * (40 - filled)
        self._ui.show_text(f"Прогрес: [{bar}] {progress_percent:.1f}%")
