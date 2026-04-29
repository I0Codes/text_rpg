import random
from entities.characters import Character, Warrior, Mage, Scout


class MainMenu:
    """Головне меню гри"""

    @staticmethod
    def show():
        while True:
            print("\n=== ГОЛОВНЕ МЕНЮ ===")
            print("1. Нова гра")
            print("2. Завантажити гру")
            print("3. Налаштування")
            print("4. Вихід")

            choice = input("Виберіть опцію: ").strip()
            if choice == "1":
                return "new_game"
            elif choice == "2":
                return "load_game"
            elif choice == "3":
                return "settings"
            elif choice == "4":
                return "exit"
            else:
                print("Невірний вибір, спробуйте ще.")


class CharacterCreationMenu:
    """Меню створення персонажа"""

    @staticmethod
    def show():
        print("\n=== СТВОРЕННЯ ПЕРСОНАЖА ===")

        classes = {
            "1": ("Warrior", Warrior),
            "2": ("Mage", Mage),
            "3": ("Scout", Scout),
        }

        selected = None
        while selected not in classes:
            for key, (label, _) in classes.items():
                print(f"{key}. {label}")
            selected = input("Виберіть клас: ").strip()

        chosen_label, chosen_cls = classes[selected]

        name = input("Введіть ім'я персонажа: ").strip()
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

        print("\nРозподіліть початкові очки характеристик.")
        while points > 0:
            print(f"\nЗалишилося очок: {points}")
            for key, (attr, label) in attrs.items():
                current = getattr(player.attributes, attr, 0)
                print(f"  {key}. {label}: {current}")
            print("  5. Випадковий розподіл")

            choice = input("Виберіть атрибут: ").strip()
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
                print("Невірний вибір.")

        print(f"\nСтворено персонажа: {player.name} ({chosen_label})")
        return player


class InventoryMenu:
    """Меню інвентаря"""

    @staticmethod
    def show(player: Character):
        if player is None:
            raise ValueError("Player не може бути None")

        while True:
            print("\n=== МЕНЮ ІНВЕНТАРЯ ===")
            player.inventory.show_inventory()

            print("1. Використати предмет")
            print("2. Екіпірувати предмет")
            print("3. Назад")

            choice = input("Виберіть опцію: ").strip()
            if choice == "1":
                if not player.inventory.items:
                    print("Інвентар порожній.")
                    continue

                idx = input("Номер предмета для використання: ").strip()
                if not idx.isdigit():
                    print("Будь ласка, введіть число.")
                    continue

                idx = int(idx) - 1
                if idx < 0 or idx >= len(player.inventory.items):
                    print("Невірний номер предмета.")
                    continue

                item = player.inventory.items[idx]
                used = player.use_item(item)
                if used:
                    print(f"{item.name} використано.")
                else:
                    print(f"Не вдалося використати {item.name}.")

            elif choice == "2":
                print("Екіпірування наразі не реалізовано.")

            elif choice == "3":
                return

            else:
                print("Невірний вибір, спробуйте ще.")
