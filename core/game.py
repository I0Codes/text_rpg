from entities.enemies import Enemy
from ui import UI, ProgressionUI
from ui.menus import InventoryMenu
from world.locations import Location

from .combat import Combat
from .game_engine import GameEngine


class Game:
    """Головний клас гри, керує ігровим циклом"""
    
    def __init__(self, player, start_location):
        """Ініціалізація гри
        
        Args:
            player: Об'єкт гравця (Character)
            start_location: Початкова локація
        """
        self.player = player
        self.current_location = start_location
        self.is_running = True
        self._combat = Combat(player)
    
    def show_status(self):
        """Виводить поточний статус гравця та локації"""
        UI.print_separator()
        status = f"Персонаж: {self.player.name}\n"
        status += f"Рівень: {self.player.level}\n"
        status += f"HP: {self.player.hp}/{self.player.max_hp}\n"
        
        # Інформація про досвід
        exp_summary = self.player.experience_manager.get_summary()
        progress = exp_summary['progress_percentage']
        status += f"Досвід: {exp_summary['total_experience']}/{exp_summary['experience_to_next_level']} ({progress:.1f}%)\n"

        totals = GameEngine.calculate_total_stats(self.player)
        status += f"Макс HP: {totals['max_hp']}  Crit: {totals['crit_chance']:.1%}  Dodge: {totals['dodge_chance']:.1%}\n"
        status += f"Фізичне ураження: {totals['physical_damage']:.1f}  Магічне ураження: {totals['magical_damage']:.1f}\n"
        status += f"Локація: {self.current_location.name}"
        
        UI.print_status(status)
        UI.print_separator()
    
    def show_actions(self):
        """Виводить доступні дії"""
        actions = self.current_location.get_actions()
        UI.print_actions(actions)
    
    def handle_action(self, choice):
        """Обробляє вибір гравця
        
        Args:
            choice: Введений гравцем вибір
        """
        choice = choice.strip()
        choice_lower = choice.lower()
        
        # Обробка системної команди "вийти"
        if choice_lower == "вийти":
            if UI.confirm("Ви впевнені що хочете вийти з гри?"):
                self.is_running = False
                print("\nВи залишаєте гру...")
            return 
        
        # Службові команди гравця
        if choice_lower in ["статус", "status", "листок", "sheet"]:
            ProgressionUI.display_character_sheet(self.player)
            return

        if choice_lower in ["атрибути", "attributes", "attribute"]:
            ProgressionUI.display_attribute_menu(self.player)
            return

        # Обробка дій локації (дослідження може повернути ворога або перейти на іншу локацію)
        result = self.current_location.handle_action(choice, self.player)

        if isinstance(result, Enemy):
            self._combat.run([result])
        elif isinstance(result, Location):
            self.current_location = result
        if choice_lower == "i":
            InventoryMenu.show(self.player)
            return

        if choice_lower == "s":
            self.show_status()
            return

            print(f"\n⇨ Ви перемістилися до {self.current_location.name}")

    def check_game_over(self):
        """Перевіряє чи гра завершена (персонаж загинув)"""
        if not self.player.is_alive():
            print("\n💀 Ваш персонаж загинув.")
            self.is_running = False
    
    def run(self):
        """Головний ігровий цикл"""
        print("\n🌲 Гра розпочалась!")
        print("Системні команди: вийти, статус, листок, атрибути")
        
        while self.is_running:
            self.show_status()
            self.show_actions()
            
            choice = input("\nВаш вибір: ")
            self.handle_action(choice)
            self.check_game_over()
        
        print("\n🎮 Гру завершено.")

# TODO: додати команду "допомога" яка показує пояснення гри
# TODO: додати клас MainMenu для вибору "Нова гра" / "Завантажити гру"
# TODO: додати систему автозбереження гри в JSON файли (чекпойнти)
# TODO: додати метод save_game() для збереження стану гри
# TODO: додати метод load_game() для завантаження збереженої гри
