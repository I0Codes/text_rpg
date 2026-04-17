from config.settings import (
    STRENGTH_DAMAGE_MULTIPLIER,
    STRENGTH_HP_MULTIPLIER,
    INTELLIGENCE_MANA_MULTIPLIER,
    INTELLIGENCE_DAMAGE_MULTIPLIER,
    BASE_CRIT_CHANCE,
    BASE_DODGE_CHANCE,
    AGILITY_CRIT_BONUS,
    AGILITY_DODGE_BONUS,
    LUCK_BONUS_MULTIPLIER
)

class Attributes:
	"""Атрибути персонажа та похідні бонуси."""

	def __init__(self, strength=0, intelligence=0, agility=0, luck=0):
		self.strength = int(strength)
		self.intelligence = int(intelligence)
		self.agility = int(agility)
		self.luck = int(luck)

	def update(self, strength=None, intelligence=None, agility=None, luck=None):
		"""Оновити атрибути на основі переданих параметрів.
		
		Приклад: attributes.update(strength=10, agility=5)
		"""
		if strength is not None:
			self.strength = int(strength)
		if intelligence is not None:
			self.intelligence = int(intelligence)
		if agility is not None:
			self.agility = int(agility)
		if luck is not None:
			self.luck = int(luck)

	def get_physical_damage_bonus(self) -> float:
		"""Бонус до фізичного ураження: +1.5 за кожен пункт сили."""
		return STRENGTH_DAMAGE_MULTIPLIER * self.strength

	def get_magic_damage_bonus(self) -> float:
		"""Бонус до магічного ураження: +2.0 за кожний пункт інтелекту."""
		return INTELLIGENCE_DAMAGE_MULTIPLIER * self.intelligence

	def get_crit_chance(self) -> float:
		"""Ймовірність критичного удару у вигляді дробу (наприклад, 0.05 для 5%).

		Формула: базова 5% + 0.5% за кожну ловкість + 0.3% за кожну удачу
		"""
		return BASE_CRIT_CHANCE + AGILITY_CRIT_BONUS * self.agility + LUCK_BONUS_MULTIPLIER * self.luck

	def get_dodge_chance(self) -> float:
		"""Ймовірність ухилення у вигляді дробу.

		Формула: базова 10% + 1% за кожну ловкість + 0.3% за кожну удачу
		"""
		return BASE_DODGE_CHANCE + AGILITY_DODGE_BONUS * self.agility + LUCK_BONUS_MULTIPLIER * self.luck

	def get_hp_bonus(self) -> float:
		"""Бонус до здоров'я від сили."""
		return STRENGTH_HP_MULTIPLIER * self.strength

	def get_mana_bonus(self) -> float:
		"""Бонус до мани від інтелекту."""
		return INTELLIGENCE_MANA_MULTIPLIER * self.intelligence

	def __str__(self) -> str:
		return (
			f"Сила: {self.strength}\n"
			f"Інтелект: {self.intelligence}\n"
			f"Ловкість: {self.agility}\n"
			f"Удача: {self.luck}\n"
			f"Бонус до фізичної шкоди: {self.get_physical_damage_bonus():.1f}\n"
			f"Бонус до магічної шкоди: {self.get_magic_damage_bonus():.1f}\n"
			f"Бонус до здоров'я: {self.get_hp_bonus():.1f}\n"
			f"Бонус до мани: {self.get_mana_bonus():.1f}\n"
			f"Шанс криту: {self.get_crit_chance():.1%}\n"
			f"Шанс ухилення: {self.get_dodge_chance():.1%}"
		)


if __name__ == "__main__":
	# Приклад використання/демо
	attrs = Attributes(strength=10, intelligence=5, agility=8, luck=6)
	print(attrs.get_physical_damage_bonus())
	print(f"Шанс криту: {attrs.get_crit_chance():.1%}")
	print()
	print(attrs)

