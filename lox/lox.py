from lox.scanner import Scanner


class Lox:
    hasError: bool = False

    def __init__(self):
        pass

    def run_file(self, filename):
        with open(filename) as file:
            file_contents = file.read()
            self.run(file_contents)
            if self.hasError:
                exit(65)

    def run_prompt(self):
        while True:
            print("> ", end="")
            line = input()
            if not line:
                break
            self.run(line)
            self.hasError = False

    def run(self, code: str):
        scanner = Scanner(code)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}")
        cls.hasError = True
