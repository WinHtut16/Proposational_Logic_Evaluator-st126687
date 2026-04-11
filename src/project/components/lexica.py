"""
components/lexica.py
--------------------
Lexical analyser for the Propositional Logic Evaluator.

Converts an input string into a stream of tokens that the parser consumes.

Supported tokens
----------------
  TRUE    →  t
  FALSE   →  f
  AND     →  ∧   (or the ASCII alternative:  &  or  ^)
  OR      →  ∨   (or the ASCII alternative:  |)
  LPAREN  →  (
  RPAREN  →  )

Whitespace (spaces and tabs) is silently ignored.
Any other character raises a clear error message.

Usage
-----
    from components.lexica import PropLexer

    lexer  = PropLexer()
    tokens = lexer.tokenize("t ∨ f ∧ f")
    for tok in tokens:
        print(tok)
"""

from sly import Lexer


class PropLexer(Lexer):
    # ------------------------------------------------------------------ #
    # Token names  (must match exactly what the parser refers to)
    # ------------------------------------------------------------------ #
    tokens = { TRUE, FALSE, AND, OR, LPAREN, RPAREN }

    # ------------------------------------------------------------------ #
    # Ignored characters
    # ------------------------------------------------------------------ #
    ignore = ' \t'          # spaces and tabs are silently skipped

    # ------------------------------------------------------------------ #
    # Token rules  (longer / more specific patterns come first)
    # ------------------------------------------------------------------ #

    # Literal truth values
    TRUE   = r't'
    FALSE  = r'f'

    # Logical operators — accept Unicode symbols AND common ASCII fallbacks
    # so the user can type either ∧ or ^ (and ∨ or |) on any keyboard.
    AND    = r'∧|&|\^'      # ∧  or  &  or  ^
    OR     = r'∨|\|'        # ∨  or  |
    

    # Parentheses (needed for sub-expressions like  (t ∨ f) ∧ t )
    LPAREN = r'\('
    RPAREN = r'\)'

    # ------------------------------------------------------------------ #
    # Error handling
    # ------------------------------------------------------------------ #
    def error(self, t):
        """Called by sly when an unrecognised character is encountered."""
        raise ValueError(
            f"Lexer error: unexpected character '{t.value[0]}' "
            f"at position {self.index}.\n"
            f"Valid characters: t  f  ∧ (or ^ or &)  ∨ (or |)  (  )"
        )


# ---------------------------------------------------------------------------
# Quick self-test  (run:  python lexica.py)
# ---------------------------------------------------------------------------
if __name__ == '__main__':

    def tokenize_to_list(text: str) -> list:
        """Helper: return list of (type, value) pairs from an input string."""
        return [(tok.type, tok.value) for tok in PropLexer().tokenize(text)]

    print("=== Basic literals ===")
    result = tokenize_to_list("t")
    print(f"  't'  →  {result}")
    assert result == [('TRUE', 't')]

    result = tokenize_to_list("f")
    print(f"  'f'  →  {result}")
    assert result == [('FALSE', 'f')]

    print("\n=== Operators (Unicode) ===")
    result = tokenize_to_list("t ∧ f")
    print(f"  't ∧ f'  →  {result}")
    assert result == [('TRUE','t'), ('AND','∧'), ('FALSE','f')]

    result = tokenize_to_list("t ∨ f")
    print(f"  't ∨ f'  →  {result}")
    assert result == [('TRUE','t'), ('OR','∨'), ('FALSE','f')]

    print("\n=== Operators (ASCII fallbacks) ===")
    result = tokenize_to_list("t ^ f")
    print(f"  't ^ f'  →  {result}")
    assert result[1][0] == 'AND'

    result = tokenize_to_list("t | f")
    print(f"  't | f'  →  {result}")
    assert result[1][0] == 'OR'

    print("\n=== Spec example:  t ∨ f ∧ f ===")
    result = tokenize_to_list("t ∨ f ∧ f")
    print(f"  {result}")
    assert [t for t,_ in result] == ['TRUE','OR','FALSE','AND','FALSE']

    print("\n=== Whitespace is ignored ===")
    r1 = tokenize_to_list("t∨f∧f")          # no spaces
    r2 = tokenize_to_list("t ∨ f ∧ f")      # with spaces
    r3 = tokenize_to_list("t  ∨  f  ∧  f")  # extra spaces
    assert [t for t,_ in r1] == [t for t,_ in r2] == [t for t,_ in r3]
    print("  Whitespace handling OK")

    print("\n=== Parentheses ===")
    result = tokenize_to_list("(t ∨ f) ∧ t")
    print(f"  '(t ∨ f) ∧ t'  →  {result}")
    assert [t for t,_ in result] == ['LPAREN','TRUE','OR','FALSE','RPAREN','AND','TRUE']

    print("\n=== Error handling ===")
    try:
        tokenize_to_list("t ∧ x")   # 'x' is not a valid token
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"  Caught expected error: {e}")

    print("\nAll lexer tests passed!")