"""Calculator state management with immutable state pattern."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from calculator.errors import (
    CalculatorError,
    DivisionByZeroError,
    InvalidOperatorError,
    InvalidExpressionError,
)


@dataclass(frozen=True)
class CalculatorState:
    """Immutable state of the calculator."""

    # Display shown to user
    display: Decimal = Decimal('0')

    # First operand (left side of operation)
    accumulator: Decimal = Decimal('0')

    # Pending operator (+, -, ×, ÷, or None)
    operator: Optional[str] = None

    # Error message if present, None otherwise
    error: Optional[str] = None

    # Flag: whether next digit input starts a fresh number
    is_new_input: bool = True


def handle_digit(digit: str, state: CalculatorState) -> CalculatorState:
    """Handle digit input (0-9)."""
    if not digit.isdigit():
        raise ValueError(f"Invalid digit: {digit}")

    if state.is_new_input:
        # Start fresh number
        new_display = Decimal(digit)
    else:
        # Append digit to display
        current_str = str(state.display)
        new_display = Decimal(current_str + digit)

    return CalculatorState(
        display=new_display,
        accumulator=state.accumulator,
        operator=state.operator,
        error=None,
        is_new_input=False,
    )


def handle_operator(op: str, state: CalculatorState, engine) -> CalculatorState:
    """Handle operator input (+, -, ×, ÷)."""
    valid_ops = ['+', '-', '×', '÷', '*', '/']
    if op not in valid_ops:
        raise InvalidOperatorError(op)

    # Normalize operators
    if op == '*':
        op = '×'
    elif op == '/':
        op = '÷'

    # If operator already set, evaluate first (continuous calculation)
    if state.operator is not None and not state.is_new_input:
        try:
            result = engine.perform_operation(
                state.accumulator,
                state.operator,
                state.display,
            )
        except DivisionByZeroError as e:
            return CalculatorState(
                display=state.display,
                accumulator=Decimal('0'),
                operator=None,
                error=e.message,
                is_new_input=True,
            )
    else:
        result = state.display

    return CalculatorState(
        display=result,
        accumulator=result,
        operator=op,
        error=None,
        is_new_input=True,
    )


def handle_equals(state: CalculatorState, engine) -> CalculatorState:
    """Handle equals button press."""
    if state.operator is None:
        return state

    try:
        result = engine.perform_operation(
            state.accumulator,
            state.operator,
            state.display,
        )
    except DivisionByZeroError as e:
        return CalculatorState(
            display=state.display,
            accumulator=Decimal('0'),
            operator=None,
            error=e.message,
            is_new_input=True,
        )

    return CalculatorState(
        display=result,
        accumulator=Decimal('0'),
        operator=None,
        error=None,
        is_new_input=True,
    )


def handle_clear(state: CalculatorState) -> CalculatorState:
    """Handle clear button press."""
    return CalculatorState(
        display=Decimal('0'),
        accumulator=Decimal('0'),
        operator=None,
        error=None,
        is_new_input=True,
    )


def handle_backspace(state: CalculatorState) -> CalculatorState:
    """Handle backspace/delete button press."""
    display_str = str(state.display)

    if len(display_str) <= 1 or display_str == '0':
        return CalculatorState(
            display=Decimal('0'),
            accumulator=state.accumulator,
            operator=state.operator,
            error=state.error,
            is_new_input=state.is_new_input,
        )

    # Remove last character
    new_display_str = display_str[:-1]
    if new_display_str == '-':
        new_display_str = '0'

    return CalculatorState(
        display=Decimal(new_display_str),
        accumulator=state.accumulator,
        operator=state.operator,
        error=None,
        is_new_input=False,
    )


def handle_sign_toggle(state: CalculatorState) -> CalculatorState:
    """Handle sign toggle button press (±)."""
    new_display = -state.display if state.display != Decimal('0') else Decimal('0')

    return CalculatorState(
        display=new_display,
        accumulator=state.accumulator,
        operator=state.operator,
        error=None,
        is_new_input=False,
    )


def handle_decimal_point(state: CalculatorState) -> CalculatorState:
    """Handle decimal point input."""
    display_str = str(state.display)

    # Check if decimal already present
    if '.' in display_str:
        raise InvalidExpressionError("Decimal point already present")

    new_display_str = display_str + '.'

    return CalculatorState(
        display=Decimal(new_display_str),
        accumulator=state.accumulator,
        operator=state.operator,
        error=None,
        is_new_input=False,
    )
