from .base_ui import GameUI


class ConsoleUI(GameUI):
    """Terminal-based UI implementation using print() and input()."""

    def show_text(self, text: str) -> None:
        print(text)

    def show_separator(self) -> None:
        print("=" * 50)

    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def confirm(self, question: str) -> bool:
        answer = input(f"{question} (Так/Ні): ").lower()
        return answer in ["так", "т", "yes", "y"]
