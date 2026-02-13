import random

from .characters import Character


class Enemy(Character):
    def __init__(self, name, hp, attack, defense, level=1, enemy_type="normal", reward_gold=None):
        # базові бойові характеристики
        self.name = name
        self.level = level
        self.max_hp = hp * level
        self.hp = self.max_hp
        self.attack = attack * level
        self.defense = defense * level

        # тип ворога та нагороди
        self.enemy_type = enemy_type
        self.reward_exp = 10 * level
        # якщо нагорода за золото не задана — обчислюємо базово
        self.reward_gold = reward_gold if reward_gold is not None else 5 * level

        # додаткові атрибути (наприклад, спритність/сила)
        self.attributes = {
            "strength": int(self.attack / max(1, level)),
            "defense": int(self.defense / max(1, level)),
            "agility": 5 * level,
        }

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        real_damage = max(0, damage - self.defense)
        self.hp -= real_damage
        return real_damage

    def deal_damage(self):
        return random.randint(max(0, self.attack - 2), self.attack + 2)

    def __str__(self):
        return f"{self.name} (HP: {self.hp}/{self.max_hp})"

    # Нагорода за перемогу
    def get_loot(self):
        return {"exp": self.reward_exp, "gold": self.reward_gold}

    # Простий AI: поки що завжди атакує
    def select_action(self, battlefield=None):
        return "attack"


class Goblin(Enemy):
    def __init__(self, level=1):
        super().__init__("Goblin", hp=30, attack=8, defense=2, level=level, enemy_type="goblin", reward_gold=3 * level)
        self.attributes.update({"agility": 8 * level, "strength": 4 * level})


class Wolf(Enemy):
    def __init__(self, level=1):
        # швидкий ворог з високою спритністю
        super().__init__("Wolf", hp=25, attack=10, defense=3, level=level, enemy_type="wolf", reward_gold=4 * level)
        self.attributes.update({"agility": 12 * level, "strength": 6 * level})


class Bandit(Enemy):
    def __init__(self, level=1):
        # збалансований ворог
        super().__init__("Bandit", hp=40, attack=12, defense=4, level=level, enemy_type="bandit", reward_gold=6 * level)
        self.attributes.update({"agility": 7 * level, "strength": 9 * level})


# Збережено старі типи як більш складні вороги (вони автоматично працюватимуть з новим Enemy)

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