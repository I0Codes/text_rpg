from core import Game
from entities import Character, Enemy
from world import Forest
from items import Item
from ui.combat_ui import CombatUI

def main():
    """Точка входу в гру"""
    # Створюємо персонажа
    player = Character(name="Hero", hp=100, max_hp=100, stamina=50, max_stamina=50)
    # демонстрація інвентарю

    potion = Item(item_type="consumable", name="Зілля здоров'я", description="Відновлює 50 HP", weight=0.5, value=0, stackable=True, quantity=1)
    player.add_item(potion)
    player.inventory.show_inventory()

    # Демонстрація бою
    enemy = Enemy(name="Гоблін", hp=50, attack=10, defense=5, level=1, xp_reward=20, reward_gold=5)
    CombatUI.display_combat_status(player, [enemy])
    CombatUI.display_combat_actions()
    CombatUI.display_damage(player, enemy, 25, is_crit=True)
    CombatUI.display_damage(enemy, player, 10)
    CombatUI.display_combat_log(["Герой розпочав бій.", "Гоблін атакував."])

    # Створюємо початкову локацію
    forest = Forest()
    
    # Створюємо та запускаємо гру
    game = Game(player, forest)
    game.run()

# TODO: інтегрувати MainMenu для вибору "Нова гра" / "Завантажити гру"
# TODO: додати вибір класу персонажа (Warrior, Mage, Scout)
# TODO: додати можливість вводити ім'я персонажа

if __name__ == "__main__":
    main()
