from entities.attributes import Attributes

class Character:
    """Базовий клас персонажа"""
    
    def __init__(self, name, hp, level=1):
        """Ініціалізація персонажа
        
        Args:
            name: Ім'я персонажа
            hp: Здоров'я персонажа
        """
        self.name = name
        self.hp = hp
        self.level = level
        self.attributes = Attributes(
            strength=5,
            intelligence=5,
            agility=5,
            luck=5
        )
        self.experience = 0
        self.gold = 0
    
    def is_alive(self):
        """Перевіряє чи персонаж живий
        
        Returns:
            True якщо персонаж живий (hp > 0), False в іншому випадку
        """
        return self.hp > 0
    
    def gain_experience(self, amount):
        self.experience += amount
        # Level up every 100 XP
        new_level = self.experience // 100 + 1
        if new_level > self.level:
            self.level_up(new_level - self.level)

    def level_up(self, levels):
        old_level = self.level
        self.level += levels
        # Increase stats on level up
        self.max_hp += 10 * levels
        self.hp = self.max_hp
        self.attributes.strength += 1 * levels
        self.attributes.intelligence += 1 * levels
        self.attributes.agility += 1 * levels
        self.attributes.luck += 1 * levels

    def gain_gold(self, amount):
        self.gold += amount

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def calculate_physical_damage(self):
        """Calculate physical damage based on attributes"""
        base_damage = 5 + self.attributes.calculate_physical_damage_bonus()
        return base_damage

# TODO: додати класи Warrior, Mage, Scout через наслідування від Character
# Приклад:
# class Warrior(Character):
#     def __init__(self, name):
#         super().__init__(name, hp=150)
#         self.strength = 10
