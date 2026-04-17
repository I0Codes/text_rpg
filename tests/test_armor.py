import pytest

from items.armor import LeatherArmor, IronChestplate, SteelHelmet


def test_leather_armor_properties():
    armor = LeatherArmor()
    assert armor.item_type == "ARMOR"
    assert armor.defense == 5
    assert armor.slot == "CHEST"
    assert armor.armor_type == "LIGHT"
    assert "Leather Armor" in armor.name


def test_iron_chestplate_properties():
    armor = IronChestplate()
    assert armor.item_type == "ARMOR"
    assert armor.defense == 15
    assert armor.slot == "CHEST"
    assert armor.armor_type == "MEDIUM"
    assert "Iron Chestplate" in armor.name


def test_steel_helmet_properties():
    armor = SteelHelmet()
    assert armor.item_type == "ARMOR"
    assert armor.defense == 10
    assert armor.slot == "HEAD"
    assert armor.armor_type == "HEAVY"
    assert "Steel Helmet" in armor.name
