"""Interactive calculator interface - Simple REPL mode."""

from calculator.engine import Calculator
from calculator.errors import CalculatorError


class InteractiveCalculator:
    """Interactive mode calculator with simple REPL interface."""

    def __init__(self):
        """Initialize the interactive calculator."""
        self.calc = Calculator()

    def run(self):
        """Run the interactive calculator REPL loop."""
        print("\n" + "="*60)
        print("   📱 iOS-Style CLI Calculator - Interactive Mode")
        print("="*60)
        print("\nEnter math expressions (type 'quit' or 'exit' to exit):")
        print("\nExamples:")
        print("  5 + 3           → 8")
        print("  0.1 + 0.2       → 0.3")
        print("  -10 + 5         → -5")
        print("  (2 + 3) * 4     → 20")
        print("  5 + 3 * 2       → 11  (PEMDAS order)")
        print("-"*60 + "\n")

        while True:
            try:
                # Get user input
                expression = input("➜ ").strip()

                # Check for quit
                if expression.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Calculator closed.\n")
                    break

                # Skip empty input
                if not expression:
                    continue

                # Calculate and display result
                result = self.calc.calculate(expression)
                formatted = self.calc.format_result(result)
                print(f"✓ Result: {formatted}\n")

            except CalculatorError as e:
                print(f"❌ Error: {e}\n")
            except KeyboardInterrupt:
                print("\n\n👋 Calculator closed.\n")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}\n")


def main_interactive():
    """Entry point for interactive mode."""
    calc = InteractiveCalculator()
    calc.run()


if __name__ == "__main__":
    main_interactive()
