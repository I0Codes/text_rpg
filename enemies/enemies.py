import random

class Enemy:
    def __init__(self, name, hp, attack, defense, level=1):
        self.name = name
        self.level = level
        self.hp = hp * level
        self.attack = attack * level
        self.defense = defense * level
        self.exp = 10 * level  
        # Нараховані очки досвіду

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        real_damage = max(0, damage - self.defense)
        self.hp -= real_damage
        return real_damage

    def deal_damage(self):
        return random.randint(self.attack - 2, self.attack + 2)

    def __str__(self):
        return f"{self.name} (HP: {self.hp})"
    
    def get_exp(self):
        return self.exp
    
    
class Goblin(Enemy):
    def __init__(self, level=1):
        super().__init__("Гоблін", hp=30, attack=8, defense=2, level=level)


class Orc(Enemy):
    def __init__(self, level=1):
        super().__init__("Орк", hp=50, attack=12, defense=4, level=level)


class Dragon(Enemy):
    def __init__(self, level=1):
        super().__init__("Дракон", hp=150, attack=25, defense=10, level=level)

    def deal_damage(self):
        # Шанс вогняної атаки
        if random.random() < 0.3:
            return random.randint(30, 45)
        return super().deal_damage()
    
    
class Troll(Enemy):
    def __init__(self, level=1):
        super().__init__("Троль", hp=80, attack=15, defense=6, level=level)

    def take_damage(self, damage):
        real_damage = super().take_damage(damage)
        # Регенерація: зцілює 10% від максимального здоров'я за хід, якщо живий
        if self.is_alive():
            self.hp = min(self.hp + int(0.1 * 80 * self.level), 80 * self.level)
        return real_damage
    
    
def create_enemy(level):
    if level < 3:
        return Goblin(level)
    elif level < 6:
        return Orc(level)
    elif level < 9:
        return Troll(level)
    else:
        return Dragon(level)