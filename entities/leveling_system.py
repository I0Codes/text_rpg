"""Система прокачки рівнів персонажа з розподілом очок."""


class LevelingSystem:
    """Керує прогресією рівнів, атрибутами та очками навичок персонажа."""
    
    # Кількість очок, які дають при підвищенні рівня
    ATTRIBUTE_POINTS_PER_LEVEL = 2
    SKILL_POINTS_PER_LEVEL = 1
    
    def __init__(self, character):
        """
        Ініціалізація системи прокачки.
        
        Параметри:
            character: Персонаж, до якого прив'язана система
        """
        self.character = character
        self.level = character.level
        self.attribute_points = 0
        self.skill_points = 0
        self.level_up_history = []  # Історія підвищень рівня
    
    def level_up(self):
        """
        Підвищення рівня персонажа:
        1. Збільшити рівень на 1
        2. Дати очки атрибутів (2 очка)
        3. Дати очки навичок (1 очко)
        4. Повністю відновити HP/stamina/mana
        5. Застосувати специфічні бонуси класу
        6. Показати гарне повідомлення
        """
        self.level += 1
        self.character.level = self.level
        
        # Видаємо очки
        self.attribute_points += self.ATTRIBUTE_POINTS_PER_LEVEL
        self.skill_points += self.SKILL_POINTS_PER_LEVEL
        
        # Відновлюємо ресурси
        self.character.hp = self.character.max_hp
        self.character.stamina = self.character.max_stamina
        self.character.mana = self.character.max_mana
        
        # Застосовуємо бонуси
        self.character.level_up_stats()
        if hasattr(self.character, 'apply_level_bonus'):
            self.character.apply_level_bonus(self.level)
        
        # Зберігаємо в історію
        level_info = {
            'level': self.level,
            'attribute_points_gained': self.ATTRIBUTE_POINTS_PER_LEVEL,
            'skill_points_gained': self.SKILL_POINTS_PER_LEVEL,
            'total_attribute_points': self.attribute_points,
            'total_skill_points': self.skill_points
        }
        self.level_up_history.append(level_info)
        
        # Виводимо гарне повідомлення
        self._print_level_up_message()
    
    def spend_attribute_point(self, attribute_name):
        """
        Витратити очко атрибуту.
        
        Параметри:
            attribute_name: Назва атрибуту (strength, intelligence, agility, luck)
            
        Повертає:
            bool: True якщо успішно, False якщо немає очок
            
        Виняток:
            ValueError: Якщо атрибут не існує
        """
        # Перевірка існування атрибуту
        valid_attributes = ['strength', 'intelligence', 'agility', 'luck']
        if attribute_name not in valid_attributes:
            raise ValueError(
                f"Невірний атрибут '{attribute_name}'. "
                f"Доступні: {', '.join(valid_attributes)}"
            )
        
        # Перевірка наявності очок
        if self.attribute_points <= 0:
            print(f"[ПОМИЛКА] Немає доступних очок атрибутів!")
            return False
        
        # Збільшуємо атрибут
        current_value = getattr(self.character.attributes, attribute_name)
        setattr(self.character.attributes, attribute_name, current_value + 1)
        
        # Витрачаємо очко
        self.attribute_points -= 1
        
        # Перерахуємо бонуси
        self._recalculate_bonuses()
        
        print(f"[УСПІХ] {attribute_name.capitalize()} збільшено на 1! "
              f"Залишилось очок: {self.attribute_points}")
        
        return True
    
    def spend_skill_point(self, skill_name):
        """
        Витратити очко навички.
        
        Параметри:
            skill_name: Назва навички
            
        Повертає:
            bool: True якщо успішно, False якщо немає очок
        """
        # Перевірка наявності очок
        if self.skill_points <= 0:
            print(f"[ПОМИЛКА] Немає доступних очок навичок!")
            return False
        
        # Перевірка наявності такої навички у персонажа
        if not hasattr(self.character, 'skills'):
            print(f"[ПОМИЛКА] У персонажа немає системи навичок!")
            return False
        
        # Спроба покращити навичку (якщо вона існує) або додати нову
        skill_improved = False
        for skill in self.character.skills:
            if skill.name == skill_name:
                skill.level += 1
                skill_improved = True
                break
        
        if not skill_improved:
            # Якщо навичка не знайдена, додаємо нову (якщо можливо)
            print(f"[ПОПЕРЕДЖЕННЯ] Навичка '{skill_name}' не знайдена. "
                  f"Перевірте назву навички.")
            return False
        
        # Витрачаємо очко
        self.skill_points -= 1
        
        print(f"[УСПІХ] Навичка '{skill_name}' покращена! "
              f"Залишилось очок: {self.skill_points}")
        
        return True
    
    def get_available_points(self):
        """
        Отримати інформацію про доступні очки.
        
        Повертає:
            dict: Словник з інформацією про очки
        """
        return {
            'attribute_points': self.attribute_points,
            'skill_points': self.skill_points,
            'total_available': self.attribute_points + self.skill_points,
            'level': self.level
        }
    
    def can_spend_attribute_point(self):
        """Перевірити, чи є доступні очки атрибутів."""
        return self.attribute_points > 0
    
    def can_spend_skill_point(self):
        """Перевірити, чи є доступні очки навичок."""
        return self.skill_points > 0
    
    def reset_points(self):
        """Скинути всі очки (для переквалірікації)."""
        self.attribute_points = 0
        self.skill_points = 0
        print("[ІНФОРМАЦІЯ] Очки скинуті.")
    
    def _recalculate_bonuses(self):
        """Перерахувати всі бонуси після зміни атрибутів."""
        # Оновлюємо HP бонус
        hp_bonus = self.character.attributes.get_hp_bonus()
        # Можна додати додаткову логіку перерахунку бонусів тут
    
    def _print_level_up_message(self):
        """Вивести гарне повідомлення про підвищення рівня."""
        print("\n" + "="*60)
        print(f"[РІВЕНЬ ПІДВИЩЕНО!] Ви тепер рівня {self.level}!")
        print("="*60)
        print(f"[ОТРИМАНІ ОЧКИ]")
        print(f"   [АТРИБУТИ] +{self.ATTRIBUTE_POINTS_PER_LEVEL} очок атрибутів "
              f"(всього: {self.attribute_points})")
        print(f"   [НАВИЧКИ] +{self.SKILL_POINTS_PER_LEVEL} очко навичок "
              f"(всього: {self.skill_points})")
        print(f"[HP ВІДНОВЛЕНО] {self.character.hp}/{self.character.max_hp}")
        print("="*60 + "\n")
    
    def get_level_up_history(self):
        """Отримати історію підвищень рівня."""
        return self.level_up_history
    
    def get_summary(self):
        """Отримати повний звіт про систему прокачки."""
        return {
            'current_level': self.level,
            'attribute_points': self.attribute_points,
            'skill_points': self.skill_points,
            'character_name': self.character.name,
            'character_level': self.character.level,
            'hp': f"{self.character.hp}/{self.character.max_hp}",
            'attributes': {
                'strength': self.character.attributes.strength,
                'intelligence': self.character.attributes.intelligence,
                'agility': self.character.attributes.agility,
                'luck': self.character.attributes.luck
            },
            'total_level_ups': len(self.level_up_history)
        }
