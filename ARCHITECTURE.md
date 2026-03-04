# Архітектура Text RPG Game

## Загальний огляд

Текстова RPG гра з системою бою, навичок, атрибутів та елементом везіння.

## Структура проєкту

```
text_rpg/
├── main.py                     # Точка входу
├── config/                     # Конфігурація гри
│   ├── __init__.py
│   ├── constants.py           # Константи (базові значення, множники)
│   └── settings.py            # Налаштування гри
│
├── core/                       # Ядро гри
│   ├── __init__.py
│   ├── game.py                # Основний ігровий цикл
│   ├── engine.py              # Механіки гри (розрахунки, перевірки)
│   └── save_manager.py        # Збереження/завантаження
│
├── entities/                   # Ігрові сутності
│   ├── __init__.py
│   ├── characters.py          # Класи персонажів (Player, Enemy)
│   ├── attributes.py          # Система атрибутів
│   ├── skills.py              # Система навичок
│   ├── inventory.py           # Інвентар
│   └── effects.py             # Ефекти (отруєння, бафи тощо)
│
├── items/                      # Предмети
│   ├── __init__.py
│   ├── base.py                # Базовий клас Item
│   ├── weapons.py             # Зброя
│   ├── armor.py               # Броня
│   └── consumables.py         # Витратні предмети (зілля, їжа)
│
├── combat/                     # Бойова система
│   ├── __init__.py
│   ├── combat_system.py       # Основна логіка бою
│   ├── actions.py             # Бойові дії
│   └── damage_calculator.py   # Розрахунок шкоди
│
├── world/                      # Ігровий світ
│   ├── __init__.py
│   ├── locations.py           # Локації
│   ├── events.py              # Випадкові події
│   └── quests.py              # Система квестів
│
├── ui/                         # Інтерфейс користувача
│   ├── __init__.py
│   ├── ui.py                  # Головний UI
│   ├── menus.py               # Різні меню
│   └── combat_ui.py           # UI для бою
│
└── data/                       # Дані
    ├── saves/                 # Файли збережень
    ├── enemies/               # Дані про ворогів
    ├── items/                 # Дані про предмети
    └── locations/             # Дані про локації
```

---

## Модулі та їх функції

### 1. **config/** - Конфігурація

#### `constants.py`

```python
# Базові значення атрибутів
BASE_HP = 100
BASE_STAMINA = 100
BASE_MANA = 50

# Множники атрибутів
STRENGTH_DAMAGE_MULTIPLIER = 1.5
INTELLIGENCE_MANA_MULTIPLIER = 2.0
AGILITY_CRIT_MULTIPLIER = 0.5
LUCK_SUCCESS_MULTIPLIER = 0.3

# Шанси
BASE_CRIT_CHANCE = 0.05  # 5%
BASE_DODGE_CHANCE = 0.1  # 10%
```

#### `settings.py`

```python
# Налаштування гри
DIFFICULTY = "NORMAL"  # EASY, NORMAL, HARD
AUTO_SAVE = True
```

---

### 2. **entities/** - Ігрові сутності

#### `attributes.py`

```python
class Attributes:
    """Система атрибутів персонажа"""
    - strength: int        # Сила (фізична атака, макс HP)
    - intelligence: int    # Інтелект (магічна атака, макс мана)
    - agility: int         # Ловкість (шанс ухилення, крит, швидкість)
    - luck: int           # Удача (шанси успіху, дроп, криті)

    methods:
    - get_physical_damage_bonus()
    - get_magic_damage_bonus()
    - get_crit_chance()
    - get_dodge_chance()
    - get_luck_modifier()
```

#### `characters.py`

