import random
from entities.enemies import Goblin, Wolf, Bandit, Orc, Troll, Dragon
from items.item import RustyDagger, IronSword, SteelAxe, WoodenStaff


class Location:
    """Базовий клас локації"""
    
    def __init__(self, name):
        self.name = name

    def _try_find_weapon(self, hero):
        """Середній шанс знайти зброю, рідкісніша — рідше."""
        # базовий шанс знайти зброю, коли нічого не зустріли
        weapon_find_chance = 0.35
        if random.random() >= weapon_find_chance:
            return None

        weapon_table = [
            (RustyDagger, 0.60),
            (IronSword, 0.25),
            (SteelAxe, 0.10),
            (WoodenStaff, 0.05),
        ]

        pick = random.random()
        cumulative = 0.0
        for cls, weight in weapon_table:
            cumulative += weight
            if pick <= cumulative:
                weapon = cls()
                if hero.add_item(weapon):
                    print(f"🎉 Ви знайшли зброю: {weapon.name} ({weapon.damage_type}, {weapon.damage} шкоди)!")
                else:
                    print("⚠️ Знахідка виявилася зброєю, але інвентар переповнений.")
                return weapon

        return None
    def get_actions(self):
        """Повертає доступні дії"""
        return {
            "1": "Дослідити місцевість",
            "2": "Відпочити"
        }
    
    def handle_action(self, choice, player):
        """Обробляє дію гравця
        
        Returns:
            Enemy об'єкт якщо зустріли ворога, None в іншому випадку
        """
        if choice == "1":
            return self._explore(player)
        elif choice == "2":
            self._rest(player)
        return None

    def _explore(self, hero):
        """Дослідження локації - 60% шанс зустріти ворога"""
        if random.random() < 0.6:
            enemy = self._get_random_enemy(hero.level)
            print(f"\n⚔️ Ви зустріли {enemy.name} (рів. {enemy.level})!")
            return enemy
        else:
            print(f"\nВи дослідили {self.name}... але нікого не зустріли.")
            found_weapon = self._try_find_weapon(hero)
            if found_weapon is None:
                print("🔎 Ви нічого корисного не знайшли цього разу.")
            return None

    def _rest(self, hero):
        """Відпочинок - +5 HP"""
        heal_amount = 5
        hero.hp = min(hero.max_hp, hero.hp + heal_amount)
        print(f"\nВи відпочили. HP: +{heal_amount}")

    def _get_random_enemy(self, hero_level):
        """Генерація випадкового ворога за рівнем героя"""
        enemy_classes = [Goblin, Wolf, Bandit, Orc, Troll, Dragon]
        enemy_level = max(1, hero_level + random.randint(-1, 1))
        enemy_class = random.choice(enemy_classes)
        return enemy_class(level=enemy_level)


class Forest(Location):
    def __init__(self):
        super().__init__("Темний ліс")

# TODO: додати нові локації - Village, Cave, EnemyForest
# TODO: додати систему переходів між локаціями
# TODO: додати випадкові події в локаціях
