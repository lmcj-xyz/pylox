import sys

from scanner import Scanner


class Lox():
    def __init__(self):
        self.had_error: bool = False

    def run_file(self, path: str):
        with open(path, "r") as file:
            data = "".join(file.readlines())
        self.run(data)
        if self.had_error:
            sys.exit(65)

    def run_prompt(self):
        while True:
            line = input("> ")
            if line == "":
                break
            self.run(line)
            self.had_error = False

    def run(self, data: str):
        scanner = Scanner(data)
        tokens: list = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print("[line: " + line + "] Error " + where + ": " + message)
        self.had_error = True


if __name__ == "__main__":
    lox = Lox()
    if len(sys.argv[1:]) > 1:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif len(sys.argv[1:]) == 1:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()