```python
class Character:
    """Базовий клас для всіх персонажів"""
    - name: str
    - level: int
    - hp: int
    - max_hp: int
    - stamina: int
    - max_stamina: int
    - mana: int
    - max_mana: int
    - attributes: Attributes
    - skills: list[Skill]
    - inventory: Inventory
    - equipped_weapon: Weapon
    - equipped_armor: dict[str, Armor]
    - active_effects: list[Effect]

class Player(Character):
    """Клас гравця"""
    - experience: int
    - gold: int
    - quests: list[Quest]

    methods:
    - gain_experience(amount)
    - level_up()
    - spend_attribute_points()

class Enemy(Character):
    """Клас ворога"""
    - enemy_type: str
    - reward_exp: int
    - reward_gold: int
    - loot_table: dict

    methods:
    - get_loot()
    - select_action()  # AI для вибору дії

# Класи персонажів
class Warrior(Player):
    """Воїн - висока сила та HP"""
    base_attributes: Attributes(strength=10, intelligence=3, agility=5, luck=5)

class Mage(Player):
    """Маг - високий інтелект та мана"""
    base_attributes: Attributes(strength=3, intelligence=10, agility=4, luck=6)

class Scout(Player):
    """Розвідник - висока ловкість та удача"""
    base_attributes: Attributes(strength=5, intelligence=4, agility=10, luck=8)
```

#### `skills.py`

```python
class Skill:
    """Базовий клас навички"""
    - name: str
    - description: str
    - skill_type: str  # "ATTACK", "DEFENSE", "BUFF", "HEAL"
    - cost: dict       # {"stamina": 20} або {"mana": 30}
    - cooldown: int
    - current_cooldown: int
    - required_attributes: dict  # Мінімальні вимоги

    methods:
    - can_use(character) -> bool
    - use(user, target=None) -> dict  # Повертає результат
    - calculate_success_chance(user) -> float
    - calculate_effect(user, target=None) -> dict

# Приклади конкретних навичок

class PowerStrike(Skill):
    """Потужний удар - фізична атака з високою шкодою"""
    cost = {"stamina": 25}
    base_damage_multiplier = 1.8
    # Залежить від: STRENGTH, LUCK

class Fireball(Skill):
    """Вогняна куля - магічна атака"""
    cost = {"mana": 35}
    base_damage = 50
    # Залежить від: INTELLIGENCE, LUCK

class QuickStab(Skill):
    """Швидкий удар - низька шкода, високий шанс криту"""
    cost = {"stamina": 15}
    crit_bonus = 0.3
    # Залежить від: AGILITY, LUCK

class Heal(Skill):
    """Самолікування"""
    cost = {"mana": 25}
    base_heal = 40
    # Залежить від: INTELLIGENCE

class Dodge(Skill):
    """Ухилення - збільшує шанс уникнути атаки"""
    cost = {"stamina": 10}
    dodge_bonus = 0.25
    duration = 1  # Тривалість в раундах
    # Залежить від: AGILITY

class Berserk(Skill):
    """Шал - збільшує атаку, але зменшує захист"""
    cost = {"stamina": 30}
    attack_bonus = 0.5
    defense_penalty = 0.3
    duration = 3
    # Залежить від: STRENGTH, LUCK
```

#### `inventory.py`

```python
class Inventory:
    """Інвентар персонажа"""
    - items: list[Item]
    - max_capacity: int

    methods:
    - add_item(item) -> bool
    - remove_item(item)
    - use_item(item, character)
    - get_items_by_type(item_type) -> list
```

#### `effects.py`

```python
class Effect:
    """Тимчасовий ефект на персонажі"""
    - name: str
    - effect_type: str  # "BUFF", "DEBUFF", "DOT", "HOT"
    - duration: int
    - attribute_modifiers: dict

    methods:
    - apply(character)
    - tick(character)  # Виконується кожен раунд
    - remove(character)

# Приклади
class Poison(Effect):
    """Отруєння - періодична шкода"""

class Strength_Buff(Effect):
    """Бафф на силу"""
```

---

### 3. **items/** - Предмети

#### `base.py`

```python
class Item:
    """Базовий клас предмета"""
    - name: str
    - description: str
    - item_type: str
    - value: int  # Ціна
    - rarity: str  # "COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY"

    methods:
    - use(character) -> bool
```

#### `weapons.py`

