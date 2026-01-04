"""Integration tests for UI and interactive interface (User Story 5)."""

import pytest
from decimal import Decimal
from calculator.state import CalculatorState
from cli.ui import CalculatorUI


@pytest.fixture
def ui():
    """Fixture for CalculatorUI instance."""
    return CalculatorUI()


class TestUIIntegration:
    """Integration tests for User Story 5: iOS-style UI."""

    def test_display_shows_initial_zero(self, ui):
        """Test that UI displays "0" at startup."""
        state = CalculatorState()
        rendered = ui.render(state)
        assert "0" in rendered

    def test_display_updates_on_digit(self, ui):
        """Test that display shows digit after input."""
        state = CalculatorState(display=Decimal('5'), is_new_input=False)
        rendered = ui.render(state)
        assert "5" in rendered

    def test_display_shows_multiple_digits(self, ui):
        """Test that display shows multiple digits."""
        state = CalculatorState(display=Decimal('123'), is_new_input=False)
        rendered = ui.render(state)
        assert "123" in rendered

    def test_display_shows_decimal(self, ui):
        """Test that display shows decimal numbers."""
        state = CalculatorState(display=Decimal('3.14'), is_new_input=False)
        rendered = ui.render(state)
        assert "3.14" in rendered

    def test_display_shows_negative(self, ui):
        """Test that display shows negative numbers."""
        state = CalculatorState(display=Decimal('-5'), is_new_input=False)
        rendered = ui.render(state)
        assert "-5" in rendered

    def test_ui_shows_operator_symbols(self, ui):
        """Test that UI contains operator symbols."""
        state = CalculatorState()
        rendered = ui.render(state)
        assert "+" in rendered
        assert "−" in rendered or "-" in rendered
        assert "×" in rendered or "*" in rendered
        assert "÷" in rendered or "/" in rendered

    def test_ui_shows_control_buttons(self, ui):
        """Test that UI shows control buttons (C, ±, ←)."""
        state = CalculatorState()
        rendered = ui.render(state)
        assert "C" in rendered
        assert "±" in rendered
        assert "←" in rendered

    def test_ui_shows_equals_button(self, ui):
        """Test that UI shows equals button."""
        state = CalculatorState()
        rendered = ui.render(state)
        assert "=" in rendered

    def test_ui_shows_digit_buttons(self, ui):
        """Test that UI shows all digit buttons (0-9)."""
        state = CalculatorState()
        rendered = ui.render(state)
        for digit in range(10):
            assert str(digit) in rendered

    def test_ui_shows_decimal_point(self, ui):
        """Test that UI shows decimal point button."""
        state = CalculatorState()
        rendered = ui.render(state)
        assert "." in rendered

    def test_error_state_displayed(self, ui):
        """Test that error message is displayed in error state."""
        state = CalculatorState(error="Cannot divide by zero")
        rendered = ui.render(state)
        assert "Cannot divide by zero" in rendered
        assert "Error" in rendered

    def test_button_grid_layout(self, ui):
        """Test that button grid maintains structure."""
        state = CalculatorState()
        rendered = ui.render(state)
        # UI should contain the display panel
        assert "Display" in rendered or "display" in rendered.lower()
        # Should have multiple rows (buttons)
        assert rendered.count("\n") > 5  # At least display + 5 rows of buttons

    def test_render_returns_string(self, ui):
        """Test that render method returns a string."""
        state = CalculatorState()
        rendered = ui.render(state)
        assert isinstance(rendered, str)
        assert len(rendered) > 0
