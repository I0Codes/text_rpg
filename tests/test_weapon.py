from entities.characters import Character
from items.item import RustyDagger, IronSword, SteelAxe, WoodenStaff


def test_weapon_constructors_and_stats():
    rusty = RustyDagger()
    assert rusty.name == "Rusty Dagger"
    assert rusty.damage == 5
    assert rusty.damage_type == "PHYSICAL"
    assert rusty.required_strength == 0

    sword = IronSword()
    assert sword.name == "Iron Sword"
    assert sword.damage == 15
    assert sword.damage_type == "PHYSICAL"
    assert sword.required_strength == 5

    axe = SteelAxe()
    assert axe.name == "Steel Axe"
    assert axe.damage == 25
    assert axe.damage_type == "PHYSICAL"
    assert axe.required_strength == 8

    staff = WoodenStaff()
    assert staff.name == "Wooden Staff"
    assert staff.damage == 20
    assert staff.damage_type == "MAGICAL"
    assert staff.required_strength == 0


def test_weapon_strength_requirements():
    char = Character("Hero", hp=100, max_hp=100, stamina=50, max_stamina=50)

    # Default character strength is 5
    assert RustyDagger().can_equip(char) is True
    assert IronSword().can_equip(char) is True
    assert SteelAxe().can_equip(char) is False
    assert WoodenStaff().can_equip(char) is True

    char.attributes.update(strength=8)
    assert SteelAxe().can_equip(char) is True

    char.attributes.update(strength=4)
    assert IronSword().can_equip(char) is False


def test_location_weapon_spawn():
    from world.locations import Location

    class TestLocation(Location):
        def __init__(self):
            super().__init__("Test")

    player = Character("TestHero", hp=100, max_hp=100, stamina=50, max_stamina=50)
    loc = TestLocation()

    # Закріплюємо random для стабільного тесту
    import random
    random.seed(0)

    # Пробуємо кілька обходів, де має бути хоча б декілька знайдених зброї
    found = 0
    for _ in range(30):
        enemy = loc.handle_action("1", player)
        if enemy is None:
            # як тільки зброя знайдена, inventory має ненульовий length
            if player.inventory.items:
                found += 1
                player.inventory.items.clear()

    assert found > 0

