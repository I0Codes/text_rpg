import random

from ui.base_ui import GameUI
from ui.combat_ui import CombatUI


class Combat:
    def __init__(self, player, ui: GameUI):
        self.player = player
        self._ui = ui
        self._combat_ui = CombatUI(ui)

    def _player_strike(self, target, target_index):
        if random.random() < target.attributes.get_dodge_chance():
            self._combat_ui.display_damage(
                self.player, target, 0, is_dodged=True,
                target_index=target_index, attacker_is_player=True,
            )
            return
        raw = int(self.player.calculate_physical_damage()) + random.randint(-2, 2)
        raw = max(1, raw)
        is_crit = random.random() < self.player.attributes.get_crit_chance()
        if is_crit:
            raw = max(1, int(raw * 1.5))
        dealt = target.take_damage(raw)
        self._combat_ui.display_damage(
            self.player, target, dealt, is_crit=is_crit,
            target_index=target_index, attacker_is_player=True,
        )

    def _enemy_strike(self, enemy, enemy_index, defending):
        if random.random() < self.player.attributes.get_dodge_chance():
            self._combat_ui.display_damage(
                enemy, self.player, 0, is_dodged=True,
                target_index=enemy_index, attacker_is_player=False,
            )
            return
        raw = int(enemy.attack())
        if defending:
            raw = max(1, raw // 2)
        is_crit = random.random() < enemy.attributes.get_crit_chance()
        if is_crit:
            raw = max(1, int(raw * 1.5))
        self.player.take_damage(raw)
        self._combat_ui.display_damage(
            enemy, self.player, raw, is_crit=is_crit,
            target_index=enemy_index, attacker_is_player=False,
        )

    def run(self, enemies):
        alive = [e for e in enemies if e.is_alive()]
        if not alive:
            return

        # Track stable indices so the UI can keep matching portraits/enemies.
        self._ui.enter_combat(self.player, enemies)
        try:
            self._ui.show_text("\n🔥 Бій розпочався!")
            while self.player.is_alive() and any(e.is_alive() for e in enemies):
                self._combat_ui.display_combat_status(
                    self.player, [e for e in enemies if e.is_alive()],
                )
                self._combat_ui.display_combat_actions()
                choice = self._ui.get_input("\nБій — ваш вибір: ").strip()
                defending = False

                if choice == "1":
                    target_index, target = self._first_alive(enemies)
                    if target is not None:
                        was_alive = target.is_alive()
                        self._player_strike(target, target_index)
                        self._ui.update_combat_state(self.player, enemies)
                        if was_alive and not target.is_alive():
                            self._ui.mark_enemy_dead(target_index)
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
                        pick = self._ui.get_input(
                            "Номер предмета (Enter — скасувати): "
                        ).strip()
                        if pick.isdigit() and 1 <= int(pick) <= len(consumables):
                            self.player.use_item(consumables[int(pick) - 1])
                            self._ui.update_combat_state(self.player, enemies)
                elif choice == "4":
                    flee_roll = 0.35 + self.player.attributes.agility * 0.02
                    if random.random() < min(flee_roll, 0.75):
                        self._ui.show_text("Вам вдалося втекти з бою.")
                        return
                    self._ui.show_text("Втеча не вдалася!")
                else:
                    self._ui.show_text("Невідома команда. Спробуйте 1–4.")
                    continue

                if not any(e.is_alive() for e in enemies):
                    break

                for idx, enemy in enumerate(enemies):
                    if not self.player.is_alive():
                        break
                    if not enemy.is_alive():
                        continue
                    if enemy.select_action() == "attack":
                        self._enemy_strike(enemy, idx, defending)
                        self._ui.update_combat_state(self.player, enemies)

            if not self.player.is_alive():
                return
            if not any(e.is_alive() for e in enemies):
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
                # Brief pause so the player sees the skull + result before
                # the screen returns to the main view.
                self._ui.get_input("\nНатисніть Enter, щоб продовжити...")
        finally:
            self._ui.exit_combat()

    @staticmethod
    def _first_alive(enemies):
        for idx, enemy in enumerate(enemies):
            if enemy.is_alive():
                return idx, enemy
        return -1, None
