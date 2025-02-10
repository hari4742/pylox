# Pylox 🦊

A Python-based frontend for a Lox interpreter, implementing lexical analysis, parsing, abstract syntax tree (AST) generation, and expression evaluation.

## 📖 Overview

Pylox is a frontend implementation of a Lox interpreter, inspired by _Crafting Interpreters_ by Robert Nystrom. It processes Lox source code by tokenizing it, constructing an abstract syntax tree, evaluating expressions, and executing statements.

## 🚀 Features

- **Lexical Analysis**: Tokenizes source code into meaningful lexical components.
- **Parsing**: Constructs an abstract syntax tree (AST) from tokenized input.
- **AST Printer**: Provides a visual representation of the parsed AST.
- **Expression Evaluation**: Computes the results of parsed expressions.
- **Error Handling**: Implements structured error reporting for syntax and runtime exceptions.
- **Scoped Environment**: Supports variable scoping and function execution.

## 📝 Usage

### Run a Lox script

```sh
python pylox.py examples/script.lox
```

Run Pylox with different commands:

### Tokenize

```sh
python pylox-cli.py tokenize examples/script.lox
```

Outputs the tokenized representation of the source code.

### Parse

```sh
python pylox-cli.py parse examples/script.lox
```

Parses the tokens into an abstract syntax tree (AST) and prints its structure.

### Evaluate

```sh
python pylox-cli.py evaluate examples/script.lox
```

Evaluates expressions in the source code and outputs computed results.

Executes the script by interpreting its statements.

## 📜 Grammar

Pylox uses a recursive descent parser based on the following context-free grammar:

```
program       -> declaration* EOF ;
declaration   -> funDecl | varDecl | statement ;
funDecl       -> "fun" function ;
function      -> IDENTIFIER "(" parameters? ")" block ;
parameters    -> IDENTIFIER ( "," IDENTIFIER )* ;
statement     -> exprStmt | forStmt | ifStmt | printStmt | returnStmt | whileStmt | block;
returnStmt    -> "return" expression? ";" ;
forStmt       -> "for" "(" (varDecl | exprStmt | ";" ) expression? ";" expression? ")" statement ;
whileStmt     -> "while" "(" expression ")" statement ;
ifStmt        -> "if" "(" expression ")" statement ( "else" statement )? ;
block         -> "{" declaration* "}" ;
varDecl       -> "var" IDENTIFIER ( "=" expression )? ";" ;
exprStmt      -> expression ";" ;
printStmt     -> "print" expression ";" ;
expression    -> assignment ;
assignment    -> IDENTIFIER "=" assignment | logic_or ;
logic_or      -> logic_and ( "or" logic_and )* ;
logic_and     -> equality ( "and" equality )* ;
equality      -> comparison ( ("!=" | "==") comparison )* ;
comparison    -> term ( ( ">" | ">=" | "<" | "<=" ) term )*;
term          -> factor ( ( "-" | "+" ) factor )* ;
factor        -> unary ( ( "/" | "*" ) unary )* ;
unary         -> ( "!" | "-" ) unary | call ;
call          -> primary ( "(" arguments? ")" )* ;
arguments     -> expression ( "," expression )* ;
primary       -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
```

## 🛠 Project Structure

```
pylox/
├── lox/
│   ├── ast_printer.py  # Prints AST structures
│   ├── environment.py  # Manages variable scopes
│   ├── error.py        # Handles error reporting
│   ├── expr.py         # Defines AST expression nodes
│   ├── interpreter.py  # Core interpreter logic
│   ├── lox_callable.py # Interface for callable functions
│   ├── lox_function.py # Implements Lox functions
│   ├── lox.py          # Main Lox class
│   ├── parser.py       # Implements parsing logic
│   ├── return_error.py # Return statement exception handling
│   ├── scanner.py      # Tokenizes source code
│   ├── stmt.py         # Defines AST statement nodes
│   ├── token.py        # Token class and type declarations
├── examples/
│   ├── script.lox  # Sample Lox scripts
├── app/
│   ├── main.py
├── tool/
│   ├── generate_ast.py # Helper script for AST node generation
├── pylox.py        # Entrypoint for the interpreter
├── pylox-cli.py    # Entry point for command execution
├── README.md
├── requirements.txt
├── LICENSE
```

## 🙌 Acknowledgments

- Inspired by [_Crafting Interpreters_](https://craftinginterpreters.com/) by Robert Nystrom.
- Special thanks to code crafters more about them [here](./code-crafters.md).
