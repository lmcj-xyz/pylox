from token import Token
from token_type import TokenType


class ErrorHandler:
    def __init__(self):
        self.had_error = False

    def error(self, culprit: int | Token, message: str):
        if isinstance(culprit, Token):
            if culprit.type == TokenType.EOF:
                self.report(culprit.line, " at end", message)
            else:
                self.report(culprit.line, " at '" + culprit.lexeme + "'", message)
        else:
            self.report(culprit, "", message)

    def report(self, line: int | Token, where: str, message: str):
        print(f"[line: {line}] Error {where}: {message}")
        self.had_error = True
