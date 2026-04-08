import pytest
from entities.characters import Character
from items.consumables import HealthPotion, StaminaPotion, ManaPotion


def test_health_potion():
    character = Character("Test", hp=10, max_hp=100, stamina=50, max_stamina=100)
    potion = HealthPotion("Health Potion", "Restores 50 HP", 10)
    potion.consume(character)
    assert character.hp == 60  # 10 + 50


def test_stamina_potion():
    character = Character("Test", hp=50, max_hp=100, stamina=10, max_stamina=100)
    potion = StaminaPotion("Stamina Potion", "Restores 40 stamina", 10)
    potion.consume(character)
    assert character.stamina == 50  # 10 + 40


def test_mana_potion():
    character = Character("Test", hp=50, max_hp=100, stamina=50, max_stamina=100)
    character.mana = 20  # set to 20 for test
    potion = ManaPotion("Mana Potion", "Restores 30 mana", 10)
    potion.consume(character)
    assert character.mana == 50  # min(50, 20+30)

    # Let's modify the test. 

def test_mana_potion():
    character = Character("Test", hp=50, max_hp=100, stamina=50, max_stamina=100)
    character.mana = 0  # set to 0 for test
    potion = ManaPotion("Mana Potion", "Restores 30 mana", 10)
    potion.consume(character)
    assert character.mana == 30