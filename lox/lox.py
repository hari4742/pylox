from lox.scanner import Scanner
from lox.parser import Parser
from lox.expr import Expr
from lox.ast_printer import AstPrinter
from lox.error import LoxRuntimeError
from lox.interpreter import Interpreter
from lox.stmt import Stmt


class Lox:
    hasError: bool = False
    has_runtime_error: bool = False
    interpreter = Interpreter()

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
            for token in tokens:
                print(token)
            if self.hasError:
                exit(65)

        elif command == 'parse':
            code = self.get_file_contents(filename)
            scanner = Scanner(code)
            tokens = scanner.scan_tokens()
            if self.hasError:
                exit(65)
            parser = Parser(tokens)
            expr: Expr = parser.expression()
            if self.hasError:
                exit(65)
            printer = AstPrinter()
            print(printer.print(expr))

        elif command == 'evaluate':
            code = self.get_file_contents(filename)
            scanner = Scanner(code)
            tokens = scanner.scan_tokens()
            parser = Parser(tokens)
            expr: Expr = parser.expression()
            try:
                value = self.interpreter.expression(expr)
                print(self.interpreter.stringify(value))
            except LoxRuntimeError as error:
                from lox.lox import Lox
                Lox.runtime_error(error)
            if self.hasError:
                exit(65)
            if self.has_runtime_error:
                exit(70)
        elif command == 'run':
            self.run_file(filename)
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
            if self.has_runtime_error:
                exit(70)

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
        statements: Stmt = parser.parse()
        self.interpreter.interpret(statements)

    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def runtime_error(cls, error: LoxRuntimeError):
        import sys
        print(error.message + f"\n[line {error.token.line}]", file=sys.stderr)
        cls.has_runtime_error = True

    @classmethod
    def report(cls, line: int, where: str, message: str):
        import sys
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        cls.hasError = True
