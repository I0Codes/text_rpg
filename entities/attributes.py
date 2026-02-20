class Attributes:
	"""Атрибути персонажа та похідні бонуси."""

	def __init__(self, strength=0, intelligence=0, agility=0, luck=0):
		self.strength = int(strength)
		self.intelligence = int(intelligence)
		self.agility = int(agility)
		self.luck = int(luck)

	def get_physical_damage_bonus(self) -> float:
		"""Бонус до фізичного ураження: +1.5 за кожен пункт сили."""
		return 1.5 * self.strength

	def get_magic_damage_bonus(self) -> float:
		"""Бонус до магічного ураження: +2.0 за кожний пункт інтелекту."""
		return 2.0 * self.intelligence

	def get_crit_chance(self) -> float:
		"""Ймовірність критичного удару у вигляді дробу (наприклад, 0.05 для 5%).

		Формула: базова 5% + 0.5% за кожну ловкість + 0.3% за кожну удачу
		"""
		return 0.05 + 0.005 * self.agility + 0.003 * self.luck

	def get_dodge_chance(self) -> float:
		"""Ймовірність ухилення у вигляді дробу.

		Формула: базова 10% + 1% за кожну ловкість + 0.3% за кожну удачу
		"""
		return 0.10 + 0.01 * self.agility + 0.003 * self.luck

	def __str__(self) -> str:
		return (
			f"Сила: {self.strength}\n"
			f"Інтелект: {self.intelligence}\n"
			f"Ловкість: {self.agility}\n"
			f"Удача: {self.luck}\n"
			f"Бонус до фізичної шкоди: {self.get_physical_damage_bonus():.1f}\n"
			f"Бонус до магічної шкоди: {self.get_magic_damage_bonus():.1f}\n"
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

