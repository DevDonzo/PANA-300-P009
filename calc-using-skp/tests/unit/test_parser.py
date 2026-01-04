"""Unit tests for expression parser with PEMDAS support."""

import pytest
from decimal import Decimal
from calculator.parser import ExpressionParser
from calculator.errors import InvalidExpressionError, DivisionByZeroError


@pytest.fixture
def parser():
    """Fixture for ExpressionParser instance."""
    return ExpressionParser()


class TestBasicOperations:
    """Tests for basic arithmetic operations."""

    def test_parse_simple_addition(self, parser):
        """Test simple addition: "5 + 3" → 8."""
        result = parser.parse("5 + 3")
        assert result == Decimal('8')

    def test_parse_simple_subtraction(self, parser):
        """Test simple subtraction: "10 - 4" → 6."""
        result = parser.parse("10 - 4")
        assert result == Decimal('6')

    def test_parse_simple_multiplication(self, parser):
        """Test simple multiplication: "6 * 7" → 42."""
        result = parser.parse("6 * 7")
        assert result == Decimal('42')

    def test_parse_simple_division(self, parser):
        """Test simple division: "15 / 3" → 5."""
        result = parser.parse("15 / 3")
        assert result == Decimal('5')


class TestPEMDAS:
    """Tests for PEMDAS (operator precedence)."""

    def test_parse_pemdas_multiplication_first(self, parser):
        """Test PEMDAS: "5 + 3 * 2" → 11 (not 16)."""
        result = parser.parse("5 + 3 * 2")
        assert result == Decimal('11')

    def test_parse_pemdas_division_first(self, parser):
        """Test PEMDAS: "10 + 20 / 2" → 20."""
        result = parser.parse("10 + 20 / 2")
        assert result == Decimal('20')

    def test_parse_pemdas_complex(self, parser):
        """Test PEMDAS with multiple operations: "2 + 3 * 4 - 5" → 9."""
        result = parser.parse("2 + 3 * 4 - 5")
        assert result == Decimal('9')

    def test_parse_pemdas_all_multiplication_division(self, parser):
        """Test left-to-right for same precedence: "20 / 4 * 3" → 15."""
        result = parser.parse("20 / 4 * 3")
        assert result == Decimal('15')


class TestNegativeNumbers:
    """Tests for negative number handling."""

    def test_parse_negative_numbers(self, parser):
        """Test negative input: "-5 + 3" → -2."""
        result = parser.parse("-5 + 3")
        assert result == Decimal('-2')

    def test_parse_double_negative(self, parser):
        """Test double negative: "-4 * -3" → 12."""
        result = parser.parse("-4 * -3")
        assert result == Decimal('12')

    def test_parse_negative_result(self, parser):
        """Test operation resulting in negative: "5 - 10" → -5."""
        result = parser.parse("5 - 10")
        assert result == Decimal('-5')

    def test_parse_unary_minus_with_parentheses(self, parser):
        """Test unary minus: "-(5 + 3)" → -8."""
        result = parser.parse("-(5 + 3)")
        assert result == Decimal('-8')


class TestDecimalNumbers:
    """Tests for decimal number handling."""

    def test_parse_decimal_numbers(self, parser):
        """Test decimals: "3.5 + 2.1" → 5.6."""
        result = parser.parse("3.5 + 2.1")
        assert result == Decimal('5.6')

    def test_parse_decimal_multiplication(self, parser):
        """Test decimal multiplication: "3.14 * 2" → 6.28."""
        result = parser.parse("3.14 * 2")
        assert result == Decimal('6.28')

    def test_parse_decimal_division(self, parser):
        """Test decimal division: "10.5 / 2" → 5.25."""
        result = parser.parse("10.5 / 2")
        assert result == Decimal('5.25')

    def test_parse_floating_point_precision(self, parser):
        """Test precision: "0.1 + 0.2" → 0.3 (not 0.30000000001)."""
        result = parser.parse("0.1 + 0.2")
        assert result == Decimal('0.3')


class TestErrors:
    """Tests for error handling."""

    def test_parse_division_by_zero(self, parser):
        """Test division by zero raises DivisionByZeroError."""
        with pytest.raises(DivisionByZeroError):
            parser.parse("5 / 0")

    def test_parse_incomplete_expression_trailing_operator(self, parser):
        """Test incomplete expression: "5 +" raises InvalidExpressionError."""
        with pytest.raises(InvalidExpressionError):
            parser.parse("5 +")

    def test_parse_empty_expression(self, parser):
        """Test empty expression raises InvalidExpressionError."""
        with pytest.raises(InvalidExpressionError):
            parser.parse("")

    def test_parse_consecutive_operators(self, parser):
        """Test consecutive operators: "5 ++ 3" is treated as "5 + (+3)"."""
        # Parser allows "5 ++ 3" because second + is unary plus
        result = parser.parse("5 ++ 3")
        assert result == Decimal('8')

    def test_parse_missing_closing_parenthesis(self, parser):
        """Test missing closing parenthesis raises InvalidExpressionError."""
        with pytest.raises(InvalidExpressionError):
            parser.parse("(5 + 3")


class TestParentheses:
    """Tests for parentheses handling."""

    def test_parse_parentheses_override_precedence(self, parser):
        """Test parentheses: "(5 + 3) * 2" → 16 (not 11)."""
        result = parser.parse("(5 + 3) * 2")
        assert result == Decimal('16')

    def test_parse_nested_parentheses(self, parser):
        """Test nested: "((5 + 3) * 2) - 1" → 15."""
        result = parser.parse("((5 + 3) * 2) - 1")
        assert result == Decimal('15')

    def test_parse_parentheses_with_negation(self, parser):
        """Test negation in parentheses: "-(5 - 3)" → -2."""
        result = parser.parse("-(5 - 3)")
        assert result == Decimal('-2')


class TestOperatorSymbols:
    """Tests for different operator symbol representations."""

    def test_parse_times_symbol(self, parser):
        """Test multiplication with × symbol: "6 × 7" → 42."""
        result = parser.parse("6 × 7")
        assert result == Decimal('42')

    def test_parse_divide_symbol(self, parser):
        """Test division with ÷ symbol: "15 ÷ 3" → 5."""
        result = parser.parse("15 ÷ 3")
        assert result == Decimal('5')

    def test_parse_asterisk_symbol(self, parser):
        """Test multiplication with * symbol: "6 * 7" → 42."""
        result = parser.parse("6 * 7")
        assert result == Decimal('42')

    def test_parse_slash_symbol(self, parser):
        """Test division with / symbol: "15 / 3" → 5."""
        result = parser.parse("15 / 3")
        assert result == Decimal('5')
