try:
    from .item import Item
except ImportError:
    from item import Item


class Consumable(Item):
    def __init__(self, name, description, value):
        super().__init__("CONSUMABLE", name, description, value=value)

    def use(self, user):
        """Override use to consume the item"""
        self.consume(user)
        return True

    def consume(self, character):
        """Використати предмет на персонажі"""
        pass


class HealthPotion(Consumable):
    def consume(self, character):
        character.heal(50)


class StaminaPotion(Consumable):
    def consume(self, character):
        character.restore_stamina(40)


class ManaPotion(Consumable):
    def consume(self, character):
        character.restore_mana(30)