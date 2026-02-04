from core import Game
from entities import Character
from world import Forest
from enemies.enemies import Enemy, Goblin, Orc, Dragon, Troll, create_enemy

def main():
    """Точка входу в гру"""
    # Створюємо персонажа
    player = Character(name="Hero", hp=100)
    
    # Створюємо початкову локацію
    forest = Forest()

    # Створюємо ворогів
    goblin = create_enemy(1)  # Рівень 1 для гобліна
    orc = create_enemy(3)     # Рівень 3 для орка
    dragon = create_enemy(10) # Рівень 10 для дракона
    
    # Створюємо та запускаємо гру
    game = Game(player, forest)
    game.run()

# TODO: інтегрувати MainMenu для вибору "Нова гра" / "Завантажити гру"
# TODO: додати вибір класу персонажа (Warrior, Mage, Scout)
# TODO: додати можливість вводити ім'я персонажа

if __name__ == "__main__":
    main()
