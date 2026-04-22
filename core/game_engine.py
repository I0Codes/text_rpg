from typing import Any

from config.constants import BASE_HP, BASE_MANA, BASE_STAMINA


class GameEngine:
    @staticmethod
    def calculate_level_requirements(level: int) -> int:
        """
        Розрахунок XP для наступного рівня.
        Формула: рівень * 100
        """
        try:
            return max(0, int(level) * 100)
        except (TypeError, ValueError):
            raise ValueError("level must be an integer")

    @staticmethod
    def calculate_total_stats(character: Any) -> dict:
        """
        Розрахунок підсумкових характеристик персонажа.
        Об'єднує базові значення, бонуси від атрибутів, екіпірування,
        активних ефектів та бонуси рівня.
        """
        base_hp = getattr(character, "max_hp", BASE_HP)
        base_stamina = getattr(character, "max_stamina", BASE_STAMINA)
        base_mana = getattr(character, "max_mana", BASE_MANA)

        equipment_bonuses = GameEngine._sum_bonus_sources(character, source="equipment")
        effect_bonuses = GameEngine._sum_bonus_sources(character, source="effects")

        return {
            "max_hp": int(base_hp + equipment_bonuses["max_hp"] + effect_bonuses["max_hp"]),
            "max_stamina": int(base_stamina + equipment_bonuses["max_stamina"] + effect_bonuses["max_stamina"]),
            "max_mana": int(base_mana + equipment_bonuses["max_mana"] + effect_bonuses["max_mana"]),
            "physical_damage": float(
                GameEngine._get_physical_damage(character)
                + equipment_bonuses["physical_damage"]
                + effect_bonuses["physical_damage"]
            ),
            "magical_damage": float(
                GameEngine._get_magical_damage(character)
                + equipment_bonuses["magical_damage"]
                + effect_bonuses["magical_damage"]
            ),
            "defense": int(
                getattr(character, "defense", 0)
                + equipment_bonuses["defense"]
                + effect_bonuses["defense"]
            ),
            "crit_chance": float(
                GameEngine._get_crit_chance(character)
                + getattr(character, "crit_bonus", 0.0)
                + equipment_bonuses["crit_chance"]
                + effect_bonuses["crit_chance"]
            ),
            "dodge_chance": float(
                GameEngine._get_dodge_chance(character)
                + getattr(character, "dodge_bonus", 0.0)
                + equipment_bonuses["dodge_chance"]
                + effect_bonuses["dodge_chance"]
            ),
        }

    @staticmethod
    def _get_physical_damage(character: Any) -> float:
        if hasattr(character, "calculate_physical_damage"):
            return float(character.calculate_physical_damage())
        if hasattr(character, "attributes") and hasattr(character.attributes, "get_physical_damage_bonus"):
            return 5.0 + float(character.attributes.get_physical_damage_bonus())
        return 0.0

    @staticmethod
    def _get_magical_damage(character: Any) -> float:
        if hasattr(character, "calculate_magical_damage"):
            return float(character.calculate_magical_damage())
        if hasattr(character, "attributes") and hasattr(character.attributes, "get_magic_damage_bonus"):
            return 5.0 + float(character.attributes.get_magic_damage_bonus())
        return 0.0

    @staticmethod
    def _get_crit_chance(character: Any) -> float:
        if hasattr(character, "attributes") and hasattr(character.attributes, "get_crit_chance"):
            return float(character.attributes.get_crit_chance())
        return 0.0

    @staticmethod
    def _get_dodge_chance(character: Any) -> float:
        if hasattr(character, "attributes") and hasattr(character.attributes, "get_dodge_chance"):
            return float(character.attributes.get_dodge_chance())
        return 0.0

    @staticmethod
    def _sum_bonus_sources(character: Any, source: str) -> dict:
        if source == "equipment":
            items = GameEngine._get_equipment_items(character)
        else:
            items = GameEngine._get_active_effects(character)

        return GameEngine._sum_bonus_items(items)

    @staticmethod
    def _get_equipment_items(character: Any) -> list:
        items = []
        for attr_name in (
            "equipped_weapon",
            "equipped_armor",
            "weapon",
            "armor",
            "main_hand",
            "off_hand",
            "equipment",
            "gear",
        ):
            attr = getattr(character, attr_name, None)
            if attr is None:
                continue

            if isinstance(attr, (list, tuple, set)):
                items.extend(attr)
            elif isinstance(attr, dict):
                items.extend([item for item in attr.values() if item is not None])
            else:
                items.append(attr)

        inventory = getattr(character, "inventory", None)
        if inventory is not None and hasattr(inventory, "items"):
            items.extend(
                [item for item in getattr(inventory, "items", []) if getattr(item, "equipped", False)]
            )

        return items

    @staticmethod
    def _get_active_effects(character: Any) -> list:
        active_effects = getattr(character, "active_effects", None)
        if active_effects is None:
            return []

        if isinstance(active_effects, dict):
            return [effect for effect in active_effects.values() if effect is not None]
        if isinstance(active_effects, (list, tuple, set)):
            return list(active_effects)

        return [active_effects]

    @staticmethod
    def _sum_bonus_items(items: list) -> dict:
        bonuses = {
            "max_hp": 0,
            "max_stamina": 0,
            "max_mana": 0,
            "physical_damage": 0,
            "magical_damage": 0,
            "defense": 0,
            "crit_chance": 0,
            "dodge_chance": 0,
        }

        for item in items:
            if item is None:
                continue

            if hasattr(item, "bonuses") and isinstance(item.bonuses, dict):
                for key, value in item.bonuses.items():
                    if key in bonuses and isinstance(value, (int, float)):
                        bonuses[key] += value
                continue

            for key in bonuses:
                value = getattr(item, key, None)
                if isinstance(value, (int, float)):
                    bonuses[key] += value

            weapon_damage = getattr(item, "damage", None)
            if isinstance(weapon_damage, (int, float)):
                bonuses["physical_damage"] += float(weapon_damage)

            magic_damage = getattr(item, "magic_damage", None)
            if isinstance(magic_damage, (int, float)):
                bonuses["magical_damage"] += float(magic_damage)

            defense_value = getattr(item, "defense_value", None)
            if isinstance(defense_value, (int, float)):
                bonuses["defense"] += int(defense_value)

            bonus_crit = getattr(item, "crit", None)
            if isinstance(bonus_crit, (int, float)):
                bonuses["crit_chance"] += float(bonus_crit)

            bonus_dodge = getattr(item, "dodge", None)
            if isinstance(bonus_dodge, (int, float)):
                bonuses["dodge_chance"] += float(bonus_dodge)

        return bonuses
