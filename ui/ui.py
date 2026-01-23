class UI:
    """Клас для інкапсуляції виводу в консоль"""
    
    @staticmethod
    def print_separator():
        """Виводить роздільник"""
        print("=" * 50)
    
    @staticmethod
    def print_status(text):
        """Виводить статус гравця"""
        print(text)
    
    @staticmethod
    def print_actions(actions):
        """Виводить доступні дії"""
        print("\nДоступні дії:")
        for key, description in actions.items():
            print(f"  {key} — {description}")
    
    @staticmethod
    def confirm(question):
        """Запитує підтвердження від користувача
        
        Args:
            question: Текст питання
            
        Returns:
            True якщо користувач підтвердив (так/т/yes/y), False в іншому випадку
        """
        answer = input(f"{question} (Так/Ні): ").lower()
        return answer in ["так", "т", "yes", "y"]

# TODO: замінитиprint() на бібліотеку rich для кращого форматування
