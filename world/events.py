import random
import sys
sys.path.append('d:\\9-B\\text_rpg')
from dice_system import DiceSystem

class Event:
    def __init__(self, name, description, event_type, chance):
        self.name = name
        self.description = description
        self.event_type = event_type  # "TREASURE", "COMBAT", "MERCHANT"
        self.chance = chance  # від 0.0 до 1.0
    
    def trigger(self, player):
        """Показати опис події"""
        print(f"⚡ Подія: {self.name}")
        print(f"📖 {self.description}")
        return self.resolve(player)
    
    def resolve(self, player):
        """Виконати подію та повернути результат"""
        pass


class TreasureChestEvent(Event):
    def __init__(self):
        super().__init__(
            name="Скриня зі скарбами",
            description="Ви знайшли таємну скриню!",
            event_type="TREASURE",
            chance=0.15
        )
    
    def resolve(self, player):
        """Випадковий лут: золото, зілля, зброю або нічого"""
        loot = random.choice(["золото", "зілля", "зброю", "нічого"])
        result = f"У скрині ви знайшли: {loot}"
        print(result)
        return result


class RestSiteEvent(Event):
    def __init__(self):
        super().__init__(
            name="Місце для відпочинку",
            description="Ви знайшли безпечне місце для відпочинку.",
            event_type="REST",
            chance=0.30
        )
    
    def resolve(self, player):
        """Відновити HP та stamina на випадкову кількість"""
        hp_restore = random.randint(20, 40)
        stamina_restore = random.randint(30, 50)
        result = f"Відновлено HP: +{hp_restore}, Stamina: +{stamina_restore}"
        print(result)
        return result


class MerchantEvent(Event):
    def __init__(self):
        super().__init__(
            name="Торговець",
            description="На вашому шляху з'явився торговець!",
            event_type="MERCHANT",
            chance=0.20
        )
        self.goods = {
            "Зілля здоров'я": 50,
            "Еліксир сили": 100,
            "Меч": 150,
            "Щит": 120,
            "Броня": 200
        }
    
    def resolve(self, player):
        """Показати меню товарів"""
        print("\n=== ТОВАРИ ТОРГОВЦЯ ===")
        for item, price in self.goods.items():
            print(f"{item}: {price} золота")
        result = "Торговець чекає вашого вибору."
        print(result)
        return result


class AmbushEvent(Event):
    def __init__(self):
        super().__init__(
            name="Засідка",
            description="Раптово вас атакують!",
            event_type="COMBAT",
            chance=0.25
        )
    
    def resolve(self, player):
        """Випадкова кількість ворогів та шанс втекти"""
        enemies_count = random.randint(1, 3)
        escape_chance = random.randint(30, 80)  # Шанс втекти від 30% до 80%
        escaped = random.random() * 100 < escape_chance
        
        if escaped:
            result = f"Вам вдалося втекти від {enemies_count} ворогів!"
        else:
            result = f"Ви потрапили в бій з {enemies_count} ворогами! (Шанс втечі був {escape_chance}%)"
        
        print(result)
        return result


class ChoiceEvent(Event):
    """Подія з варіантами вибору"""
    def __init__(self, name, description, chance):
        super().__init__(name, description, "CHOICE", chance)
        self.choices = []  # Список варіантів
    
    def add_choice(self, text, action_function):
        """Додати варіант вибору"""
        self.choices.append((text, action_function))
    
    def show_choices(self):
        """Показати всі варіанти гравцю"""
        print("\n=== ВАРІАНТИ ВИБОРУ ===")
        for i, (text, _) in enumerate(self.choices, 1):
            print(f"{i}. {text}")
    
    def resolve(self, player, choice_index):
        """Виконати обраний варіант"""
        if 1 <= choice_index <= len(self.choices):
            _, action = self.choices[choice_index - 1]
            return action(player)
        else:
            return "Невірний вибір."


