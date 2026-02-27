from core import Game
from entities import Character, Enemy
from world import Forest

def main():
    """Точка входу в гру"""
    # Створюємо персонажа
    player = Character(name="Hero", hp=100)
    # демонстрація інвентарю
    from items import Item
    potion = Item(item_type="consumable", name="Зілля здоров'я", description="Відновлює 50 HP", weight=0.5, value=0, stackable=True, quantity=1)
    player.add_item(potion)
    player.inventory.show_inventory()

    # Створюємо початкову локацію
    forest = Forest()
    
    # Створюємо та запускаємо гру
    game = Game(player, forest)
    game.run()

# TODO: інтегрувати MainMenu для вибору "Нова гра" / "Завантажити гру"
# TODO: додати вибір класу персонажа (Warrior, Mage, Scout)
# TODO: додати можливість вводити ім'я персонажа

if __name__ == "__main__":
    main()
