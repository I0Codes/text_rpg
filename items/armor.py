try:
    from .item import Item
except ImportError:
    from item import Item


class Armor(Item):
    def __init__(self, name, description, defense, slot, armor_type, value):
        super().__init__("ARMOR", name, description, value=value)
        self.defense = defense
        self.slot = slot
        self.armor_type = armor_type

    def __str__(self):
        return (
            f"Armor(name={self.name!r}, slot={self.slot}, type={self.armor_type}, "
            f"defense={self.defense}, value={self.value})"
        )


class LeatherArmor(Armor):
    def __init__(self, name="Leather Armor", description="Light armor with modest protection.", value=15):
        super().__init__(name, description, defense=5, slot="CHEST", armor_type="LIGHT", value=value)


class IronChestplate(Armor):
    def __init__(self, name="Iron Chestplate", description="Medium armor offering solid defense.", value=35):
        super().__init__(name, description, defense=15, slot="CHEST", armor_type="MEDIUM", value=value)


class SteelHelmet(Armor):
    def __init__(self, name="Steel Helmet", description="Heavy helmet with strong protection.", value=25):
        super().__init__(name, description, defense=10, slot="HEAD", armor_type="HEAVY", value=value)
