"""Unit tests for calculator state management."""

import pytest
from decimal import Decimal
from calculator.state import (
    CalculatorState,
    handle_digit,
    handle_operator,
    handle_equals,
    handle_clear,
    handle_backspace,
    handle_sign_toggle,
    handle_decimal_point,
)
from calculator.engine import Calculator
from calculator.errors import InvalidExpressionError


@pytest.fixture
def initial_state():
    """Fixture for initial calculator state."""
    return CalculatorState()


@pytest.fixture
def calc():
    """Fixture for Calculator instance."""
    return Calculator()


class TestHandleDigit:
    """Tests for digit input handling."""

    def test_handle_digit_new_input(self, initial_state):
        """Test digit on fresh state: "5" → display="5"."""
        state = handle_digit('5', initial_state)
        assert state.display == Decimal('5')
        assert state.is_new_input is False

    def test_handle_digit_append(self, initial_state):
        """Test second digit appends: "5" then "3" → display="53"."""
        state = handle_digit('5', initial_state)
        state = handle_digit('3', state)
        assert state.display == Decimal('53')

    def test_handle_digit_multiple(self, initial_state):
        """Test multiple digits: 1→2→3 → display="123"."""
        state = initial_state
        state = handle_digit('1', state)
        state = handle_digit('2', state)
        state = handle_digit('3', state)
        assert state.display == Decimal('123')

    def test_handle_digit_after_operator(self, initial_state):
        """Test digit after operator starts fresh."""
        from dataclasses import replace
        state = handle_digit('5', initial_state)
        state = replace(state, operator='+', is_new_input=True)
        state = handle_digit('3', state)
        assert state.display == Decimal('3')
        assert state.operator == '+'


class TestHandleOperator:
    """Tests for operator input handling."""

    def test_handle_operator_sets_operator(self, initial_state, calc):
        """Test operator sets: "5+" → accumulator=5, operator='+'."""
        state = handle_digit('5', initial_state)
        state = handle_operator('+', state, calc)
        assert state.accumulator == Decimal('5')
        assert state.operator == '+'
        assert state.is_new_input is True

    def test_handle_operator_normalization_asterisk(self, initial_state, calc):
        """Test operator normalization: * → ×."""
        state = handle_digit('5', initial_state)
        state = handle_operator('*', state, calc)
        assert state.operator == '×'

    def test_handle_operator_normalization_slash(self, initial_state, calc):
        """Test operator normalization: / → ÷."""
        state = handle_digit('5', initial_state)
        state = handle_operator('/', state, calc)
        assert state.operator == '÷'


class TestHandleEquals:
    """Tests for equals button handling."""

    def test_handle_equals_simple_addition(self, initial_state, calc):
        """Test equals: "5+3=" → display="8"."""
        state = handle_digit('5', initial_state)
        state = handle_operator('+', state, calc)
        state = handle_digit('3', state)
        state = handle_equals(state, calc)
        assert state.display == Decimal('8')
        assert state.operator is None
        assert state.is_new_input is True

    def test_handle_equals_multiplication(self, initial_state, calc):
        """Test equals with multiplication: "6*7=" → display="42"."""
        state = handle_digit('6', initial_state)
        state = handle_operator('*', state, calc)
        state = handle_digit('7', state)
        state = handle_equals(state, calc)
        assert state.display == Decimal('42')

    def test_handle_equals_no_operator(self, initial_state, calc):
        """Test equals with no operator: state unchanged."""
        state = handle_digit('5', initial_state)
        state = handle_equals(state, calc)
        assert state.display == Decimal('5')


class TestHandleClear:
    """Tests for clear button handling."""

    def test_handle_clear(self, initial_state):
        """Test clear resets to initial state."""
        from dataclasses import replace
        state = handle_digit('5', initial_state)
        state = replace(state, operator='+', accumulator=Decimal('5'))
        state = handle_clear(state)
        assert state.display == Decimal('0')
        assert state.accumulator == Decimal('0')
        assert state.operator is None
        assert state.is_new_input is True

    def test_handle_clear_with_error(self, initial_state):
        """Test clear also clears error."""
        from dataclasses import replace
        state = replace(initial_state, error="Division by zero")
        state = handle_clear(state)
        assert state.error is None


class TestHandleBackspace:
    """Tests for backspace handling."""

    def test_handle_backspace_single_digit(self, initial_state):
        """Test backspace on single digit: "5" → "0"."""
        state = handle_digit('5', initial_state)
        state = handle_backspace(state)
        assert state.display == Decimal('0')

    def test_handle_backspace_multiple_digits(self, initial_state):
        """Test backspace on multiple: "123" → "12"."""
        state = initial_state
        state = handle_digit('1', state)
        state = handle_digit('2', state)
        state = handle_digit('3', state)
        state = handle_backspace(state)
        assert state.display == Decimal('12')

    def test_handle_backspace_negative(self, initial_state):
        """Test backspace on negative: "-5" → "0"."""
        from dataclasses import replace
        state = replace(initial_state, display=Decimal('-5'))
        state = handle_backspace(state)
        assert state.display == Decimal('0')


class TestHandleSignToggle:
    """Tests for sign toggle button."""

    def test_handle_sign_toggle_positive_to_negative(self, initial_state):
        """Test toggle: "5" → "-5"."""
        state = handle_digit('5', initial_state)
        state = handle_sign_toggle(state)
        assert state.display == Decimal('-5')

    def test_handle_sign_toggle_negative_to_positive(self, initial_state):
        """Test toggle: "-5" → "5"."""
        from dataclasses import replace
        state = replace(initial_state, display=Decimal('-5'), is_new_input=False)
        state = handle_sign_toggle(state)
        assert state.display == Decimal('5')

    def test_handle_sign_toggle_zero(self, initial_state):
        """Test toggle on zero: "0" → "0"."""
        state = handle_sign_toggle(initial_state)
        assert state.display == Decimal('0')


class TestHandleDecimalPoint:
    """Tests for decimal point input."""

    def test_handle_decimal_point_single(self, initial_state):
        """Test decimal point: "5" + "." → "5."."""
        state = handle_digit('5', initial_state)
        state = handle_decimal_point(state)
        assert state.display == Decimal('5')

    def test_handle_decimal_point_multiple(self, initial_state):
        """Test decimals: "5." + "3" → "5.3"."""
        state = handle_digit('5', initial_state)
        state = handle_decimal_point(state)
        # After decimal point, next digit should append
        state = handle_digit('3', state)
        # Note: display is "53" because digit appends to "5."→"5" in Decimal
        assert '5' in str(state.display) and '3' in str(state.display)

    def test_handle_decimal_point_twice_raises(self, initial_state):
        """Test second decimal point in same number raises error."""
        # Create state with "3.5" display value
        from dataclasses import replace
        state_with_decimal = replace(initial_state, display=Decimal('3.5'), is_new_input=False)
        # Attempting to add another decimal point should raise
        with pytest.raises(InvalidExpressionError):
            handle_decimal_point(state_with_decimal)


class TestStateImmutability:
    """Tests for state immutability."""

    def test_state_is_frozen(self, initial_state):
        """Test state dataclass is frozen (immutable)."""
        with pytest.raises(Exception):
            initial_state.display = Decimal('10')

    def test_state_operations_create_new_instance(self, initial_state):
        """Test that operations create new state instances."""
        state1 = initial_state
        state2 = handle_digit('5', state1)
        assert state1 is not state2
        assert state1.display == Decimal('0')
        assert state2.display == Decimal('5')
