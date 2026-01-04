"""CLI entry point for iOS-style Calculator.

Supports two modes:
1. One-shot mode: python -m calculator "5 + 3" → prints "8"
2. Interactive mode: python -m calculator → starts interactive REPL
"""

import sys
from lib import calculate
from calculator.errors import CalculatorError


def main():
    """Main entry point for CLI calculator."""
    # One-shot mode: expression provided as argument
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
        try:
            result = calculate(expression)
            print(result)
            return 0
        except CalculatorError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1

    # Interactive mode - launch GUI
    try:
        from .gui import main_gui
        main_gui()
        return 0
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("GUI mode requires: Tkinter (usually comes with Python)", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error in GUI mode: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
