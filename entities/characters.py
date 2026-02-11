"""Класи персонажів для текстової РПГ"""

from typing import Dict, List, Optional
import random


class Character:
    """Базовий клас персонажа.

    Підтримує базові атрибути (HP, рівень, досвід, статистики), простий інвентар,
    методи бою, отримання завданої шкоди, лікування й підняття рівня.
    """

    def __init__(
        self,
        name: str,
        hp: Optional[int] = None,
        max_hp: Optional[int] = None,
        level: int = 1,
        xp: int = 0,
        strength: int = 5,
        dexterity: int = 5,
        intelligence: int = 5,
        defense: int = 0,
        luck: int = 0,
        stamina: int = 0,
    ):
        self.name = name
        self.level = level
        self.xp = xp
        self.stats: Dict[str, int] = {
            "strength": strength,
            "dexterity": dexterity,
            "intelligence": intelligence,
            "defense": defense,
            "luck": luck,
            "stamina": stamina,
        }

        # Розрахунок максимального HP якщо не задано явно
        if max_hp is None:
            self.max_hp = hp if hp is not None else 50 + self.stats["strength"] * 5 + self.level * 5
        else:
            self.max_hp = max_hp

        # Поточне HP встановлюємо на max або на передане значення
        self.hp = self.max_hp if hp is None else min(hp, self.max_hp)

        # Інвентар простий - список рядків (можна розширити до об'єктів Item)
        self.inventory: List[str] = []

        # Екіпірування: прості слоти для прикладу
        self.equipment: Dict[str, Optional[str]] = {"weapon": None, "armor": None}
    def is_alive(self) -> bool:
        """Чи персонаж живий"""
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        """Наносить персонажу шкоду з урахуванням його захисту та шансом ухилення.

        Повертає фактично отриману шкоду.
        """
        # Шанс ухилення залежить від dexterity + половини luck (у відсотках)
        dodge_base = self.stats.get("dexterity", 0)
        dodge_luck = self.stats.get("luck", 0) // 2
        dodge_chance = min(50, dodge_base + dodge_luck)
        if random.randint(1, 100) <= dodge_chance:
            # Ухилилися — не отримали шкоди
            return 0

        effective = max(0, amount - self.stats.get("defense", 0))
        self.hp -= effective
        if self.hp < 0:
            self.hp = 0
        return effective

    def heal(self, amount: int) -> int:
        """Лікує персонажа на вказану кількість HP. Повертає поточне HP."""
        if amount <= 0:
            return self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp

    def roll_luck(self, bonus_percent: int = 0) -> bool:
        """Перевірка удачі: повертає True якщо випадок пройшов.

        bonus_percent: додатковий відсоток до шансу, корисно для ефектів.
        """
        total = self.stats.get("luck", 0) + bonus_percent
        roll = random.randint(1, 100)
        return roll <= total

    def get_luck(self) -> int:
        """Повертає значення удачі персонажа"""
        return self.stats.get("luck", 0)

    def base_damage(self) -> int:
        """Базова формула для обчислення завданої шкоди (без випадкових ефектів)."""
        return max(1, self.stats.get("strength", 1) * 2)

    def attack(self, target: "Character") -> Dict[str, int]:
        """Атакує ціль і повертає інформацію про атаку.

        Повертає словник з полями: damage (фактична шкода), raw (початкова шкода до захисту).
        """
        # Невелика випадкова модифікація
        variance = random.randint(-2, 2)
        raw = max(0, self.base_damage() + variance)

        # Простий бонус залежно від зброї (можна ускладнити)
        weapon_bonus = 0
        if self.equipment.get("weapon"):
            # приклад: "Меч (+3)" — парсити можна пізніше, зараз фіксовано
            weapon_bonus = 3

        raw += weapon_bonus
        damage = target.take_damage(raw)
        return {"raw": raw, "damage": damage}

    def xp_to_next_level(self) -> int:
        return 100 * self.level

    def gain_xp(self, amount: int) -> None:
        """Нараховує досвід і піднімає рівень при потребі."""
        if amount <= 0:
            return
        self.xp += amount
        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            self.level_up()

    def level_up(self) -> None:
        """Піднімає рівень персонажа, збільшує характеристики та HP."""
        self.level += 1
        # Просте зростання статів при піднятті рівня
        self.stats["strength"] += 1
        self.stats["dexterity"] += 1
        self.stats["intelligence"] += 1
        self.stats["defense"] += 1
        self.stats["luck"] = self.stats.get("luck", 0) + 1

        # Збільшуємо max HP і лікуємо персонажа на частину нового максимуму
        self.max_hp += 10
        self.hp = min(self.max_hp, self.hp + 10)

    # Інвентарні операції
    def add_item(self, item: str) -> None:
        self.inventory.append(item)

    def remove_item(self, item: str) -> bool:
        try:
            self.inventory.remove(item)
            return True
        except ValueError:
            return False

    def equip(self, slot: str, item: Optional[str]) -> None:
        """Екіпірує або знімає предмет у слоті (weapon/armor)."""
        if slot not in self.equipment:
            raise ValueError("Невідомий слот екіпірування")
        self.equipment[slot] = item

    def to_dict(self) -> Dict:
        """Серилізує стан персонажа в словник для збереження"""
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "stats": dict(self.stats),
            "inventory": list(self.inventory),
            "equipment": dict(self.equipment),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Character":
        return cls(
            name=data.get("name", "Невідоме"),
            hp=data.get("hp"),
            max_hp=data.get("max_hp"),
            level=data.get("level", 1),
            xp=data.get("xp", 0),
            strength=data.get("stats", {}).get("strength", 5),
            dexterity=data.get("stats", {}).get("dexterity", 5),
            intelligence=data.get("stats", {}).get("intelligence", 5),
            defense=data.get("stats", {}).get("defense", 0),
            luck=data.get("stats", {}).get("luck", 0),
        )

    def __str__(self) -> str:
        return f"{self.name} (рівень {self.level}) HP: {self.hp}/{self.max_hp}"


