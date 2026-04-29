import unittest
from entities.experience import ExperienceManager


class MockCharacter:
    """Макет персонажа для тестування"""
    def __init__(self):
        self.level = 1
        self.max_hp = 100
        self.hp = 100
    
    def level_up_stats(self):
        """Макет методу level_up_stats"""
        self.max_hp += 10
        self.hp = self.max_hp


class TestExperienceManager(unittest.TestCase):
    
    def setUp(self):
        self.character = MockCharacter()
        self.exp_manager = ExperienceManager(self.character)
    
    def test_gain_experience_single_source(self):
        """Отримати досвід від одного джерела"""
        self.exp_manager.gain_experience(50, source="combat")
        self.assertEqual(self.exp_manager.total_experience, 50)
        self.assertEqual(len(self.exp_manager.experience_sources), 1)
        self.assertEqual(self.exp_manager.experience_sources[0]['source'], "combat")
    
    def test_gain_experience_multiple_sources(self):
        """Отримати досвід від різних джерел"""
        self.exp_manager.gain_experience(30, source="combat")
        self.exp_manager.gain_experience(20, source="quest")
        self.exp_manager.gain_experience(15, source="exploration")
        
        self.assertEqual(self.exp_manager.total_experience, 65)
        self.assertEqual(len(self.exp_manager.experience_sources), 3)
    
    def test_calculate_experience_equal_level(self):
        """Розрахунок досвіду для ворога однакового рівня"""
        reward = self.exp_manager.calculate_experience_reward(
            enemy_level=1, player_level=1
        )
        self.assertEqual(reward, 50)  # 1 * 50 * 1.0
    
    def test_calculate_experience_higher_level_enemy(self):
        """Розрахунок досвіду для ворога вищого рівня"""
        # Рівень 5 ворога для гравця рівня 1 (різниця 4)
        reward = self.exp_manager.calculate_experience_reward(
            enemy_level=5, player_level=1
        )
        expected = int(5 * 50 * (1 + 0.25 * 4))  # 250 * 2.0 = 500
        self.assertEqual(reward, expected)
    
    def test_calculate_experience_lower_level_enemy(self):
        """Розрахунок досвіду для ворога нижчого рівня"""
        # Рівень 1 ворога для гравця рівня 5 (різниця -4)
        reward = self.exp_manager.calculate_experience_reward(
            enemy_level=1, player_level=5
        )
        expected = int(1 * 50 * max(0.25, 1 + 0.25 * (-4)))  # 50 * 0.25 = 12.5 -> 12
        self.assertGreaterEqual(reward, 10)  # Мінімум 10
    
    def test_experience_minimum(self):
        """Мінімум досвіду = 10"""
        reward = self.exp_manager.calculate_experience_reward(
            enemy_level=1, player_level=10
        )
        self.assertGreaterEqual(reward, 10)
    
    def test_level_up(self):
        """Перевірити рівень при переборі досвіду"""
        initial_level = self.character.level
        self.exp_manager.gain_experience(100, source="combat")
        
        self.assertEqual(self.character.level, initial_level + 1)
        self.assertEqual(self.exp_manager.total_experience, 0)

    def test_level_up_applies_level_bonus(self):
        """Перевірка виклику apply_level_bonus під час level_up"""
        class BonusCharacter(MockCharacter):
            def __init__(self):
                super().__init__()
                self.bonus_applied = False

            def apply_level_bonus(self, level):
                self.bonus_applied = True

        character = BonusCharacter()
        exp_manager = ExperienceManager(character)
        exp_manager.gain_experience(100, source="combat")

        self.assertTrue(character.bonus_applied)
    
    def test_multiple_level_ups(self):
        """Кілька рівнів одночасно"""
        self.exp_manager.gain_experience(300, source="quest")
        self.assertGreater(self.character.level, 1)
    
    def test_progress_percentage(self):
        """Перевірити відсоток прогресу до рівня"""
        self.exp_manager.gain_experience(50)
        progress = self.exp_manager.get_progress_percentage()
        self.assertAlmostEqual(progress, 50.0, places=1)
    
    def test_experience_sources_logging(self):
        """Перевірити логування джерел досвіду"""
        self.exp_manager.gain_experience(25, source="combat")
        self.exp_manager.gain_experience(15, source="exploration")
        
        log = self.exp_manager.get_experience_sources_log()
        sources = [entry['source'] for entry in log]
        
        self.assertIn("combat", sources)
        self.assertIn("exploration", sources)
    
    def test_experience_scaling_by_level(self):
        """Перевірити що масштабування досвіду за рівнями"""
        # Ворог рівня 3 повинен давати більше досвіду ніж рівня 1
        exp_level1 = self.exp_manager.calculate_experience_reward(
            enemy_level=1, player_level=1
        )
        exp_level3 = self.exp_manager.calculate_experience_reward(
            enemy_level=3, player_level=1
        )
        self.assertGreater(exp_level3, exp_level1)


if __name__ == '__main__':
    unittest.main()
