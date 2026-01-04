# iOS-Style CLI Calculator

A beautiful, functional command-line calculator that mimics iOS design with seamless user experience. Supports basic arithmetic operations with proper decimal handling, negative number support, PEMDAS order of operations, and comprehensive error handling.

## Features

✨ **Beautiful iOS-Inspired Design**
- Clean button grid layout (5 rows × 4 columns)
- Color-coded buttons (operators, numbers, control buttons)
- Real-time display updates
- Error messages with clear feedback

🧮 **Core Arithmetic**
- Addition, Subtraction, Multiplication, Division
- PEMDAS order of operations (5 + 3 * 2 = 11, not 16)
- Parentheses support for operator precedence override
- Continuous calculation (5 + 3 + 2 = 10)

🔢 **Advanced Math**
- Decimal number support with precision handling
- Negative numbers (input and calculation)
- Sign toggle (±) for quick negation
- Backspace/delete functionality

⚠️ **Error Handling**
- Division by zero protection with clear messages
- Invalid expression detection
- Graceful error recovery
- Helpful error descriptions

## Installation

### Quick Start

```bash
# Install from source
pip install -e .

# Or install requirements
pip install -r requirements.txt
```

### Requirements

- Python 3.11+
- `rich>=13.0.0` (for beautiful terminal UI)
- `pytest>=7.0.0` (for testing)
- `pytest-cov>=4.0.0` (for test coverage)

## Usage

### One-Shot Mode

Calculate a single expression from the command line:

```bash
python -m calculator "5 + 3"
# Output: 8

python -m calculator "0.1 + 0.2"
# Output: 0.3

python -m calculator "5 + 3 * 2"
# Output: 11
```

### Interactive Mode

Launch the interactive calculator:

```bash
python -m calculator
```

Use keyboard to input numbers, operators, and perform calculations.

## Testing

Run the test suite:

```bash
pytest tests/

# With coverage
pytest --cov=src tests/
```

## Architecture

```
src/
├── calculator/      # Core calculation engine
│   ├── errors.py   # Exception definitions
│   ├── state.py    # Calculator state management
│   ├── validator.py # Input validation
│   ├── parser.py   # Expression parsing with PEMDAS
│   └── engine.py   # Core arithmetic operations
├── cli/            # Command-line interface
│   ├── main.py     # Entry point
│   ├── interface.py # Interactive mode
│   └── ui.py       # iOS-style UI rendering
└── lib.py          # Public library API

tests/
├── unit/           # Unit tests for components
└── integration/    # End-to-end tests
```

## Development

### Test-First Approach

Tests are written before implementation (TDD):

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Check coverage
pytest --cov=src --cov-report=term-missing tests/
```

## Requirements

- Python 3.11+
- rich (for beautiful CLI rendering)
- pytest (for testing)
