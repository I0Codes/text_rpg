import random

class DiceSystem:
    @staticmethod
    def attribute_check(player, attribute, difficulty):
        """Перевіряє атрибут гравця: кидає d20 + атрибут vs difficulty * 10"""
        if not hasattr(player, attribute):
            return False  # Якщо атрибут відсутній, провал
        attr_value = getattr(player, attribute)
        roll = random.randint(1, 20) + attr_value
        return roll >= difficulty * 10  # Приклад: difficulty 4 означає 40
