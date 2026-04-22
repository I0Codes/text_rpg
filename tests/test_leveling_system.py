"""Тести для системи прокачки рівнів (LevelingSystem)."""

import pytest
from entities import Character
from entities.leveling_system import LevelingSystem


# Фіксири для тестів
@pytest.fixture
def test_character():
    """Створює тестового персонажа."""
    character = Character(
        name="TestHero",
        hp=100,
        max_hp=100,
        stamina=50,
        max_stamina=50,
        level=1
    )
    return character


@pytest.fixture
def leveling_system(test_character):
    """Створює систему прокачки для тестового персонажа."""
    return test_character.leveling_system


class TestLevelingSystemBasics:
    """Тести базових функцій системи прокачки."""
    
    def test_leveling_system_initialization(self, test_character, leveling_system):
        """Тест ініціалізації LevelingSystem."""
        assert leveling_system.level == 1
        assert leveling_system.attribute_points == 0
        assert leveling_system.skill_points == 0
        assert leveling_system.character == test_character
    
    def test_get_available_points_initial(self, leveling_system):
        """Тест отримання доступних очок на початок гри."""
        points = leveling_system.get_available_points()
        
        assert points['attribute_points'] == 0
        assert points['skill_points'] == 0
        assert points['total_available'] == 0
        assert points['level'] == 1


class TestLevelUp:
    """Тести підвищення рівня."""
    
    def test_single_level_up(self, test_character, leveling_system):
        """Тест підвищення на один рівень."""
        initial_level = leveling_system.level
        
        leveling_system.level_up()
        
        assert leveling_system.level == initial_level + 1
        assert test_character.level == initial_level + 1
        assert leveling_system.attribute_points == 2
        assert leveling_system.skill_points == 1
    
    def test_multiple_level_ups(self, test_character, leveling_system):
        """Тест підвищення на кілька рівнів."""
        # Піднімаємось на 3 рівні
        leveling_system.level_up()
        leveling_system.level_up()
        leveling_system.level_up()
        
        assert leveling_system.level == 4
        assert leveling_system.attribute_points == 6  # 2 * 3
        assert leveling_system.skill_points == 3      # 1 * 3
    
    def test_hp_restoration_on_level_up(self, test_character, leveling_system):
        """Тест відновлення HP при підвищенні рівня."""
        # Скорочуємо HP
        test_character.hp = 10
        initial_max_hp = test_character.max_hp
        
        leveling_system.level_up()
        
        assert test_character.hp == test_character.max_hp
        assert test_character.hp > 10
    
    def test_stamina_restoration_on_level_up(self, test_character, leveling_system):
        """Тест відновлення stamina при підвищенні рівня."""
        # Скорочуємо stamina
        test_character.stamina = 10
        initial_max_stamina = test_character.max_stamina
        
        leveling_system.level_up()
        
        assert test_character.stamina == test_character.max_stamina
    
    def test_mana_restoration_on_level_up(self, test_character, leveling_system):
        """Тест відновлення mana при підвищенні рівня."""
        # Скорочуємо mana
        test_character.mana = 10
        
        leveling_system.level_up()
        
        assert test_character.mana == test_character.max_mana
    
    def test_level_up_history(self, leveling_system):
        """Тест історії підвищень рівня."""
        leveling_system.level_up()
        leveling_system.level_up()
        
        history = leveling_system.get_level_up_history()
        
        assert len(history) == 2
        assert history[0]['level'] == 2
        assert history[1]['level'] == 3
        assert history[0]['attribute_points_gained'] == 2
        assert history[0]['skill_points_gained'] == 1