```python
class Weapon(Item):
    """Зброя"""
    - damage: int
    - damage_type: str  # "PHYSICAL", "MAGICAL"
    - attack_speed: float
    - required_attributes: dict
    - special_effects: list[Effect]

    methods:
    - calculate_damage(attacker, defender) -> int

# Приклади
class IronSword(Weapon):
    damage = 25
    damage_type = "PHYSICAL"
    required_attributes = {"strength": 5}

class MagicStaff(Weapon):
    damage = 30
    damage_type = "MAGICAL"
    required_attributes = {"intelligence": 7}
```

#### `armor.py`

```python
class Armor(Item):
    """Броня"""
    - defense: int
    - armor_type: str  # "LIGHT", "MEDIUM", "HEAVY"
    - slot: str  # "HEAD", "CHEST", "LEGS", "FEET", "HANDS"
    - required_attributes: dict

    methods:
    - reduce_damage(damage) -> int
```

#### `consumables.py`

```python
class Consumable(Item):
    """Витратний предмет"""
    - effect: Effect
    - instant: bool

    methods:
    - consume(character)

# Приклади
class HealthPotion(Consumable):
    effect = Heal(amount=50)
    instant = True

class StaminaPotion(Consumable):
    effect = RestoreStamina(amount=40)
    instant = True
```

---

### 4. **combat/** - Бойова система

#### `combat_system.py`

```python
class CombatSystem:
    """Головна логіка бою"""
    - player: Player
    - enemies: list[Enemy]
    - turn: int
    - combat_log: list[str]

    methods:
    - start_combat()
    - process_turn()
    - end_combat()
    - determine_turn_order() -> list  # За швидкістю (agility)
    - check_combat_end() -> bool
```

#### `actions.py`

```python
class CombatAction:
    """Базова бойова дія"""
    - action_type: str  # "ATTACK", "SKILL", "ITEM", "DEFEND", "FLEE"

    methods:
    - execute(user, target, combat_system)

class AttackAction(CombatAction):
    """Звичайна атака"""

class SkillAction(CombatAction):
    """Використання навички"""

class DefendAction(CombatAction):
    """Захист - зменшує шкоду"""

class FleeAction(CombatAction):
    """Втеча з бою"""
    # Залежить від: AGILITY, LUCK
```

#### `damage_calculator.py`

```python
class DamageCalculator:
    """Розрахунок шкоди та шансів"""

    @staticmethod
    def calculate_damage(attacker, defender, skill=None) -> dict:
        """
        Розраховує шкоду з урахуванням:
        - Базова шкода (зброя + атрибути)
        - Навичка (якщо використовується)
        - Захист противника
        - Шанс критичного удару
        - Везіння

        Returns:
            {
                "damage": int,
                "is_critical": bool,
                "is_dodged": bool
            }
        """

    @staticmethod
    def calculate_success_chance(character, action, difficulty=1.0) -> float:
        """
        Розраховує шанс успіху дії:
        - Базовий шанс
        - Атрибути персонажа
        - Везіння
        - Складність дії

        Returns:
            float: шанс від 0.0 до 1.0
        """

    @staticmethod
    def roll_luck_check(character, base_chance=0.5) -> bool:
        """Перевірка на везіння"""
```

---

### 5. **world/** - Світ гри

#### `locations.py`

```python
class Location:
    """Базовий клас локації"""
    - name: str
    - description: str
    - connected_locations: dict[str, Location]
    - encounters: list  # Можливі зустрічі (вороги, NPC)
    - events: list[Event]
    - can_rest: bool

    methods:
    - get_actions() -> dict
    - handle_action(action, player)
    - trigger_random_event()

# Приклади локацій
class Village(Location):
    """Село - безпечна зона з торговцями"""

class Forest(Location):
    """Ліс - зустрічі з ворогами"""

class Cave(Location):
    """Печера - складні вороги, гарний лут"""

class DarkForest(Location):
    """Темний ліс - сильні вороги"""
```

#### `events.py`

