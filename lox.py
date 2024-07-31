import sys
from scanner import Scanner
from error_handler import ErrorHandler
from parser import Parser
from expr import Expr
from ast_printer import ASTPrinter


class Lox():
    def __init__(self):
        self.error_handler = ErrorHandler()

    def run_file(self, path: str):
        with open(path, "r") as file:
            data = "".join(file.readlines())
        self.run(data)
        if self.error_handler.had_error:
            sys.exit(65)

    def run_prompt(self):
        while True:
            line = input("pylox> ")
            if line == "":
                break
            self.run(line)
            self.error_handler.had_error = False

    def run(self, data: str):
        scanner = Scanner(data)
        tokens: list = scanner.scan_tokens()

        #for token in tokens:
        #    print(token)

        parser: Parser = Parser(tokens)
        expression: Expr = parser.parse()

        if self.error_handler.had_error:
            return

        printer = ASTPrinter()
        print(printer.print(expression))


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv[1:]) > 1:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif len(sys.argv[1:]) == 1:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
