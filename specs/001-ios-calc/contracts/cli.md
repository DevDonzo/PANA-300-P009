# CLI Contract: iOS-Style CLI Calculator

**Feature**: iOS-Style CLI Calculator (001-ios-calc)
**Date**: 2026-01-04
**Purpose**: Define the command-line interface and interaction patterns

---

## CLI Modes

### Mode 1: Interactive Mode (Default)

Launches an interactive calculator with persistent state, similar to iOS calculator.

**Invocation**:
```bash
python -m calculator
# or
calculator
```

**Behavior**:
1. Displays initial calculator interface with display showing "0"
2. User interacts with number pad and operator buttons using keyboard
3. State persists across multiple calculations
4. User can press `Q` or `Ctrl+C` to quit

**Example Session**:
```
$ python -m calculator

┌─────────────────────────────────────┐
│          Display: 0                 │
├─────────────────────────────────────┤
│  C  │  ±  │  ←  │  ÷              │
├─────────────────────────────────────┤
│  7  │  8  │  9  │  ×              │
├─────────────────────────────────────┤
│  4  │  5  │  6  │  -              │
├─────────────────────────────────────┤
│  1  │  2  │  3  │  +              │
├─────────────────────────────────────┤
│  0  │  .  │     =                 │
└─────────────────────────────────────┘

[User presses: 5]
Display updates to: 5

[User presses: +]
Display updates to: 5

[User presses: 3]
Display updates to: 3

[User presses: =]
Display updates to: 8

[User presses: Q]
Goodbye!
```

### Mode 2: One-Shot Mode

Calculates a single expression and outputs the result.

**Invocation**:
```bash
python -m calculator "5 + 3"
# or
calculator "5 + 3"
```

**Input**: Mathematical expression as command-line argument
**Output**: Result to stdout
**Exit Code**: 0 on success, 1 on error

**Example**:
```bash
$ python -m calculator "5 + 3"
8

$ python -m calculator "10 * 2"
20

$ python -m calculator "0.1 + 0.2"
0.3
```

---

## Input Specification

### Interactive Mode: Keyboard Input

#### Number Keys
- **Keys**: 0-9
- **Action**: Append digit to display or start new number
- **Example**: Press 1, then 5 → Display shows "15"

#### Decimal Point
- **Key**: `.`
- **Action**: Add decimal point to display
- **Validation**: Reject if decimal point already present in current number
- **Example**: Press 3, then "." → Display shows "3."

#### Operators
- **Keys**: `+` (plus), `-` (minus), `*` (multiply), `/` (divide)
- **Symbols Shown**: `+`, `-`, `×`, `÷` (converted for display)
- **Action**: Set operator and prepare for next operand
- **Evaluation**: If operator already pending, evaluate first (continuous calculation)

#### Equals / Calculate
- **Key**: `=` or `Enter`
- **Action**: Evaluate complete expression and display result
- **Error**: If incomplete expression (e.g., "5 +"), show error message

#### Clear
- **Key**: `C`
- **Action**: Reset calculator to initial state (display "0", clear operator)

#### Delete / Backspace
- **Key**: `←` or `Backspace`
- **Action**: Remove last digit from display
- **Behavior**: If display becomes empty, show "0"

#### Sign Toggle
- **Key**: `±`
- **Action**: Toggle sign of displayed number (positive ↔ negative)
- **Examples**:
  - Display "5" → press ± → Display "-5"
  - Display "-5" → press ± → Display "5"

#### Quit
- **Key**: `Q` or `Ctrl+C`
- **Action**: Exit calculator, display "Goodbye!"

### One-Shot Mode: Command-Line Argument

**Format**: `calculator "<expression>"`

**Expression Syntax**:
```
<expression> ::= <term> (('+' | '-') <term>)*
<term> ::= <factor> (('*' | '/' | '×' | '÷') <factor>)*
<factor> ::= ['-'] (<number> | '(' <expression> ')')
<number> ::= <digit>+ ('.' <digit>+)?
```

**Examples**:
- `"5 + 3"` → Valid, result 8
- `"10 - 4"` → Valid, result 6
- `"6 × 7"` or `"6 * 7"` → Valid, result 42
- `"10 / 2"` or `"10 ÷ 2"` → Valid, result 5
- `"5 + 3 × 2"` → Valid, result 11 (PEMDAS: multiply first)
- `"0.1 + 0.2"` → Valid, result 0.3
- `"-5 + 3"` → Valid, result -2

---

## Output Specification

### Success Output

#### Interactive Mode
- Display updates in real-time showing current state
- Button presses show visual feedback (color change, animation)
- Result appears immediately in display area

