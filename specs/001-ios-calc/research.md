# Research: iOS-Style CLI Calculator

**Feature**: iOS-Style CLI Calculator (001-ios-calc)
**Date**: 2026-01-04
**Purpose**: Document design decisions, technology choices, and technical rationale

## Executive Summary

This calculator is implemented as a Python library with a beautiful CLI interface using the `rich` library. The core calculation engine uses `decimal.Decimal` for precision, implements a recursive descent parser for PEMDAS compliance, and features iOS-inspired interactive UI with responsive button feedback.

---

## 1. Decimal Precision Handling

### Decision
Use Python's `decimal.Decimal` module for all arithmetic operations instead of native floats.

### Rationale
- **Requirement**: SC-002 requires "Decimal calculations accurate to at least 10 decimal places without floating-point errors"
- **Problem**: Native Python floats use binary floating-point, causing precision loss (e.g., 0.1 + 0.2 = 0.30000000000000004)
- **Solution**: `decimal.Decimal` provides arbitrary-precision decimal arithmetic, ensuring 0.1 + 0.2 = 0.3 exactly
- **Impact**: Small performance overhead (~1-5% slower), but meets requirement precisely

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| **Native floats** | Fast, built-in | Fails precision requirement SC-002 | Rejected |
| **fractions.Fraction** | Exact rational arithmetic | Slower, overkill for calculator | Rejected |
| **Decimal (CHOSEN)** | Meets requirement, familiar from spreadsheets | Slightly slower | **Selected** |

### Implementation
```python
from decimal import Decimal, ROUND_HALF_UP

# All calculations use Decimal
result = Decimal('0.1') + Decimal('0.2')  # Returns Decimal('0.3')

# Rounding for display (10 decimal places max)
display_value = result.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
```

---

## 2. Order of Operations (PEMDAS)

### Decision
Implement recursive descent parser supporting full operator precedence: Parentheses, Exponents (not required), Multiplication/Division, Addition/Subtraction.

### Rationale
- **Requirement**: FR-012 specifies "System MUST follow standard mathematical order of operations"
- **User Clarification**: Selected PEMDAS over left-to-right evaluation (user chose mathematical precedence)
- **Example**: 5 + 3 × 2 = 11 (not 16), multiply first due to higher precedence

### Alternatives Considered

| Alternative | Behavior | Pros | Cons | Decision |
|-------------|----------|------|------|----------|
| **Left-to-right** | 5 + 3 × 2 = 16 | Simple to implement | Violates mathematical standard, fails FR-012 | Rejected |
| **PEMDAS (CHOSEN)** | 5 + 3 × 2 = 11 | Matches user expectation, mathematically correct | Slightly more complex parser | **Selected** |

### Implementation Strategy
Recursive descent parser with operator precedence levels:

1. **Level 1** (lowest precedence): Addition (+) and Subtraction (-)
2. **Level 2** (higher precedence): Multiplication (×) and Division (÷)
3. **Level 3** (highest): Numbers and parentheses (future)

Parser evaluates higher-precedence operations first by recursively calling lower levels.

```python
def parse_expression(tokens):
    return parse_addition(tokens)

def parse_addition(tokens):
    left = parse_multiplication(tokens)
    while peek() in ['+', '-']:
        op = consume()
        right = parse_multiplication(tokens)
        left = apply_operation(left, op, right)
    return left

def parse_multiplication(tokens):
    left = parse_number(tokens)
    while peek() in ['×', '÷']:
        op = consume()
        right = parse_number(tokens)
        left = apply_operation(left, op, right)
    return left
```

---

## 3. Beautiful CLI Rendering

### Decision
Use the `rich` library for terminal UI rendering with iOS-style button grid, colors, and visual feedback.

### Rationale
- **Requirement**: SC-006 specifies "Calculator aesthetics match iOS design principles"
- **P2 User Story**: "Experience Seamless, Beautiful iOS-Like Interface" requires button layout, visual feedback, smooth transitions
- **Tool Choice**: `rich` library provides:
  - Table rendering for button grid layout
  - Color and styling support
  - Box drawing for professional appearance
  - Text centering and alignment
  - Built-in layout management
  - Pure Python, cross-platform (macOS, Linux, Windows)

