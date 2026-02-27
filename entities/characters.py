from items.inventory import Inventory


class Character:
    """Базовий клас персонажа"""
    
    def __init__(self, name, hp, inventory_capacity: int = 20):
        """Ініціалізація персонажа
        
        Args:
            name: Ім'я персонажа
            hp: Здоров'я персонажа
            inventory_capacity: максимальна кількість слотів у інвентарі
        """
        self.name = name
        self.hp = hp
        # інтегруємо інвентар
        self.inventory = Inventory(max_capacity=inventory_capacity)
    
    def is_alive(self):
        """Перевіряє чи персонаж живий
        
        Returns:
            True якщо персонаж живий (hp > 0), False в іншому випадку
        """
        return self.hp > 0

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