```python
class Event:
    """Випадкова подія"""
    - name: str
    - description: str
    - event_type: str  # "COMBAT", "TREASURE", "NPC", "TRAP"
    - chance: float

    methods:
    - trigger(player) -> dict
    - resolve(player, choice) -> dict

# Приклади
class TreasureChest(Event):
    """Знайдена скриня"""
    # Можливість пастки (залежить від LUCK)

class AmbushEvent(Event):
    """Засідка ворогів"""
    # Можливість уникнути (залежить від AGILITY, LUCK)

class MerchantEvent(Event):
    """Зустріч з торговцем"""
```

#### `quests.py`

```python
class Quest:
    """Квест"""
    - name: str
    - description: str
    - objectives: list[Objective]
    - rewards: dict  # {"exp": 100, "gold": 50, "items": [...]}
    - status: str  # "ACTIVE", "COMPLETED", "FAILED"

    methods:
    - check_progress()
    - complete()

class Objective:
    """Ціль квесту"""
    - description: str
    - objective_type: str  # "KILL", "COLLECT", "VISIT"
    - target: str
    - current: int
    - required: int
```

---

### 6. **core/** - Ядро гри

#### `engine.py`

```python
class GameEngine:
    """Головні механіки гри"""

    @staticmethod
    def calculate_level_requirements(level: int) -> int:
        """Розрахунок необхідного досвіду для рівня"""

    @staticmethod
    def generate_loot(enemy: Enemy, player_luck: float) -> list[Item]:
        """Генерація луту з урахуванням удачі"""

    @staticmethod
    def calculate_attribute_bonuses(attributes: Attributes) -> dict:
        """Розрахунок бонусів від атрибутів"""
```

#### `save_manager.py`

```python
class SaveManager:
    """Управління збереженнями"""

    @staticmethod
    def save_game(player, game_state, filename="save.json"):
        """Зберегти гру"""

    @staticmethod
    def load_game(filename="save.json") -> dict:
        """Завантажити гру"""

    @staticmethod
    def get_save_list() -> list:
        """Список збережень"""
```

---

### 7. **ui/** - Інтерфейс

#### `menus.py`

```python
class MainMenu:
    """Головне меню"""
    - Нова гра
    - Завантажити гру
    - Налаштування
    - Вихід

class CharacterCreationMenu:
    """Меню створення персонажа"""
    - Вибір класу (Warrior, Mage, Scout)
    - Введення імені
    - Розподіл початкових атрибутів

class InventoryMenu:
    """Меню інвентаря"""
    - Перегляд предметів
    - Використання предметів
    - Екіпірування
```

#### `combat_ui.py`

```python
class CombatUI:
    """UI для бою"""

    @staticmethod
    def display_combat_status(player, enemies):
        """Відображення статусу бою"""

    @staticmethod
    def display_combat_actions():
        """Доступні дії в бою"""

    @staticmethod
    def display_damage_log(log_entry):
        """Лог шкоди та дій"""
```

---

## Система розрахунків

### Атрибути та їх вплив

1. **STRENGTH (Сила)**
   - +2 HP за кожну одиницю
   - +1.5 до фізичної шкоди за кожну одиницю
   - Вимоги для важкої зброї та броні

2. **INTELLIGENCE (Інтелект)**
   - +2 Mana за кожну одиницю
   - +2.0 до магічної шкоди за кожну одиницю
   - Ефективність зцілення

3. **AGILITY (Ловкість)**
   - +0.5% шанс критичного удару за одиницю
   - +1% шанс ухилення за одиницю
   - Швидкість (порядок ходів)
   - Шанс втечі з бою

4. **LUCK (Удача)**
   - +0.3% до всіх шансів успіху за одиницю
   - Збільшує шанс критичного удару
   - Якість луту
   - Шанс спрацювання спеціальних ефектів
   - Уникнення пасток

### Формули розрахунків

#### Фізична атака:

```
базова_шкода = зброя.damage + (сила * 1.5)
шанс_криту = BASE_CRIT + (ловкість * 0.005) + (удача * 0.003)
фінальна_шкода = базова_шкода * (2.0 якщо крит) - захист_ворога
фінальна_шкода = max(1, фінальна_шкода)  # Мінімум 1 шкоди
```

#### Магічна атака:

