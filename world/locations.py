class Forest:
    """Клас локації - Темний ліс"""
    
    def __init__(self):
        self.name = "Темний ліс"
    
    def get_actions(self):
        """Повертає словник доступних дій у цій локації
        
        Returns:
            dict: Словник {ключ: опис дії}
        """
        return {
            "1": "Дослідити місцевість",
            "2": "Відпочити"
        }
    
    def handle_action(self, choice, player):
        """Обробляє вибрану дію гравця
        
        Args:
            choice: Вибір гравця (ключ дії)
            player: Об'єкт гравця (Character)
        """
        if choice == "1":
            print("\nВи обережно оглядаєте ліс...")
            print("Навколо тихо, лише шелест листя.")
        elif choice == "2":
            print("\nВи знаходите затишне місце і відпочиваєте.")
            player.hp += 5
            print(f"Ви відновили 5 HP. Поточне HP: {player.hp}")
        else:
            print("\nНевідома дія.")

# TODO: додати нові локації - Village, Cave, EnemyForest
# TODO: додати систему переходів між локаціями
# TODO: додати випадкові події в локаціях
