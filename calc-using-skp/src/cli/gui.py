"""GUI application for iOS-style calculator using Tkinter."""

import tkinter as tk
from decimal import Decimal
from calculator.engine import Calculator
from calculator.errors import CalculatorError


class CalculatorGUI:
    """GUI application for the calculator."""

    def __init__(self, root):
        """Initialize the calculator GUI.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("iOS Calculator")
        self.root.geometry("350x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1c1c1c")

        # Calculator engine
        self.calc = Calculator()

        # Expression and display
        self.expression = ""
        self.display_value = "0"

        # Setup UI
        self._setup_display()
        self._setup_buttons()

    def _setup_display(self):
        """Setup the display area."""
        # Display frame using grid
        display_frame = tk.Frame(self.root, bg="#1c1c1c", height=100)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=20)
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        # Display label
        self.display_label = tk.Label(
            display_frame,
            text=self.display_value,
            font=("Helvetica", 60, "bold"),
            bg="#1c1c1c",
            fg="#ffffff",
            anchor="e",
            padx=20
        )
        self.display_label.grid(row=0, column=0, sticky="nsew")

    def _setup_buttons(self):
        """Setup the button grid."""
        # Button layout: 5 rows × 4 columns
        buttons = [
            [("C", "#a5a5a5"), ("±", "#a5a5a5"), ("←", "#a5a5a5"), ("÷", "#ff9500")],
            [("7", "#333333"), ("8", "#333333"), ("9", "#333333"), ("×", "#ff9500")],
            [("4", "#333333"), ("5", "#333333"), ("6", "#333333"), ("−", "#ff9500")],
            [("1", "#333333"), ("2", "#333333"), ("3", "#333333"), ("+", "#ff9500")],
            [("0", "#333333"), (".", "#333333"), ("", "#1c1c1c"), ("=", "#4caf50")],
        ]

        for row_idx, row in enumerate(buttons, start=1):
            for col_idx, (text, color) in enumerate(row):
                if text == "":  # Empty space
                    empty = tk.Frame(self.root, bg="#1c1c1c")
                    empty.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=8)
                elif text == "0":  # 0 button spans 2 columns
                    btn = self._create_button(text, color)
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, sticky="nsew", padx=5, pady=8)
                else:
                    btn = self._create_button(text, color)
                    btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=5, pady=8)

        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        for i in range(1, 6):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def _create_button(self, text, bg_color):
        """Create a styled button.

        Args:
            text: Button label
            bg_color: Background color

        Returns:
            Configured button widget
        """
        # Determine text color based on button type
        if text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            text_color = "#ffffff"
            font_size = 28
        elif text in ["+", "−", "×", "÷", "="]:
            text_color = "#ffffff"
            font_size = 28
        else:  # Control buttons (C, ±, ←)
            text_color = "#000000"
            font_size = 24

        btn = tk.Button(
            self.root,
            text=text,
            font=("Helvetica", font_size, "bold"),
            bg=bg_color,
            fg=text_color,
            border=0,
            activebackground=self._lighten_color(bg_color),
            activeforeground=text_color,
            command=lambda: self._on_button_click(text)
        )
        return btn

    @staticmethod
    def _lighten_color(color):
        """Lighten a hex color."""
        # Simple lightening effect
        color_map = {
            "#333333": "#555555",
            "#a5a5a5": "#c5c5c5",
            "#ff9500": "#ffb143",
            "#4caf50": "#66bb6a",
            "#1c1c1c": "#3c3c3c",
        }
        return color_map.get(color, color)

    def _on_button_click(self, char):
        """Handle button click.

        Args:
            char: Character/operation pressed
        """
        if char == "C":
            # Clear
            self.expression = ""
            self.display_value = "0"
        elif char == "←":
            # Backspace - remove last character from expression
            self.expression = self.expression[:-1]
            self.display_value = self.expression if self.expression else "0"
        elif char == "±":
            # Toggle sign
            try:
                val = float(self.expression) if self.expression else 0
                val = -val
                self.expression = str(val)
                self.display_value = self.expression
            except (ValueError, TypeError):
                pass
        elif char == "=":
            # Calculate result
            try:
                result = self.calc.calculate(self.expression)
                self.display_value = self.calc.format_result(result)
                self.expression = self.display_value
            except CalculatorError as e:
                self.display_value = f"Error: {e}"
                self.expression = ""
            except Exception as e:
                self.display_value = "Error"
                self.expression = ""
        elif char in ["+", "−", "×", "÷"]:
            # Operators - normalize symbols
            op_map = {"−": "-", "×": "*", "÷": "/"}
            op = op_map.get(char, char)

            if self.expression:
                self.expression += f" {op} "
            self.display_value = self.expression
        elif char == ".":
            # Decimal point
            if "." not in self.expression.split()[-1] if self.expression else True:
                self.expression += char
                self.display_value = self.expression
        else:
            # Number
            if self.display_value == "0" and char != "0":
                self.expression = char
            else:
                self.expression += char
            self.display_value = self.expression

        # Update display
        self.display_label.config(text=self.display_value)


def main_gui():
    """Launch the GUI calculator."""
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main_gui()
