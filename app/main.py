import sys
from lox.scanner import Scanner
from lox.lox import Lox


def get_file_contents(filename):
    with open(filename) as file:
        return file.read()


def get_tokens(code):
    scanner = Scanner(code)
    return scanner.scan_tokens()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh <command> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    code = get_file_contents(filename)

    if command == 'tokenize':
        tokens = get_tokens(code)
        for token in tokens:
            print(token)

    elif command == 'parse':
        lox = Lox()
        lox.run_file(filename)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
