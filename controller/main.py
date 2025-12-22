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
    "E010": "Syntax Error: Unknown operator '{op}' in CLC."
}

RED = "\033[91m"
RESET = "\033[0m"


def tokenize(line):
    tokens = []
    current = ""
    in_string = False

    for char in line:
        if char == '"':
            if in_string:
                current += char
                tokens.append(current)
                current = ""
                in_string = False
            else:
                if current.strip():
                    tokens.extend(current.strip().split())
                current = char
                in_string = True
        elif char.isspace() and not in_string:
            if current:
                tokens.append(current)
                current = ""
        else:
            current += char

    if current:
        tokens.append(current)

    return tokens


class EduLangInterpreter:
    def __init__(self):
        self.variables = {}

    # ---------- Error Handler ----------
    def error(self, code, **kwargs):
        message = ERROR_CODES.get(code, "Unknown Error")
        print(f"{RED}{message.format(**kwargs)}{RESET}")

    # ---------- Line Executor ----------
    def execute_line(self, line):
        parts = tokenize(line)
        if not parts:
            return

        cmd = parts[0]

        if cmd == "SET":
            if len(parts) < 3:
                self.error("E006", cmd=cmd)
                return

            value = parts[2]
            if value in self.variables:
                value = self.variables[value]
            else:
                try:
                    value = float(value)
                except ValueError:
                    value = value.strip('"')

            self.variables[parts[1]] = value

        elif cmd == "INPUT":
            try:
                inp = input(f"{parts[1]} = ")
            except KeyboardInterrupt:
                self.error("E005", var=parts[1])
                return

            try:
                inp = float(inp)
            except ValueError:
                pass

            self.variables[parts[1]] = inp

        elif cmd in ("ADD", "SUB", "MUL", "DIV", "MOD"):
            self.execute_arithmetic(cmd, parts)

        elif cmd == "CLC":
            self.execute_clc(parts)

        elif cmd == "PRINT":
            self.execute_print(parts)

        else:
            self.error("E001", cmd=cmd)

    # ---------- Arithmetic (Destructive) ----------
    def execute_arithmetic(self, cmd, parts):
        if len(parts) < 3:
            self.error("E006", cmd=cmd)
            return

        var, value = parts[1], parts[2]

        if var not in self.variables or not isinstance(self.variables[var], (int, float)):
            self.error("E003", var=var)
            return

        if value in self.variables:
            value = self.variables[value]
        else:
            try:
                value = float(value)
            except ValueError:
                self.error("E002", cmd=cmd, val=value)
                return

        if cmd == "ADD":
            self.variables[var] += value
        elif cmd == "SUB":
            self.variables[var] -= value
        elif cmd == "MUL":
            self.variables[var] *= value
        elif cmd == "DIV":
            if value == 0:
                self.error("E004")
                return
            self.variables[var] //= value
        elif cmd == "MOD":
            self.variables[var] %= value

    # ---------- CLC (Non-destructive) ----------
    def execute_clc(self, parts):
        if len(parts) != 5:
            self.error("E007")
            return

        target, left, op, right = parts[1:]

        if left not in self.variables:
            self.error("E008", var=left)
            return

        if right not in self.variables:
            self.error("E008", var=right)
            return

        a, b = self.variables[left], self.variables[right]

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            self.error("E009")
            return

        if op == "ADD":
            self.variables[target] = a + b
        elif op == "SUB":
            self.variables[target] = a - b
        elif op == "MUL":
            self.variables[target] = a * b
        elif op == "DIV":
            if b == 0:
                self.error("E004")
                return
            self.variables[target] = a / b
        elif op == "MOD":
            self.variables[target] = a % b
        else:
            self.error("E010", op=op)

    # ---------- PRINT ----------
    def execute_print(self, parts):
        output = []
        for token in parts[1:]:
            if token.startswith('"') and token.endswith('"'):
                output.append(token[1:-1])
            elif token in self.variables:
                output.append(str(self.variables[token]))
            else:
                output.append(token)

        print(" ".join(output))


def run_program(filename):
    interpreter = EduLangInterpreter()
    with open(filename) as file:
        for line in file:
            interpreter.execute_line(line)


if __name__ == "__main__":
    run_program("user_program.edl")