### Alternatives Considered

| Tool | Pros | Cons | Decision |
|------|------|------|----------|
| **ANSI codes** | Full control, minimal deps | Verbose, error-prone, need to manage state | Rejected |
| **curses** | Powerful | Platform-dependent, complex API | Rejected |
| **rich (CHOSEN)** | High-level, beautiful output, active community | Adds dependency | **Selected** |
| **No styling** | Minimal code | Fails aesthetic requirement | Rejected |

### UI Design
```
┌─────────────────────────────────┐
│          Display: 15.5           │
├─────────────────────────────────┤
│  C  |  ±  |  ←  |  ÷           │
├─────────────────────────────────┤
│  7  |  8  |  9  |  ×           │
├─────────────────────────────────┤
│  4  |  5  |  6  |  -           │
├─────────────────────────────────┤
│  1  |  2  |  3  |  +           │
├─────────────────────────────────┤
│  0  |  .  |    =               │
└─────────────────────────────────┘
```

Button colors:
- **Number buttons**: Light gray background
- **Operator buttons** (+, -, ×, ÷): Orange background (like iOS)
- **Equals button** (=): Green background
- **Control buttons** (C, ←, ±): Dark gray background
- **Visual feedback**: Button highlights on press, brief color flash

---

## 4. Interactive vs One-Shot Calculation Modes

### Decision
Support both interactive (REPL-like) and one-shot (single calculation from arguments) modes.

### Rationale
- **Use Case 1** (Interactive): User launches calculator, enters expression, sees result, continues calculating (matches iOS feel)
- **Use Case 2** (One-shot): Automation/scripting: `python -m calculator "5 + 3"`
- **Flexibility**: Covers both user personas (interactive user and automation)

### Modes

**Interactive Mode** (default):
```
$ python -m calculator
┌──────────────────┐
│    Display: 0    │
└──────────────────┘
[Button grid shown]
> [user types: "5 + 3 ="]
Display: 8
```

**One-Shot Mode** (with argument):
```
$ python -m calculator "5 + 3"
8
```

---

## 5. State Management Architecture

### Decision
Use immutable calculation state with pure functions for state transitions.

### Rationale
- **Testability**: Pure functions = predictable, easy to test
- **Correctness**: Immutability prevents accidental state mutations
- **Clarity**: Each operation → new state, making intent clear
- **Support FR-010**: "Continuous calculations" (result becomes operand for next operation)

### State Model

```python
@dataclass(frozen=True)
class CalculatorState:
    display: Decimal = Decimal('0')          # What user sees
    accumulator: Decimal = Decimal('0')      # First operand
    operator: Optional[str] = None           # Pending operation
    error: Optional[str] = None              # Error message if present
    is_new_input: bool = True                # Whether next digit starts fresh
```

### State Transitions

```python
# Example: User presses "5", then "+", then "3", then "="

# Initial state
state = CalculatorState()

# After pressing "5"
state = handle_digit('5', state)
# → CalculatorState(display=5, accumulator=0, operator=None, is_new_input=False)

# After pressing "+"
state = handle_operator('+', state)
# → CalculatorState(display=5, accumulator=5, operator='+', is_new_input=True)

# After pressing "3"
state = handle_digit('3', state)
# → CalculatorState(display=3, accumulator=5, operator='+', is_new_input=False)

# After pressing "="
state = handle_equals(state)
# → CalculatorState(display=8, accumulator=0, operator=None, is_new_input=True)
```

---

## 6. Error Handling Strategy

### Decision
Validate all inputs before processing, provide user-friendly error messages for all failure modes.

### Rationale
- **Requirement**: FR-006, FR-007, FR-008 specify error handling for division by zero, invalid operators, incomplete expressions
- **UX**: Clear error messages help users understand what went wrong
- **Robustness**: No crashes, graceful degradation

### Error Categories

