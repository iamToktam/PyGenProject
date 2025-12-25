class GetError:
    ERROR_CODES = {
        "E001": "Syntax Error: Command '{cmd}' is unknown.",
        "E002": "Arithmetic Error: Cannot perform {cmd} on non-numeric value '{val}'.",
        "E003": "Arithmetic Error: Variable '{var}' is not defined or not numeric.",
        "E004": "Math Error: Division by zero is not allowed.",
        "E005": "Input Error: Input was cancelled for variable '{var}'.",
        "E006": "Syntax Error: Missing arguments for command '{cmd}'.",
        "E007": "Syntax Error: Invalid CLC syntax. Expected: CLC target left OP right.",
        "E008": "Arithmetic Error: Undefined variable '{var}' in CLC.",
        "E009": "Arithmetic Error: Non-numeric value in CLC.",
        "E010": "Syntax Error: Unknown operator '{op}' in CLC.",
        "E011": "Syntax Error: Invalid expression in condition.",
        "E012": "Syntax Error: Invalid comparison operator '{op}' in condition.",
        "E013": "Syntax Error: Invalid condition syntax.",
        "E014": "Syntax Error: Invalid IF syntax. Expected: IF <condition> THEN",
        "E015": "Syntax Error: Missing ENDIF for IF statement.",
        "E016": "Syntax Error: Invalid WHILE syntax. Expected: WHILE <condition> DO",
        "E017": "Syntax Error: Missing ENDWHILE for WHILE statement.",
        "E018": "Syntax Error: Invalid FOR syntax. Expected: FOR <var> FROM <start> TO <end> [STEP <step>] DO",
        "E019": "Arithmetic Error: Non-numeric values in FOR loop parameters.",
        "E020": "Syntax Error: Missing ENDFOR for FOR statement."
    }

    RED = "\033[91m"
    RESET = "\033[0m"

    def get_error(self, code, **kwargs):
        message = self.ERROR_CODES.get(code, "Unknown Error: Code '{code}' not defined.")
        print(f"{self.RED}{message.format(**kwargs)}{self.RESET}")
