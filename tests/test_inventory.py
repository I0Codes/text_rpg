import pytest

from items.inventory import Inventory
from items.item import Item
from entities.characters import Character


def test_add_and_show():
    inv = Inventory(max_capacity=2)
    assert str(inv) == "Inventory(0/2)"
    sword = Item("weapon", "Меч")
    assert inv.add_item(sword) is True
    assert len(inv.items) == 1
    # adding second item
    shield = Item("armor", "Щит")
    assert inv.add_item(shield) is True
    assert len(inv.items) == 2
    # trying to overfill
    potion = Item("consumable", "Зілля")
    assert inv.add_item(potion) is False


def test_stackable_items():
    inv = Inventory()
    potion = Item("consumable", "Зілля", stackable=True, quantity=1)
    inv.add_item(potion)
    # add another of same type
    another = Item("consumable", "Зілля", stackable=True, quantity=2)
    inv.add_item(another)
    assert len(inv.items) == 1
    assert inv.items[0].quantity == 3


def test_remove_item():
    inv = Inventory()
    potion = Item("consumable", "Зілля", stackable=True, quantity=3)
    inv.add_item(potion)
    assert inv.remove_item(potion) is True
    assert potion.quantity == 2
    # remove until gone
    inv.remove_item(potion)
    inv.remove_item(potion)
    assert potion not in inv.items


def test_use_item_consumable():
    inv = Inventory()
    player = Character("Test", hp=10)
    class Heal(Item):
        def use(self, user):
            user.hp += 5
            return True
    heal = Heal("consumable", "Гілка", stackable=False)
    inv.add_item(heal)
    assert inv.use_item(heal, player) is True
    assert player.hp == 15
    assert heal not in inv.items


def test_get_items_by_type():
    inv = Inventory()
    inv.add_item(Item("weapon", "Сокира"))
    inv.add_item(Item("consumable", "Зілля"))
    weapons = inv.get_items_by_type("weapon")
    assert len(weapons) == 1
    assert weapons[0].name == "Сокира"
