"""
main.py
-------
Entry point for the Propositional Logic Evaluator.

Features
--------
  - Symbol buttons: click to insert  t  f  ∧  ∨  (  )  at the cursor position
  - Keyboard fallbacks: type  ^ or &  for ∧,  | for ∨  (auto-converted on the fly)
  - Smart spacing: a space is automatically added before/after an inserted symbol
    so the expression stays readable without the user having to press Space
  - Enter key triggers evaluation
  - Clear button resets everything

How to run (from src/project/)
-------------------------------
    python main.py
"""

import sys
import os

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore    import Qt

from components.lexica  import PropLexer
from components.parsers import PropParser


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ── Load .ui file ──────────────────────────────────────────────
        ui_path = os.path.join(os.path.dirname(__file__), "components", "main.ui")
        loader  = QUiLoader()
        self.ui = loader.load(ui_path)

        if self.ui is None:
            print(f"ERROR: Could not load UI file at {ui_path}")
            sys.exit(1)

        self.setCentralWidget(self.ui)
        self.setWindowTitle("Propositional Logic Evaluator")
        self.resize(560, 420)

        # ── Widget references ──────────────────────────────────────────
        self.input_field        = self.ui.findChild(object, "inputField")
        self.evaluate_button    = self.ui.findChild(object, "evaluateButton")
        self.truth_value_label  = self.ui.findChild(object, "truthValueLabel")
        self.prefix_value_label = self.ui.findChild(object, "prefixValueLabel")
        self.error_label        = self.ui.findChild(object, "errorLabel")

        # Symbol buttons
        self.btn_true   = self.ui.findChild(object, "btnTrue")
        self.btn_false  = self.ui.findChild(object, "btnFalse")
        self.btn_and    = self.ui.findChild(object, "btnAnd")
        self.btn_or     = self.ui.findChild(object, "btnOr")
        self.btn_lparen = self.ui.findChild(object, "btnLParen")
        self.btn_rparen = self.ui.findChild(object, "btnRParen")
        self.btn_clear  = self.ui.findChild(object, "btnClear")

        # ── Connect signals ────────────────────────────────────────────
        self.evaluate_button.clicked.connect(self.on_evaluate)
        self.input_field.returnPressed.connect(self.on_evaluate)

        # Symbol buttons — each inserts the corresponding character
        self.btn_true.clicked.connect(lambda: self._insert_symbol('t'))
        self.btn_false.clicked.connect(lambda: self._insert_symbol('f'))
        self.btn_and.clicked.connect(lambda: self._insert_symbol('∧'))
        self.btn_or.clicked.connect(lambda: self._insert_symbol('∨'))
        self.btn_lparen.clicked.connect(lambda: self._insert_symbol('('))
        self.btn_rparen.clicked.connect(lambda: self._insert_symbol(')'))
        self.btn_clear.clicked.connect(self._on_clear)

        # Live keyboard conversion: ^ → ∧,  & → ∧,  | → ∨
        self.input_field.textChanged.connect(self._auto_convert_keyboard)

    # ------------------------------------------------------------------ #
    # Symbol insertion
    # ------------------------------------------------------------------ #

    def _insert_symbol(self, symbol: str):
        """
        Insert a symbol at the current cursor position in the input field,
        with smart spacing:
          - Add a space before the symbol if the preceding character is not
            a space or an opening parenthesis.
          - Add a space after the symbol if the following character is not
            a space or a closing parenthesis.
        This keeps expressions like  t ∧ f  readable automatically.
        """
        field  = self.input_field
        text   = field.text()
        cursor = field.cursorPosition()

        before = text[:cursor]
        after  = text[cursor:]

        # Decide whether to pad with spaces
        needs_space_before = (
            len(before) > 0
            and before[-1] not in (' ', '(')
            and symbol not in ('(', ')')
        )
        needs_space_after = (
            len(after) > 0
            and after[0] not in (' ', ')')
            and symbol not in ('(', ')')
        )

        # Also add a trailing space after ( so cursor is ready for next token
        if symbol == '(':
            needs_space_after = False   # user will type content inside

        prefix_space = ' ' if needs_space_before else ''
        suffix_space = ' ' if needs_space_after  else ''

        insertion     = prefix_space + symbol + suffix_space
        new_text      = before + insertion + after
        new_cursor    = cursor + len(insertion)

        field.setText(new_text)
        field.setCursorPosition(new_cursor)
        field.setFocus()   # return focus to input field after button click

    # ------------------------------------------------------------------ #
    # Keyboard ASCII → Unicode conversion (live, as the user types)
    # ------------------------------------------------------------------ #

    def _auto_convert_keyboard(self, text: str):
        """
        Automatically replace ASCII operator shortcuts with their Unicode
        equivalents as the user types, so they don't have to copy-paste:
            ^  →  ∧
            &  →  ∧
            |  →  ∨
        The cursor position is preserved after the replacement.
        """
        replacements = {'^': '∧', '&': '∧', '|': '∨'}

        new_text = text
        for ascii_char, unicode_char in replacements.items():
            new_text = new_text.replace(ascii_char, unicode_char)

        if new_text != text:
            cursor = self.input_field.cursorPosition()
            # Block signal to avoid recursive call
            self.input_field.blockSignals(True)
            self.input_field.setText(new_text)
            self.input_field.setCursorPosition(cursor)
            self.input_field.blockSignals(False)

    # ------------------------------------------------------------------ #
    # Clear button
    # ------------------------------------------------------------------ #

    def _on_clear(self):
        """Clear the input field and reset all result labels."""
        self.input_field.clear()
        self.input_field.setFocus()
        self._clear_results()
        self._show_error("")

    # ------------------------------------------------------------------ #
    # Evaluate
    # ------------------------------------------------------------------ #

    def on_evaluate(self):
        """
        Read the expression, run lexer + parser, display results.
        """
        expression = self.input_field.text().strip()

        if not expression:
            self._show_error("Please enter an expression.")
            self._clear_results()
            return

        try:
            tokens = PropLexer().tokenize(expression)
            ast    = PropParser().parse(tokens)

            truth_value = ast.evaluate()
            prefix      = ast.to_prefix()

            # Show truth value with colour feedback
            self.truth_value_label.setText('t' if truth_value else 'f')
            self.truth_value_label.setStyleSheet(
                "font-size: 14px; font-weight: bold; color: green;"
                if truth_value else
                "font-size: 14px; font-weight: bold; color: red;"
            )

            self.prefix_value_label.setText(prefix)
            self.prefix_value_label.setStyleSheet("font-size: 14px;")
            self._show_error("")

        except ValueError as e:
            self._show_error(f"Lexer error: {e}")
            self._clear_results()

        except SyntaxError as e:
            self._show_error(f"Syntax error: {e}")
            self._clear_results()

        except Exception as e:
            self._show_error(f"Unexpected error: {e}")
            self._clear_results()

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _show_error(self, message: str):
        self.error_label.setText(message)

    def _clear_results(self):
        self.truth_value_label.setText("—")
        self.truth_value_label.setStyleSheet("font-size: 14px;")
        self.prefix_value_label.setText("—")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    app    = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()