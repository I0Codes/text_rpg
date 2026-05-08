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
