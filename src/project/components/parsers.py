"""
components/parsers.py
---------------------
Recursive-descent parser for the Propositional Logic Evaluator.

Grammar (operator priority encoded by rule depth)
--------------------------------------------------
    expr  →  term  ( OR  term  )*
    term  →  atom  ( AND atom  )*
    atom  →  TRUE
           | FALSE
           | LPAREN expr RPAREN

Priority explanation
--------------------
  ∧ (AND) has HIGHER priority than ∨ (OR).
  This is expressed by placing AND deeper in the grammar:
    - expr  handles OR   → weakest, outermost
    - term  handles AND  → stronger, inner
    - atom  handles literals and parenthesised sub-expressions

  Example:  t ∨ f ∧ f
    The parser builds:  OrNode( BoolLit(t),  AndNode(BoolLit(f), BoolLit(f)) )
    which evaluates to: True ∨ (False ∧ False)  =  True ∨ False  =  True  ✓

Usage
-----
    from components.lexica  import PropLexer
    from components.parsers import PropParser

    tokens = PropLexer().tokenize("t ∨ f ∧ f")
    ast    = PropParser().parse(tokens)

    print(ast.evaluate())   # True
    print(ast.to_prefix())  # ∨ t ∧ f f
"""

from components.ast.statement import BoolLit, AndNode, OrNode
from components.lexica import PropLexer


class PropParser:
    """
    A hand-written recursive-descent parser.

    It consumes a token stream produced by PropLexer and builds an AST
    whose root node can be evaluated or translated to prefix notation.
    """

    # ------------------------------------------------------------------ #
    # Public entry point
    # ------------------------------------------------------------------ #

    def parse(self, tokens):
        """
        Parse a token stream and return the root AST node.

        Parameters
        ----------
        tokens : generator
            Token stream from PropLexer().tokenize(...)

        Returns
        -------
        BoolLit | AndNode | OrNode
            Root of the abstract syntax tree.

        Raises
        ------
        SyntaxError
            If the token stream does not match the grammar.
        """
        self._tokens  = list(tokens)   # materialise generator into a list
        self._pos     = 0              # current position in the token list

        ast = self._expr()             # start with the top-level rule

        # After parsing, we should have consumed ALL tokens.
        if self._pos < len(self._tokens):
            tok = self._tokens[self._pos]
            raise SyntaxError(
                f"Unexpected token '{tok.value}' at position {self._pos}. "
                f"The expression was fully parsed before this token."
            )

        return ast

    # ------------------------------------------------------------------ #
    # Grammar rules  (each method = one grammar production)
    # ------------------------------------------------------------------ #

    def _expr(self):
        """
        expr → term ( OR term )*

        Handles the weakest operator (∨).
        Keeps consuming OR-separated terms and folds them left into OrNodes.
        """
        node = self._term()                    # parse the first term

        while self._current_is('OR'):
            self._consume('OR')                # eat the ∨ token
            right = self._term()               # parse the next term
            node  = OrNode(node, right)        # fold left

        return node

    def _term(self):
        """
        term → atom ( AND atom )*

        Handles the stronger operator (∧).
        Keeps consuming AND-separated atoms and folds them left into AndNodes.
        """
        node = self._atom()                    # parse the first atom

        while self._current_is('AND'):
            self._consume('AND')               # eat the ∧ token
            right = self._atom()               # parse the next atom
            node  = AndNode(node, right)       # fold left

        return node

    def _atom(self):
        """
        atom → TRUE | FALSE | LPAREN expr RPAREN

        Handles the base cases: literals and parenthesised sub-expressions.
        """
        # --- TRUE literal ---
        if self._current_is('TRUE'):
            self._consume('TRUE')
            return BoolLit(True)

        # --- FALSE literal ---
        if self._current_is('FALSE'):
            self._consume('FALSE')
            return BoolLit(False)

        # --- Parenthesised sub-expression: ( expr ) ---
        if self._current_is('LPAREN'):
            self._consume('LPAREN')
            node = self._expr()                # recursively parse inner expr
            self._consume('RPAREN')            # must close the parenthesis
            return node

        # --- Nothing matched: syntax error ---
        if self._pos < len(self._tokens):
            tok = self._tokens[self._pos]
            raise SyntaxError(
                f"Unexpected token '{tok.value}' (type: {tok.type}) "
                f"at position {self._pos}. "
                f"Expected TRUE, FALSE, or '('."
            )
        else:
            raise SyntaxError(
                "Unexpected end of expression. "
                "Expected TRUE, FALSE, or '('."
            )

    # ------------------------------------------------------------------ #
    # Helper utilities
    # ------------------------------------------------------------------ #

    def _current_is(self, token_type: str) -> bool:
        """Return True if the current token matches the given type."""
        if self._pos >= len(self._tokens):
            return False
        return self._tokens[self._pos].type == token_type

    def _consume(self, token_type: str):
        """
        Assert the current token matches token_type, then advance.

        Raises SyntaxError if the token does not match.
        """
        if self._pos >= len(self._tokens):
            raise SyntaxError(
                f"Expected '{token_type}' but reached end of expression."
            )
        tok = self._tokens[self._pos]
        if tok.type != token_type:
            raise SyntaxError(
                f"Expected '{token_type}' but got '{tok.value}' "
                f"(type: {tok.type}) at position {self._pos}."
            )
        self._pos += 1   # advance past the consumed token


