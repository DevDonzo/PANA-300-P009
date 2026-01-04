"""Integration tests for decimal precision (User Story 2)."""

import pytest
from decimal import Decimal
from calculator.engine import Calculator


@pytest.fixture
def calc():
    """Fixture for Calculator instance."""
    return Calculator()


class TestDecimalPrecisionIntegration:
    """Integration tests for User Story 2: Handle Decimal Numbers and Precision."""

    def test_decimal_addition(self, calc):
        """Test decimal addition: "3.14 + 2.1" → "5.24"."""
        result = calc.calculate("3.14 + 2.1")
        assert result == Decimal('5.24')

    def test_decimal_multiplication(self, calc):
        """Test decimal multiplication: "3.14 * 2" → "6.28"."""
        result = calc.calculate("3.14 * 2")
        assert result == Decimal('6.28')

    def test_decimal_division(self, calc):
        """Test decimal division: "10.5 / 2" → "5.25"."""
        result = calc.calculate("10.5 / 2")
        assert result == Decimal('5.25')

    def test_floating_point_precision(self, calc):
        """Test floating point precision: "0.1 + 0.2" → "0.3" (CRITICAL)."""
        result = calc.calculate("0.1 + 0.2")
        assert result == Decimal('0.3')

    def test_decimal_with_integer(self, calc):
        """Test mixed decimal and integer: "5 + 2.5" → "7.5"."""
        result = calc.calculate("5 + 2.5")
        assert result == Decimal('7.5')

    def test_many_decimals(self, calc):
        """Test many decimal places: "0.1234567890 + 0.0000000001" → correct to 10 places."""
        result = calc.calculate("0.1234567890 + 0.0000000001")
        # Result should be precise, not floating point errors
        assert str(result) == "0.1234567891"

    def test_decimal_subtraction(self, calc):
        """Test decimal subtraction: "10.5 - 2.3" → "8.2"."""
        result = calc.calculate("10.5 - 2.3")
        assert result == Decimal('8.2')

    def test_decimal_with_pemdas(self, calc):
        """Test decimal with PEMDAS: "2.5 + 3.5 * 2" → "9.5"."""
        result = calc.calculate("2.5 + 3.5 * 2")
        assert result == Decimal('9.5')
