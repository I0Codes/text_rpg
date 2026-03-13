from items.inventory import Inventory
from entities.attributes import Attributes
from entities.experience import ExperienceManager
from config.settings import BASE_HP, BASE_STAMINA, BASE_MANA

class Character:
    """Базовий клас персонажа"""

    def __init__(self, name, hp, max_hp, stamina, max_stamina, level=1, inventory_capacity: int = 20):
        """Ініціалізація персонажа
        
        Args:
            name: Ім'я персонажа
            hp: Здоров'я персонажа
            inventory_capacity: максимальна кількість слотів у інвентарі
        """
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        # інтегруємо інвентар
        self.inventory = Inventory(max_capacity=inventory_capacity)
        self.level = level
        self.stamina = stamina
        self.max_stamina = max_stamina
        self.max_mana = BASE_MANA
        self.mana = BASE_MANA
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
        self.max_hp += 10 + self.attributes.get_hp_bonus()
        self.hp = self.max_hp
        
        # Збільшення мани
        self.max_mana += self.attributes.get_mana_bonus()
        self.mana = self.max_mana
        
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

    def restore_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)
        print(f"{self.name} відновив {amount} мани. Мана: {self.mana}")
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, hp=BASE_HP + 20, max_hp=BASE_HP + 20, stamina=BASE_STAMINA, max_stamina=BASE_STAMINA)
        self.attributes.strength = 10
        self.attributes.intelligence = 3
        self.attributes.agility = 5
        self.attributes.luck = 5

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, hp=BASE_HP - 20, max_hp=BASE_HP - 20, stamina=BASE_STAMINA - 40, max_stamina=BASE_STAMINA - 40)
        self.max_mana = BASE_MANA + 70
        self.mana = BASE_MANA + 70
        self.attributes.strength = 3
        self.attributes.intelligence = 10
        self.attributes.agility = 4
        self.attributes.luck = 6

class Scout(Character):
    def __init__(self, name):
        super().__init__(name, hp=BASE_HP - 10, max_hp=BASE_HP - 10, stamina=BASE_STAMINA + 20, max_stamina=BASE_STAMINA + 20)
        self.attributes.strength = 5
        self.attributes.intelligence = 4
        self.attributes.agility = 10
        self.attributes.luck = 8
        
        


    # додаткові методи-заглушки для зручності
    def add_item(self, item):
        """Обгортає Inventory.add_item"""
        return self.inventory.add_item(item)

    def remove_item(self, item):
        """Обгортає Inventory.remove_item"""
        return self.inventory.remove_item(item)

    def use_item(self, item):
        """Спробувати використати предмет із інвентаря"""
        return self.inventory.use_item(item, self)

# TODO: додати класи Warrior, Mage, Scout через наслідування від Character
# Приклад:
# class Warrior(Character):
#     def __init__(self, name):
#         super().__init__(name, hp=150)
#         self.strength = 10
