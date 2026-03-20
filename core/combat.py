import random

from ui.combat_ui import CombatUI


class Combat:
    """Текстовий бій: гравець ходить першим, потім усі живі вороги."""

    def __init__(self, player):
        self.player = player

    def _player_strike(self, target):
        if random.random() < target.attributes.get_dodge_chance():
            CombatUI.display_damage(self.player, target, 0, is_dodged=True)
            return
        raw = int(self.player.calculate_physical_damage()) + random.randint(-2, 2)
        raw = max(1, raw)
        is_crit = random.random() < self.player.attributes.get_crit_chance()
        if is_crit:
            raw = max(1, int(raw * 1.5))
        dealt = target.take_damage(raw)
        CombatUI.display_damage(self.player, target, dealt, is_crit=is_crit)

    def _enemy_strike(self, enemy, defending):
        if random.random() < self.player.attributes.get_dodge_chance():
            CombatUI.display_damage(enemy, self.player, 0, is_dodged=True)
            return
        raw = int(enemy.attack())
        if defending:
            raw = max(1, raw // 2)
        is_crit = random.random() < enemy.attributes.get_crit_chance()
        if is_crit:
            raw = max(1, int(raw * 1.5))
        self.player.take_damage(raw)
        CombatUI.display_damage(enemy, self.player, raw, is_crit=is_crit)

    def run(self, enemies):
        alive = [e for e in enemies if e.is_alive()]
        if not alive:
            return

        print("\n🔥 Бій розпочався!")
        while self.player.is_alive() and alive:
            alive = [e for e in alive if e.is_alive()]
            if not alive:
                break

            CombatUI.display_combat_status(self.player, alive)
            CombatUI.display_combat_actions()
            choice = input("\nБій — ваш вибір: ").strip()
            defending = False

            if choice == "1":
                self._player_strike(alive[0])
            elif choice == "2":
                defending = True
                print("Ви зайняли оборону (наступні удари по вам слабші).")
            elif choice == "3":
                consumables = self.player.inventory.get_items_by_type("consumable")
                if not consumables:
                    print("Немає споживних предметів.")
                else:
                    for i, it in enumerate(consumables, 1):
                        q = f" x{it.quantity}" if it.stackable else ""
                        print(f"  {i}. {it.name}{q}")
                    pick = input("Номер предмета (Enter — скасувати): ").strip()
                    if pick.isdigit() and 1 <= int(pick) <= len(consumables):
                        self.player.use_item(consumables[int(pick) - 1])
            elif choice == "4":
                flee_roll = 0.35 + self.player.attributes.agility * 0.02
                if random.random() < min(flee_roll, 0.75):
                    print("Вам вдалося втекти з бою.")
                    return
                print("Втеча не вдалася!")
            else:
                print("Невідома команда. Спробуйте 1–4.")
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
            print("\n🏆 Перемога!")
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
                print(f"💰 Золото: +{total_gold}")
