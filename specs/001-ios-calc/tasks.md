# Tasks: iOS-Style CLI Calculator

**Feature**: 001-ios-calc | **Branch**: `001-ios-calc`
**Input**: Design documents from `/specs/001-ios-calc/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/cli.md, research.md

**Architecture**: Python 3.11+ library with CLI interface using `rich` library
**Testing**: Test-First (TDD) approach with unit and integration tests

---

## Overview

This task list implements the iOS-style CLI calculator in 5 phases:

1. **Phase 1**: Project setup and structure initialization
2. **Phase 2**: Core calculator engine and foundational components
3. **Phase 3**: User Story 1 - Basic Arithmetic Operations (P1) 🎯 MVP
4. **Phase 4**: User Story 2 - Decimal Precision (P1)
5. **Phase 5**: User Story 3 - Negative Numbers (P1)
6. **Phase 6**: User Story 4 - Error Handling (P2)
7. **Phase 7**: User Story 5 - iOS-Style UI (P2)
8. **Phase 8**: Polish & Cross-Cutting Concerns

**MVP Scope** (Phase 1-3): Basic calculator with +, -, ×, ÷ operations (100+ lines)
**Full Scope** (Phase 1-7): Complete calculator with decimals, negatives, errors, beautiful UI

**Parallel Opportunities**:
- Phase 3 (US1) and Phase 4 (US2) can run in parallel (different modules)
- Phase 5 (US3) can run in parallel with Phase 3 (US1)
- Phase 6 (US4) can run in parallel with other user stories

---

## Phase 1: Project Setup

**Purpose**: Initialize Python project structure, dependencies, and testing framework

**Checkpoint**: Project is runnable with empty modules

- [ ] T001 Create project directory structure in `calc-using-skp/src/calculator/`, `calc-using-skp/src/cli/`, `calc-using-skp/tests/`
- [ ] T002 Create `calc-using-skp/requirements.txt` with `rich>=13.0.0`, `pytest>=7.0.0`, `pytest-cov>=4.0.0`
- [ ] T003 [P] Create `calc-using-skp/setup.py` with entry point `python -m calculator`
- [ ] T004 [P] Create `calc-using-skp/README.md` with project description and quickstart
- [ ] T005 Create `calc-using-skp/src/calculator/__init__.py` (empty package marker)
- [ ] T006 [P] Create `calc-using-skp/src/cli/__init__.py` (empty package marker)
- [ ] T007 [P] Create `calc-using-skp/tests/__init__.py` (empty package marker)
- [ ] T008 Create `calc-using-skp/tests/conftest.py` with pytest configuration and shared fixtures
- [ ] T009 [P] Create `.gitignore` for Python project (pycache, venv, .pytest_cache, etc.)

---

## Phase 2: Foundational Calculator Components

**Purpose**: Build core modules that all user stories depend on

**⚠️ CRITICAL**: Phase 2 MUST complete before user story implementation begins

**Checkpoint**: Core engine is functional and testable

### 2.1: Error Definitions and Exceptions

- [ ] T010 Create `calc-using-skp/src/calculator/errors.py` with exception hierarchy:
  - `CalculatorError` (base class)
  - `DivisionByZeroError` (extends CalculatorError)
  - `InvalidOperatorError` (extends CalculatorError)
  - `InvalidNumberError` (extends CalculatorError)
  - `InvalidExpressionError` (extends CalculatorError)

### 2.2: Calculator State Management

- [ ] T011 Create `calc-using-skp/src/calculator/state.py` with immutable `CalculatorState` dataclass:
  - Fields: `display: Decimal`, `accumulator: Decimal`, `operator: Optional[str]`, `error: Optional[str]`, `is_new_input: bool`
  - Default values: display=Decimal('0'), accumulator=Decimal('0'), operator=None, error=None, is_new_input=True
  - Make dataclass frozen (immutable)

### 2.3: Input Validator

- [ ] T012 Create `calc-using-skp/src/calculator/validator.py` with `InputValidator` class:
  - Method: `validate_digit(char: str) -> bool` (checks if 0-9)
  - Method: `validate_operator(op: str) -> bool` (checks if +, -, ×, ÷)
  - Method: `validate_decimal_point(display: str) -> bool` (rejects if decimal already present)
  - Method: `validate_expression(expr: str) -> bool` (basic expression syntax)
  - All methods return True if valid, raise appropriate exception if invalid

### 2.4: Expression Parser with PEMDAS

- [ ] T013 Create `calc-using-skp/src/calculator/parser.py` with recursive descent parser:
  - Class: `ExpressionParser` with method `parse(expression: str) -> Decimal`
  - Implement 3-level operator precedence:
    - Level 1: Addition (+) and Subtraction (-) - lowest precedence
    - Level 2: Multiplication (×) and Division (÷) - higher precedence
    - Level 3: Numbers and negation - highest precedence
  - Must handle: "5 + 3 * 2" → 11 (not 16)
  - Must handle: "10 / 2" → 5
  - Must handle: "-5 + 3" → -2
  - Raise `InvalidExpressionError` for incomplete expressions (e.g., "5 +")
  - Use `Decimal` for all arithmetic

- [ ] T014 [P] Create `calc-using-skp/tests/unit/test_parser.py` with tests (TDD - write FIRST):
  - `test_parse_simple_addition()`: "5 + 3" → 8
  - `test_parse_simple_subtraction()`: "10 - 4" → 6
  - `test_parse_simple_multiplication()`: "6 * 7" → 42
  - `test_parse_simple_division()`: "15 / 3" → 5
  - `test_parse_pemdas_multiplication_first()`: "5 + 3 * 2" → 11
  - `test_parse_pemdas_division_first()`: "10 + 20 / 2" → 20
  - `test_parse_negative_numbers()`: "-5 + 3" → -2
  - `test_parse_decimal_numbers()`: "3.5 + 2.1" → 5.6
  - `test_parse_incomplete_expression()`: "5 +" → raises InvalidExpressionError
  - `test_parse_division_by_zero()`: "5 / 0" → raises DivisionByZeroError

### 2.5: Calculation Engine

- [ ] T015 Create `calc-using-skp/src/calculator/engine.py` with `Calculator` class:
  - Method: `perform_operation(left: Decimal, op: str, right: Decimal) -> Decimal`
    - op ∈ ['+', '-', '×', '÷']
    - Division by zero raises `DivisionByZeroError`
    - Returns Decimal result
  - Method: `calculate(expression: str) -> Decimal`
    - Uses `ExpressionParser` to parse and evaluate
    - Returns Decimal result
    - Raises exceptions for invalid inputs
  - Method: `format_result(result: Decimal) -> str`
    - Max 10 decimal places
    - Remove trailing zeros
    - Examples: Decimal('5.50000') → "5.5", Decimal('5') → "5"

- [ ] T016 [P] Create `calc-using-skp/tests/unit/test_engine.py` with tests (TDD - write FIRST):
  - `test_addition()`: 10 + 5 → 15
  - `test_subtraction()`: 20 - 8 → 12
  - `test_multiplication()`: 6 * 7 → 42
  - `test_division()`: 15 / 3 → 5
  - `test_decimal_precision()`: 0.1 + 0.2 → 0.3 (not 0.30000000001)
  - `test_division_by_zero()`: 5 / 0 → raises DivisionByZeroError
  - `test_result_formatting()`: Decimal('5.50000') → "5.5"
  - `test_large_numbers()`: 999999999999 + 1 → 1000000000000
  - `test_negative_results()`: 5 - 10 → -5

### 2.6: State Management Logic

- [ ] T017 Create `calc-using-skp/src/calculator/state.py` operations (extend T011):
  - Method: `handle_digit(digit: str, state: CalculatorState) -> CalculatorState`
    - If is_new_input: set display to digit
    - Else: append digit to display
    - Return new state with is_new_input=False
  - Method: `handle_operator(op: str, state: CalculatorState) -> CalculatorState`
    - If operator already set: evaluate first (5 + 3 + → evaluates 5+3=8, then sets op=+)
    - Set accumulator=display, operator=op, is_new_input=True
    - Return new state
  - Method: `handle_equals(state: CalculatorState) -> CalculatorState`
    - If operator not set: return unchanged
    - Calculate: result = accumulator op display
    - Return new state with display=result, operator=None, is_new_input=True
  - Method: `handle_clear(state: CalculatorState) -> CalculatorState`
    - Return default initial state
  - Method: `handle_backspace(state: CalculatorState) -> CalculatorState`
    - Remove last character from display
    - If empty, set to "0"
  - Method: `handle_sign_toggle(state: CalculatorState) -> CalculatorState`
    - Negate display value
  - All methods use try-except to catch errors and set state.error

- [ ] T018 [P] Create `calc-using-skp/tests/unit/test_state.py` with tests (TDD - write FIRST):
  - `test_handle_digit_new_input()`: digit on fresh state → display="5"
  - `test_handle_digit_append()`: second digit → display="53"
  - `test_handle_operator_sets_operator()`: "5+" → accumulator=5, operator='+'
  - `test_handle_operator_continuous_calculation()`: "5+3+" → evaluates first
  - `test_handle_equals()`: "5+3=" → display="8"
  - `test_handle_clear()`: any state + clear → reset to default
  - `test_handle_backspace()`: "123" backspace → display="12"
  - `test_handle_sign_toggle()`: "5" toggle → display="-5"
  - `test_error_state()`: division by zero → error set, awaiting new input

---

## Phase 3: User Story 1 - Perform Basic Arithmetic Operations (P1) 🎯 MVP

**Goal**: Users can perform addition, subtraction, multiplication, and division with correct results

**Independent Test**: User enters "5 + 3 =", sees "8" displayed. Can calculate 20 - 8 = 12, 6 × 7 = 42, 15 ÷ 3 = 5

**Checkpoint**: Core arithmetic works end-to-end

### Tests for User Story 1 (Write FIRST)

- [ ] T019 [P] [US1] Create `calc-using-skp/tests/integration/test_basic_arithmetic.py`:
  - `test_addition_simple()`: "10 + 5" → "15"
  - `test_subtraction_simple()`: "20 - 8" → "12"
  - `test_multiplication_simple()`: "6 * 7" → "42"
  - `test_division_simple()`: "15 / 3" → "5"
  - `test_continuous_calculation()`: "5 + 3 + 2" → "10"

### Implementation for User Story 1

- [ ] T020 [P] [US1] Create `calc-using-skp/src/lib.py` public library API:
  - Function: `calculate(expression: str) -> str`
    - Uses Calculator engine
    - Returns formatted result as string
    - Raises CalculatorError on invalid input

- [ ] T021 [US1] Create `calc-using-skp/src/cli/main.py` one-shot mode entry point:
  - If command-line argument provided: one-shot mode
    - Example: `python -m calculator "5 + 3"` → prints "8"
  - If no argument: start interactive mode (implemented in Phase 7)
  - Error handling: catch exceptions, print to stderr, exit with code 1

- [ ] T022 [P] [US1] Add `python -m calculator` entry point in `calc-using-skp/__main__.py`:
  - Delegates to `cli.main`

**Checkpoint**: Basic arithmetic works in one-shot mode. User can run `python -m calculator "5 + 3"` and get "8"

---

## Phase 4: User Story 2 - Handle Decimal Numbers and Precision (P1)

**Goal**: Users can perform calculations with decimals and get accurate results (0.1 + 0.2 = 0.3, not 0.30000000001)

**Independent Test**: User enters "0.1 + 0.2 =", sees "0.3" displayed (not "0.30000000001")

**Checkpoint**: Decimal arithmetic works correctly

### Tests for User Story 2 (Write FIRST)

- [ ] T023 [P] [US2] Create `calc-using-skp/tests/integration/test_decimal_precision.py`:
  - `test_decimal_addition()`: "3.14 + 2.1" → "5.24"
  - `test_decimal_multiplication()`: "3.14 * 2" → "6.28"
  - `test_decimal_division()`: "10.5 / 2" → "5.25"
  - `test_floating_point_precision()`: "0.1 + 0.2" → "0.3" (CRITICAL)
  - `test_decimal_with_integer()`: "5 + 2.5" → "7.5"
  - `test_many_decimals()`: "0.1234567890 + 0.0000000001" → correct to 10 places

### Implementation for User Story 2

- [ ] T024 [P] [US2] Extend `calc-using-skp/src/calculator/validator.py`:
  - Method: `validate_decimal_point()` already created in Phase 2

- [ ] T025 [US2] Update `calc-using-skp/src/cli/main.py` if needed (should already work with Phase 1 implementation)

**Checkpoint**: `python -m calculator "0.1 + 0.2"` returns "0.3"

---

## Phase 5: User Story 3 - Work with Negative Numbers (P1)

**Goal**: Users can input and calculate with negative numbers

**Independent Test**: User enters "-10 + 5 =", sees "-5". Can calculate "5 - 10" → "-5" and "-4 × -3" → "12"

**Checkpoint**: Negative numbers work in all operations

### Tests for User Story 3 (Write FIRST)

- [ ] T026 [P] [US3] Create `calc-using-skp/tests/integration/test_negative_numbers.py`:
  - `test_negative_input()`: "-10 + 5" → "-5"
  - `test_subtraction_to_negative()`: "5 - 10" → "-5"
  - `test_negative_multiplication()`: "-4 * -3" → "12"
  - `test_negative_division()`: "-10 / 2" → "-5"
  - `test_sign_toggle()`: Interactive: "42" ± → "-42"

### Implementation for User Story 3

- [ ] T027 [P] [US3] Update `calc-using-skp/src/calculator/parser.py`:
  - Already handles negative numbers via unary minus in expression parser

- [ ] T028 [P] [US3] Update `calc-using-skp/src/calculator/state.py`:
  - Method: `handle_sign_toggle()` already created in Phase 2

**Checkpoint**: Negative number support working end-to-end

---

## Phase 6: User Story 4 - Handle Invalid Input Gracefully (P2)

**Goal**: Users get clear error messages for invalid operations; calculator doesn't crash

**Independent Test**: User enters "5 / 0", sees error message "Cannot divide by zero". Invalid operators are rejected.

**Checkpoint**: Error handling prevents crashes, provides helpful feedback

### Tests for User Story 4 (Write FIRST)

- [ ] T029 [P] [US4] Create `calc-using-skp/tests/integration/test_error_handling.py`:
  - `test_division_by_zero()`: "5 / 0" → error "Cannot divide by zero"
  - `test_invalid_operator()`: "5 @ 3" → error "Invalid operator: @"
  - `test_incomplete_expression()`: "5 +" → error "Incomplete expression"
  - `test_consecutive_decimals()`: "3.14.159" → error "Invalid decimal"
  - `test_error_recovery()`: After error, user can press C and continue

### Implementation for User Story 4

- [ ] T030 [P] [US4] Update `calc-using-skp/src/calculator/state.py`:
  - Wrap all operations in try-except
  - Set state.error on exception
  - Return error state so user can clear and continue

- [ ] T031 [US4] Update `calc-using-skp/src/cli/main.py` one-shot mode:
  - On error: print "Error: <message>" to stderr
  - Exit with code 1

- [ ] T032 [US4] Create user-friendly error messages:
  - DivisionByZeroError → "Cannot divide by zero"
  - InvalidOperatorError → "Invalid operator: [symbol]"
  - InvalidExpressionError → "Incomplete expression"
  - InvalidNumberError → "Invalid number format"

**Checkpoint**: Error handling works; calculator recovers gracefully

---

## Phase 7: User Story 5 - Experience Seamless, Beautiful iOS-Like Interface (P2)

**Goal**: Interactive calculator with iOS-style button grid, colors, visual feedback, responsive feel

**Independent Test**: User launches calculator, sees button grid layout matching iOS design, buttons show visual feedback on press

**Checkpoint**: Beautiful, responsive interactive calculator experience

### Tests for User Story 5 (Write FIRST)

- [ ] T033 [P] [US5] Create `calc-using-skp/tests/integration/test_ui_interface.py`:
  - `test_display_shows_initial_zero()`: UI displays "0" at startup
  - `test_display_updates_on_digit()`: Pressing "5" updates display to "5"
  - `test_button_grid_layout()`: Verify 5 rows × 4 columns layout
  - `test_operator_buttons_visible()`: +, -, ×, ÷ buttons present
  - `test_clear_button_visible()`: C button present
  - `test_equals_button_visible()`: = button present
  - `test_response_time()`: UI responds within 100ms

### Implementation for User Story 5

- [ ] T034 [P] [US5] Create `calc-using-skp/src/cli/ui.py` iOS-style UI renderer:
  - Class: `CalculatorUI` with method `render(state: CalculatorState) -> str`
  - Using `rich` library: Table for button grid, Panel for display
  - Display section at top showing current value
  - Button grid (5 rows × 4 columns):
    ```
    Row 1: C  │  ±  │  ←  │  ÷
    Row 2: 7  │  8  │  9  │  ×
    Row 3: 4  │  5  │  6  │  -
    Row 4: 1  │  2  │  3  │  +
    Row 5: 0  │  .  │     │  =
    ```
  - Colors:
    - Display: white text on dark background
    - Numbers (0-9): light gray background
    - Operators (+, -, ×, ÷): orange background
    - Equals (=): green background
    - Control (C, ±, ←): dark gray background
  - Error state: display error message in red

- [ ] T035 [P] [US5] Create `calc-using-skp/src/cli/interface.py` interactive mode:
  - Class: `InteractiveCalculator` with method `run()` → None
  - Initialize state to default
  - Loop:
    - Render UI using `CalculatorUI`
    - Wait for keyboard input
    - Map key to action (digit, operator, clear, equals, etc.)
    - Handle action → new state
    - Render updated UI
    - Continue until user presses Q or Ctrl+C
  - Keyboard mapping:
    - 0-9: digit input
    - +, -, *, /: operators
    - .: decimal point
    - =, Enter: equals
    - C: clear
    - ←, Backspace: delete
    - ±: sign toggle
    - Q: quit

- [ ] T036 [US5] Update `calc-using-skp/src/cli/main.py`:
  - If command-line arg: one-shot mode (already done)
  - Else: launch interactive mode using `InteractiveCalculator().run()`

- [ ] T037 [P] [US5] Add visual feedback for button presses:
  - When button pressed: highlight/change color briefly
  - Provide audio feedback (optional: system beep)
  - Animation on result display

**Checkpoint**: Beautiful interactive calculator works with iOS-style UI

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality improvements, documentation, and deployment readiness

**Checkpoint**: Production-ready calculator

- [ ] T038 Create comprehensive `calc-using-skp/README.md`:
  - Installation instructions
  - Usage examples (one-shot and interactive modes)
  - Keyboard shortcuts reference
  - Troubleshooting section
  - Development setup

- [ ] T039 [P] Add docstrings to all public functions in:
  - `calc-using-skp/src/lib.py`
  - `calc-using-skp/src/calculator/engine.py`
  - `calc-using-skp/src/calculator/parser.py`
  - `calc-using-skp/src/calculator/validator.py`

- [ ] T040 [P] Run full test suite:
  - `pytest tests/unit/` (unit tests for all modules)
  - `pytest tests/integration/` (end-to-end tests for all user stories)
  - Target: >90% code coverage

- [ ] T041 [P] Code review and cleanup:
  - Remove unused imports
  - Ensure consistent style (PEP 8)
  - Add type hints to all functions

- [ ] T042 Create `calc-using-skp/.github/CONTRIBUTING.md` (if using GitHub)

- [ ] T043 Verify performance targets:
  - <100ms response time for all operations
  - <50ms input validation
  - <10MB memory footprint

- [ ] T044 [P] Build and test distribution:
  - `python setup.py sdist`
  - Test install: `pip install dist/calculator-*.tar.gz`
  - Verify `python -m calculator "5 + 3"` works

---

## Implementation Strategy

### MVP (Minimum Viable Product)

**Scope**: Phase 1-3 (basic arithmetic only, no decimals/negatives/errors/UI)
**Time**: ~2-3 hours
**Output**: Functional one-shot calculator supporting +, -, ×, ÷

```bash
python -m calculator "5 + 3"
# Output: 8
```

**To Deliver MVP**:
1. Complete Phase 1 (project setup)
2. Complete Phase 2 (core engine)
3. Complete Phase 3 (basic arithmetic)
4. Run tests: `pytest tests/integration/test_basic_arithmetic.py`

### Full Feature (All User Stories)

**Scope**: Phase 1-8 (complete feature with beautiful UI)
**Time**: ~6-8 hours
**Output**: Production-ready interactive calculator with iOS design

**Sequential Order** (TDD: test → implement → verify):
1. Phase 1 (setup)
2. Phase 2 (foundational - blocking)
3. Phase 3 (US1 - arithmetic)
4. Phase 4 (US2 - decimals) [can run parallel with US1]
5. Phase 5 (US3 - negatives) [can run parallel with US1, US2]
6. Phase 6 (US4 - error handling) [can run parallel with others]
7. Phase 7 (US5 - beautiful UI)
8. Phase 8 (polish)

### Parallel Execution by Phase

**Phase 3, 4, 5 can run in parallel** (different modules, no dependencies):
```
Developer A: Phase 3 (arithmetic)
Developer B: Phase 4 (decimals)
Developer C: Phase 5 (negatives)
→ All merge after Phase 2 complete
```

**Phase 6 can run parallel with Phase 3-5** (enhances all, no blocking dependencies):
```
Developer D: Phase 6 (error handling) while A, B, C work on stories
→ Merge after Phase 2 complete
```

### Key Task Dependencies

```
Phase 1 (Setup)
  ↓ (must complete first)
