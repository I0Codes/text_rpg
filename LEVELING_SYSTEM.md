# Система прокачки рівнів (LevelingSystem)

## Опис

`LevelingSystem` — це клас для керування прогресією персонажа, включаючи підвищення рівня, розподіл очок атрибутів та навичок, а також відслідковування прогресу.

## Основні компоненти

### Клас LevelingSystem

Знаходиться в: [entities/leveling_system.py](../entities/leveling_system.py)

#### Атрибути
- `character` — персонаж, прив'язаний до системи
- `level` — поточний рівень (синхронізується з character.level)
- `attribute_points` — доступні очки атрибутів для розподілу
- `skill_points` — доступні очки навичок для розподілу
- `level_up_history` — історія всіх підвищень рівня

#### Константи
- `ATTRIBUTE_POINTS_PER_LEVEL = 2` — очки атрибутів за рівень
- `SKILL_POINTS_PER_LEVEL = 1` — очки навичок за рівень

### Методи

#### `level_up()`
Підвищує рівень персонажа:
1. Збільшує `level` на 1
2. Дає 2 очка атрибутів
3. Дає 1 очко навичок
4. Повністю відновлює HP, stamina, mana
5. Застосовує специфічні бонуси класу
6. Зберігає інформацію в історію

```python
leveling_system.level_up()
# Вивід:
# ============================================================
# [РІВЕНЬ ПІДВИЩЕНО!] Ви тепер рівня 2!
# ============================================================
# ...
```

#### `spend_attribute_point(attribute_name)`
Витрачає очко атрибуту на покращення певного атрибуту.

**Параметри:**
- `attribute_name` (str) — назва атрибуту (strength, intelligence, agility, luck)

**Повертає:**
- `True` якщо успішно потрачено
- `False` якщо немає доступних очок

**Валідація:**
- Перевіряє наявність очок
- Перевіряє існування атрибуту (викидає ValueError)

```python
result = leveling_system.spend_attribute_point('strength')
if result:
    print(f"Strength збільшено! Залишилось очок: {leveling_system.attribute_points}")
else:
    print("Недостатньо очок атрибутів!")
```

#### `spend_skill_point(skill_name)`
Витрачає очко навички на покращення або розблокування навички.

**Параметри:**
- `skill_name` (str) — назва навички

**Повертає:**
- `True` якщо успішно потрачено
- `False` якщо немає доступних очок або навичка не знайдена

```python
result = leveling_system.spend_skill_point('fireball')
```

#### `get_available_points()`
Повертає словник з інформацією про доступні очки:

```python
points = leveling_system.get_available_points()
# {
#     'attribute_points': 2,
#     'skill_points': 1,
#     'total_available': 3,
#     'level': 3
# }
```

#### `can_spend_attribute_point()` та `can_spend_skill_point()`
Швидка перевірка наявності очок:

```python
if leveling_system.can_spend_attribute_point():
    leveling_system.spend_attribute_point('agility')
```

#### `get_summary()`
Отримати повний звіт про систему:

```python
summary = leveling_system.get_summary()
# {
#     'current_level': 5,
#     'attribute_points': 3,
#     'skill_points': 1,
#     'character_name': 'Hero',
#     'character_level': 5,
#     'hp': '150/150',
#     'attributes': {
#         'strength': 8,
#         'intelligence': 6,
#         'agility': 7,
#         'luck': 5
#     },
#     'total_level_ups': 4
# }
```

#### `reset_points()`
Скидає всі очки (для переквалірікації/переспеціалізації):

```python
leveling_system.reset_points()
```

#### `get_level_up_history()`
Отримати історію підвищень рівня:

```python
history = leveling_system.get_level_up_history()
# [
#     {
#         'level': 2,
#         'attribute_points_gained': 2,
#         'skill_points_gained': 1,
#         'total_attribute_points': 2,
#         'total_skill_points': 1
#     },
#     ...
# ]
```

## Валідація

Система містить вбудовану валідацію:

1. **Неможливо потратити більше очок, ніж є** — система перевіряє баланс перед витратою
2. **Невалідні атрибути** — викидає `ValueError` якщо спробувати потратити на неіснуючий атрибут
3. **Синхронізація з персонажем** — `level` завжди синхронізує з `character.level`

## Інтеграція з Character

`LevelingSystem` автоматично створюється при ініціалізації персонажа:

```python
from entities import Character

character = Character("Hero", hp=100, max_hp=100, stamina=50, max_stamina=50)
leveling_system = character.leveling_system

# Система вже інтегрована і готова до використання
leveling_system.level_up()
```

## Приклади використання

### Приклад 1: Підвищення рівня та розподіл очок

```python
character = Character("Warrior", hp=100, max_hp=100, stamina=50, max_stamina=50)
leveling_system = character.leveling_system

# Піднімаємось 3 рази
for _ in range(3):
    leveling_system.level_up()

# Розподіляємо очки
leveling_system.spend_attribute_point('strength')   # Сила +1
leveling_system.spend_attribute_point('strength')   # Сила +1
leveling_system.spend_attribute_point('constitution')  # HP бонус

print(leveling_system.get_available_points())
```

### Приклад 2: Перевірка та розподіл очок

```python
while leveling_system.can_spend_attribute_point():
    # Логіка для покращення бойових навичок
    leveling_system.spend_attribute_point('strength')
    leveling_system.spend_attribute_point('agility')
```

## Тести

Повний набір тестів знаходиться в [tests/test_leveling_system.py](../tests/test_leveling_system.py)

**Класи тестів:**
- `TestLevelingSystemBasics` — базові тести ініціалізації
- `TestLevelUp` — тести підвищення рівня
- `TestAttributePoints` — тести розподілу очок атрибутів
- `TestSkillPoints` — тести розподілу очок навичок
- `TestValidation` — тести валідації
- `TestSummary` — тести отримання інформації
- `TestIntegrationScenarios` — інтеграційні тести

**Запуск тестів:**
```bash
pytest tests/test_leveling_system.py -v
```

## Майбутні покращення

1. Система переквалірікації (переспеціалізації)
2. Кастомні бонуси за певні комбінації атрибутів
3. Система досягнень при підвищенні рівня
4. Інтеграція з збереженням ігри
5. UI для розподілу очок у меню персонажа
