"""Integration tests for negative number handling (User Story 3)."""

import pytest
from decimal import Decimal
from calculator.engine import Calculator


@pytest.fixture
def calc():
    """Fixture for Calculator instance."""
    return Calculator()


class TestNegativeNumbersIntegration:
    """Integration tests for User Story 3: Work with Negative Numbers."""

    def test_negative_input(self, calc):
        """Test negative input: "-10 + 5" → "-5"."""
        result = calc.calculate("-10 + 5")
        assert result == Decimal('-5')

    def test_subtraction_to_negative(self, calc):
        """Test subtraction resulting in negative: "5 - 10" → "-5"."""
        result = calc.calculate("5 - 10")
        assert result == Decimal('-5')

    def test_negative_multiplication(self, calc):
        """Test negative multiplication: "-4 * -3" → "12"."""
        result = calc.calculate("-4 * -3")
        assert result == Decimal('12')

    def test_negative_division(self, calc):
        """Test negative division: "-10 / 2" → "-5"."""
        result = calc.calculate("-10 / 2")
        assert result == Decimal('-5')

    def test_negative_with_decimals(self, calc):
        """Test negative with decimals: "-3.5 + 1.5" → "-2"."""
        result = calc.calculate("-3.5 + 1.5")
        assert result == Decimal('-2')

    def test_negative_multiplication_mixed(self, calc):
        """Test mixed sign multiplication: "-5 * 3" → "-15"."""
        result = calc.calculate("-5 * 3")
        assert result == Decimal('-15')

    def test_negative_with_pemdas(self, calc):
        """Test negative with PEMDAS: "-2 + 3 * 4" → "10"."""
        result = calc.calculate("-2 + 3 * 4")
        assert result == Decimal('10')

    def test_unary_minus_parentheses(self, calc):
        """Test unary minus with parentheses: "-(5 + 3)" → "-8"."""
        result = calc.calculate("-(5 + 3)")
        assert result == Decimal('-8')

    def test_double_negative(self, calc):
        """Test double negative: "--5" → "5"."""
        result = calc.calculate("--5")
        assert result == Decimal('5')