```
базова_шкода = скіл.damage + (інтелект * 2.0)
шанс_криту = BASE_CRIT + (інтелект * 0.003) + (удача * 0.003)
фінальна_шкода = базова_шкода * (1.5 якщо крит) - (магічний_захист / 2)
```

#### Шанс ухилення:

```
шанс_ухилення = BASE_DODGE + (ловкість * 0.01) + (удача * 0.003)
```

#### Шанс успіху дії:

```
базовий_шанс = 0.5  # 50%
модифікатор_атрибуту = відповідний_атрибут * 0.02
модифікатор_удачі = удача * 0.003
фінальний_шанс = min(0.95, базовий_шанс + модифікатор_атрибуту + модифікатор_удачі)
```

---

## Ігровий процес

### 1. Початок гри

1. Головне меню (Нова гра / Завантажити)
2. Створення персонажа (вибір класу, ім'я)
3. Стартова локація (Село)

### 2. Геймплей

1. Дослідження локацій
2. Випадкові події та зустрічі
3. Бої з ворогами
4. Збір ресурсів та луту
5. Прокачка персонажа
6. Виконання квестів

### 3. Бій

1. Ініціатива (за швидкістю)
2. Вибір дії (атака, навичка, предмет, захист, втеча)
3. Розрахунок результату
4. Застосування ефектів
5. Перевірка закінчення бою
6. Нагороди (досвід, золото, лут)

---

## Приклад ігрового сценарію

1. Гравець створює Warrior з ім'ям "Артур"
2. Починає в Village
3. Йде в Forest на дослідження
4. Спрацьовує випадкова подія - зустріч з Goblin
5. Розпочинається бій:
   - Артур атакує мечем (базова атака)
   - Goblin промахується (низька ловкість)
   - Артур використовує PowerStrike (витрачає stamina)
   - Критичний удар! (удача спрацювала)
   - Goblin переможений
6. Нагорода: +50 exp, +20 gold, знайдено HealthPotion
7. Артур отримує рівень! Розподіляє +2 до strength
8. Продовжує дослідження...

---

## План розробки (по пріоритету)

### Фаза 1 - Базова механіка

- [x] Базовий Character
- [ ] Система атрибутів
- [ ] Класи персонажів (Warrior, Mage, Scout)
- [ ] Базова бойова система
- [ ] Прості вороги

### Фаза 2 - Навички та предмети

- [ ] Система навичок
- [ ] Базова зброя та броня
- [ ] Інвентар
- [ ] Витратні предмети

### Фаза 3 - Розширена механіка

- [ ] Система удачі та розрахунків
- [ ] Ефекти (бафи, дебафи)
- [ ] Розширена бойова система з навичками
- [ ] Критичні удари та ухилення

### Фаза 4 - Контент

- [ ] Різні локації
- [ ] Випадкові події
- [ ] Різноманітні вороги
- [ ] Система квестів

### Фаза 5 - Поліровка

- [ ] Система збереження
- [ ] Покращений UI (rich library)
- [ ] Баланс гри
- [ ] Додатковий контент

---

## Технічні деталі

### Залежності

```
rich>=13.0.0  # Для красивого UI
```

### Формат збереження (JSON)

```json
{
    "player": {
        "name": "Артур",
        "class": "Warrior",
        "level": 5,
        "experience": 450,
        "attributes": {"strength": 12, "intelligence": 5, "agility": 7, "luck": 6},
        "hp": 150,
        "max_hp": 150,
        "equipped": {"weapon": "iron_sword", "armor": {...}},
        "inventory": [...],
        "quests": [...]
    },
    "game_state": {
        "current_location": "forest",
        "turn": 120,
        "flags": {...}
    }
}
```

---

## Висновок

Ця архітектура забезпечує:

- ✅ Модульність (легко додавати нових персонажів, навички, предмети)
- ✅ Розширюваність (можна додати нові системи без зміни існуючих)
- ✅ Систему атрибутів з впливом на геймплей
- ✅ Елемент везіння у всіх діях
- ✅ Різноманітні навички для різних стилів гри
- ✅ Глибоку бойову систему

Гра може розвиватися поступово, додаючи функціонал по фазах.
