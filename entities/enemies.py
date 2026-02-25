import random
from .characters import Character
from entities.attributes import Attributes


class Enemy(Character):
    def __init__(self, name, hp, attack, defense, level=1, xp_reward=0, gold_reward=0):
        super().__init__(name, hp, level)
        # Базові бойові характеристики
        self.base_attack = attack
        self.defense = defense
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self._scale_to_level()

    def _scale_to_level(self):
        """Scale enemy stats based on level"""
        scaling_factor = 1 + (self.level - 1) * 0.15
        self.max_hp = int(self.max_hp * scaling_factor)
        self.hp = self.max_hp
        self.base_attack = int(self.base_attack * scaling_factor)
        self.defense = int(self.defense * scaling_factor)
        # Scale attributes for damage calculations
        self.attributes.strength = int(self.attributes.strength * scaling_factor)
        self.attributes.intelligence = int(self.attributes.intelligence * scaling_factor)
        self.attributes.agility = int(self.attributes.agility * scaling_factor)
        self.attributes.luck = int(self.attributes.luck * scaling_factor)
        self.xp_reward = int(self.xp_reward * scaling_factor)
        self.gold_reward = int(self.gold_reward * scaling_factor)

    def attack(self):
        """Return attack damage with variance"""
        base_damage = self.calculate_physical_damage()
        variance = random.randint(-2, 2)
        return max(1, base_damage + variance)

    def get_rewards(self):
        # Нагорода за перемогу
        return {
            'xp': self.xp_reward,
            'gold': self.gold_reward
        }

    def take_action(self):
        # Простий AI: поки що завжди атакує
        return 'attack'


class Goblin(Enemy):
    def __init__(self, level=1):
        super().__init__('Goblin', 30, 8, 2, level, xp_reward=25, gold_reward=10)
        self.attributes = Attributes(strength=3, intelligence=2, agility=4, luck=3)
        self._scale_to_level()


class Wolf(Enemy):
    def __init__(self, level=1):
        # Швидкий ворог з високою спритністю
        super().__init__('Wolf', 25, 10, 3, level, xp_reward=35, gold_reward=15)
        self.attributes = Attributes(strength=4, intelligence=1, agility=6, luck=2)
        self._scale_to_level()


class Bandit(Enemy):
    def __init__(self, level=1):
        # збалансований ворог
        super().__init__('Bandit', 40, 12, 4, level, xp_reward=50, gold_reward=30)
        self.attributes = Attributes(strength=4, intelligence=3, agility=5, luck=4)
        self._scale_to_level()


# Збережено старі типи як більш складні вороги (вони автоматично працюватимуть з новим Enemy)

class Orc(Enemy):
    def __init__(self, level=1):
        super().__init__('Orc', 50, 12, 5, level, xp_reward=60, gold_reward=40)
        self.attributes = Attributes(strength=6, intelligence=2, agility=3, luck=2)
        self._scale_to_level()


class Dragon(Enemy):
    def __init__(self, level=1):
        super().__init__('Dragon', 150, 25, 8, level, xp_reward=150, gold_reward=100)
        self.attributes = Attributes(strength=10, intelligence=8, agility=4, luck=3)
        self._scale_to_level()

    def deal_damage(self):
        # Шанс вогняної атаки
        if random.random() < 0.3:
            return random.randint(30, 45)
        return super().deal_damage()
    def attack(self):
        """Дракон може використовувати вогняну атаку в 30% випадків"""
        if random.random() < 0.3:
            # Вогняна атака: магічна шкода
            base_damage = self.calculate_magical_damage()
            variance = random.randint(-3, 3)
            return max(2, base_damage + variance)
        return super().attack()


class Troll(Enemy):
    def __init__(self, level=1):
        super().__init__('Troll', 80, 15, 6, level, xp_reward=80, gold_reward=50)
        self.attributes = Attributes(strength=7, intelligence=1, agility=2, luck=1)
        self._scale_to_level()
    
    def attack(self):
        """Регенерація: зцілює 10% від максимального здоров'я за хід, якщо живий"""
        if random.random() < 0.1:
            heal_amount = int(self.max_hp * 0.1)
            self.hp = min(self.max_hp, self.hp + heal_amount)
        return super().attack()