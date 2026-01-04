"""Public library API for iOS-style CLI Calculator.

This module provides the main entry point for programmatic access to the calculator.
It encapsulates the core calculation logic and error handling.
"""

from decimal import Decimal
from calculator.engine import Calculator
from calculator.errors import CalculatorError


def calculate(expression: str) -> str:
    """Calculate a mathematical expression and return the formatted result.

    Args:
        expression: A mathematical expression string (e.g., "5 + 3", "10 * 2.5")

    Returns:
        Formatted result as a string (e.g., "8", "25")

    Raises:
        CalculatorError: If the expression is invalid or contains unsupported operations
        DivisionByZeroError: If attempting to divide by zero
        InvalidExpressionError: If the expression syntax is malformed
    """
    calc = Calculator()
    result = calc.calculate(expression)
    return calc.format_result(result)


__all__ = ["calculate"]
