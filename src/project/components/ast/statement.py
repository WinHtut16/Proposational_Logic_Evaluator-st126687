"""
ast/statement.py
----------------
AST node classes for the Propositional Logic Evaluator.

Three node types:
  - BoolLit  : a literal truth value  (t / f)
  - AndNode  : binary AND expression  (B ∧ B')
  - OrNode   : binary OR  expression  (B ∨ B')

Each node supports two operations:
  - evaluate()   → bool   : computes the truth value of the expression
  - to_prefix()  → str    : converts the expression to prefix notation
  
future work - ¬ (alt+0172)
→
↔
"""


class BoolLit:
    """
    A leaf node representing a boolean literal.

    Examples
    --------
    >>> BoolLit(True).evaluate()
    True
    >>> BoolLit(False).to_prefix()
    'f'
    """

    def __init__(self, val: bool):
        self.val = val

    def evaluate(self) -> bool:
        """Return the literal's truth value."""
        return self.val

    def to_prefix(self) -> str:
        """Return 't' for True, 'f' for False."""
        return 't' if self.val else 'f'

    def __repr__(self) -> str:
        return f"BoolLit({'t' if self.val else 'f'})"


class AndNode:
    """
    An internal node representing a conjunction (B ∧ B').

    The ∧ operator has HIGHER priority than ∨, which is reflected
    in the grammar (term level), not here.

    Examples
    --------
    >>> AndNode(BoolLit(True), BoolLit(False)).evaluate()
    False
    >>> AndNode(BoolLit(True), BoolLit(True)).to_prefix()
    '∧ t t'
    """

    def __init__(self, left, right):
        """
        Parameters
        ----------
        left  : BoolLit | AndNode | OrNode
        right : BoolLit | AndNode | OrNode
        """
        self.left  = left
        self.right = right

    def evaluate(self) -> bool:
        """Return True only when both operands are True."""
        return self.left.evaluate() and self.right.evaluate()

    def to_prefix(self) -> str:
        """Return prefix string:  ∧ <left> <right>"""
        return f'∧ {self.left.to_prefix()} {self.right.to_prefix()}'

    def __repr__(self) -> str:
        return f"AndNode({self.left!r}, {self.right!r})"


class OrNode:
    """
    An internal node representing a disjunction (B ∨ B').

    The ∨ operator has LOWER priority than ∧, which is reflected
    in the grammar (expr level), not here.

    Examples
    --------
    >>> OrNode(BoolLit(True), BoolLit(False)).evaluate()
    True
    >>> OrNode(BoolLit(True), AndNode(BoolLit(False), BoolLit(False))).to_prefix()
    '∨ t ∧ f f'
    """

    def __init__(self, left, right):
        """
        Parameters
        ----------
        left  : BoolLit | AndNode | OrNode
        right : BoolLit | AndNode | OrNode
        """
        self.left  = left
        self.right = right

    def evaluate(self) -> bool:
        """Return True when at least one operand is True."""
        return self.left.evaluate() or self.right.evaluate()

    def to_prefix(self) -> str:
        """Return prefix string:  ∨ <left> <right>"""
        return f'∨ {self.left.to_prefix()} {self.right.to_prefix()}'

    def __repr__(self) -> str:
        return f"OrNode({self.left!r}, {self.right!r})"


# ---------------------------------------------------------------------------
# Quick self-test  (run:  python statement.py)
# ---------------------------------------------------------------------------
if __name__ == '__main__':

    print("=== BoolLit ===")
    assert BoolLit(True).evaluate()  == True
    assert BoolLit(False).evaluate() == False
    assert BoolLit(True).to_prefix()  == 't'
    assert BoolLit(False).to_prefix() == 'f'
    print("  BoolLit tests passed")

    print("\n=== AndNode ===")
    assert AndNode(BoolLit(True),  BoolLit(True) ).evaluate() == True
    assert AndNode(BoolLit(True),  BoolLit(False)).evaluate() == False
    assert AndNode(BoolLit(False), BoolLit(True) ).evaluate() == False
    assert AndNode(BoolLit(False), BoolLit(False)).evaluate() == False
    assert AndNode(BoolLit(True),  BoolLit(True) ).to_prefix() == '∧ t t'
    assert AndNode(BoolLit(False), BoolLit(True) ).to_prefix() == '∧ f t'
    print("  AndNode tests passed")

    print("\n=== OrNode ===")
    assert OrNode(BoolLit(True),  BoolLit(True) ).evaluate() == True
    assert OrNode(BoolLit(True),  BoolLit(False)).evaluate() == True
    assert OrNode(BoolLit(False), BoolLit(True) ).evaluate() == True
    assert OrNode(BoolLit(False), BoolLit(False)).evaluate() == False
    assert OrNode(BoolLit(True),  BoolLit(False)).to_prefix() == '∨ t f'
    assert OrNode(BoolLit(False), BoolLit(False)).to_prefix() == '∨ f f'
    print("  OrNode tests passed")

    print("\n=== Spec example:  t ∨ f ∧ f  ===")
    # Build tree manually: OR( t,  AND(f, f) )
    # This reflects the priority rule: ∧ binds tighter than ∨
    tree = OrNode(
        BoolLit(True),
        AndNode(BoolLit(False), BoolLit(False))
    )
    result = tree.evaluate()
    prefix = tree.to_prefix()
    print(f"  evaluate()  = {result}  (expected: True)")
    print(f"  to_prefix() = {prefix}  (expected: ∨ t ∧ f f)")
    assert result == True
    assert prefix == '∨ t ∧ f f'

    print("\n=== Nested expression:  (t ∧ f) ∨ (t ∧ t) ===")
    tree2 = OrNode(
        AndNode(BoolLit(True),  BoolLit(False)),
        AndNode(BoolLit(True),  BoolLit(True))
    )
    print(f"  evaluate()  = {tree2.evaluate()}   (expected: True)")
    print(f"  to_prefix() = {tree2.to_prefix()}  (expected: ∨ ∧ t f ∧ t t)")
    assert tree2.evaluate()   == True
    assert tree2.to_prefix()  == '∨ ∧ t f ∧ t t'

    print("\nAll tests passed!")