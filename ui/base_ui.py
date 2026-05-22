from abc import ABC, abstractmethod


class GameUI(ABC):
    """Contract that all UI backends must satisfy.

    Subclasses implement the four primitives; everything else has a default
    implementation built on those primitives, so any subclass is substitutable
    anywhere a GameUI is expected (Liskov Substitution Principle).
    """

    @abstractmethod
    def show_text(self, text: str) -> None:
        """Append a line of text to the game output."""

    @abstractmethod
    def show_separator(self) -> None:
        """Display a visual section separator."""

    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Show *prompt* and return the user's response as a string."""

    @abstractmethod
    def confirm(self, question: str) -> bool:
        """Ask a yes/no question; return True if the user confirms."""

    # ------------------------------------------------------------------
    # Non-abstract helpers — override for richer presentation
    # ------------------------------------------------------------------

    def show_status(self, text: str) -> None:
        self.show_text(text)

    def show_actions(self, actions: dict) -> None:
        self.show_text("\nДоступні дії:")
        for key, description in actions.items():
            self.show_text(f"  {key} — {description}")

    # ------------------------------------------------------------------
    # Combat screen hooks — overridden by graphical backends. Defaults
    # are no-ops so console UI keeps its text-only behaviour.
    # ------------------------------------------------------------------

    def enter_combat(self, player, enemies) -> None:
        """Called once when a combat encounter begins."""

    def exit_combat(self) -> None:
        """Called once when a combat encounter ends (victory / flee / death)."""

    def update_combat_state(self, player, enemies) -> None:
        """Refresh HP bars and other live combat info."""

    def show_combat_log(self, text: str) -> None:
        """Append a line to the combat log. Defaults to show_text."""
        self.show_text(text)

    def animate_player_attack(self, target_index: int, outcome: str) -> None:
        """Flash effect when the player strikes target_index.

        outcome ∈ {"hit", "crit", "miss", "dodge", "blocked"}.
        """

    def animate_enemy_attack(self, enemy_index: int, outcome: str) -> None:
        """Flash effect when an enemy strikes the player."""

    def mark_enemy_dead(self, enemy_index: int) -> None:
        """Swap the enemy image to a skull / death indicator."""
