"""iOS-style UI renderer for the calculator.

Provides beautiful terminal rendering with rich library.
"""

from decimal import Decimal
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from calculator.state import CalculatorState


class CalculatorUI:
    """Renders iOS-style calculator UI using rich library."""

    def __init__(self):
        """Initialize the UI renderer."""
        self.console = Console()

    def render(self, state: CalculatorState) -> str:
        """Render calculator UI based on current state.

        Args:
            state: Current CalculatorState

        Returns:
            Rendered UI as string
        """
        from io import StringIO

        # Display panel at top
        display_text = str(state.display) if state.display != Decimal('0') or state.is_new_input else "0"
        if state.error:
            display_panel = Panel(
                f"[red]{state.error}[/red]",
                title="[bold]Error[/bold]",
                padding=(1, 2),
                border_style="red"
            )
        else:
            display_panel = Panel(
                f"[bold white]{display_text}[/bold white]",
                title="[bold cyan]Display[/bold cyan]",
                padding=(1, 2),
                border_style="cyan"
            )

        # Button grid: 5 rows × 4 columns
        button_grid = Table(show_header=False, show_footer=False, padding=(1, 2), pad_edge=False)
        button_grid.add_column(width=10)
        button_grid.add_column(width=10)
        button_grid.add_column(width=10)
        button_grid.add_column(width=10)

        # Row 1: C, ±, ←, ÷
        button_grid.add_row(
            self._format_button("C", "gray", "control"),
            self._format_button("±", "gray", "control"),
            self._format_button("←", "gray", "control"),
            self._format_button("÷", "orange3", "operator")
        )

        # Row 2: 7, 8, 9, ×
        button_grid.add_row(
            self._format_button("7", "bright_black", "number"),
            self._format_button("8", "bright_black", "number"),
            self._format_button("9", "bright_black", "number"),
            self._format_button("×", "orange3", "operator")
        )

        # Row 3: 4, 5, 6, -
        button_grid.add_row(
            self._format_button("4", "bright_black", "number"),
            self._format_button("5", "bright_black", "number"),
            self._format_button("6", "bright_black", "number"),
            self._format_button("−", "orange3", "operator")
        )

        # Row 4: 1, 2, 3, +
        button_grid.add_row(
            self._format_button("1", "bright_black", "number"),
            self._format_button("2", "bright_black", "number"),
            self._format_button("3", "bright_black", "number"),
            self._format_button("+", "orange3", "operator")
        )

        # Row 5: 0, ., blank, =
        button_grid.add_row(
            self._format_button("0", "bright_black", "number"),
            self._format_button(".", "bright_black", "number"),
            self._format_button("", "white", "blank"),
            self._format_button("=", "green", "equals")
        )

        # Render to string using console buffer
        buffer = StringIO()
        temp_console = Console(file=buffer, force_terminal=True)
        temp_console.print(display_panel)
        temp_console.print(button_grid)
        return buffer.getvalue()

    @staticmethod
    def _format_button(text: str, color: str, button_type: str) -> str:
        """Format a button with appropriate styling.

        Args:
            text: Button label
            color: Color name for rich
            button_type: Type of button (number, operator, control, equals, blank)

        Returns:
            Formatted button as rich-styled string
        """
        if button_type == "blank":
            return "[dim]   [/dim]"

        if button_type == "number":
            return f"[{color} on gray23]{text:^7}[/{color} on gray23]"
        elif button_type == "operator":
            return f"[bold white on {color}]{text:^7}[/bold white on {color}]"
        elif button_type == "equals":
            return f"[bold white on {color}]{text:^7}[/bold white on {color}]"
        elif button_type == "control":
            return f"[white on gray15]{text:^7}[/white on gray15]"
        else:
            return f"[white]{text:^7}[/white]"

    def clear_screen(self):
        """Clear the terminal screen."""
        self.console.clear()

    def print_message(self, message: str, style: str = ""):
        """Print a message to the console.

        Args:
            message: Message to print
            style: Rich style to apply
        """
        if style:
            self.console.print(f"[{style}]{message}[/{style}]")
        else:
            self.console.print(message)
