import pytest

from core.game import Game
from ui.console_ui import ConsoleUI
from ui.menus import MainMenu, CharacterCreationMenu, InventoryMenu
from world.locations import Village
from entities.characters import Character
from items.item import Item


def _ui():
    return ConsoleUI()


def test_main_menu_new_game(monkeypatch):
    inputs = iter(["invalid", "5", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = MainMenu(_ui()).show()
    assert result == "new_game"


def test_character_creation_menu(monkeypatch):
    # "2" → Mage, name, "5" → random attribute distribution
    inputs = iter(["2", "Мой герой", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    player = CharacterCreationMenu(_ui()).show()

    assert player.name == "Мой герой"
    assert player.is_alive()


def test_inventory_menu_use_item(monkeypatch):
    player = Character(name="Test", hp=100, max_hp=100, stamina=50, max_stamina=50)
    potion = Item("consumable", "Зілля", description="Лікує", weight=0.1, value=1, stackable=True, quantity=1)
    player.add_item(potion)

    inputs = iter(["1", "1", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    InventoryMenu(_ui()).show(player)
    assert potion not in player.inventory.items


def test_game_inventory_action_opens_inventory_menu(monkeypatch):
    player = Character(name="Test", hp=100, max_hp=100, stamina=50, max_stamina=50)
    game = Game(player, Village(), _ui())
    called = []

    monkeypatch.setattr(InventoryMenu, "show", lambda self, p: called.append(p))
    game.handle_action("i")

    assert called == [player]


def test_game_status_action_shows_status(monkeypatch):
    player = Character(name="Test", hp=100, max_hp=100, stamina=50, max_stamina=50)
    game = Game(player, Village(), _ui())
    called = []

    monkeypatch.setattr(game, "show_status", lambda: called.append(True))
    game.handle_action("s")

    assert called == [True]
