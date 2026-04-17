from entities.characters import Character


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

        # Вибір класу (просто для відображення, реалізуємо як дані)
        classes = {
            "1": "Warrior",
            "2": "Mage",
            "3": "Scout",
        }

        selected = None
        while selected not in classes:
            for key, value in classes.items():
                print(f"{key}. {value}")
            selected = input("Виберіть клас: ").strip()

        chosen_class = classes[selected]

        name = input("Введіть ім'я персонажа: ").strip()
        if not name:
            name = "Герой"

        # Базова конфігурація персонажа
        player = Character(name=name, hp=100, max_hp=100, stamina=50, max_stamina=50)

        points = 10
        attrs = ["strength", "intelligence", "agility", "luck"]

        print("\nРозподіліть початкові очки характеристик.")
        while points > 0:
            print(f"Залишилося очок: {points}")
            for attribute in attrs:
                current = getattr(player.attributes, attribute, 0)
                print(f"  {attribute}: {current}")

            choice = input("Введіть атрибут для додавання (або 'готово'): ").strip().lower()
            if choice in attrs:
                old = getattr(player.attributes, choice, 0)
                setattr(player.attributes, choice, old + 1)
                points -= 1
            elif choice in ["готово", "гото", "end"]:
                break
            else:
                print("Невірний вибір атрибуту.")

        print(f"\nСтворено персонажа: {player.name} ({chosen_class})")
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
