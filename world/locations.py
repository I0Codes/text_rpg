import random

from entities.enemies import Goblin, Wolf, Bandit, Orc, Troll, Dragon


class Location:
    """Базовий клас локації"""

    def __init__(self, name):
        self.name = name
        self.neighbors = {}

    def add_neighbor(self, location):
        key = str(len(self.neighbors) + 3)
        self.neighbors[key] = location
        return key

    def get_actions(self):
        actions = {
            "1": "Дослідити місцевість",
            "2": "Відпочити",
            "i": "Переглянути інвентар",
            "s": "Переглянути статус персонажа",
        }
        for key, loc in self.neighbors.items():
            actions[key] = f"Перейти до {loc.name}"
        return actions

    def handle_action(self, choice, player):
        if choice == "1":
            return self._explore(player)
        elif choice == "2":
            self._rest(player)
            return None
        elif choice in self.neighbors:
            return self.neighbors[choice]
        else:
            print("Невідома дія")
            return None

    def _explore(self, hero):
        chance = 0.6
        if random.random() < chance:
            enemy = self._get_random_enemy(hero.level)
            print(f"\n⚔️ Ви зустріли {enemy.name} (рів. {enemy.level})!")
            return enemy
        print(f"\nВи дослідили {self.name}, але нікого не зустріли.")
        return None

    def _rest(self, hero):
        heal_amount = 5
        hero.hp = min(hero.max_hp, hero.hp + heal_amount)
        print(f"\nВи відпочили. HP +{heal_amount}")

    def _get_random_enemy(self, hero_level):
        enemy_classes = [Goblin, Wolf, Bandit, Orc, Troll, Dragon]
        enemy_level = max(1, hero_level + random.randint(-1, 1))
        enemy_class = random.choice(enemy_classes)
        return enemy_class(level=enemy_level)


class Village(Location):
    def __init__(self):
        super().__init__("Село")

    def _explore(self, hero):
        if random.random() < 0.2:
            enemy = self._get_random_enemy(hero.level)
            print(f"\n⚔️ У селі вас атакує {enemy.name}!")
            return enemy
        print("\nСело безпечне. Торговці і мир.")
        return None

    def _rest(self, hero):
        heal_amount = 15
        hero.hp = min(hero.max_hp, hero.hp + heal_amount)
        print(f"\nВи відпочили у таверні. HP +{heal_amount}")


class Cave(Location):
    def __init__(self):
        super().__init__("Печера")

    def _explore(self, hero):
        if random.random() < 0.8:
            enemy = random.choice([Orc, Troll, Dragon])(level=max(1, hero.level))
            print(f"\n⚔️ Ви зустріли {enemy.name} у печері!")
            return enemy
        print("\nПечера тиха, але напружена.")
        return None


class DarkForest(Location):
    def __init__(self):
        super().__init__("Темний ліс")

    def _explore(self, hero):
        if random.random() < 0.75:
            enemy = random.choice([Bandit, Wolf, Troll, Dragon])(level=max(1, hero.level))
            print(f"\n⚔️ У темному лісі вас атакує {enemy.name}!")
            return enemy
        print("\nТемний ліс. Ви йдете обережно.")
        return None


class Forest(Location):
    """Ліс - початкова локація з помірним шансом зустрічі ворога"""
    
    def __init__(self):
        super().__init__("Ліс")

    def _explore(self, hero):
        """Дослідження лісу з середнім шансом зустрічі ворога"""
        chance = 0.5  # 50% шанс зустрічі
        if random.random() < chance:
            enemy = self._get_random_enemy(hero.level)
            print(f"\n⚔️ Ви зустріли {enemy.name} (рів. {enemy.level}) у лісі!")
            return enemy
        print(f"\nВи дослідили {self.name}, але нікого не зустріли.")
        return None


def create_world_map():
    """Створити карту світу"""
    village = Village()
    forest = Forest()
    dark_forest = DarkForest()
    cave = Cave()

    # Налаштування зв'язків між локаціями
    village.neighbors = {
        "3": dark_forest,
    }
    forest.neighbors = {
        "3": dark_forest,
        "4": village,
    }
    dark_forest.neighbors = {
        "3": cave,
        "4": village,
        "5": forest,
    }
    cave.neighbors = {
        "3": dark_forest,
    }

    return forest  # Ліс - початкова локація

