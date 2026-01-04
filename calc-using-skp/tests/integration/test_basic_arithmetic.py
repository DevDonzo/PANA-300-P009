"""Integration tests for basic arithmetic operations (User Story 1)."""

import pytest
from decimal import Decimal
from calculator.engine import Calculator


@pytest.fixture
def calc():
    """Fixture for Calculator instance."""
    return Calculator()


class TestBasicArithmeticIntegration:
    """Integration tests for User Story 1: Basic Arithmetic Operations."""

    def test_addition_simple(self, calc):
        """Test simple addition: "10 + 5" → "15"."""
        result = calc.calculate("10 + 5")
        assert result == Decimal('15')

    def test_subtraction_simple(self, calc):
        """Test simple subtraction: "20 - 8" → "12"."""
        result = calc.calculate("20 - 8")
        assert result == Decimal('12')

    def test_multiplication_simple(self, calc):
        """Test simple multiplication: "6 * 7" → "42"."""
        result = calc.calculate("6 * 7")
        assert result == Decimal('42')

    def test_division_simple(self, calc):
        """Test simple division: "15 / 3" → "5"."""
        result = calc.calculate("15 / 3")
        assert result == Decimal('5')

    def test_continuous_calculation(self, calc):
        """Test continuous calculation: "5 + 3 + 2" → "10"."""
        result = calc.calculate("5 + 3 + 2")
        assert result == Decimal('10')

    def test_mixed_operations(self, calc):
        """Test mixed operations with PEMDAS: "2 + 3 * 4" → "14"."""
        result = calc.calculate("2 + 3 * 4")
        assert result == Decimal('14')

    def test_parentheses(self, calc):
        """Test parentheses override precedence: "(2 + 3) * 4" → "20"."""
        result = calc.calculate("(2 + 3) * 4")
        assert result == Decimal('20')

    def test_result_formatting_integer(self, calc):
        """Test that integer results are formatted without decimals: 5 → "5"."""
        result = calc.calculate("10 / 2")
        formatted = calc.format_result(result)
        assert formatted == "5"

    def test_result_formatting_decimal(self, calc):
        """Test that decimal results maintain precision: "10.5 / 2" → "5.25"."""
        result = calc.calculate("10.5 / 2")
        formatted = calc.format_result(result)
        assert formatted == "5.25"
