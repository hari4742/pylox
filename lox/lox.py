from lox.scanner import Scanner
from lox.parser import Parser
from lox.expr import Expr
from lox.ast_printer import AstPrinter


class Lox:
    hasError: bool = False

    def __init__(self):
        pass

    def get_file_contents(self, filename):
        with open(filename) as file:
            return file.read()

    def run_cmd(self, command, filename):
        if command == 'tokenize':
            code = self.get_file_contents(filename)
            scanner = Scanner(code)
            tokens = scanner.scan_tokens()
            if self.hasError:
                exit(65)
            tokens = tokens
            for token in tokens:
                print(token)

        elif command == 'parse':
            code = self.get_file_contents(filename)
            scanner = Scanner(code)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expr: Expr = parser.parse()
            if self.hasError:
                exit(65)
            printer = AstPrinter()
            print(printer.print(expr))
        else:
            import sys
            print(f"Unknown command: {command}", file=sys.stderr)
            exit(1)

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
        parser = Parser(tokens)
        expr: Expr = parser.parse()

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
