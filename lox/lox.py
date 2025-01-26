from lox.scanner import Scanner
from lox.parser import Parser
from lox.expr import Expr
from lox.ast_printer import AstPrinter


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
        self.tokens = scanner.scan_tokens()
        parser = Parser(self.tokens)
        self.expr: Expr = parser.parse()

        if self.hasError:
            return

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        import sys
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        cls.hasError = True