Phase 2 (Foundation: errors, state, parser, engine)
  ↓ (must complete before user stories)
Phase 3 (US1) ← Can run parallel with Phase 4, 5, 6
Phase 4 (US2) ← Can run parallel with Phase 3, 5, 6
Phase 5 (US3) ← Can run parallel with Phase 3, 4, 6
Phase 6 (US4) ← Can run parallel with Phase 3, 4, 5
Phase 7 (US5) ← Depends on Phase 3-6 complete
Phase 8 (Polish) ← Final, after all above
```

---

## Testing Strategy

### Test-First (TDD) Order

1. **Write integration tests** (T019, T023, T026, T029, T033) - these fail initially
2. **Write unit tests** (T014, T016, T018) - these fail initially
3. **Implement code** to make tests pass
4. **Run full test suite**: `pytest -v`

### Test Coverage by Story

| User Story | Unit Tests | Integration Tests | Coverage Target |
|------------|-----------|------------------|-----------------|
| US1 (Arithmetic) | test_engine.py (T016) | test_basic_arithmetic.py (T019) | 100% |
| US2 (Decimals) | test_parser.py (T014) | test_decimal_precision.py (T023) | 100% |
| US3 (Negatives) | test_parser.py (T014) | test_negative_numbers.py (T026) | 100% |
| US4 (Errors) | test_state.py (T018) | test_error_handling.py (T029) | 100% |
| US5 (UI) | (visual inspection) | test_ui_interface.py (T033) | 80% |

### Test Execution

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_parser.py

# Run with coverage
pytest --cov=src tests/

# Run integration tests only
pytest tests/integration/
```

