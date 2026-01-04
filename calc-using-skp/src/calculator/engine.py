"""Core calculator engine."""

from decimal import Decimal, ROUND_HALF_UP
from calculator.parser import ExpressionParser
from calculator.errors import DivisionByZeroError, InvalidOperatorError


class Calculator:
    """Main calculator engine for arithmetic operations."""

    def __init__(self):
        self.parser = ExpressionParser()

    def perform_operation(self, left: Decimal, op: str, right: Decimal) -> Decimal:
        """Perform a single arithmetic operation.

        Args:
            left: Left operand (Decimal)
            op: Operator (+, -, ×, ÷, *, /)
            right: Right operand (Decimal)

        Returns:
            Decimal: Result of operation

        Raises:
            DivisionByZeroError: If dividing by zero
            InvalidOperatorError: If operator is not supported
        """
        # Normalize operators
        if op == '×':
            op = '*'
        elif op == '÷':
            op = '/'

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == Decimal('0'):
                raise DivisionByZeroError()
            return left / right
        else:
            raise InvalidOperatorError(op)

    def calculate(self, expression: str) -> Decimal:
        """Calculate result of expression.

        Args:
            expression: Mathematical expression as string

        Returns:
            Decimal: Result of calculation

        Raises:
            Exception: Various calculator errors
        """
        return self.parser.parse(expression)

    def format_result(self, result: Decimal) -> str:
        """Format decimal result for display.

        Args:
            result: Decimal result to format

        Returns:
            str: Formatted result with max 10 decimal places, trailing zeros removed
        """
        # Quantize to 10 decimal places
        quantized = result.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)

        # Convert to string and remove trailing zeros
        result_str = str(quantized)

        # Remove trailing zeros after decimal point
        if '.' in result_str:
            result_str = result_str.rstrip('0').rstrip('.')

        return result_str
