# PyGen

A Small Programming Language (Python Generation)

## Introduction

**PyGen** (short for *Python Generation*) is a small, custom programming language developed as a university project for the course **Design of Programming Languages**.

The project follows the classical steps of language design:
1. Defining a formal grammar
2. Designing language constructs
3. Implementing an interpreter in Python
4. Executing user-written programs based on the defined grammar

PyGen supports variable declaration, arithmetic and logical operations, conditional statements, loops, and comments.  
Its main purpose is educational: to provide a clear and practical example of how a programming language is designed and implemented from scratch.

## Goal

Our goal is to demonstrate the process of designing a small programming language, from formal grammar definition to practical implementation. (PyGen is designed for educational purposes only and acts as a tool for learning the principles of programming language design and interpreter implementation.)

## Grammar

The formal grammar of PyGen is defined as follows:
```ebnf
<program> ::= { <statement> | <comment> }

<statement> ::= <simple_statement>
              | <logical_statement>
              | <if_statement>
              | <while_statement>
              | <for_statement>

<simple_statement> ::= <set_statement>
                     | <input_statement>
                     | <arithmetic_statement>
                     | <clc_statement>
                     | <print_statement>

<set_statement> ::= "SET" <identifier> <value>
<input_statement> ::= "INPUT" <identifier>

<arithmetic_statement> ::= ("ADD" | "SUB" | "MUL" | "DIV" | "MOD")
                           <identifier> <value>

<clc_statement> ::= "CLC" <identifier> <identifier> <operator> <identifier>

<print_statement> ::= "PRINT" { <string> | <identifier> | <value> }

<logical_statement> ::= ("AND" | "OR" | "XOR") <identifier> <value>
                      | "NOT" <identifier>

<if_statement> ::= "IF" <condition> "THEN" <block>
                   { <elif_statement> }
                   [ <else_statement> ]
                   "ENDIF"

<elif_statement> ::= "ELIF" <condition> "THEN" <block>
<else_statement> ::= "ELSE" <block>

<while_statement> ::= "WHILE" <condition> "DO" <block> "ENDWHILE"

<for_statement> ::= "FOR" <identifier> "FROM" <value> "TO" <value>
                    [ "STEP" <value> ]
                    "DO" <block> "ENDFOR"

<block> ::= { <statement> | <comment> }

<condition> ::= <expression> { ("AND" | "OR") <expression> }

<expression> ::= [ "NOT" ] <simple_expression>

<simple_expression> ::= <identifier> <comparison_op> <value>
                      | <identifier>

<comparison_op> ::= "==" | "!=" | "<" | ">" | "<=" | ">="

<comment> ::= "//" { <any_character> }

<identifier> ::= <letter> { <letter> | <digit> | "_" }

<value> ::= <number> | <boolean> | <string> | <identifier>

<number> ::= <integer> | <float>
<integer> ::= <digit> { <digit> }
<float> ::= <integer> "." <integer>

<boolean> ::= "TRUE" | "FALSE"
<string> ::= '"' { <any_character> } '"'

<operator> ::= "ADD" | "SUB" | "MUL" | "DIV" | "MOD"

<letter> ::= [A-Za-z]
<digit> ::= [0-9]
<any_character> ::= [^"] | .
```

## Features

- **Variable handling**
  - Assignment using `SET`
  - User input using `INPUT`

- **Arithmetic operations**
  - `ADD`, `SUB`, `MUL`, `DIV`, `MOD`
  - Direct arithmetic and calculated assignments (`CLC`)

- **Logical operations**
  - `AND`, `OR`, `XOR`, `NOT`
  - Boolean values: `TRUE`, `FALSE`

- **Control flow**
  - Conditional statements:
    - `IF ... THEN ... ENDIF`
    - `IF ... ELIF ... ELSE ... ENDIF`
  - Loops:
    - `WHILE ... DO ... ENDWHILE`
    - `FOR ... FROM ... TO ... STEP ... ENDFOR`

- **Output**
  - Printing strings, variables, and values using `PRINT`

- **Comments**
  - Single-line comments using `//`

## Usage
To run a PyGen program:
1. Clone the repository:
```
git clone  https://github.com/iamToktam/spl_project.git
cd spl_project
```
2. Execute the interpreter:
```
python -m PyGenProject.core.commands sample.pyg
```

## Examples
Example Program in the sample.pyg
```
SET x 10
SET y 5

IF x > y THEN
    PRINT "x is greater than y"
ELSE
    PRINT "x is not greater than y"
ENDIF

ADD x 2
PRINT "x after addition:" x
```
Output
```
x is greater than y
x after addition: 12
```

## Limitations & Future Work

Although PyGen successfully demonstrates the design and implementation of a small programming language, it has some limitations:
- No functions or procedures
- No arrays or complex data structures
- No nested scopes
- Interpreter-based execution only (no compilation)

Possible future improvements include:
- Function definitions
- User-defined data structures
- Enhanced error reporting with line numbers
- Abstract Syntax Tree (AST) based execution
