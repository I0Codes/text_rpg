import random

class DiceSystem:
    @staticmethod
    def roll_dice(sides=6):
        """Кинути кубик з N гранями"""
        return random.randint(1, sides)

    @staticmethod
    def attribute_check(character, attribute_name, difficulty=3):
        """
        Перевірка атрибуту:
        1. Кинути кубик
        2. Додати бонус від атрибуту (кожні 3 очки = +1 бонус)
        3. Порівняти результат зі складністю

        Повертає словник: {"success": bool, "roll": int, "bonus": int, "total": int}
        """
        roll = DiceSystem.roll_dice()
        attribute_value = getattr(character.attributes, attribute_name)
        bonus = attribute_value // 3
        total = roll + bonus
        success = total >= difficulty
        return {"success": success, "roll": roll, "bonus": bonus, "total": total}