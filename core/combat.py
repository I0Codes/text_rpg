import random

from ui.base_ui import GameUI
from ui.combat_ui import CombatUI


class Combat:
    def __init__(self, player, ui: GameUI):
        self.player = player
        self._ui = ui
        self._combat_ui = CombatUI(ui)

    def _player_strike(self, target):
        if random.random() < target.attributes.get_dodge_chance():
            self._combat_ui.display_damage(self.player, target, 0, is_dodged=True)
            return
        raw = int(self.player.calculate_physical_damage()) + random.randint(-2, 2)
        raw = max(1, raw)
        is_crit = random.random() < self.player.attributes.get_crit_chance()
        if is_crit:
            raw = max(1, int(raw * 1.5))
        dealt = target.take_damage(raw)
        self._combat_ui.display_damage(self.player, target, dealt, is_crit=is_crit)

    def _enemy_strike(self, enemy, defending):
        if random.random() < self.player.attributes.get_dodge_chance():
            self._combat_ui.display_damage(enemy, self.player, 0, is_dodged=True)
            return
        raw = int(enemy.attack())
        if defending:
            raw = max(1, raw // 2)
        is_crit = random.random() < enemy.attributes.get_crit_chance()
        if is_crit:
            raw = max(1, int(raw * 1.5))
        self.player.take_damage(raw)
        self._combat_ui.display_damage(enemy, self.player, raw, is_crit=is_crit)

    def run(self, enemies):
        alive = [e for e in enemies if e.is_alive()]
        if not alive:
            return

        self._ui.show_text("\n🔥 Бій розпочався!")
        while self.player.is_alive() and alive:
            alive = [e for e in alive if e.is_alive()]
            if not alive:
                break

            self._combat_ui.display_combat_status(self.player, alive)
            self._combat_ui.display_combat_actions()
            choice = self._ui.get_input("\nБій — ваш вибір: ").strip()
            defending = False

            if choice == "1":
                self._player_strike(alive[0])
            elif choice == "2":
                defending = True
                self._ui.show_text("Ви зайняли оборону (наступні удари по вам слабші).")
            elif choice == "3":
                consumables = self.player.inventory.get_items_by_type("consumable")
                if not consumables:
                    self._ui.show_text("Немає споживних предметів.")
                else:
                    for i, it in enumerate(consumables, 1):
                        q = f" x{it.quantity}" if it.stackable else ""
                        self._ui.show_text(f"  {i}. {it.name}{q}")
                    pick = self._ui.get_input("Номер предмета (Enter — скасувати): ").strip()
                    if pick.isdigit() and 1 <= int(pick) <= len(consumables):
                        self.player.use_item(consumables[int(pick) - 1])
            elif choice == "4":
                flee_roll = 0.35 + self.player.attributes.agility * 0.02
                if random.random() < min(flee_roll, 0.75):
                    self._ui.show_text("Вам вдалося втекти з бою.")
                    return
                self._ui.show_text("Втеча не вдалася!")
            else:
                self._ui.show_text("Невідома команда. Спробуйте 1–4.")
                continue

            alive = [e for e in alive if e.is_alive()]
            if not alive:
                break

            for enemy in alive:
                if not self.player.is_alive():
                    break
                if enemy.select_action() == "attack":
                    self._enemy_strike(enemy, defending)

        alive = [e for e in alive if e.is_alive()]
        if not self.player.is_alive():
            return
        if not alive:
            self._ui.show_text("\n🏆 Перемога!")
            total_gold = 0
            for e in enemies:
                if not e.is_alive():
                    xp = self.player.experience_manager.calculate_experience_reward(
                        e.level, self.player.level
                    )
                    self.player.gain_experience(xp, source="combat")
                    loot = e.get_loot()
                    total_gold += loot.get("gold", 0)
            if total_gold:
                self.player.gain_gold(total_gold)
                self._ui.show_text(f"💰 Золото: +{total_gold}")
