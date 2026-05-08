from kivy.app import App

from core import Game
from ui.kivy_ui import KivyUI
from ui.menus import MainMenu, CharacterCreationMenu
from world import Forest


def main():
    ui = KivyUI()

    def game_loop():
        menu = MainMenu(ui)
        char_menu = CharacterCreationMenu(ui)

        while True:
            action = menu.show()

            if action == "exit":
                ui.show_text("Вихід з гри.")
                App.get_running_app().stop()
                return

            if action == "load_game":
                ui.show_text("Функція завантаження поки не реалізована.")
                continue

            player = char_menu.show()
            forest = Forest()
            game = Game(player, forest, ui)
            game.run()

    ui.run(game_loop)


if __name__ == "__main__":
    main()
