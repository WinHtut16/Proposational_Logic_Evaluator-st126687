# Propositional Logic Evaluator

A compiler mini-project built for the **Programming Language and Compiler** course @ AIT (March 2026).

The evaluator accepts propositional logic expressions using the operators `∧` (AND) and `∨` (OR), and produces two outputs:
- The **truth value** of the expression (`t` or `f`)
- An equivalent expression in **prefix notation**

---

## Features

- Recursive-descent parser with correct operator priority (`∧` binds tighter than `∨`)
- AST-based evaluation and prefix translation
- PySide6 GUI with clickable symbol buttons (`t`, `f`, `∧`, `∨`, `(`, `)`)
- Live keyboard conversion: type `^` or `&` for `∧`, and `|` for `∨`
- Smart auto-spacing when inserting symbols via buttons
- Clear error messages for invalid expressions

---

## Project structure

```

PLC_PROJECT/
├── code/
│   └── src/project/
│       ├── components/
│       │   ├── ast/
│       │   │   └── statement.py        ← AST node classes (BoolLit, AndNode, OrNode)
│       │   ├── lexica.py               ← lexer  (sly.Lexer)
│       │   ├── main.ui                 ← PySide6 designer layout file
│       │   └── parsers.py              ← recursive-descent parser
│       └── main.py                     ← application entry point + GUI logic
├── .gitignore
├── pyproject.toml
├── README.md
├── uv.lock
└── report.docx

---

## Grammar

```
expr  →  term  ( ∨  term  )*
term  →  atom  ( ∧  atom  )*
atom  →  t  |  f  |  ( expr )
```

`∧` has higher priority than `∨` because it appears at the deeper `term` level of the grammar.

---

## Dependencies

- Python 3.9+
- [`uv`](https://docs.astral.sh/uv/) for environment management
- `sly` — lexer/parser library
- `PySide6` — GUI framework

---

## Getting started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd PLC_project/code
```

### 2. Install dependencies

```bash
uv sync
```

If `pyside6-designer` does not launch inside the `uv` context, install PySide6 directly:

```bash
pip install pyside6 sly
```

### 3. Run the application

```bash
cd src/project
python main.py
```

---

## Running the self-tests

Each component has a built-in self-test. Run them from `src/project/`:

```bash
# Test AST nodes
python components/ast/statement.py

# Test lexer
python components/lexica.py

# Test parser (lexer + parser + AST together)
python components/parsers.py
```

---

## Usage

### With the GUI

1. Type an expression in the input field, **or** click the symbol buttons to build one.
2. Press **Evaluate** or hit **Enter**.
3. The truth value and prefix notation are displayed below.

**Keyboard shortcuts for operators:**

| Key(s) | Inserts |
|--------|---------|
| `^` or `&` | `∧` (AND) |
| `\|` | `∨` (OR) |
| `Enter` | Evaluate |

### Example expressions

| Expression | Truth value | Prefix notation |
|------------|-------------|-----------------|
| `t` | `t` | `t` |
| `t ∧ f` | `f` | `∧ t f` |
| `t ∨ f ∧ f` | `t` | `∨ t ∧ f f` |
| `(t ∨ f) ∧ f` | `f` | `∧ ∨ t f f` |
| `f ∨ f ∨ t` | `t` | `∨ ∨ f f t` |

---

## Author
Win Htut Naing (st126687)

## License

This project is for educational purposes.