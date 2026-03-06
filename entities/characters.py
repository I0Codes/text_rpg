from entities.attributes import Attributes
from entities.experience import ExperienceManager

class Character:
    """Базовий клас персонажа"""
    
    def __init__(self, name, hp, max_hp, stamina, max_stamina, level=1):
        """Ініціалізація персонажа
        
        Args:
            name: Ім'я персонажа
            hp: Здоров'я персонажа
        """
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_hp = hp
        self.level = level
        self.max_hp = max_hp
        self.stamina = stamina
        self.max_stamina = max_stamina
        self.attributes = Attributes(
            strength=5,
            intelligence=5,
            agility=5,
            luck=5
        )
        self.experience_manager = ExperienceManager(self)
        self.gold = 0
    
    def is_alive(self):
        """Перевіряє чи персонаж живий
        
        Returns:
            True якщо персонаж живий (hp > 0), False в іншому випадку
        """
        return self.hp > 0
    
    def gain_experience(self, amount, source="unknown"):
        """Отримати досвід через ExperienceManager"""
        self.experience_manager.gain_experience(amount, source=source)
    
    def level_up_stats(self):
        """Покращити характеристики при підвищенні рівня"""
        # Збільшення максимального здоров'я
        self.max_hp += 10
        self.hp = self.max_hp
        
        # Збільшення характеристик
        self.attributes.strength += 1
        self.attributes.intelligence += 1
        self.attributes.agility += 1
        self.attributes.luck += 1

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
    
    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"блбплпбплпбплпбп {amount}. вбвбьавбьавбьавдладлав: {self.hp}")

    def restore_stamina(self, amount):
        self.stamina = min(self.stamina + amount, self.max_stamina)
        print(f"fmnvnvdnvm {amount}.bubochka: {self.stamina}")
    def use_stamina(self, cost):
        if self.stamina >= cost:
            self.stamina -= cost
            return True
        print("biba")
        return False
class Warrior(Character):
    def __init__(self, name):
        super()._init_(name, hp=120, stamina = 100, agility = 5, strength = 10, intelligence = 3, luck = 5)
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, hp=80, stamina=60, str=3, int=10, dex=4, luck=6)
        self.max_mana = 120
        self.mana = 120

    def restore_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)
        print(f"{self.name} відновив {amount} мани. Мана: {self.mana}")

class Scout(Character):
    def __init__(self, name):
        super().__init__(name, hp=90, stamina=120, str=5, int=4, dex=10, luck=8)
        
        


# TODO: додати класи Warrior, Mage, Scout через наслідування від Character
# Приклад:
# class Warrior(Character):
#     def __init__(self, name):
#         super().__init__(name, hp=150)
#         self.strength = 10
