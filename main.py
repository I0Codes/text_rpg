import random
from core import Game
from world import Forest
from world.events import get_random_event
from ui.menus import MainMenu, CharacterCreationMenu


def main():
    """Точка входу в гру"""
    while True:
        action = MainMenu.show()

        if action == "exit":
            print("Вихід з гри.")
            return

        if action == "load_game":
            print("Функція завантаження поки не реалізована.")
            continue

        player = CharacterCreationMenu.show()

        forest = Forest()
        game = Game(player, forest)
        game.run()


if __name__ == "__main__":
    main()
