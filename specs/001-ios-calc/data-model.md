# Data Model: iOS-Style CLI Calculator

**Feature**: iOS-Style CLI Calculator (001-ios-calc)
**Date**: 2026-01-04
**Purpose**: Define calculator state, entities, and data structures

---

## Core Data Model

### CalculatorState (Primary Entity)

The `CalculatorState` represents the complete state of a calculation at any moment. It is immutable—each operation creates a new state object.

```python
@dataclass(frozen=True)
class CalculatorState:
    """Immutable state of the calculator"""

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
```

### State Invariants (Validation Rules)

1. **display** and **accumulator** must always be valid `Decimal` values
2. **operator** must be one of: `+`, `-`, `×`, `÷`, or `None`
3. **is_new_input** must be boolean
4. When **error** is not None:
   - **operator** must be None
   - **accumulator** must be Decimal('0')
   - User cannot proceed with calculation until new input starts

### State Transitions

All state changes follow the same pattern:
```
User Input → Validation → State Modification → New CalculatorState
```

#### Transition 1: Digit Input

**Before**: User enters digit "5"
```python
state = CalculatorState(
    display=Decimal('0'),
    accumulator=Decimal('0'),
    operator=None,
    is_new_input=True
)
```

**After**:
```python
state = CalculatorState(
    display=Decimal('5'),
    accumulator=Decimal('0'),
    operator=None,
    is_new_input=False
)
```

**Rule**: If `is_new_input=True`, replace display; if False, append digit to display

#### Transition 2: Operator Input

**Before**: User enters operator "+"
```python
state = CalculatorState(
    display=Decimal('5'),
    accumulator=Decimal('0'),
    operator=None,
    is_new_input=False
)
```

**After**:
```python
state = CalculatorState(
    display=Decimal('5'),
    accumulator=Decimal('5'),
    operator='+',
    is_new_input=True
)
```

**Rule**: Save display value to accumulator, set operator, mark next input as fresh

#### Transition 3: Equals (Complete Operation)

**Before**: User presses "=" (state: "5 + 3")
```python
state = CalculatorState(
    display=Decimal('3'),
    accumulator=Decimal('5'),
    operator='+',
    is_new_input=False
)
```

**After**:
```python
state = CalculatorState(
    display=Decimal('8'),
    accumulator=Decimal('0'),
    operator=None,
    is_new_input=True
)
```

**Calculation**: `5 + 3 = 8`, result becomes new display

#### Transition 4: Clear Button

**Before**: Any state
```python
state = CalculatorState(...)
```

**After**:
```python
state = CalculatorState(
    display=Decimal('0'),
    accumulator=Decimal('0'),
    operator=None,
    error=None,
    is_new_input=True
)
```

**Rule**: Reset all to initial state

#### Transition 5: Error State

**Before**: User enters "5 ÷ 0" and presses "="
```python
state = CalculatorState(
    display=Decimal('0'),
    accumulator=Decimal('5'),
    operator='÷',
    is_new_input=False
)
```

**After**:
```python
state = CalculatorState(
    display=Decimal('5'),
    accumulator=Decimal('0'),
    operator=None,
    error='Cannot divide by zero',
    is_new_input=True
)
```

**Rule**: Capture error message, reset operator/accumulator, mark for fresh input

### Continuous Calculation Support (FR-010)

Users can chain operations: `5 + 3 + 2 = 10`

**State Progression**:

1. User enters "5", presses "+" → accumulator=5, operator=+
2. User enters "3", presses "+" →
   - First evaluate: 5 + 3 = 8
   - Then set: accumulator=8, operator=+
   - Display: 8

This is accomplished by evaluating the previous operation before accepting a new operator.

---

## Related Entities

### Operation (Enum)

Represents a mathematical operation.

```python
from enum import Enum

class Operation(Enum):
    """Mathematical operations supported by calculator"""
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '×'
    DIVIDE = '÷'
```

### CalculatorError (Exception Hierarchy)