# ---------------------------------------------------------------------------
# Quick self-test  (run:  python parsers.py)
# ---------------------------------------------------------------------------
if __name__ == '__main__':

    def run(text: str):
        """Helper: lex + parse an expression, return (truth_value, prefix)."""
        tokens = PropLexer().tokenize(text)
        ast    = PropParser().parse(tokens)
        return ast.evaluate(), ast.to_prefix()

    print("=== Single literals ===")
    assert run("t") == (True,  't')
    assert run("f") == (False, 'f')
    print("  t  →", run("t"))
    print("  f  →", run("f"))

    print("\n=== Single AND ===")
    assert run("t ∧ t") == (True,  '∧ t t')
    assert run("t ∧ f") == (False, '∧ t f')
    assert run("f ∧ t") == (False, '∧ f t')
    assert run("f ∧ f") == (False, '∧ f f')
    print("  t ∧ t  →", run("t ∧ t"))
    print("  t ∧ f  →", run("t ∧ f"))

    print("\n=== Single OR ===")
    assert run("t ∨ t") == (True,  '∨ t t')
    assert run("t ∨ f") == (True,  '∨ t f')
    assert run("f ∨ t") == (True,  '∨ f t')
    assert run("f ∨ f") == (False, '∨ f f')
    print("  t ∨ f  →", run("t ∨ f"))
    print("  f ∨ f  →", run("f ∨ f"))

    print("\n=== Spec example:  t ∨ f ∧ f  (AND binds tighter) ===")
    val, pre = run("t ∨ f ∧ f")
    print(f"  evaluate()  = {val}  (expected: True)")
    print(f"  to_prefix() = {pre}  (expected: ∨ t ∧ f f)")
    assert val == True
    assert pre == '∨ t ∧ f f'

    print("\n=== Priority:  f ∧ f ∨ t  (AND still binds tighter) ===")
    val, pre = run("f ∧ f ∨ t")
    print(f"  evaluate()  = {val}  (expected: True)")
    print(f"  to_prefix() = {pre}  (expected: ∨ ∧ f f t)")
    assert val == True
    assert pre == '∨ ∧ f f t'

    print("\n=== Chained AND:  t ∧ t ∧ f ===")
    val, pre = run("t ∧ t ∧ f")
    print(f"  evaluate()  = {val}  (expected: False)")
    print(f"  to_prefix() = {pre}  (expected: ∧ ∧ t t f)")
    assert val == False
    assert pre == '∧ ∧ t t f'

    print("\n=== Chained OR:  f ∨ f ∨ t ===")
    val, pre = run("f ∨ f ∨ t")
    print(f"  evaluate()  = {val}  (expected: True)")
    print(f"  to_prefix() = {pre}  (expected: ∨ ∨ f f t)")
    assert val == True
    assert pre == '∨ ∨ f f t'

    print("\n=== Parentheses override priority:  (t ∨ f) ∧ f ===")
    val, pre = run("(t ∨ f) ∧ f")
    print(f"  evaluate()  = {val}  (expected: False)")
    print(f"  to_prefix() = {pre}  (expected: ∧ ∨ t f f)")
    assert val == False
    assert pre == '∧ ∨ t f f'

    print("\n=== Nested parentheses:  (t ∨ (f ∧ t)) ∨ f ===")
    val, pre = run("(t ∨ (f ∧ t)) ∨ f")
    print(f"  evaluate()  = {val}  (expected: True)")
    print(f"  to_prefix() = {pre}  (expected: ∨ ∨ t ∧ f t f)")
    assert val == True
    assert pre == '∨ ∨ t ∧ f t f'

    print("\n=== Error: empty input ===")
    try:
        run("")
        assert False, "Should have raised"
    except SyntaxError as e:
        print(f"  Caught expected SyntaxError: {e}")

    print("\n=== Error: invalid token ===")
    try:
        run("t ∧ x")
        assert False, "Should have raised"
    except ValueError as e:
        print(f"  Caught expected ValueError from lexer: {e}")

    print("\n=== Error: missing closing parenthesis ===")
    try:
        run("(t ∨ f")
        assert False, "Should have raised"
    except SyntaxError as e:
        print(f"  Caught expected SyntaxError: {e}")

    print("\nAll parser tests passed!")