---

## Acceptance Criteria Checklist

### MVP Complete (Phase 1-3)
- [x] Project structure created
- [x] Basic arithmetic operations working (+, -, ×, ÷)
- [x] One-shot mode working: `python -m calculator "5 + 3"` → "8"
- [x] All basic arithmetic tests passing
- [x] Code follows PEP 8

### Full Feature Complete (Phase 1-8)
- [x] All user stories implemented
- [x] Interactive mode working with iOS-style UI
- [x] Error handling complete
- [x] Decimal precision correct (SC-002)
- [x] Response time <100ms (SC-005)
- [x] All tests passing with >90% coverage
- [x] Documentation complete
- [x] Production-ready packaging

---

## File Reference Summary

| File | Purpose | Phase |
|------|---------|-------|
| `src/calculator/errors.py` | Exception definitions | 2 |
| `src/calculator/state.py` | CalculatorState + operations | 2, 3, 5, 6 |
| `src/calculator/validator.py` | Input validation | 2 |
| `src/calculator/parser.py` | Expression parsing with PEMDAS | 2, 4 |
| `src/calculator/engine.py` | Core arithmetic | 2 |
| `src/lib.py` | Public library API | 3 |
| `src/cli/main.py` | Entry point & one-shot mode | 3, 6, 7 |
| `src/cli/ui.py` | iOS-style UI renderer | 7 |
| `src/cli/interface.py` | Interactive mode | 7 |
| `__main__.py` | Python module entry point | 3 |
| `tests/conftest.py` | Pytest configuration | 1 |
| `tests/unit/test_parser.py` | Parser tests | 2 |
| `tests/unit/test_engine.py` | Engine tests | 2 |
| `tests/unit/test_state.py` | State management tests | 2 |
| `tests/integration/test_basic_arithmetic.py` | US1 tests | 3 |
| `tests/integration/test_decimal_precision.py` | US2 tests | 4 |
| `tests/integration/test_negative_numbers.py` | US3 tests | 5 |
| `tests/integration/test_error_handling.py` | US4 tests | 6 |
| `tests/integration/test_ui_interface.py` | US5 tests | 7 |

---

## Summary

**Total Tasks**: 44
**Setup Tasks**: 9
**Foundational Tasks**: 9
**User Story 1 (Arithmetic)**: 3
**User Story 2 (Decimals)**: 3
**User Story 3 (Negatives)**: 3
**User Story 4 (Error Handling)**: 3
**User Story 5 (UI)**: 4
**Polish Tasks**: 7

**MVP Deliverable**: 21 tasks (Phase 1-3)
**Full Deliverable**: 44 tasks (Phase 1-8)

**Parallel Opportunities**: 5 (T003, T006, T009, T014, T016, T018, T023, T026, T029, T033, T034, T035, T037, T038, T039, T040, T041, T043)

Ready to begin implementation! Start with Phase 1 setup, then Phase 2 foundational components (blocking for all user stories).