class TestAttributePoints:
    """Тести витрати очок атрибутів."""
    
    def test_spend_attribute_point_valid(self, test_character, leveling_system):
        """Тест витрати очка атрибуту на валідний атрибут."""
        # Даємо очки
        leveling_system.level_up()
        
        initial_strength = test_character.attributes.strength
        result = leveling_system.spend_attribute_point('strength')
        
        assert result is True
        assert test_character.attributes.strength == initial_strength + 1
        assert leveling_system.attribute_points == 1  # 2 - 1
    
    def test_spend_all_attribute_points(self, test_character, leveling_system):
        """Тест витрати всіх очок атрибутів."""
        leveling_system.level_up()
        
        initial_strength = test_character.attributes.strength
        
        # Витрачаємо обидва очка на силу
        leveling_system.spend_attribute_point('strength')
        leveling_system.spend_attribute_point('strength')
        
        assert test_character.attributes.strength == initial_strength + 2
        assert leveling_system.attribute_points == 0
    
    def test_spend_attribute_point_no_points(self, test_character, leveling_system):
        """Тест спроби витрати очка атрибуту без доступних очок."""
        result = leveling_system.spend_attribute_point('strength')
        
        assert result is False
        assert leveling_system.attribute_points == 0
    
    def test_spend_attribute_point_invalid_attribute(self, test_character, leveling_system):
        """Тест спроби витрати очка на невалідний атрибут."""
        leveling_system.level_up()
        
        with pytest.raises(ValueError, match="Невірний атрибут"):
            leveling_system.spend_attribute_point('invalid_attribute')
    
    def test_spend_attribute_points_different_attributes(self, test_character, leveling_system):
        """Тест розподілу очок між різними атрибутами."""
        leveling_system.level_up()
        leveling_system.level_up()
        
        initial_str = test_character.attributes.strength
        initial_int = test_character.attributes.intelligence
        initial_agi = test_character.attributes.agility
        
        # Розподіляємо очки
        leveling_system.spend_attribute_point('strength')
        leveling_system.spend_attribute_point('intelligence')
        leveling_system.spend_attribute_point('agility')
        leveling_system.spend_attribute_point('luck')
        
        assert test_character.attributes.strength == initial_str + 1
        assert test_character.attributes.intelligence == initial_int + 1
        assert test_character.attributes.agility == initial_agi + 1
        assert leveling_system.attribute_points == 0
    
    def test_cannot_overspend_attribute_points(self, test_character, leveling_system):
        """Тест неможливості потратити більше очок, ніж є."""
        leveling_system.level_up()  # Даємо 2 очка
        
        # Намагаємось потратити 3 очка
        assert leveling_system.spend_attribute_point('strength') is True
        assert leveling_system.spend_attribute_point('strength') is True
        assert leveling_system.spend_attribute_point('strength') is False
        
        assert leveling_system.attribute_points == 0


class TestSkillPoints:
    """Тести витрати очок навичок."""
    
    def test_can_spend_skill_point(self, test_character, leveling_system):
        """Тест можливості витрати очка навички."""
        leveling_system.level_up()
        
        # За замовчуванням навичок може не бути, але система повинна про це красиво повідомити
        result = leveling_system.spend_skill_point('test_skill')
        
        # Повертає False так як навички не знайдені
        assert result is False
    
    def test_skill_points_no_points(self, test_character, leveling_system):
        """Тест спроби витрати очка навички без доступних очок."""
        result = leveling_system.spend_skill_point('any_skill')
        
        assert result is False
        assert leveling_system.skill_points == 0


class TestValidation:
    """Тести валідації."""
    
    def test_cannot_get_more_points_below(self, test_character, leveling_system):
        """Тест неможливості отримати більше очок за формулою."""
        # Максимум очок повинен бути кількість_рівнів * очки_за_рівень
        leveling_system.level_up()
        leveling_system.level_up()
        leveling_system.level_up()
        
        # 3 рівні * 2 очка = 6 очок атрибутів
        # 3 рівні * 1 очко = 3 очка навичок
        assert leveling_system.attribute_points == 6
        assert leveling_system.skill_points == 3
        
        # Намагаємось маніпулювати очками безпосередньо - не повинно бути способу
        # (у реальній грі це буде захищено)
    
    def test_can_check_available_points(self, test_character, leveling_system):
        """Тест перевірки доступних очок."""
        assert leveling_system.can_spend_attribute_point() is False
        assert leveling_system.can_spend_skill_point() is False
        
        leveling_system.level_up()
        
        assert leveling_system.can_spend_attribute_point() is True
        assert leveling_system.can_spend_skill_point() is True
    
    def test_reset_points(self, test_character, leveling_system):
        """Тест скидання очок (для переквалірікації)."""
        leveling_system.level_up()
        leveling_system.level_up()
        
        assert leveling_system.attribute_points == 4
        assert leveling_system.skill_points == 2
        
        leveling_system.reset_points()
        
        assert leveling_system.attribute_points == 0
        assert leveling_system.skill_points == 0


