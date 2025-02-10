import sys
from lox.ast_printer import AstPrinter
from lox.lox import Lox


def main():
    lox = Lox()
    if len(sys.argv) > 1:
        # File execution mode
        filename = sys.argv[1]
        lox.run_file(filename)
    else:
        # Interactive mode (REPL)
        lox.run_prompt()


if __name__ == "__main__":
    main()
