class Tokenizer:
    KEYWORDS = {
        "SET", "INPUT", "PRINT",
        "ADD", "SUB", "MUL", "DIV", "MOD",
        "CLC",
        "IF", "THEN", "ELIF", "ELSE", "ENDIF",
        "WHILE", "DO", "ENDWHILE",
        "FOR", "FROM", "TO", "STEP", "ENDFOR",
        "AND", "OR", "NOT", "XOR",
        "TRUE", "FALSE"
    }

    OPERATORS = {"==", "!=", "<=", ">=", "<", ">"}

    def tokenize(self, line: str):
        if "//" in line:
            line = line.split("//", 1)[0]

        tokens = []
        current = ""
        in_string = False
        i = 0

        while i < len(line):
            char = line[i]

            if char == '"':
                if in_string:
                    current += char
                    tokens.append(current)
                    current = ""
                    in_string = False
                else:
                    if current:
                        tokens.append(current)
                        current = ""
                    current = char
                    in_string = True
                i += 1
                continue

            if in_string:
                current += char
                i += 1
                continue

            two_char = line[i:i + 2]
            if two_char in self.OPERATORS:
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(two_char)
                i += 2
                continue

            if char in "<>":
                if current:
                    tokens.append(current)
                    current = ""
                tokens.append(char)
                i += 1
                continue

            if char.isspace():
                if current:
                    tokens.append(current)
                    current = ""
                i += 1
                continue

            current += char
            i += 1

        if current:
            tokens.append(current)

        final_tokens = []
        for token in tokens:
            if token.startswith('"'):
                final_tokens.append(token)
            else:
                upper = token.upper()
                if upper in self.KEYWORDS:
                    final_tokens.append(upper)
                else:
                    final_tokens.append(token)

        return final_tokens
