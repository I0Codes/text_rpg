import random

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