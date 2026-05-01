class ProgressionUI:
    """UI клас для відображення прогресу персонажа"""
    
    # ANSI кольори
    COLORS = {
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'DIM': '\033[2m',
        'GOLD': '\033[93m',
        'GREEN': '\033[92m',
        'CYAN': '\033[96m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'RED': '\033[91m',
        'WHITE': '\033[97m',
        'GREY': '\033[90m',
    }
    
    # Символи для дизайну
    SYMBOLS = {
        'STAR': '⭐',
        'CROWN': '👑',
        'FLAME': '🔥',
        'ZAPS': '✨',
        'CHECK': '✓',
        'CROSS': '✗',
        'ARROW': '→',
        'EMPTY_BOX': '☐',
        'FILLED_BOX': '☑',
        'HEART': '❤',
    }
    
    @staticmethod
    def _print_colored(text, color, bold=False):
        """Вивести текст з кольором"""
        style = ProgressionUI.COLORS['BOLD'] if bold else ''
        print(f"{style}{color}{text}{ProgressionUI.COLORS['RESET']}")
    
    @staticmethod
    def _print_frame_top(width=60):
        """Вивести верхню рамку"""
        print(ProgressionUI.COLORS['CYAN'] + '╔' + '═' * (width - 2) + '╗' + ProgressionUI.COLORS['RESET'])
    
    @staticmethod
    def _print_frame_bottom(width=60):
        """Вивести нижню рамку"""
        print(ProgressionUI.COLORS['CYAN'] + '╚' + '═' * (width - 2) + '╝' + ProgressionUI.COLORS['RESET'])
    
    @staticmethod
    def _print_frame_line(text, width=60):
        """Вивести лінію в рамці"""
        padding = (width - 2 - len(text)) // 2
        line = '║' + ' ' * padding + text + ' ' * (width - 2 - padding - len(text)) + '║'
        print(ProgressionUI.COLORS['CYAN'] + line + ProgressionUI.COLORS['RESET'])
    
    @staticmethod
    def _print_progress_bar(current, maximum, width=40, label=""):
        """Вивести прогрес-бар"""
        if maximum == 0:
            percentage = 100
        else:
            percentage = (current / maximum) * 100
        
        filled = int((percentage / 100) * width)
        empty = width - filled
        
        bar = '█' * filled + '░' * empty
        
        if percentage >= 75:
            color = ProgressionUI.COLORS['GREEN']
        elif percentage >= 50:
            color = ProgressionUI.COLORS['YELLOW']
        elif percentage >= 25:
            color = ProgressionUI.COLORS['GOLD']
        else:
            color = ProgressionUI.COLORS['RED']
        
        label_str = f"{label}: " if label else ""
        print(f"{label_str}{color}[{bar}]{ProgressionUI.COLORS['RESET']} {percentage:.1f}%")
    
    @staticmethod
    def display_level_up(character, new_level):
        """
        Красиве повідомлення про підняття рівня:
        - Анімація або рамка
        - Новий рівень
        - Отримані очки
        - Класові бонуси
        - Наступний milestone
        """
        print("\n")
        ProgressionUI._print_frame_top(60)
        
        # Заголовок
        ProgressionUI._print_frame_line("", 60)
        ProgressionUI._print_frame_line(f"{ProgressionUI.SYMBOLS['CROWN']} ПІДНЯТТЯ РІВНЯ {ProgressionUI.SYMBOLS['CROWN']}", 60)
        ProgressionUI._print_frame_line("", 60)
        
        # Основна інформація
        ProgressionUI._print_frame_line(f"{character.name}", 60)
        ProgressionUI._print_frame_line("", 60)
        
        # Новий рівень
        level_text = f"Рівень: {new_level - 1} → {new_level}"
        print(ProgressionUI.COLORS['CYAN'] + "║ " + level_text.center(56) + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Отримані очки
        available_points = 3  # За замовчуванням 3 очки за рівень
        points_text = f"{ProgressionUI.SYMBOLS['ZAPS']} +{available_points} очок атрибутів"
        print(ProgressionUI.COLORS['GOLD'] + "║ " + points_text.center(56) + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Класові бонуси
        class_bonus_text = "Касові бонуси застосовані!"
        print(ProgressionUI.COLORS['MAGENTA'] + "║ " + class_bonus_text.center(56) + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Наступний milestone
        exp_summary = character.experience_manager.get_summary()
        next_milestone_text = f"До рівня {new_level + 1}: {exp_summary['experience_to_next_level']} досвіду"
        print(ProgressionUI.COLORS['BLUE'] + "║ " + next_milestone_text.center(56) + " ║" + ProgressionUI.COLORS['RESET'])
        
        print(ProgressionUI.COLORS['CYAN'] + "║" + " " * 58 + "║" + ProgressionUI.COLORS['RESET'])
        
        ProgressionUI._print_frame_bottom(60)
        print()
    
    @staticmethod
    def display_character_sheet(character):
        """
        Повна інформація про персонажа:
        - Рівень та досвід
        - Прогрес-бар до наступного рівня
        - Всі атрибути з бонусами
        - Доступні очки
        - Навички
        - Екіпірування
        """
        print("\n")
        ProgressionUI._print_frame_top(70)
        
        # Заголовок
        ProgressionUI._print_frame_line(f"{ProgressionUI.SYMBOLS['CROWN']} {character.name.upper()} {ProgressionUI.SYMBOLS['CROWN']}", 70)
        ProgressionUI._print_frame_line("", 70)
        
        # Базова інформація
        print(ProgressionUI.COLORS['CYAN'] + "║ " + f"Рівень: {character.level}".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Здоров'я та стан
        print(ProgressionUI.COLORS['RED'] + "║ " + f"Здоров'я: {character.hp}/{character.max_hp}".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        print(ProgressionUI.COLORS['BLUE'] + "║ " + f"Мана: {character.mana}/{character.max_mana}".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        print(ProgressionUI.COLORS['YELLOW'] + "║ " + f"Витривалість: {character.stamina}/{character.max_stamina}".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Прогрес-бар досвіду
        exp_summary = character.experience_manager.get_summary()
        print(ProgressionUI.COLORS['CYAN'] + "║ " + ProgressionUI.COLORS['RESET'])
        print(ProgressionUI.COLORS['CYAN'] + "║ " + f"Досвід: {character.experience_manager.total_experience}/{character.experience_manager.experience_to_next_level}".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Прогрес бар в рамці
        print(ProgressionUI.COLORS['CYAN'] + "║ " + ProgressionUI.COLORS['RESET'], end='')
        filled = int((exp_summary['progress_percentage'] / 100) * 50)
        bar = '█' * filled + '░' * (50 - filled)
        print(ProgressionUI.COLORS['GOLD'] + f"[{bar}]" + ProgressionUI.COLORS['RESET'], end='')
        print(f" {exp_summary['progress_percentage']:.1f}%" + ProgressionUI.COLORS['CYAN'] + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Атрибути
        print(ProgressionUI.COLORS['CYAN'] + "║" + " " * 68 + "║" + ProgressionUI.COLORS['RESET'])
        print(ProgressionUI.COLORS['MAGENTA'] + "║ " + "АТРИБУТИ".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        
        attrs = character.attributes
        print(ProgressionUI.COLORS['CYAN'] + "║ " + ProgressionUI.COLORS['RESET'], end='')
        print(f"  Сила: {attrs.strength:<5} (+{attrs.get_physical_damage_bonus():.1f} шкода, +{attrs.get_hp_bonus():.1f} HP)")
        
        print(ProgressionUI.COLORS['CYAN'] + "║ " + ProgressionUI.COLORS['RESET'], end='')
        print(f"  Інтелект: {attrs.intelligence:<5} (+{attrs.get_magic_damage_bonus():.1f} магія, +{attrs.get_mana_bonus():.1f} мана)")
        
        print(ProgressionUI.COLORS['CYAN'] + "║ " + ProgressionUI.COLORS['RESET'], end='')
        print(f"  Ловкість: {attrs.agility:<5} (Крит: {attrs.get_crit_chance():.1%}, Ухил: {attrs.get_dodge_chance():.1%})")
        
        print(ProgressionUI.COLORS['CYAN'] + "║ " + ProgressionUI.COLORS['RESET'], end='')
        print(f"  Удача: {attrs.luck:<5} (Бонус: {LUCK_BONUS_MULTIPLIER * attrs.luck:.1%})")
        
        # Товари та інвентар
        print(ProgressionUI.COLORS['CYAN'] + "║" + " " * 68 + "║" + ProgressionUI.COLORS['RESET'])
        print(ProgressionUI.COLORS['YELLOW'] + "║ " + f"Золото: {character.gold}".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        
        # Інвентар
        items_count = len(character.inventory.items)
        capacity = character.inventory.max_capacity
        print(ProgressionUI.COLORS['CYAN'] + "║ " + f"Інвентар: {items_count}/{capacity}".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        
        ProgressionUI._print_frame_bottom(70)
        print()
    
    @staticmethod
    def display_attribute_menu(character):
        """
        Меню розподілу очок атрибутів:
        - Поточні значення
        - Доступні очки
        - Що дасть +1 до кожного атрибуту
        - Можливість підтвердити/скасувати
        """
        available_points = 5  # Приклад
        
        print("\n")
        ProgressionUI._print_frame_top(70)
        
        # Заголовок
        ProgressionUI._print_frame_line("РОЗПОДІЛ ОЧОК АТРИБУТІВ", 70)
        ProgressionUI._print_frame_line("", 70)
        
        # Доступні очки
        points_text = f"Доступні очки: {available_points}"
        print(ProgressionUI.COLORS['GOLD'] + "║ " + points_text.ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        print(ProgressionUI.COLORS['CYAN'] + "║" + " " * 68 + "║" + ProgressionUI.COLORS['RESET'])
        
        # Атрибути з описаннями
        attrs = character.attributes
        
        attributes_info = [
            {
                'name': 'Сила (Strength)',
                'current': attrs.strength,
                'bonus': '+1.5 до фізичної шкоди, +2 до HP'
            },
            {
                'name': 'Інтелект (Intelligence)',
                'current': attrs.intelligence,
                'bonus': '+2 до магічної шкоди, +2 до мани'
            },
            {
                'name': 'Ловкість (Agility)',
                'current': attrs.agility,
                'bonus': '+0.5% до крита, +1% до ухилення'
            },
            {
                'name': 'Удача (Luck)',
                'current': attrs.luck,
                'bonus': '+0.3% до крита та ухилення'
            }
        ]
        
        for i, attr_info in enumerate(attributes_info, 1):
            print(ProgressionUI.COLORS['BLUE'] + f"║ {i}. {attr_info['name']:<40} ".ljust(68) + "║" + ProgressionUI.COLORS['RESET'])
            print(ProgressionUI.COLORS['CYAN'] + f"║    Поточно: {attr_info['current']}".ljust(68) + "║" + ProgressionUI.COLORS['RESET'])
            print(ProgressionUI.COLORS['GREEN'] + f"║    Бонус: {attr_info['bonus']}".ljust(68) + "║" + ProgressionUI.COLORS['RESET'])
            print(ProgressionUI.COLORS['CYAN'] + "║" + " " * 68 + "║" + ProgressionUI.COLORS['RESET'])
        
        # Дії
        print(ProgressionUI.COLORS['CYAN'] + "║" + " " * 68 + "║" + ProgressionUI.COLORS['RESET'])
        print(ProgressionUI.COLORS['YELLOW'] + "║ " + "Введіть номер атрибута (1-4) або 0 для скасування".ljust(66) + " ║" + ProgressionUI.COLORS['RESET'])
        
        ProgressionUI._print_frame_bottom(70)
        print()
    
    @staticmethod
    def display_experience_gain(amount, source, progress_percent):
        """Показати отримання досвіду з прогрес-баром"""
        print(ProgressionUI.COLORS['GOLD'] + f"\n✨ +{amount} досвіду від {source}!" + ProgressionUI.COLORS['RESET'])
        
        filled = int((progress_percent / 100) * 40)
        bar = '█' * filled + '░' * (40 - filled)
        
        if progress_percent >= 75:
            color = ProgressionUI.COLORS['GREEN']
        elif progress_percent >= 50:
            color = ProgressionUI.COLORS['YELLOW']
        elif progress_percent >= 25:
            color = ProgressionUI.COLORS['GOLD']
        else:
            color = ProgressionUI.COLORS['CYAN']
        
        print(f"Прогрес: {color}[{bar}]{ProgressionUI.COLORS['RESET']} {progress_percent:.1f}%\n")


# Імпорт для констант, якщо потрібно
try:
    from config.settings import LUCK_BONUS_MULTIPLIER
except ImportError:
    LUCK_BONUS_MULTIPLIER = 0.003
    