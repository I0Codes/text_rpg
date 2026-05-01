import unittest

from config.settings import BASE_HP
from core.game_engine import GameEngine
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


class TestGameEngine(unittest.TestCase):
    def test_calculate_level_requirements(self):
        self.assertEqual(GameEngine.calculate_level_requirements(1), 100)
        self.assertEqual(GameEngine.calculate_level_requirements(5), 500)

    def test_calculate_total_stats_aggregates_equipment_bonuses(self):
        warrior = Warrior("Test")
        weapon = type(
            "Weapon",
            (),
            {"bonuses": {"physical_damage": 5.0, "crit_chance": 0.02}},
        )()
        armor = type(
            "Armor",
            (),
            {"bonuses": {"defense": 3, "max_hp": 20}},
        )()
        warrior.equipped_weapon = weapon
        warrior.equipped_armor = armor

        totals = GameEngine.calculate_total_stats(warrior)

        self.assertEqual(totals["max_hp"], warrior.max_hp + 20)
        self.assertEqual(
            totals["physical_damage"], warrior.calculate_physical_damage() + 5.0
        )
        self.assertEqual(totals["defense"], 3)
        self.assertAlmostEqual(
            totals["crit_chance"], warrior.attributes.get_crit_chance() + 0.02, places=6
        )

    def test_calculate_total_stats_includes_active_effects(self):
        warrior = Warrior("Test")
        effect = type(
            "Effect",
            (),
            {"bonuses": {"dodge_chance": 0.05, "max_stamina": 10}},
        )()
        warrior.active_effects = [effect]

        totals = GameEngine.calculate_total_stats(warrior)

        expected_dodge = warrior.attributes.get_dodge_chance() + 0.05
        self.assertAlmostEqual(totals["dodge_chance"], expected_dodge, places=6)
        self.assertEqual(totals["max_stamina"], warrior.max_stamina + 10)


if __name__ == '__main__':
    unittest.main()