class TestSummary:
    """Тести отримання інформації про систему."""
    
    def test_get_summary(self, test_character, leveling_system):
        """Тест отримання повного звіту."""
        leveling_system.level_up()
        
        summary = leveling_system.get_summary()
        
        assert summary['current_level'] == 2
        assert summary['attribute_points'] == 2
        assert summary['skill_points'] == 1
        assert summary['character_name'] == "TestHero"
        assert summary['total_level_ups'] == 1
        assert 'attributes' in summary
        assert 'hp' in summary
    
    def test_get_available_points_after_spending(self, test_character, leveling_system):
        """Тест отримання доступних очок після витрати."""
        leveling_system.level_up()
        leveling_system.spend_attribute_point('strength')
        
        points = leveling_system.get_available_points()
        
        assert points['attribute_points'] == 1
        assert points['skill_points'] == 1
        assert points['total_available'] == 2


class TestIntegrationScenarios:
    """Інтеграційні тести (реальні сценарії гри)."""
    
    def test_level_up_multiple_times_and_distribute_points(self, test_character, leveling_system):
        """Сценарій: Персонаж піднімається кілька разів і розподіляє очки."""
        # Початковий рівень
        assert leveling_system.level == 1
        
        # Піднімаємось 3 рази
        for _ in range(3):
            leveling_system.level_up()
        
        # Повинно бути 6 очок атрибутів і 3 очка навичок
        assert leveling_system.level == 4
        assert leveling_system.attribute_points == 6
        assert leveling_system.skill_points == 3
        
        # Розподіляємо очки: +2 сила, +2 інтелект, +2 ловкість
        initial_attrs = {
            'strength': test_character.attributes.strength,
            'intelligence': test_character.attributes.intelligence,
            'agility': test_character.attributes.agility
        }
        
        leveling_system.spend_attribute_point('strength')
        leveling_system.spend_attribute_point('strength')
        leveling_system.spend_attribute_point('intelligence')
        leveling_system.spend_attribute_point('intelligence')
        leveling_system.spend_attribute_point('agility')
        leveling_system.spend_attribute_point('agility')
        
        # Перевіряємо результати
        assert test_character.attributes.strength == initial_attrs['strength'] + 2
        assert test_character.attributes.intelligence == initial_attrs['intelligence'] + 2
        assert test_character.attributes.agility == initial_attrs['agility'] + 2
        assert leveling_system.attribute_points == 0
    
    def test_cannot_exceed_attribute_point_limit(self, test_character, leveling_system):
        """Сценарій: Спроба потратити більше очок, ніж отримано."""
        leveling_system.level_up()  # +2 очка
        
        # Намагаємось потратити 3 очка
        assert leveling_system.spend_attribute_point('strength') is True
        assert leveling_system.spend_attribute_point('strength') is True
        assert leveling_system.spend_attribute_point('strength') is False  # Третя невдача
        
        assert leveling_system.attribute_points == 0
    
    def test_recovery_after_damage_on_level_up(self, test_character, leveling_system):
        """Сценарій: Персонаж отримав урон, потім підвищив рівень - повне відновлення."""
        # Імітуємо урон
        test_character.hp = 20
        test_character.stamina = 5
        test_character.mana = 15
        
        initial_max_hp = test_character.max_hp
        initial_max_stamina = test_character.max_stamina
        initial_max_mana = test_character.max_mana
        
        # Підвищуємо рівень
        leveling_system.level_up()
        
        # Перевіряємо повне відновлення
        assert test_character.hp == test_character.max_hp
        assert test_character.stamina == test_character.max_stamina
        assert test_character.mana == test_character.max_mana


if __name__ == "__main__":
    # Запуск тестів: pytest tests/test_leveling_system.py -v
    print("Запустіть: pytest tests/test_leveling_system.py -v")
