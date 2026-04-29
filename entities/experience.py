from ui.progression_ui import ProgressionUI


class ExperienceManager:
    def __init__(self, character):
        from core.game_engine import GameEngine

        self.character = character
        self.total_experience = 0
        self.experience_to_next_level = GameEngine.calculate_level_requirements(self.character.level)
        self.experience_sources = []  # Логування джерел досвіду
    
    def gain_experience(self, amount, source="unknown"):
        """
        Додати досвід:
        1. Додати до total_experience
        2. Показати повідомлення
        3. Перевірити чи досягнуто нового рівня
        4. Якщо так - викликати level_up()
        """
        if amount <= 0:
            return
        
        self.total_experience += amount
        self.experience_sources.append({
            'source': source,
            'amount': amount,
            'total': self.total_experience
        })
        
        ProgressionUI.display_experience_gain(amount, source, self.get_progress_percentage())
        
        # Перевірка рівня
        while self.total_experience >= self.experience_to_next_level:
            self._level_up()
    
    def _level_up(self):
        """Підвищення рівня персонажа"""
        from core.game_engine import GameEngine

        remaining_exp = self.total_experience - self.experience_to_next_level
        self.character.level += 1
        self.total_experience = remaining_exp
        
        self.experience_to_next_level = GameEngine.calculate_level_requirements(self.character.level)
        
        # Викликаємо метод покращення характеристик
        if hasattr(self.character, 'level_up_stats'):
            self.character.level_up_stats()
        if hasattr(self.character, 'apply_level_bonus'):
            self.character.apply_level_bonus(self.character.level)
        
        ProgressionUI.display_level_up(self.character, self.character.level)
    
    def calculate_experience_reward(self, enemy_level, player_level):
        """
        Розрахунок досвіду від ворога:
        - Базовий досвід = enemy_level * 50
        - Якщо ворог вищого рівня: +25% за кожен рівень різниці
        - Якщо ворог нижчого рівня: -25% за кожен рівень різниці
        - Мінімум 10 досвіду
        """
        base_experience = enemy_level * 50
        level_difference = enemy_level - player_level
        
        if level_difference > 0:
            # Ворог вищого рівня
            multiplier = 1 + (0.25 * level_difference)
        elif level_difference < 0:
            # Ворог нижчого рівня
            multiplier = max(0.25, 1 + (0.25 * level_difference))
        else:
            # Однаковий рівень
            multiplier = 1.0
        
        reward = int(base_experience * multiplier)
        return max(10, reward)  # Мінімум 10 досвіду
    
    def get_progress_percentage(self):
        """Відсоток прогресу до наступного рівня"""
        if self.experience_to_next_level == 0:
            return 100
        
        progress = (self.total_experience / self.experience_to_next_level) * 100
        return min(100, progress)
    
    def get_experience_sources_log(self):
        """Отримати логування джерел досвіду"""
        return self.experience_sources
    
    def get_summary(self):
        """Отримати зведення про досвід"""
        return {
            'total_experience': self.total_experience,
            'experience_to_next_level': self.experience_to_next_level,
            'progress_percentage': self.get_progress_percentage(),
            'level': self.character.level
        }
