from core import Game
from entities import Character
from world import Forest


def main():
    """Точка входу в гру"""
    # Створюємо персонажа
    player = Character(name="Герой", hp=100)
    
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
