import random
from entities.enemies import Goblin, Wolf, Bandit, Orc, Troll, Dragon


class Location:
    """Базовий клас локації"""
    
    def __init__(self, name):
        self.name = name
    
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
            return enemy
        else:
            print(f"\nВи дослідили {self.name}... але нікого не зустріли.")
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
