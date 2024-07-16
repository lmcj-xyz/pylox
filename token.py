from token_type import TokenType


class Token:
    def __init__(self,
                 tokentype: TokenType,
                 lexeme: str,
                 literal: object,
                 line: int):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self):
        return self.type + " " + self.lexeme + " " + self.literal
