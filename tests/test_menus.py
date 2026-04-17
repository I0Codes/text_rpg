import pytest

from core.game import Game
from ui.menus import MainMenu, CharacterCreationMenu, InventoryMenu
from world.locations import Village
from entities.characters import Character
from items.item import Item


def test_main_menu_new_game(monkeypatch):
    inputs = iter(["invalid", "5", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = MainMenu.show()
    assert result == "new_game"


def test_character_creation_menu(monkeypatch):
    inputs = iter(["2", "Мой герой", "strength", "strength", "гото"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    player = CharacterCreationMenu.show()

    assert player.name == "Мой герой"
    assert player.is_alive()
    assert player.attributes.strength >= 7


def test_inventory_menu_use_item(monkeypatch):
    player = Character(name="Test", hp=100, max_hp=100, stamina=50, max_stamina=50)
    potion = Item("consumable", "Зілля", description="Лікує", weight=0.1, value=1, stackable=True, quantity=1)
    player.add_item(potion)

    inputs = iter(["1", "1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    InventoryMenu.show(player)
    assert potion not in player.inventory.items


def test_game_inventory_action_opens_inventory_menu(monkeypatch):
    player = Character(name="Test", hp=100, max_hp=100, stamina=50, max_stamina=50)
    game = Game(player, Village())
    called = []

    monkeypatch.setattr(InventoryMenu, "show", lambda p: called.append(p))
    game.handle_action("i")

    assert called == [player]


def test_game_status_action_shows_status(monkeypatch):
    player = Character(name="Test", hp=100, max_hp=100, stamina=50, max_stamina=50)
    game = Game(player, Village())
    called = []

    monkeypatch.setattr(game, "show_status", lambda: called.append(True))
    game.handle_action("s")

    assert called == [True]
