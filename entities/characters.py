from items.inventory import Inventory
from entities.attributes import Attributes
from entities.experience import ExperienceManager
from entities.leveling_system import LevelingSystem
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
        self.crit_bonus = 0.0
        self.dodge_bonus = 0.0
        self.mana_cost_reduction = 0.0
        self.skills = []
        self.attributes = Attributes(
            strength=5,
            intelligence=5,
            agility=5,
            luck=5
        )
        self.experience_manager = ExperienceManager(self)
        self.leveling_system = LevelingSystem(self)
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

    def get_level_bonuses(self, level):
        """
        Повертає словник бонусів для конкретного рівня.
        Кожен клас перевизначає цей метод.
        Повертає: {"hp": 0, "stamina": 0, "mana": 0, "crit": 0, "dodge": 0, "skill": None}
        """
        return {}

    def apply_level_bonus(self, level):
        """
        Застосовує бонуси при досягненні рівня.
        Викликається автоматично при level_up().
        """
        bonuses = self.get_level_bonuses(level)
        if not bonuses:
            return {}

        messages = []

        if 'hp' in bonuses:
            self.max_hp += bonuses['hp']
            self.hp = self.max_hp
            messages.append(f"+{bonuses['hp']} HP")

        if 'stamina' in bonuses:
            self.max_stamina += bonuses['stamina']
            self.stamina = self.max_stamina
            messages.append(f"+{bonuses['stamina']} Stamina")

        if 'mana' in bonuses:
            self.max_mana += bonuses['mana']
            self.mana = self.max_mana
            messages.append(f"+{bonuses['mana']} Mana")

        if 'crit' in bonuses:
            self.crit_bonus += bonuses['crit']
            messages.append(f"+{int(bonuses['crit'] * 100)}% Crit Chance")

        if 'dodge' in bonuses:
            self.dodge_bonus += bonuses['dodge']
            messages.append(f"+{int(bonuses['dodge'] * 100)}% Dodge Chance")

        if 'mana_cost_reduction' in bonuses:
            self.mana_cost_reduction += bonuses['mana_cost_reduction']
            messages.append(f"-{int(bonuses['mana_cost_reduction'] * 100)}% Spell Cost")

        if 'skill' in bonuses:
            self.skills.append(bonuses['skill'])
            messages.append(f"Skill unlocked: {bonuses['skill']}")

        if messages:
            print(f"🎁 Бонуси за рівень {level}: {'; '.join(messages)}")

        return bonuses

    def get_next_milestone(self):
        """
        Показує наступний важливий рівень та що дасть.
        """
        next_level = self.level + 1
        while next_level <= self.level + 20:
            bonuses = self.get_level_bonuses(next_level)
            if bonuses:
                return {'level': next_level, 'bonuses': bonuses}
            next_level += 1

        return None

    def gain_gold(self, amount):
        self.gold += amount

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def calculate_physical_damage(self):
        """Calculate physical damage based on attributes"""
        base_damage = 5 + self.attributes.get_physical_damage_bonus()
        return base_damage

    def calculate_magical_damage(self):
        """Calculate magical damage based on attributes"""
        base_damage = 5 + self.attributes.get_magic_damage_bonus()
        return base_damage
    
    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"блбплпбплпбплпбп {amount}. вбвбьавбьавбьавдладлав: {self.hp}")

    def restore_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)
        print(f"{self.name} відновив {amount} мани. Мана: {self.mana}")
        
    def restore_stamina(self, amount):
        self.stamina = min(self.stamina + amount, self.max_stamina)
        print(f"fmnvnvdnvm {amount}.bubochka: {self.stamina}")
        
    def use_stamina(self, cost):
        if self.stamina >= cost:
            self.stamina -= cost
            return True
        print("biba")
        return False

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
      
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, hp=120, max_hp=120, stamina=100, max_stamina=100)
        self.attributes.update(strength=10, intelligence=3, agility=5, luck=5)

    def get_level_bonuses(self, level):
        bonuses = {
            2: {"hp": 5},
            4: {"hp": 10},
            6: {"skill": "Whirlwind"},
            8: {"stamina": 5},
            10: {"hp": 15}
        }
        return bonuses.get(level, {})
        
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, hp=80, max_hp=80, stamina=60, max_stamina=60)
        self.max_mana = 120
        self.mana = 120
        self.attributes.update(strength=3, intelligence=10, agility=4, luck=6)

    def restore_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)
        print(f"{self.name} відновив {amount} мани. Мана: {self.mana}")

    def get_level_bonuses(self, level):
        bonuses = {
            2: {"mana": 10},
            4: {"mana": 15},
            6: {"skill": "Ice Storm"},
            8: {"mana": 5},
            10: {"mana_cost_reduction": 0.1}
        }
        return bonuses.get(level, {})

class Scout(Character):
    def __init__(self, name):
        super().__init__(name, hp=BASE_HP - 10, max_hp=BASE_HP - 10, stamina=BASE_STAMINA + 20, max_stamina=BASE_STAMINA + 20)
        self.attributes.strength = 5
        self.attributes.intelligence = 4
        self.attributes.agility = 10
        self.attributes.luck = 8

    def get_level_bonuses(self, level):
        bonuses = {
            2: {"stamina": 5},
            4: {"crit": 0.02},
            6: {"skill": "Smoke Bomb"},
            8: {"dodge": 0.03},
            10: {"stamina": 10}
        }
        return bonuses.get(level, {})

# TODO: додати класи Warrior, Mage, Scout через наслідування від Character
# Приклад:
# class Warrior(Character):
#     def __init__(self, name):
#         super().__init__(name, hp=150)
#         self.strength = 10
