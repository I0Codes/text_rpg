import random

from world.locations import Village, Cave, DarkForest, create_world_map
from entities.characters import Character


def test_location_actions_include_inventory_and_status():
    village = Village()
    actions = village.get_actions()

    assert actions["i"] == "Переглянути інвентар"
    assert actions["s"] == "Переглянути статус персонажа"


def test_location_transitions():
    world = create_world_map()
    assert world.name == "Село"
    assert "3" in world.neighbors

    dark_forest = world.neighbors["3"]
    assert isinstance(dark_forest, DarkForest)
    assert "3" in dark_forest.neighbors

    cave = dark_forest.neighbors["3"]
    assert isinstance(cave, Cave)


def test_village_safe_explore(monkeypatch, capsys):
    hero = Character("Test", hp=50, max_hp=100, stamina=50, max_stamina=50)
    village = Village()
    monkeypatch.setattr(random, "random", lambda: 0.9)

    enemy = village._explore(hero)
    assert enemy is None

    out = capsys.readouterr().out
    assert "Село безпечне" in out


def test_cave_danger_explore(monkeypatch):
    hero = Character("Test", hp=50, max_hp=100, stamina=50, max_stamina=50)
    cave = Cave()
    monkeypatch.setattr(random, "random", lambda: 0.1)

    enemy = cave._explore(hero)
    assert enemy is not None
    assert enemy.name in {"Orc", "Troll", "Dragon"}
