import sys
from lox.ast_printer import AstPrinter
from lox.lox import Lox


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    lox = Lox()
    lox.run_file(filename)

    if command == 'tokenize':
        tokens = lox.tokens
        for token in tokens:
            print(token)

    elif command == 'parse':
        if lox.hasError:
            return

        printer = AstPrinter()
        print(printer.print(lox.expr))
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
