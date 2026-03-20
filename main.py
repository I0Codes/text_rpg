from core import Game
from world import Forest
from ui.menus import MainMenu, CharacterCreationMenu


def main():
    """Точка входу в гру"""
    action = MainMenu.show()

    if action == "exit":
        print("Вихід з гри.")
        return

    if action == "load_game":
        print("Функція завантаження поки не реалізована.")
        return

    if action == "new_game":
        player = CharacterCreationMenu.show()
    else:
        player = CharacterCreationMenu.show()

    forest = Forest()
    game = Game(player, forest)
    game.run()


if __name__ == "__main__":
    main()
