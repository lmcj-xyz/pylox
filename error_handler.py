class ErrorHandler:
    def __init__(self):
        self.had_error = False

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print(f"[line: {line}] Error {where}: {message}")
        self.had_error = True