| Error | Trigger | Message | Recovery |
|-------|---------|---------|----------|
| **Division by zero** | User tries "5 ÷ 0" | "Cannot divide by zero" | Display clears when user starts new calculation |
| **Invalid operator** | User enters invalid symbol | "Invalid operator" | Ignored, prompt for valid input |
| **Incomplete expression** | User presses "=" after "5 +" | "Incomplete expression" | Display shows error, user can continue |
| **Invalid decimal** | User enters "3.14.159" | "Invalid number format" | Decimal point rejected on second occurrence |

### Implementation
```python
class CalculatorError(Exception):
    """Base calculator error"""
    pass

class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero"""
    pass

class InvalidOperatorError(CalculatorError):
    """Raised for unsupported operators"""
    pass

class InvalidExpressionError(CalculatorError):
    """Raised for malformed expressions"""
    pass
```

---

## 7. Testing Strategy

### Decision
Use pytest with three test layers: unit tests (calculator logic), contract tests (CLI interface), integration tests (end-to-end).

### Rationale
- **Requirement**: Test-First principle (Constitution)
- **Coverage**: Unit tests ensure math correctness; Integration tests ensure CLI works as advertised
- **Quality**: All user scenarios from spec must pass as acceptance tests

### Test Pyramid

```
Integration Tests (test_cli.py)
    ├── End-to-end UI interaction tests
    ├── Multi-step calculation scenarios
    └── Error recovery workflows

Unit Tests
    ├── test_engine.py (arithmetic correctness)
    ├── test_parser.py (PEMDAS parsing)
    ├── test_validator.py (input validation)
    └── test_state.py (state transitions)
```

### Critical Test Cases

**Decimal Precision** (validates SC-002):
```python
def test_decimal_precision():
    result = calculator.calculate(Decimal('0.1') + Decimal('0.2'))
    assert result == Decimal('0.3')  # Not 0.30000000000000004
```

**Order of Operations** (validates FR-012):
```python
def test_pemdas_precedence():
    result = calculator.calculate("5 + 3 * 2")
    assert result == Decimal('11')  # Multiply first, then add
```

**Error Handling** (validates FR-006):
```python
def test_division_by_zero():
    with pytest.raises(DivisionByZeroError):
        calculator.calculate("5 / 0")
```

---

## 8. Dependencies and Justification

| Dependency | Purpose | Why | Lighter Alternative |
|------------|---------|-----|---------------------|
| `rich` | Beautiful CLI rendering | Required for SC-006 (iOS aesthetics) | ANSI codes (too verbose) |
| `decimal` | Precision arithmetic | Required for SC-002 (decimal precision) | Built-in (no alternative) |
| `pytest` | Testing framework | Standard, powerful, widely used | unittest (verbose) |
| `dataclasses` | State management | Python 3.7+ standard, clean syntax | attrs/pydantic (overkill) |

### Minimal Dependency Philosophy
- No web frameworks, no databases, no external APIs
- Pure Python stdlib where possible
- Only `rich` added beyond stdlib (1 external dependency)

---

## 9. Future Extensibility

This architecture enables future features without redesign:

1. **GUI Version**: Swap CLI UI for Qt/Tkinter while keeping calculator library
2. **Web Version**: Expose calculator.lib as HTTP API
3. **Mobile**: Port library to Swift/Kotlin
4. **Advanced Math**: Add square root, power, trigonometric functions without changing core structure
5. **History/Undo**: Add state history as wrapper around immutable state

---

## Summary of Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Arithmetic | `decimal.Decimal` | Precision requirement (SC-002) |
| Parsing | Recursive descent + PEMDAS | User selected mathematical precedence |
| UI Library | `rich` | Beautiful output required (SC-006) |
| Modes | Interactive + one-shot | Flexibility for different users |
| State | Immutable with pure functions | Testability, correctness, clarity |
| Errors | Validated inputs, friendly messages | Robustness (FR-006, FR-007, FR-008) |
| Testing | Pytest with unit/integration layers | Constitution requirement (Test-First) |

All decisions support the specification requirements and Constitution principles while maintaining simplicity and maintainability.
