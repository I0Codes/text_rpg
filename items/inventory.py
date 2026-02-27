from __future__ import annotations

from typing import List, Any

from .item import Item


class Inventory:
    """Сховище предметів персонажа.

    Attributes:
        items (list[Item]): перелік об'єктів у інвентарі
        max_capacity (int): максимальна кількість слотів
    """

    def __init__(self, max_capacity: int = 20) -> None:
        self.items: List[Item] = []
        self.max_capacity: int = max_capacity

    def add_item(self, item: Item) -> bool:
        """Додає предмет до інвентарю, якщо є вільне місце.

        Якщо предмет стекується і вже є в інвентарі, просто додає кількість.
        Повертає True якщо предмет успішно додано, False інакше.
        """
        # по кількості слотів
        if len(self.items) >= self.max_capacity:
            print(f"Інвентар повний ({self.max_capacity} слотів)!")
            return False

        if item.stackable:
            for existing in self.items:
                if existing.name == item.name:
                    existing.quantity += item.quantity
                    return True

        # якщо не стекується або не знайдено стеканий екземпляр
        self.items.append(item)
        return True

    def remove_item(self, item: Item) -> bool:
        """Видаляє предмет із інвентарю.

        Якщо предмет стекується, зменшує кількість або видаляє повністю.
        Повертає True якщо предмет було знайдено й видалено, False якщо ні.
        """
        if item not in self.items:
            return False

        if item.stackable and item.quantity > 1:
            item.quantity -= 1
        else:
            self.items.remove(item)
        return True

    def use_item(self, item: Item, character: Any) -> bool:
        """Спробувати використати предмет на персонажі.

        Якщо метод ``Item.use`` повертає True, і предмет споживний,
        то він автоматично зникає з інвентарю або зменшується кількість.
        Повертає результат виклику ``item.use``.
        """
        if item not in self.items:
            print(f"У інвентарі немає {item.name}.")
            return False

        used = item.use(character)
        if used:
            # припускаємо, що всі предмети, які використовуються, витрачаються
            self.remove_item(item)
        return used

    def get_items_by_type(self, item_type: str) -> List[Item]:
        """Повертає перелік предметів указаного типу."""
        return [i for i in self.items if i.item_type == item_type]

    def show_inventory(self) -> None:
        """Виводить список усіх предметів у інвентарі."""
        if not self.items:
            print("Інвентар порожній.")
            return

        print("---- Інвентар ----")
        for idx, itm in enumerate(self.items, start=1):
            qty = f" x{itm.quantity}" if itm.stackable else ""
            print(f"{idx}. {itm.name}{qty} ({itm.item_type})")
        print("------------------")

    def __str__(self) -> str:
        return f"Inventory({len(self.items)}/{self.max_capacity})"