#### One-Shot Mode
```
<result>
```
- Single line with numeric result
- No additional text
- Exit code 0

**Examples**:
```bash
$ calculator "5 + 3"
8

$ calculator "0.1 + 0.2"
0.3

$ calculator "100 / 4"
25
```

### Error Output

#### Interactive Mode
- Error message displayed in place of number
- Message clears on next input
- User can continue without restarting

**Example**:
```
Display: "Cannot divide by zero"
[User presses: C]
Display: "0"
```

#### One-Shot Mode
```
Error: <error_message>
```
- Error message to stderr
- Exit code 1

**Examples**:
```bash
$ calculator "5 / 0" 2>&1
Error: Cannot divide by zero

$ calculator "5 +" 2>&1
Error: Incomplete expression

$ calculator "5 @ 3" 2>&1
Error: Invalid operator: @
```

---

## Error Handling

### Error Messages

| Scenario | Message | Recovery |
|----------|---------|----------|
| Division by zero | `"Cannot divide by zero"` | Clear on next input or press C |
| Invalid operator | `"Invalid operator: [symbol]"` | Operator ignored, continue |
| Incomplete expression | `"Incomplete expression"` | Display clears, user can press C or continue |
| Malformed number | `"Invalid number format"` | Input rejected, continue |
| Consecutive decimals | `"Invalid decimal"` | Decimal point ignored |

### Interactive Mode Error Recovery

1. Error message displayed
2. User can:
   - Press any digit to start fresh calculation
   - Press `C` to clear and reset
   - Press `←` to delete last input
   - Press any operator to continue

### One-Shot Mode Error Handling

1. Error printed to stderr
2. Exit code set to 1
3. No partial results returned

---

## Display Format

### Interactive Mode Display

```
┌────────────────────────────────────┐
│        Display Value               │
└────────────────────────────────────┘
```

**Format Rules**:
- Maximum width: ~35 characters
- Number right-aligned in display
- Decimal places: up to 10 visible (trailing zeros removed)
- Negative numbers: prefixed with `-`

**Examples**:
- `"5"` (integer)
- `"5.5"` (decimal)
- `"-5"` (negative)
- `"0.3"` (result of 0.1 + 0.2)
- `"3.14159265"` (up to 10 decimal places)

### Button Layout

```
┌────────────────────────────────────┐
│        Display Value               │
├────────────────────────────────────┤
│  C  │  ±  │  ←  │  ÷             │  Function buttons (4 across)
├────────────────────────────────────┤
│  7  │  8  │  9  │  ×             │
├────────────────────────────────────┤
│  4  │  5  │  6  │  -             │  Number pad (3x3 grid)
├────────────────────────────────────┤
│  1  │  2  │  3  │  +             │
├────────────────────────────────────┤
│  0  │  .  │     =                │  Bottom row: 0, decimal, equals
└────────────────────────────────────┘
```

**Colors** (ANSI/rich):
- **Display**: White text on dark background
- **Number buttons** (0-9): Light gray background, black text
- **Operator buttons** (+, -, ×, ÷): Orange background, white text
- **Equals button** (=): Green background, white text
- **Control buttons** (C, ±, ←): Dark gray background, white text
- **Pressed/Active**: Highlighted with brighter color or border

---

## Performance SLOs

All CLI operations must meet these requirements:

| Operation | SLO | Requirement |
|-----------|-----|-------------|
| **Button press response** | <50ms visual feedback | SC-005 |
| **Calculation result** | <100ms | SC-003, SC-005 |
| **Display update** | <50ms | SC-005 |
| **Startup** | <500ms | SC-005 |
| **One-shot calculation** | <100ms | SC-004 |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success (one-shot mode) or normal exit (interactive mode) |
| `1` | Calculation error (invalid expression, divide by zero, etc.) |
| `2` | Usage error (invalid command-line arguments) |

---

## Library API (for programmatic use)

The calculator is also exposed as a Python library for non-CLI use:

```python
from calculator import Calculator

calc = Calculator()

# One calculation
result = calc.calculate("5 + 3")  # Returns Decimal('8')

# With state management
state = calc.state
result = calc.press_digit('5')      # Returns new state
result = calc.press_operator('+')   # Returns new state
result = calc.press_digit('3')      # Returns new state
result = calc.press_equals()        # Returns result
```

---

## Summary

**Interactive Mode**: Beautiful, responsive CLI interface matching iOS calculator design for user-friendly manual calculations.

**One-Shot Mode**: Simple, scriptable interface for automation and integration.

**Both modes**: Fast, accurate calculations with comprehensive error handling and user-friendly feedback.
