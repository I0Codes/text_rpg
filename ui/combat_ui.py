# ui/combat_ui.py

class CombatUI:
    """Клас для відображення інтерфейсу бою"""

    # ANSI escape codes for colors
    RED = "\033[91m"  # For damage
    GREEN = "\033[92m"  # For healing
    RESET = "\033[0m"  # Reset to default

    @staticmethod
    def display_combat_status(player, enemies):
        """Показати статус всіх учасників бою
        
        Args:
            player: Об'єкт гравця (Character)
            enemies: Список ворогів (list of Enemy)
        """
        print("\n" + "=" * 50)
        print("СТАТУС БОЮ:")
        print(f"Гравець: {player.name} | HP: {player.hp}/{player.max_hp} | Рівень: {player.level}")
        print("Вороги:")
        for i, enemy in enumerate(enemies, 1):
            print(f"  {i}. {enemy.name} | HP: {enemy.hp}/{enemy.max_hp}")
        print("=" * 50)

    @staticmethod
    def display_combat_actions():
        """Показати доступні дії"""
        actions = {
            "1": "Атакувати",
            "2": "Захиститися",
            "3": "Використати предмет",
            "4": "Втекти"
        }
        print("\nДоступні дії:")
        for key, description in actions.items():
            print(f"  {key} — {description}")

    @staticmethod
    def display_damage(attacker, defender, damage, is_crit=False, is_dodged=False):
        """Красиво показати результат атаки
        
        Args:
            attacker: Об'єкт атакуючого (Character або Enemy)
            defender: Об'єкт захисника (Character або Enemy)
            damage: Кількість шкоди (int)
            is_crit: Чи був це критичний удар (bool)
            is_dodged: Чи ухилився захисник (bool)
        """
        if is_dodged:
            print(f"{defender.name} ухилився від атаки {attacker.name}!")
        elif damage > 0:
            crit_text = " (КРИТ!)" if is_crit else ""
            print(f"{attacker.name} атакує {defender.name} на {CombatUI.RED}{damage}{CombatUI.RESET} шкоди{crit_text}!")
        else:
            print(f"{attacker.name} не завдав шкоди {defender.name}.")

    @staticmethod
    def display_combat_log(log_entries):
        """Показати лог бою
        
        Args:
            log_entries: Список записів логу (list of str)
        """
        print("\nЛОГ БОЮ:")
        for entry in log_entries:
            print(f"  - {entry}")
        print()

# Example usage for testing (can be added to a test file or main.py)
if __name__ == "__main__":
    from entities.characters import Character
    from entities.enemies import Enemy

    # Create test instances
    player = Character(name="Герой", hp=100, max_hp=100, stamina=50, max_stamina=50)
    enemy1 = Enemy(name="Гоблін", hp=50, attack=10, defense=5, level=1, xp_reward=20, reward_gold=5)
    enemy2 = Enemy(name="Орк", hp=80, attack=15, defense=10, level=2, xp_reward=40, reward_gold=10)
    enemies = [enemy1, enemy2]

    # Test display_combat_status
    CombatUI.display_combat_status(player, enemies)

    # Test display_combat_actions
    CombatUI.display_combat_actions()

    # Test display_damage with various scenarios
    CombatUI.display_damage(player, enemy1, 25, is_crit=True)  # Normal crit damage
    CombatUI.display_damage(enemy1, player, 10)  # Normal damage
    CombatUI.display_damage(enemy2, player, 0, is_dodged=True)  # Dodge
    CombatUI.display_damage(player, enemy2, 30)  # Normal damage

    # Test display_combat_log
    log_entries = [
        "Герой розпочав бій.",
        "Гоблін атакував на 10 шкоди.",
        "Герой ухилився від атаки Орка.",
        "Герой переміг!"
    ]
    CombatUI.display_combat_log(log_entries)