# Класи-нащадки з початковими налаштуваннями
class Warrior(Character):
    def __init__(self, name: str):
        super().__init__(name, hp=150, max_hp=150, level=1, xp=0, strength=12, dexterity=6, intelligence=3, defense=3)


class Mage(Character):
    def __init__(self, name: str):
        super().__init__(name, hp=80, max_hp=80, level=1, xp=0, strength=3, dexterity=6, intelligence=14, defense=1)
        self.mana = 30

    def cast_spell(self, target: "Character", cost: int = 8) -> Dict[str, int]:
        """Примітивна магічна атака, яка витрачає ману.

        Повертає словник з інформацією про атаку або порожній словник якщо не вистачає мани.
        """
        if self.mana < cost:
            return {}
        self.mana -= cost
        power = self.stats.get("intelligence", 1) * 3
        raw = max(0, power + random.randint(-3, 3))
        # Удача може посилити заклинання (критичний ефект)
        critical = False
        if self.roll_luck():
            raw *= 2
            critical = True
        damage = target.take_damage(raw)
        res = {"raw": raw, "damage": damage}
        if critical:
            res["critical"] = True
        return res


class Scout(Character):
    def __init__(self, name: str):
        super().__init__(name, hp=100, max_hp=100, level=1, xp=0, strength=5, dexterity=12, intelligence=6, defense=2)

    def attack(self, target: "Character") -> Dict[str, int]:
        """Має шанс на критичну атаку залежно від влучності (dexterity) та удачі (luck)."""
        res = super().attack(target)
        crit_chance = min(75, self.stats.get("dexterity", 5) * 2 + self.stats.get("luck", 0))  # відсотків
        if random.randint(1, 100) <= crit_chance:
            # Подвоюємо фактичну шкоду (після захисту)
            extra = res["damage"]
            target.take_damage(extra)
            res["critical"] = True
            res["damage"] += extra
        else:
            res["critical"] = False
        return res
    
    def attempt_flee(self, enemy, intel_threshold=10):
        """Спроба втечі з бою.
        Умови: інтелект >= intel_threshold і поточна стаміна >= 50% від макс.
        Після вдалого втечі: відняти 10 одиниць стаміни і додати лише XP.
        Повертає True якщо втекли, False інакше.
        """
        # поточна/макс стаміна (підтримка різних імен полів)
        max_st = getattr(self, "max_stamina", getattr(self, "stamina_max", 100))
        cur_st = getattr(self, "stamina", getattr(self, "stamina_current", None))
        if cur_st is None:
            cur_st = getattr(self, "stamina", 100)

        # інтелект (підтримка різних імен полів)
        intel = getattr(self, "intelligence", getattr(self, "int", 0))

        # перевірки умов
        st_percent = (cur_st / max_st) * 100 if max_st else 0
        if intel < intel_threshold or st_percent < 50:
            return False

        # віднімаємо 10 стаміни (мінімум 0)
        new_st = max(0, cur_st - 10)
        if hasattr(self, "stamina"):
            self.stamina = new_st
        elif hasattr(self, "stamina_current"):
            self.stamina_current = new_st

        # нарахувати тільки XP (підтримка gain_xp() або прямого поля xp)
        xp_gain = getattr(enemy, "xp_reward", 2)
        if hasattr(self, "gain_xp") and callable(getattr(self, "gain_xp")):
            self.gain_xp(xp_gain)
        else:
            self.xp = getattr(self, "xp", 0) + xp_gain

        # позначити кінець бою для цього персонажа, якщо є відповідне поле
        if hasattr(self, "in_combat"):
            self.in_combat = False

        return True