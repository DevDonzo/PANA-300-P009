"""Expression parser with recursive descent and PEMDAS support."""

import re
from decimal import Decimal
from calculator.errors import (
    InvalidExpressionError,
    DivisionByZeroError,
    InvalidOperatorError,
)


class ExpressionParser:
    """Recursive descent parser with operator precedence (PEMDAS)."""

    def __init__(self):
        self.tokens = []
        self.pos = 0

    def parse(self, expression: str) -> Decimal:
        """Parse and evaluate expression with PEMDAS.

        Args:
            expression: Mathematical expression as string

        Returns:
            Decimal: Result of calculation

        Raises:
            InvalidExpressionError: For malformed expressions
            DivisionByZeroError: For division by zero
        """
        expr = expression.strip()
        if not expr:
            raise InvalidExpressionError("Empty expression")

        # Tokenize
        self.tokens = self._tokenize(expr)
        self.pos = 0

        if not self.tokens:
            raise InvalidExpressionError("No tokens to parse")

        result = self._parse_addition()

        if self.pos < len(self.tokens):
            raise InvalidExpressionError(f"Unexpected token: {self.tokens[self.pos]}")

        return result

    def _tokenize(self, expr: str) -> list:
        """Split expression into tokens."""
        # Replace × with * and ÷ with / for consistent parsing
        expr = expr.replace('×', '*').replace('÷', '/')

        # Tokenize: numbers (including decimals), operators, parentheses
        pattern = r'(-?\d+\.?\d*|[+\-*/()\s])'
        tokens = re.findall(pattern, expr)

        # Filter out whitespace
        tokens = [t for t in tokens if t and not t.isspace()]

        if not tokens:
            raise InvalidExpressionError("No valid tokens in expression")

        return tokens

    def _current_token(self) -> str:
        """Get current token without advancing."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ''

    def _advance(self) -> str:
        """Get current token and advance position."""
        token = self._current_token()
        self.pos += 1
        return token

    def _peek_token(self) -> str:
        """Get next token without advancing."""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return ''

    def _parse_addition(self) -> Decimal:
        """Parse addition and subtraction (lowest precedence)."""
        left = self._parse_multiplication()

        while self._current_token() in ['+', '-']:
            op = self._advance()
            right = self._parse_multiplication()
            if op == '+':
                left = left + right
            else:  # op == '-'
                left = left - right

        return left

    def _parse_multiplication(self) -> Decimal:
        """Parse multiplication and division (higher precedence)."""
        left = self._parse_unary()

        while self._current_token() in ['*', '/']:
            op = self._advance()
            right = self._parse_unary()
            if op == '*':
                left = left * right
            elif op == '/':
                if right == Decimal('0'):
                    raise DivisionByZeroError()
                left = left / right

        return left

    def _parse_unary(self) -> Decimal:
        """Parse unary minus and parentheses (highest precedence)."""
        token = self._current_token()

        # Handle unary minus
        if token == '-':
            self._advance()
            return -self._parse_unary()

        # Handle unary plus
        if token == '+':
            self._advance()
            return self._parse_unary()

        # Handle parentheses
        if token == '(':
            self._advance()
            result = self._parse_addition()
            if self._current_token() != ')':
                raise InvalidExpressionError("Missing closing parenthesis")
            self._advance()
            return result

        # Parse number
        return self._parse_number()

    def _parse_number(self) -> Decimal:
        """Parse a number (integer or decimal)."""
        token = self._current_token()

        if not token:
            raise InvalidExpressionError("Expected number, got end of expression")

        # Check if token is a number
        try:
            return Decimal(self._advance())
        except Exception:
            raise InvalidExpressionError(f"Expected number, got {token}")
