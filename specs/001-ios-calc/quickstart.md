# Quickstart: iOS-Style CLI Calculator

**Feature**: iOS-Style CLI Calculator (001-ios-calc)
**Date**: 2026-01-04
**Purpose**: Setup guide and usage examples

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository** (if not already done)
```bash
git clone <repository-url>
cd PANA-300-P009
```

2. **Navigate to the project**
```bash
cd calc-using-skp
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

The `requirements.txt` will include:
```
rich>=13.0.0
pytest>=7.0.0
pytest-cov>=4.0.0
```

4. **Verify installation**
```bash
python -m calculator --help
```

---

## Usage Modes

### Interactive Mode (Default)

Launch the beautiful interactive calculator:

```bash
python -m calculator
```

This displays the iOS-style button grid and accepts keyboard input.

**Example Session**:
```
$ python -m calculator

┌─────────────────────────────────┐
│        Display: 0               │
├─────────────────────────────────┤
│  C  │  ±  │  ←  │  ÷          │
├─────────────────────────────────┤
│  7  │  8  │  9  │  ×          │
├─────────────────────────────────┤
│  4  │  5  │  6  │  -          │
├─────────────────────────────────┤
│  1  │  2  │  3  │  +          │
├─────────────────────────────────┤
│  0  │  .  │     =              │
└─────────────────────────────────┘

> [User presses: 1, 5, +, 3, =]
Display: 18
```

**Keyboard Shortcuts**:
| Key | Action |
|-----|--------|
| `0-9` | Input digit |
| `.` | Input decimal point |
| `+` | Addition |
| `-` | Subtraction |
| `*` or `×` | Multiplication |
| `/` or `÷` | Division |
| `=` or `Enter` | Calculate |
| `C` | Clear |
| `←` or `Backspace` | Delete last digit |
| `±` | Toggle sign |
| `Q` or `Ctrl+C` | Quit |

### One-Shot Mode

Calculate a single expression from the command line:

```bash
python -m calculator "5 + 3"
```

**Output**:
```
8
```

**More Examples**:
```bash
# Addition
$ python -m calculator "10 + 5"
15

# Subtraction
$ python -m calculator "20 - 8"
12

# Multiplication
$ python -m calculator "6 * 7"
42

# Division
$ python -m calculator "15 / 3"
5

# Decimals
$ python -m calculator "0.1 + 0.2"
0.3

# Order of operations (PEMDAS)
$ python -m calculator "5 + 3 * 2"
11

# Negative numbers
$ python -m calculator "-10 + 5"
-5
```

---

## Common Workflows

### Calculation with Multiple Steps

**Goal**: Calculate (5 + 3) × 2

**Interactive Mode**:
1. Press: `5`
2. Press: `+`
3. Press: `3`
4. Press: `×` (automatically evaluates 5 + 3 = 8)
5. Press: `2`
6. Press: `=`
7. Result: `16`

**One-Shot Mode**:
```bash
$ python -m calculator "5 + 3 * 2"
11
```

Note: Result is 11 (not 16) because of PEMDAS—multiplication is done first.

### Decimal Calculations

**Goal**: Verify 0.1 + 0.2 = 0.3 (not 0.30000000001)

**Interactive Mode**:
```
1. Press: 0
2. Press: .
3. Press: 1
4. Press: +
5. Press: 0
6. Press: .
7. Press: 2
8. Press: =
Result: 0.3 ✓
```

**One-Shot Mode**:
```bash
$ python -m calculator "0.1 + 0.2"
0.3
```

### Working with Negatives

**Goal**: Calculate -5 + 3

**Interactive Mode**:
```
1. Press: 5
2. Press: ± (toggles to -5)
3. Press: +
4. Press: 3
5. Press: =
Result: -2
```

**One-Shot Mode**:
```bash
$ python -m calculator "-5 + 3"
-2
```

---

## Error Handling

### Error Cases

#### Division by Zero
```bash
$ python -m calculator "5 / 0"
Error: Cannot divide by zero
```

**Interactive Mode**: Error displays, press `C` to clear

#### Incomplete Expression
```bash
$ python -m calculator "5 +"
Error: Incomplete expression
```

**Interactive Mode**: Error displays, press any digit to start fresh or press `C`

#### Invalid Operator
```bash
$ python -m calculator "5 @ 3"
Error: Invalid operator: @
```

**Interactive Mode**: Invalid operator is ignored

#### Malformed Input
```bash
$ python -m calculator "5.5.5"
Error: Invalid number format
```

---

## Development Setup

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=calculator

# Run specific test file
pytest tests/unit/test_engine.py

# Run with verbose output
pytest -v
```

### Project Structure for Developers

```
calc-using-skp/
├── src/
│   ├── calculator/
│   │   ├── engine.py         # Core calculation logic
│   │   ├── parser.py         # Expression parsing
│   │   ├── validator.py      # Input validation
│   │   ├── state.py          # State management
│   │   └── errors.py         # Error definitions
│   ├── cli/
│   │   ├── interface.py      # Interactive CLI
│   │   ├── ui.py             # iOS-style UI
│   │   └── main.py           # Entry point
│   └── lib.py                # Public API
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── conftest.py           # Test configuration
├── README.md
├── requirements.txt
└── setup.py
```

### Running from Source

If modifying code locally:

```bash
# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run interactive mode
python -m src.cli.main

# Run one-shot calculation
python -m src.cli.main "5 + 3"

# Run tests
pytest tests/
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'rich'"

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Calculator not responding to keyboard input

**Solution**: Ensure you're using a terminal that supports ANSI codes:
- ✅ Works: macOS Terminal, Linux shell, Windows Terminal (v1.0+)
- ❌ May not work: Windows Command Prompt (legacy)

For Windows, upgrade to Windows Terminal (available free from Microsoft Store).

### Issue: Decimal precision not matching expectations

**Solution**: The calculator uses `decimal.Decimal` for precision. This is intentional and ensures accuracy (e.g., 0.1 + 0.2 = 0.3).

### Issue: Order of operations not matching expectations

**Solution**: The calculator uses PEMDAS (standard mathematical order). For example:
- `5 + 3 * 2 = 11` (multiply first)
- NOT `5 + 3 * 2 = 16` (left-to-right)

This is the correct mathematical behavior.

---

## Next Steps

1. **Interactive Testing**: Try the calculator with various expressions
2. **Development**: Run the test suite to verify all features
3. **Integration**: Use the calculator library in your own Python code

```python
from calculator import Calculator

calc = Calculator()
result = calc.calculate("5 + 3")
print(result)  # Output: 8
```

---

## Support

For issues or questions, refer to:
- **Plan**: `specs/001-ios-calc/plan.md`
- **Data Model**: `specs/001-ios-calc/data-model.md`
- **CLI Contract**: `specs/001-ios-calc/contracts/cli.md`
- **Research**: `specs/001-ios-calc/research.md`
