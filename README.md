# Propositional Logic Evaluator

A compiler mini-project built for the **Programming Language and Compiler** course @ AIT (March 2026).

The evaluator accepts propositional logic expressions using the operators `∧` (AND) and `∨` (OR), and produces two outputs:

* The **truth value** of the expression (`t` or `f`)
* An equivalent expression in **prefix notation**

---

## Features

* Recursive-descent parser with correct operator priority (`∧` binds tighter than `∨`)
* AST-based evaluation and prefix translation
* PySide6 GUI with clickable symbol buttons (`t`, `f`, `∧`, `∨`, `(`, `)`)
* Live keyboard conversion: type `^` or `&` for `∧`, and `|` for `∨`
* Smart auto-spacing when inserting symbols via buttons
* Clear error messages for invalid expressions

---

## Project structure

```
PLC_PROJECT/
├── code/
│   └── src/project/
│       ├── components/
│       │   ├── ast/
│       │   │   ├── __init__.py
│       │   │   └── statement.py        ← AST node classes (BoolLit, AndNode, OrNode)
│       │   ├── __init__.py
│       │   ├── lexica.py               ← lexer (sly.Lexer)
│       │   ├── main.ui                 ← PySide6 UI layout
│       │   └── parsers.py              ← recursive-descent parser
│       ├── __init__.py
│       └── main.py                     ← application entry point (GUI)
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## Grammar

```
expr  →  term  ( ∨  term )*
term  →  atom  ( ∧  atom )*
atom  →  t  |  f  |  ( expr )
```

`∧` has higher priority than `∨` because it appears at the deeper `term` level of the grammar.

---

## Dependencies

* Python 3.9+
* `sly` — lexer/parser library
* `PySide6` — GUI framework
* [`uv`](https://docs.astral.sh/uv/) (optional, for environment management)

---

## Getting started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd PLC_PROJECT/code
```

---

### 2. Install dependencies

#### Option A (recommended - using uv)

```bash
uv sync
```

#### Option B (standard pip)

```bash
pip install pyside6 sly
```

---

### 3. Run the application

```bash
cd src/project
python main.py
```

---

## Running the self-tests

Run these from `src/project/`:

```bash
# Test AST
python components/ast/statement.py

# Test lexer
python components/lexica.py

# Test parser (full pipeline)
python components/parsers.py
```

---

## Usage

### GUI

1. Enter an expression manually **or** use the symbol buttons.
2. Press **Evaluate** or hit **Enter**.
3. View:

   * Truth value (`t` or `f`)
   * Prefix notation

---

### Input rules

* Use lowercase `t` and `f`
* AND: `∧`, `^`, or `&`
* OR: `∨` or `|`
* Parentheses: `( )`

---

### Example expressions

| Expression    | Truth value | Prefix notation |
| ------------- | ----------- | --------------- |
| `t`           | `t`         | `t`             |
| `t ∧ f`       | `f`         | `∧ t f`         |
| `t ∨ f ∧ f`   | `t`         | `∨ t ∧ f f`     |
| `(t ∨ f) ∧ f` | `f`         | `∧ ∨ t f f`     |
| `f ∨ f ∨ t`   | `t`         | `∨ ∨ f f t`     |

---

## Author

Win Htut Naing (st126687)

---

## License

This project is for educational purposes.
