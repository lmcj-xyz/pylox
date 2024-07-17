from token import Token
from token_type import TokenType
from error_handler import ErrorHandler


class Scanner:
    def __init__(self, source: str):
        self.error_handler = ErrorHandler
        self.source: str = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 1
        self.keywords = {
                "and": TokenType.AND,
                "class": TokenType.CLASS,
                "else": TokenType.ELSE,
                "false": TokenType.FALSE,
                "for": TokenType.FOR,
                "fun": TokenType.FUN,
                "if": TokenType.IF,
                "nil": TokenType.NIL,
                "or": TokenType.OR,
                "print": TokenType.PRINT,
                "return": TokenType.RETURN,
                "super": TokenType.SUPER,
                "this": TokenType.THIS,
                "true": TokenType.TRUE,
                "var": TokenType.VAR,
                "while": TokenType.WHILE,
                }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token("EOF", "", None, self.line))

    def scan_token(self):
        c: str = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
                return
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
                return
            case "<":
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
                return
            case ">":
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
                return
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                return
            case "\n":
                self.line += 1
                return
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    self.error_handler.error(self.line,
                                             "Unexpected character.")

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        text: str = self.source[self.start:self.current]
        if text in self.keywords:
            tokentype = self.keywords[text]
        else:
            tokentype = TokenType.IDENTIFIER
        self.add_token(tokentype)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER,
                       float(self.source[self.start:self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
                self.advance()
        if self.is_at_end():
            self.error_handler.error(self.line, "Unterminated string.")
            return

        self.advance()

        value: str = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, tokentype: TokenType, literal: object = None):
        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(tokentype, text, literal, self.line))
