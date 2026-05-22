import random

from entities.characters import Character, Warrior, Mage, Scout
from ui.base_ui import GameUI


class MainMenu:
    def __init__(self, ui: GameUI):
        self._ui = ui

    def show(self) -> str:
        while True:
            self._ui.show_text("\n=== ГОЛОВНЕ МЕНЮ ===")
            self._ui.show_text("1. Нова гра")
            self._ui.show_text("2. Завантажити гру")
            self._ui.show_text("3. Налаштування")
            self._ui.show_text("4. Вихід")

            choice = self._ui.get_input("Виберіть опцію: ").strip()
            if choice == "1":
                return "new_game"
            elif choice == "2":
                return "load_game"
            elif choice == "3":
                return "settings"
            elif choice == "4":
                return "exit"
            else:
                self._ui.show_text("Невірний вибір, спробуйте ще.")


class CharacterCreationMenu:
    def __init__(self, ui: GameUI):
        self._ui = ui

    def show(self) -> Character:
        self._ui.show_text("\n=== СТВОРЕННЯ ПЕРСОНАЖА ===")

        classes = {
            "1": ("Warrior", Warrior),
            "2": ("Mage", Mage),
            "3": ("Scout", Scout),
        }

        selected = None
        while selected not in classes:
            for key, (label, _) in classes.items():
                self._ui.show_text(f"{key}. {label}")
            selected = self._ui.get_input("Виберіть клас: ").strip()

        chosen_label, chosen_cls = classes[selected]
        name = self._ui.get_input("Введіть ім'я персонажа: ").strip()
        if not name:
            name = "Герой"

        player = chosen_cls(name)

        points = 10
        attrs = {
            "1": ("strength", "Strength"),
            "2": ("intelligence", "Intelligence"),
            "3": ("agility", "Agility"),
            "4": ("luck", "Luck"),
        }

        self._ui.show_text("\nРозподіліть початкові очки характеристик.")
        while points > 0:
            self._ui.show_text(f"\nЗалишилося очок: {points}")
            for key, (attr, label) in attrs.items():
                current = getattr(player.attributes, attr, 0)
                self._ui.show_text(f"  {key}. {label}: {current}")
            self._ui.show_text("  5. Випадковий розподіл")

            choice = self._ui.get_input("Виберіть атрибут: ").strip()
            if choice in attrs:
                attr_name = attrs[choice][0]
                old = getattr(player.attributes, attr_name, 0)
                setattr(player.attributes, attr_name, old + 1)
                points -= 1
            elif choice == "5":
                attr_names = [a for a, _ in attrs.values()]
                for _ in range(points):
                    attr = random.choice(attr_names)
                    old = getattr(player.attributes, attr, 0)
                    setattr(player.attributes, attr, old + 1)
                points = 0
            else:
                self._ui.show_text("Невірний вибір.")

        self._ui.show_text(f"\nСтворено персонажа: {player.name} ({chosen_label})")
        return player


class InventoryMenu:
    def __init__(self, ui: GameUI):
        self._ui = ui

    def show(self, player: Character) -> None:
        if player is None:
            raise ValueError("Player не може бути None")

        while True:
            self._ui.show_text("\n=== МЕНЮ ІНВЕНТАРЯ ===")
            player.inventory.show_inventory()

            self._ui.show_text("1. Використати предмет")
            self._ui.show_text("2. Екіпірувати предмет")
            self._ui.show_text("3. Назад")

            choice = self._ui.get_input("Виберіть опцію: ").strip()
            if choice == "1":
                if not player.inventory.items:
                    self._ui.show_text("Інвентар порожній.")
                    continue

                idx = self._ui.get_input("Номер предмета для використання: ").strip()
                if not idx.isdigit():
                    self._ui.show_text("Будь ласка, введіть число.")
                    continue

                idx = int(idx) - 1
                if idx < 0 or idx >= len(player.inventory.items):
                    self._ui.show_text("Невірний номер предмета.")
                    continue

                item = player.inventory.items[idx]
                used = player.use_item(item)
                if used:
                    self._ui.show_text(f"{item.name} використано.")
                else:
                    self._ui.show_text(f"Не вдалося використати {item.name}.")

            elif choice == "2":
                self._ui.show_text("Екіпірування наразі не реалізовано.")

            elif choice == "3":
                return

            else:
                self._ui.show_text("Невірний вибір, спробуйте ще.")
