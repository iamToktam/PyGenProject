from PyGenProject.utils.error_codes import GetError
from tokenizer import Tokenizer
from commands import Commands


class PyGenInterpreter:
    def __init__(self):
        self.error_handler = GetError()
        self.tokenizer = Tokenizer()
        self.command = Commands()

    def run_program(self, lines):
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("//"):  # Skip empty lines or full comment lines
                i += 1
                continue
            parts = self.tokenizer.tokenize(line)
            if not parts:
                i += 1
                continue
            cmd = parts[0].upper()
            if cmd in ("SET", "INPUT", "ADD", "SUB", "MUL", "DIV", "MOD", "CLC", "PRINT", "AND", "OR", "NOT", "XOR"):
                self.execute_line(line)
                i += 1
            elif cmd == "IF":
                i = self.execute_if(lines, i)
            elif cmd == "WHILE":  # Added handling for WHILE
                i = self.execute_while(lines, i)
            elif cmd == "FOR":  # Added handling for FOR
                i = self.execute_for(lines, i)
            else:
                self.error_handler.get_error("E001", cmd=cmd)
                i += 1

    def execute_line(self, line):
        if "//" in line:
            line = line.split("//")[0].strip()
        parts = self.tokenizer.tokenize(line)
        if not parts:
            return
        cmd = parts[0].upper()
        if cmd == "SET":
            self.command.execute_set(parts)
        elif cmd == "INPUT":
            self.command.execute_input(parts)
        elif cmd in ("ADD", "SUB", "MUL", "DIV", "MOD"):
            self.command.execute_arithmetic(cmd, parts)
        elif cmd == "CLC":
            self.command.execute_clc(parts)
        elif cmd == "PRINT":
            self.command.execute_print(parts)
        elif cmd in ("AND", "OR", "NOT", "XOR"):
            self.command.execute_logical(cmd, parts)
        else:
            self.error_handler.get_error("E001", cmd=cmd)

    def execute_if(self, lines, start_index):
        current_line = lines[start_index].strip()
        parts = self.tokenizer.tokenize(current_line)
        if parts[0].upper() != "IF" or "THEN" not in [p.upper() for p in parts]:
            self.error_handler.get_error("E014")  # E014: Invalid IF syntax
            return start_index + 1
        then_index = [p.upper() for p in parts].index("THEN")
        condition_parts = parts[1:then_index]
        condition_str = " ".join(condition_parts)
        blocks = {"if": [], "elifs": [], "else": []}
        current_block = "if"
        i = start_index + 1
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("//"):
                i += 1
                continue
            upper_line = line.upper()
            if upper_line.startswith("ENDIF"):
                break
            elif upper_line.startswith("ELIF"):
                elif_parts = self.tokenizer.tokenize(line)
                then_index = [p.upper() for p in elif_parts].index("THEN")
                elif_condition = " ".join(elif_parts[1:then_index])
                blocks["elifs"].append({"condition": elif_condition, "block": []})
                current_block = f"elif_{len(blocks['elifs']) - 1}"
            elif upper_line.startswith("ELSE"):
                blocks["else"] = []
                current_block = "else"
            else:
                if current_block == "if":
                    blocks["if"].append(line)
                elif current_block.startswith("elif_"):
                    idx = int(current_block.split("_")[1])
                    blocks["elifs"][idx]["block"].append(line)
                elif current_block == "else":
                    blocks["else"].append(line)
            i += 1
        if i >= len(lines) or not lines[i].strip().upper().startswith("ENDIF"):
            self.error_handler.get_error("E015")  # E015: Missing ENDIF
            return i
        executed = False
        if self.command.evaluate_condition(condition_str):
            self.run_program(blocks["if"])
            executed = True
        if not executed:
            for elif_block in blocks["elifs"]:
                if self.command.evaluate_condition(elif_block["condition"]):
                    self.run_program(elif_block["block"])
                    executed = True
                    break
        if not executed and blocks["else"]:
            self.run_program(blocks["else"])
        return i + 1

    def execute_for(self, lines, start_index):
        current_line = lines[start_index].strip()
        parts = self.tokenizer.tokenize(current_line)
        if parts[0].upper() != "FOR" or "DO" not in [p.upper() for p in parts]:
            self.error_handler.get_error("E018")
            return start_index + 1
        var = parts[1]
        from_index = next((idx for idx, p in enumerate(parts) if p.upper() == "FROM"), -1)
        to_index = next((idx for idx, p in enumerate(parts) if p.upper() == "TO"), -1)
        step_index = next((idx for idx, p in enumerate(parts) if p.upper() == "STEP"), -1)
        do_index = next((idx for idx, p in enumerate(parts) if p.upper() == "DO"), -1)
        if from_index == -1 or to_index == -1 or do_index == -1:
            self.error_handler.get_error("E018")
            return start_index + 1
        start_val = self.command.detect_type(parts[from_index + 1])
        end_val = self.command.detect_type(parts[to_index + 1])
        step_val = self.command.detect_type(parts[step_index + 1]) if step_index != -1 else 1
        if not all(isinstance(val, (int, float)) for val in [start_val, end_val, step_val]):
            self.error_handler.get_error("E019")
            return start_index + 1
        block = []
        i = start_index + 1
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("//"):
                i += 1
                continue
            if line.upper().startswith("ENDFOR"):
                break
            block.append(line)
            i += 1
        if i >= len(lines) or not lines[i].strip().upper().startswith("ENDFOR"):
            self.error_handler.get_error("E020")
            return i
        self.command.variables[var] = start_val
        while ((step_val > 0 and self.command.variables[var] <= end_val) or
               (step_val < 0 and self.command.variables[var] >= end_val)):
            self.run_program(block)
            self.command.variables[var] += step_val
        return i + 1

    def execute_while(self, lines, start_index):
        current_line = lines[start_index].strip()
        parts = self.tokenizer.tokenize(current_line)
        if parts[0].upper() != "WHILE" or "DO" not in [p.upper() for p in parts]:
            self.error_handler.get_error("E016")
            return start_index + 1
        do_index = [p.upper() for p in parts].index("DO")
        condition_parts = parts[1:do_index]
        condition_str = " ".join(condition_parts)
        block = []
        i = start_index + 1
        while i < len(lines):
            line = lines[i].strip()
            if not line or line.startswith("//"):
                i += 1
                continue
            if line.upper().startswith("ENDWHILE"):
                break
            block.append(line)
            i += 1
        if i >= len(lines) or not lines[i].strip().upper().startswith("ENDWHILE"):
            self.error_handler.get_error("E017")
            return i
        while self.command.evaluate_condition(condition_str):
            self.run_program(block)
        return i + 1
