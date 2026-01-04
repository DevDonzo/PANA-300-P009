"""Input validation for calculator."""

from calculator.errors import (
    InvalidOperatorError,
    InvalidNumberError,
    InvalidExpressionError,
)


class InputValidator:
    """Validates user input for the calculator."""

    @staticmethod
    def validate_digit(char: str) -> bool:
        """Check if character is a valid digit (0-9)."""
        if not isinstance(char, str) or len(char) != 1:
            return False
        return char.isdigit()

    @staticmethod
    def validate_operator(op: str) -> bool:
        """Check if operator is valid (+, -, ×, ÷, *, /)."""
        valid_ops = ['+', '-', '×', '÷', '*', '/']
        if op not in valid_ops:
            raise InvalidOperatorError(op)
        return True

    @staticmethod
    def validate_decimal_point(display: str) -> bool:
        """Check if decimal point can be added to display."""
        display_str = str(display)
        if '.' in display_str:
            raise InvalidExpressionError("Decimal point already present")
        return True

    @staticmethod
    def validate_expression(expr: str) -> bool:
        """Validate basic expression syntax."""
        if not expr or not isinstance(expr, str):
            raise InvalidExpressionError("Empty expression")

        # Strip whitespace
        expr = expr.strip()

        # Check for valid characters
        valid_chars = set('0123456789+-×÷*/.() ')
        if not all(c in valid_chars for c in expr):
            raise InvalidExpressionError("Invalid characters in expression")

        # Check for consecutive operators (except at start for negation)
        operators = ['+', '-', '×', '÷', '*', '/']
        for i, char in enumerate(expr):
            if char in operators and i > 0:
                prev_char = expr[i - 1].strip()
                if prev_char and prev_char in operators:
                    raise InvalidExpressionError("Consecutive operators")

        # Check for incomplete expressions (ending with operator)
        if expr[-1] in operators and expr[-1] != '-':
            raise InvalidExpressionError("Incomplete expression")

        return True
