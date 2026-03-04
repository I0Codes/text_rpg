from ui import UI


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
        choice_lower = choice.lower()
        
        # Обробка системної команди "вийти"
        if choice_lower == "вийти":
            if UI.confirm("Ви впевнені що хочете вийти з гри?"):
                self.is_running = False
                print("\nВи залишаєте гру...")
            return
        
        # Обробка дій локації
        self.current_location.handle_action(choice, self.player)
    
    def check_game_over(self):
        """Перевіряє чи гра завершена (персонаж загинув)"""
        if not self.player.is_alive():
            print("\n💀 Ваш персонаж загинув.")
            self.is_running = False
    
    def run(self):
        """Головний ігровий цикл"""
        print("\n🌲 Гра розпочалась!")
        print("Системні команди: вийти")
        
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
