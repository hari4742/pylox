import sys
from lox.lox import Lox


def cli():
    if len(sys.argv) < 3:
        print("Usage: ./program <command> <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    lox = Lox()
    lox.run_cmd(command, filename)


if __name__ == "__main__":
    cli()
