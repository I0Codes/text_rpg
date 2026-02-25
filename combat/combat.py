import random


class Combat:
    """Система боротьби"""
    
    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy

    def handle_combat(self):
        """Основний цикл боротьби"""
        print(f"\n⚔️ Ви зустріли {self.enemy.name}!\n")
        
        while self.hero.is_alive() and self.enemy.is_alive():
            # Атака героя
            hero_damage = self.hero.deal_damage()
            self.enemy.take_damage(hero_damage)
            print(f"Ви атакуєте на {hero_damage} шкоди! HP {self.enemy.name}: {self.enemy.hp}")
            
            if not self.enemy.is_alive():
                break
            
            # Атака ворога
            enemy_damage = self.enemy.deal_damage()
            self.hero.take_damage(enemy_damage)
            print(f"{self.enemy.name} атакує на {enemy_damage} шкоди! Ваше HP: {self.hero.hp}\n")
        
        # Результат
        if self.hero.is_alive():
            loot = self.enemy.get_loot()
            self.hero.gain_experience(loot['exp'])
            self.hero.gain_gold(loot['gold'])
            print(f"✨ Перемога! +{loot['exp']} XP, +{loot['gold']} Gold\n")
            return True
        else:
            print(f"💀 Ви загинули!\n")
            return False