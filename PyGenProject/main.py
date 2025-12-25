from core.interpreter import PyGenInterpreter


class Main:
    def __init__(self, filename):
        self.filename = filename
        self.interpreter = PyGenInterpreter()

    def load_program(self):
        try:
            with open(self.filename, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            print(f"{self.filename} Not Found")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def run_program(self):
        lines = self.load_program()
        if lines:
            self.interpreter.run_program(lines)


if __name__ == "__main__":
    runner = Main("user_program.pyg")
    runner.run_program()
