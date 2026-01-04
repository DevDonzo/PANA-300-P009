"""Integration tests for error handling (User Story 4)."""

import pytest
from calculator.engine import Calculator
from calculator.errors import DivisionByZeroError, InvalidExpressionError, InvalidOperatorError


@pytest.fixture
def calc():
    """Fixture for Calculator instance."""
    return Calculator()


class TestErrorHandlingIntegration:
    """Integration tests for User Story 4: Handle Invalid Input Gracefully."""

    def test_division_by_zero(self, calc):
        """Test division by zero raises DivisionByZeroError: "5 / 0"."""
        with pytest.raises(DivisionByZeroError):
            calc.calculate("5 / 0")

    def test_invalid_operator(self, calc):
        """Test invalid operator raises InvalidExpressionError: "5 @ 3"."""
        with pytest.raises(InvalidExpressionError):
            calc.calculate("5 @ 3")

    def test_incomplete_expression(self, calc):
        """Test incomplete expression raises InvalidExpressionError: "5 +"."""
        with pytest.raises(InvalidExpressionError):
            calc.calculate("5 +")

    def test_incomplete_expression_with_operator(self, calc):
        """Test incomplete expression: "10 * " raises InvalidExpressionError."""
        with pytest.raises(InvalidExpressionError):
            calc.calculate("10 * ")

    def test_missing_closing_parenthesis(self, calc):
        """Test missing closing parenthesis raises InvalidExpressionError: "(5 + 3"."""
        with pytest.raises(InvalidExpressionError):
            calc.calculate("(5 + 3")

    def test_empty_expression(self, calc):
        """Test empty expression raises InvalidExpressionError: ""."""
        with pytest.raises(InvalidExpressionError):
            calc.calculate("")

    def test_division_by_zero_in_expression(self, calc):
        """Test division by zero in complex expression: "5 + 10 / 0"."""
        with pytest.raises(DivisionByZeroError):
            calc.calculate("5 + 10 / 0")

    def test_consecutive_operators(self, calc):
        """Test consecutive operators are handled (second is unary): "5 ++ 3" → "8"."""
        # Parser allows this - second + is unary plus
        result = calc.calculate("5 ++ 3")
        assert str(result) == "8"

    def test_multiple_decimal_points(self, calc):
        """Test multiple decimal points in one number raises error: "3.14.159"."""
        with pytest.raises(InvalidExpressionError):
            calc.calculate("3.14.159")
