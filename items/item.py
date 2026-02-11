class Item:
    """Базовий клас предмета (plain class)

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
        print(f"Ви намагаєтеся використати {self.name}, але нічого не відбувається.")
        return False

    def __str__(self):
        return f"Item(name={self.name!r}, qty={self.quantity})"
