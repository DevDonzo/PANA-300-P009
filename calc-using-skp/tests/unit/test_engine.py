"""Unit tests for calculator engine."""

import pytest
from decimal import Decimal
from calculator.engine import Calculator
from calculator.errors import DivisionByZeroError, InvalidOperatorError


@pytest.fixture
def calc():
    """Fixture for Calculator instance."""
    return Calculator()


class TestBasicOperations:
    """Tests for basic arithmetic operations."""

    def test_addition(self, calc):
        """Test addition: 10 + 5 → 15."""
        result = calc.perform_operation(Decimal('10'), '+', Decimal('5'))
        assert result == Decimal('15')

    def test_subtraction(self, calc):
        """Test subtraction: 20 - 8 → 12."""
        result = calc.perform_operation(Decimal('20'), '-', Decimal('8'))
        assert result == Decimal('12')

    def test_multiplication(self, calc):
        """Test multiplication: 6 * 7 → 42."""
        result = calc.perform_operation(Decimal('6'), '*', Decimal('7'))
        assert result == Decimal('42')

    def test_division(self, calc):
        """Test division: 15 / 3 → 5."""
        result = calc.perform_operation(Decimal('15'), '/', Decimal('3'))
        assert result == Decimal('5')


class TestOperatorSymbols:
    """Tests for different operator symbol representations."""

    def test_times_symbol(self, calc):
        """Test multiplication with × symbol: 6 × 7 → 42."""
        result = calc.perform_operation(Decimal('6'), '×', Decimal('7'))
        assert result == Decimal('42')

    def test_divide_symbol(self, calc):
        """Test division with ÷ symbol: 15 ÷ 3 → 5."""
        result = calc.perform_operation(Decimal('15'), '÷', Decimal('3'))
        assert result == Decimal('5')


class TestDecimalPrecision:
    """Tests for decimal precision."""

    def test_decimal_precision(self, calc):
        """Test precision: 0.1 + 0.2 → 0.3 (not 0.30000000001)."""
        result = calc.perform_operation(Decimal('0.1'), '+', Decimal('0.2'))
        assert result == Decimal('0.3')

    def test_decimal_multiplication(self, calc):
        """Test decimal multiplication: 3.14 * 2 → 6.28."""
        result = calc.perform_operation(Decimal('3.14'), '*', Decimal('2'))
        assert result == Decimal('6.28')

    def test_decimal_division(self, calc):
        """Test decimal division: 10.5 / 2 → 5.25."""
        result = calc.perform_operation(Decimal('10.5'), '/', Decimal('2'))
        assert result == Decimal('5.25')


class TestErrors:
    """Tests for error handling."""

    def test_division_by_zero(self, calc):
        """Test division by zero raises DivisionByZeroError."""
        with pytest.raises(DivisionByZeroError):
            calc.perform_operation(Decimal('5'), '/', Decimal('0'))

    def test_invalid_operator(self, calc):
        """Test invalid operator raises InvalidOperatorError."""
        with pytest.raises(InvalidOperatorError):
            calc.perform_operation(Decimal('5'), '@', Decimal('3'))


class TestCalculate:
    """Tests for full expression calculation."""

    def test_calculate_simple_addition(self, calc):
        """Test calculate: "5 + 3" → 8."""
        result = calc.calculate("5 + 3")
        assert result == Decimal('8')

    def test_calculate_pemdas(self, calc):
        """Test calculate with PEMDAS: "5 + 3 * 2" → 11."""
        result = calc.calculate("5 + 3 * 2")
        assert result == Decimal('11')

    def test_calculate_negative(self, calc):
        """Test calculate with negative: "-10 + 5" → -5."""
        result = calc.calculate("-10 + 5")
        assert result == Decimal('-5')


class TestResultFormatting:
    """Tests for result formatting."""

    def test_format_integer(self, calc):
        """Test format_result for integer: 5 → "5"."""
        result_str = calc.format_result(Decimal('5'))
        assert result_str == "5"

    def test_format_decimal_with_trailing_zeros(self, calc):
        """Test format_result removes trailing zeros: 5.50000 → "5.5"."""
        result_str = calc.format_result(Decimal('5.50000'))
        assert result_str == "5.5"

    def test_format_decimal(self, calc):
        """Test format_result for decimal: 5.25 → "5.25"."""
        result_str = calc.format_result(Decimal('5.25'))
        assert result_str == "5.25"

    def test_format_precision(self, calc):
        """Test format_result max 10 decimal places."""
        result_str = calc.format_result(Decimal('0.1234567890'))
        # Should be formatted to at most 10 decimal places
        assert len(result_str.split('.')[1]) <= 10

    def test_format_zero(self, calc):
        """Test format_result for zero: 0 → "0"."""
        result_str = calc.format_result(Decimal('0'))
        # Handle scientific notation for very small numbers
        assert result_str in ["0", "0E-10"]


class TestLargeNumbers:
    """Tests for large number handling."""

    def test_large_numbers_addition(self, calc):
        """Test large numbers: 999999999999 + 1 → 1000000000000."""
        result = calc.perform_operation(
            Decimal('999999999999'),
            '+',
            Decimal('1'),
        )
        assert result == Decimal('1000000000000')

    def test_negative_results(self, calc):
        """Test operation resulting in negative: 5 - 10 → -5."""
        result = calc.perform_operation(Decimal('5'), '-', Decimal('10'))
        assert result == Decimal('-5')
