import random
from .characters import Character
from .attributes import Attributes


class Enemy(Character):
    def __init__(self, name, hp, attack, defense, level=1, xp_reward=0, reward_gold=0):
        super().__init__(name, hp, max_hp=hp, stamina=0, max_stamina=0, level=level)
        # Базові бойові характеристики
        self.base_attack = attack
        self.defense = defense
        self.xp_reward = xp_reward
        self.reward_gold = reward_gold
        self._scale_to_level()

    def _scale_to_level(self):
        """Scale enemy stats based on level"""
        scaling_factor = 1 + (self.level - 1) * 0.15
        self.max_hp = int(self.max_hp * scaling_factor)
        self.hp = self.max_hp
        self.base_attack = int(self.base_attack * scaling_factor)
        self.defense = int(self.defense * scaling_factor)

    def attack(self):
        """Return attack damage with variance"""
        base_damage = self.calculate_physical_damage()
        variance = random.randint(-2, 2)
        return max(1, base_damage + variance)

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        real_damage = max(0, damage - self.defense)
        self.hp -= real_damage
        return real_damage

    def __str__(self):
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"

    # Нагорода за перемогу
    def get_loot(self):
        return {"exp": self.xp_reward, "gold": self.reward_gold}

    # Простий AI: поки що завжди атакує
    def select_action(self, battlefield=None):
        return "attack"


class Goblin(Enemy):
    def __init__(self, level=1):
        super().__init__("Goblin", hp=30, attack=8, defense=2, level=level, reward_gold=3 * level)
        self.attributes.update(agility = 8 * level, strength = 4 * level)


class Wolf(Enemy):
    def __init__(self, level=1):
        # Швидкий ворог з високою спритністю
        super().__init__("Wolf", hp=25, attack=10, defense=3, level=level, reward_gold=4 * level)
        self.attributes.update(agility = 12 * level, strength = 6 * level)


class Bandit(Enemy):
    def __init__(self, level=1):
        # Збалансований ворог
        super().__init__("Bandit", hp=40, attack=12, defense=4, level=level, reward_gold=6 * level)
        self.attributes.update(agility = 7 * level, strength = 9 * level)


# Збережено старі типи як більш складні вороги (вони автоматично працюватимуть з новим Enemy)

class Orc(Enemy):
    def __init__(self, level=1):
        super().__init__('Orc', hp=50, attack=12, defense=4, level=level)
        self.attributes = Attributes(strength=6, intelligence=2, agility=3, luck=2)
        self._scale_to_level()


class Dragon(Enemy):
    def __init__(self, level=1):
        super().__init__('Dragon', hp=150, attack=25, defense=10, level=level)
        self.attributes = Attributes(strength=10, intelligence=8, agility=4, luck=3)
        self._scale_to_level()

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
        super().__init__('Troll', hp=80, attack=15, defense=6, level=level)
        self.attributes = Attributes(strength=7, intelligence=1, agility=2, luck=1)
        self._scale_to_level()

    def take_damage(self, damage):
        real_damage = super().take_damage(damage)
        # Регенерація: зцілює 10% від максимального здоров'я за хід, якщо живий
        if self.is_alive():
            self.hp = min(self.hp + int(0.1 * 80 * self.level), 80 * self.level)
        return real_damage
    
    # def attack(self):
        # """Регенерація: зцілює 10% від максимального здоров'я за хід, якщо живий"""
        # if random.random() < 0.1:
        #     heal_amount = int(self.max_hp * 0.1)
        #     self.hp = min(self.max_hp, self.hp + heal_amount)
        # return super().attack()