```python
class CalculatorError(Exception):
    """Base exception for calculator errors"""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero"""
    pass

class InvalidOperatorError(CalculatorError):
    """Raised for unsupported operators"""
    pass

class InvalidNumberError(CalculatorError):
    """Raised for malformed number input"""
    pass

class InvalidExpressionError(CalculatorError):
    """Raised for incomplete or malformed expressions"""
    pass
```

---

## Data Flow Diagram

```
User Input (digit/operator/button)
    ↓
Input Validator
    ├─→ Valid: Proceed
    └─→ Invalid: Raise CalculatorError
    ↓
State Transition Handler
    ├─→ Digit: Add to display
    ├─→ Operator: Save accumulator, set operator
    ├─→ Equals: Calculate result, reset operator
    ├─→ Clear: Reset state
    └─→ Delete: Remove last character
    ↓
New CalculatorState
    ↓
Render to Display (via CLI)
```

---

## Validation Rules

### Input Validation

| Input | Validation | Action |
|-------|-----------|--------|
| **Digit (0-9)** | Always valid | Append to display or replace if new input |
| **Decimal point (.)** | Valid if not already in display | Add to display |
| **Operator (+,-,×,÷)** | Valid if display is not empty | Evaluate prior operation, set new operator |
| **Equals** | Valid if operator is set | Calculate result |
| **Delete/Backspace** | Valid if display length > 1 | Remove last character |
| **Clear** | Always valid | Reset to initial state |
| **Sign toggle (±)** | Valid if display is not empty | Negate display value |

### Calculation Validation

| Scenario | Validation | Result |
|----------|-----------|--------|
| **Divide by zero** | Operand2 = 0 | Raise DivisionByZeroError, set error state |
| **Incomplete expression** | User presses "=" with operator but no second operand | Raise InvalidExpressionError, set error state |
| **Invalid operator** | Operator not in [+, -, ×, ÷] | Raise InvalidOperatorError, reject input |
| **Consecutive decimals** | Display already contains "." | Reject input |

---

## Number Representation

### Precision Requirements

- **Internal**: Use `decimal.Decimal` for all arithmetic to meet SC-002 (10+ decimal places)
- **Display**: Format to maximum 10 decimal places, removing trailing zeros

### Examples

```python
# Precision handling
Decimal('0.1') + Decimal('0.2')  # = Decimal('0.3') ✓ (not 0.30000000001)
Decimal('10.5') / Decimal('2')   # = Decimal('5.25') ✓

# Display formatting
format_for_display(Decimal('5.50000000000'))  # → "5.5"
format_for_display(Decimal('5'))              # → "5"
format_for_display(Decimal('0.3'))            # → "0.3"
```

---

## State Size and Performance

### Memory Footprint

- Single `CalculatorState` object: ~200 bytes
- Application memory: <10 MB (requirement: FR-005)
- No persistence (no database, no file storage)

### State Immutability Benefits

1. **Thread-safety**: Multiple states can coexist safely
2. **Undo/Redo**: Future feature enabled by keeping state history
3. **Testability**: Pure functions, no hidden state mutations
4. **Debugging**: Each state snapshot is complete, self-contained

---

## Entity Relationships

```
CalculatorState
    ├── display: Decimal
    ├── accumulator: Decimal
    ├── operator: Optional[Operation]
    ├── error: Optional[CalculatorError]
    └── is_new_input: bool

Operation
    ├── ADD
    ├── SUBTRACT
    ├── MULTIPLY
    └── DIVIDE

CalculatorError (base)
    ├── DivisionByZeroError
    ├── InvalidOperatorError
    ├── InvalidNumberError
    └── InvalidExpressionError
```

---

## Summary

The data model is intentionally simple and immutable:
- Single primary entity (`CalculatorState`)
- Clear state transitions
- Strong validation at input boundaries
- Error cases handled explicitly
- Precision guaranteed via `Decimal`
- Design supports testing, extensibility, and continuous calculations (FR-010)
