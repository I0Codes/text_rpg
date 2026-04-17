import unittest

from config.settings import BASE_HP
from entities.characters import Warrior, Mage, Scout


class TestCharacterLevelBonuses(unittest.TestCase):
    def test_warrior_get_level_bonuses(self):
        warrior = Warrior("Test")
        self.assertEqual(warrior.get_level_bonuses(2), {"hp": 5})
        milestone = warrior.get_next_milestone()
        self.assertEqual(milestone, {"level": 2, "bonuses": {"hp": 5}})

    def test_warrior_apply_level_bonus(self):
        warrior = Warrior("Test")
        warrior.apply_level_bonus(2)
        self.assertEqual(warrior.max_hp, BASE_HP + 20 + 5)
        self.assertEqual(warrior.hp, warrior.max_hp)

    def test_mage_get_level_bonuses(self):
        mage = Mage("Test")
        self.assertEqual(mage.get_level_bonuses(6), {"skill": "Ice Storm"})
        milestone = mage.get_next_milestone()
        self.assertEqual(milestone, {"level": 2, "bonuses": {"mana": 10}})

    def test_scout_get_level_bonuses(self):
        scout = Scout("Test")
        self.assertEqual(scout.get_level_bonuses(8), {"dodge": 0.03})
        milestone = scout.get_next_milestone()
        self.assertEqual(milestone, {"level": 2, "bonuses": {"stamina": 5}})

    def test_apply_level_bonus_adds_skill(self):
        scout = Scout("Test")
        scout.apply_level_bonus(6)
        self.assertIn("Smoke Bomb", scout.skills)


if __name__ == '__main__':
    unittest.main()
