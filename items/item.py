class Item:
    """Базовий клас предмета

    Поля:
        item_type (str): тип предмета (наприклад, "weapon", "consumable", "armor")
        name (str): ім'я предмета
        description (str): опис
        weight (float): вага предмета
        value (int): вартість/корисність
        stackable (bool): чи можна стекувати
        quantity (int): кількість (для стекованих)
    """


    def __init__(self, item_type, name, description="", weight=0.0, value=0, stackable=False, quantity=1):
        self.item_type = item_type
        self.name = name
        self.description = description
        self.weight = weight
        self.value = value
        self.stackable = stackable
        self.quantity = quantity

    def use(self, user):
        """Спроба використати предмет на користувача.

        Повертає True якщо предмет використано, False за замовчуванням.
        """
        if self.item_type == "consumable":
            heal_amount = getattr(self, "value", 0) or 10
            if hasattr(user, "heal"):
                user.heal(heal_amount)
            print(f"Ви використовуєте {self.name}, відновлено {heal_amount} HP.")
            return True

        print(f"Ви намагаєтеся використати {self.name}, але нічого не відбувається.")
        return False

    def __str__(self):
        return f"Item(name={self.name!r}, qty={self.quantity})"


class Weapon(Item):
    """Клас зброї"""

    def __init__(self, name, description, damage, damage_type, value, required_strength=0, weight=0.0):
        if damage_type not in ("PHYSICAL", "MAGICAL"):
            raise ValueError("damage_type must be 'PHYSICAL' or 'MAGICAL'")

        super().__init__("weapon", name, description=description, weight=weight, value=value)
        self.damage = damage
        self.damage_type = damage_type
        self.required_strength = required_strength

    def can_equip(self, character):
        attrs = getattr(character, "attributes", None)
        if attrs is None or not hasattr(attrs, "strength"):
            return False
        return attrs.strength >= self.required_strength


class Dagger(Weapon):
    """Клас кинджалів"""
    pass


class Sword(Weapon):
    """Клас мечів"""
    pass


class Axe(Weapon):
    """Клас сокир"""
    pass


class Club(Weapon):
    """Клас булав"""
    pass


class Staff(Weapon):
    """Клас посохів"""
    pass


class RustyDagger(Dagger):
    def __init__(self):
        super().__init__(
            name="Rusty Dagger",
            description="Початкова кинджалоподібна зброя.",
            damage=5,
            damage_type="PHYSICAL",
            value=10,
            required_strength=0,
            weight=1.0,
        )


class IronSword(Sword):
    def __init__(self):
        super().__init__(
            name="Iron Sword",
            description="Базовий меч з заліза.",
            damage=15,
            damage_type="PHYSICAL",
            value=50,
            required_strength=5,
            weight=4.0,
        )


class SteelAxe(Axe):
    def __init__(self):
        super().__init__(
            name="Steel Axe",
            description="Важка сокира, що наносить багато шкоди.",
            damage=25,
            damage_type="PHYSICAL",
            value=90,
            required_strength=8,
            weight=6.0,
        )


class WoodenStaff(Staff):
    def __init__(self):
        super().__init__(
            name="Wooden Staff",
            description="Магічний посох для початківців.",
            damage=20,
            damage_type="MAGICAL",
            value=45,
            required_strength=0,
            weight=3.0,
        )
