from PyGenProject.utils.error_codes import GetError
from tokenizer import Tokenizer


class Commands:
    def __init__(self):
        self.variables = {}
        self.error_handler = GetError()
        self.tokenizer = Tokenizer()

    def detect_type(self, value):
        try:
            return int(value)
        except ValueError:
            pass
        try:
            return float(value)
        except ValueError:
            pass
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        return value

    def execute_set(self, parts):
        if len(parts) < 3:
            self.error_handler.get_error("E006", cmd="SET")
            return
        value = parts[2]
        if value in self.variables:
            value = self.variables[value]
        else:
            value = self.detect_type(value)
        self.variables[parts[1]] = value

    def execute_input(self, parts):
        try:
            inp = input(f"{parts[1]} = ")
        except KeyboardInterrupt:
            self.error_handler.get_error("E005", var=parts[1])
            return
        inp = self.detect_type(inp)
        self.variables[parts[1]] = inp

    def execute_arithmetic(self, cmd, parts):
        if len(parts) < 3:
            self.error_handler.get_error("E006", cmd=cmd)
            return
        var, value = parts[1], parts[2]
        if var not in self.variables or not isinstance(self.variables[var], (int, float)):
            self.error_handler.get_error("E003", var=var)
            return
        if value in self.variables:
            value = self.variables[value]
        else:
            value = self.detect_type(value)
        if not isinstance(value, (int, float)):
            self.error_handler.get_error("E002", cmd=cmd, val=value)
            return
        if cmd == "ADD":
            self.variables[var] += value
        elif cmd == "SUB":
            self.variables[var] -= value
        elif cmd == "MUL":
            self.variables[var] *= value
        elif cmd == "DIV":
            if value == 0:
                self.error_handler.get_error("E004")
                return
            self.variables[var] /= value
        elif cmd == "MOD":
            self.variables[var] %= value

    def execute_clc(self, parts):
        if len(parts) != 5:
            self.error_handler.get_error("E007")
            return
        target, left, op, right = parts[1:]
        if left not in self.variables:
            self.error_handler.get_error("E008", var=left)
            return
        if right not in self.variables:
            self.error_handler.get_error("E008", var=right)
            return
        a, b = self.variables[left], self.variables[right]
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            self.error_handler.get_error("E009")
            return
        if op == "ADD":
            self.variables[target] = a + b
        elif op == "SUB":
            self.variables[target] = a - b
        elif op == "MUL":
            self.variables[target] = a * b
        elif op == "DIV":
            if b == 0:
                self.error_handler.get_error("E004")
                return
            self.variables[target] = a / b
        elif op == "MOD":
            self.variables[target] = a % b
        else:
            self.error_handler.get_error("E010", op=op)

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

    def execute_logical(self, cmd, parts):
        if cmd == "NOT":
            if len(parts) != 2:
                self.error_handler.get_error("E006", cmd=cmd)
                return
            var = parts[1]
            if var not in self.variables or not isinstance(self.variables[var], bool):
                self.error_handler.get_error("E003", var=var)
                return
            self.variables[var] = not self.variables[var]
        else:
            if len(parts) < 3:
                self.error_handler.get_error("E006", cmd=cmd)
                return
            var = parts[1]
            value = parts[2]
            if var not in self.variables or not isinstance(self.variables[var], bool):
                self.error_handler.get_error("E003", var=var)
                return
            if value in self.variables:
                value = self.variables[value]
            elif value.lower() in ["true", "false"]:
                value = value.lower() == "true"
            else:
                self.error_handler.get_error("E002", cmd=cmd, val=value)
                return
            if cmd == "AND":
                self.variables[var] = self.variables[var] and value
            elif cmd == "OR":
                self.variables[var] = self.variables[var] or value
            elif cmd == "XOR":
                self.variables[var] = (self.variables[var] and not value) or (not self.variables[var] and value)
            else:
                self.error_handler.get_error("E001", cmd=cmd, val=value)

    def evaluate_expression(self, expr_parts):
        if not expr_parts:
            self.error_handler.get_error("E011")
            return False

        not_flag = False
        if expr_parts[0].upper() == "NOT":
            not_flag = True
            expr_parts = expr_parts[1:]

        if len(expr_parts) != 3:
            self.error_handler.get_error("E011")
            return False

        left = expr_parts[0]
        op = expr_parts[1]
        right = expr_parts[2]

        a = self.variables.get(left) if left in self.variables else self.detect_type(left)
        b = self.variables.get(right) if right in self.variables else self.detect_type(right)

        if not (isinstance(a, (int, float, bool, str)) and isinstance(b, type(a))):
            self.error_handler.get_error("E009")
            return False

        if op == "==":
            result = a == b
        elif op == "!=":
            result = a != b
        elif op == "<":
            result = a < b
        elif op == ">":
            result = a > b
        elif op == "<=":
            result = a <= b
        elif op == ">=":
            result = a >= b
        else:
            self.error_handler.get_error("E012", op=op)
            return False

        return not result if not_flag else result

    def evaluate_condition(self, condition_str):
        parts = self.tokenizer.tokenize(condition_str)

        if not parts:
            self.error_handler.get_error("E013")
            return False

        expressions = []
        operators = []
        current_expr = []
        for token in parts:
            upper_token = token.upper()
            if upper_token in ["AND", "OR"]:
                if current_expr:
                    expressions.append(current_expr)
                operators.append(upper_token)
                current_expr = []
            else:
                current_expr.append(token)
        if current_expr:
            expressions.append(current_expr)

        if not expressions:
            self.error_handler.get_error("E013")
            return False

        result = self.evaluate_expression(expressions[0])

        for idx, op in enumerate(operators):
            next_result = self.evaluate_expression(expressions[idx + 1])
            if op == "AND":
                result = result and next_result
            elif op == "OR":
                result = result or next_result

        return result