class SwampStreamEvent(ChoiceEvent):
    def __init__(self):
        super().__init__(
            name="Болотний потічок",
            description="Перед вами каламутний потічок. Як перейти?",
            chance=0.30
        )
        self.add_choice("Перестрибнути (перевірка Ловкості)", self.jump_over)
        self.add_choice("Обійти довкола", self.go_around)
        self.add_choice("Обережно перейти", self.cross_carefully)
    
    def jump_over(self, player):
        if DiceSystem.attribute_check(player, "dexterity", 4):
            result = "Ви успішно перестрибнули! 0 шкоди."
        else:
            player.hp -= 15
            result = "Ви послизнулися! -15 HP."
        print(result)
        return result
    
    def go_around(self, player):
        player.stamina -= 20
        result = "Ви обійшли довкола. -20 stamina."
        print(result)
        return result
    
    def cross_carefully(self, player):
        player.hp -= 8
        result = "Ви обережно перейшли. -8 HP."
        print(result)
        return result


class CliffClimbEvent(ChoiceEvent):
    def __init__(self):
        super().__init__(
            name="Крутий схил",
            description="Попереду крутий схил. Як подолати?",
            chance=0.25
        )
        self.add_choice("Залізти (перевірка Сили та Ловкості)", self.climb)
        self.add_choice("Знайти обхідний шлях (перевірка Інтелекту)", self.find_path)
        self.add_choice("Пропустити", self.skip)
    
    def climb(self, player):
        str_success = DiceSystem.attribute_check(player, "strength", 4)
        dex_success = DiceSystem.attribute_check(player, "dexterity", 4)
        if str_success and dex_success:
            result = "Ви успішно залізли і знайшли скарб!"
        elif str_success or dex_success:
            player.hp -= 10
            result = "Ви залізли, але отримали поранення. -10 HP."
        else:
            player.hp -= 20
            result = "Ви впали! -20 HP."
        print(result)
        return result
    
    def find_path(self, player):
        if DiceSystem.attribute_check(player, "intelligence", 4):
            result = "Ви знайшли безпечний обхідний шлях."
        else:
            result = "Ви не змогли знайти шлях."
        print(result)
        return result
    
    def skip(self, player):
        result = "Ви вирішили пропустити схил. Нічого не сталося."
        print(result)
        return result


class MysteriousChestEvent(ChoiceEvent):
    def __init__(self):
        super().__init__(
            name="Підозріла скриня",
            description="Ви знайшли підозрілу скриню з пасткою. Що робити?",
            chance=0.20
        )
        self.add_choice("Відкрити обережно (Ловкість + Удача)", self.open_carefully)
        self.add_choice("Відкрити силою (перевірка Сили)", self.open_force)
        self.add_choice("Спочатку оглянути (перевірка Інтелекту)", self.inspect)
        self.add_choice("Залишити скриню", self.leave)
    
    def open_carefully(self, player):
        dex_success = DiceSystem.attribute_check(player, "dexterity", 4)
        luck_success = DiceSystem.attribute_check(player, "luck", 4)
        if dex_success and luck_success:
            gold = random.randint(40, 70)
            player.gold += gold
            result = f"Ви уникнули пастки і знайшли {gold} золота!"
        elif dex_success:
            player.hp -= 10
            result = "Ви частково уникнули пастки, але отримали шкоду. -10 HP."
        else:
            player.hp -= 25
            result = "Пастка спрацювала! -25 HP."
        print(result)
        return result
    
    def open_force(self, player):
        if DiceSystem.attribute_check(player, "strength", 4):
            gold = random.randint(15, 30)
            player.gold += gold
            result = f"Ви зламали замок і знайшли {gold} золота!"
        else:
            player.stamina -= 15
            result = "Ви не змогли відкрити. -15 stamina."
        print(result)
        return result
    
    def inspect(self, player):
        if DiceSystem.attribute_check(player, "intelligence", 4):
            gold = random.randint(40, 70)
            player.gold += gold
            result = f"Ви вимкнули пастку і знайшли {gold} золота!"
        else:
            result = "Ви нічого не помітили."
        print(result)
        return result
    
    def leave(self, player):
        result = "Ви залишили скриню. Нічого не сталося."
        print(result)
        return result

def get_random_event():
    events = [
        TreasureChestEvent(),
        RestSiteEvent(),
        MerchantEvent(),
        AmbushEvent(),
        SwampStreamEvent(),
        CliffClimbEvent(),
        MysteriousChestEvent()
    ]
    total_chance = sum(event.chance for event in events)
    rand = random.uniform(0, total_chance)
    cumulative = 0
    for event in events:
        cumulative += event.chance
        if rand <= cumulative:
            return event
    return None