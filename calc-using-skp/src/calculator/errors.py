"""Calculator exception hierarchy."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""

    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""

    def __init__(self, message: str = "Cannot divide by zero"):
        self.message = message
        super().__init__(self.message)


class InvalidOperatorError(CalculatorError):
    """Raised for unsupported operators."""

    def __init__(self, operator: str):
        self.operator = operator
        self.message = f"Invalid operator: {operator}"
        super().__init__(self.message)


class InvalidNumberError(CalculatorError):
    """Raised for malformed number input."""

    def __init__(self, value: str):
        self.value = value
        self.message = f"Invalid number: {value}"
        super().__init__(self.message)


class InvalidExpressionError(CalculatorError):
    """Raised for incomplete or malformed expressions."""

    def __init__(self, message: str = "Invalid expression"):
        self.message = message
        super().__init__(self.message)
