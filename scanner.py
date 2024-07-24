from token import Token
from token_type import TokenType
from error_handler import ErrorHandler


class Scanner:
    """
    Scanner of tokens for the interpreter.`

    This is the object which will scan the tokens provided in the
    interpreter, either by using an interactive session or while
    running a script.

    Attributes:
        error_handler: ErrorHandler
            Handles errors.

        source: str
            The source code.

        tokens: list[Token]
            The tokenized version of the source code.

        start: int
            The starting index for the scanning process.

        current: int
            The current index in the scanning process.

        line: int
            The current line of the file one is in the scanning
            process.

        keywords: dict
            Reserved words of the 'lox' language.
    """

    def __init__(self, source: str):
<<<<<<< HEAD
        """
        Args:
            source: str
                The source code, given by the user in the session or
                or in a file.
        """
=======
>>>>>>> b0d8bdc (Instantiate ErrorHandler)
        self.error_handler = ErrorHandler()
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
        return self.tokens

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
                return
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                if self.match("*"):
                    self.block_comment()
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
                return
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    self.error_handler.error(self.line,
                                             "Unexpected character.")

    def block_comment(self):
        # this is not yet working
        while not self.is_at_end() \
                and not (self.peek != "*" and self.peek_next != "/"):
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.error_handler.error(self.line, "Unterminated block comment.")
            return
        self.advance()

    def identifier(self):
        """
        Parses an identifier.

        Alphanumeric identifiers are valid.

        Checks for the text to be in the list of keywords, if not
        then it's an identifier.
        """
        while self.peek().isalnum() and not self.is_at_end():
            self.advance()

        text: str = self.source[self.start:self.current]
        if text in self.keywords:
            tokentype = self.keywords[text]
        else:
            tokentype = TokenType.IDENTIFIER
        self.add_token(tokentype)

    def number(self):
        """
        Processes a multi digit number.

        All numbers are of type double and have to start and end with
        a number.

        .1 and 1. are not valid numbers in lox.

        '.' is handled as a character on its own and the implementation
        of leading dot numbers would be as a conditional within the
        parsing of '.'.
        """
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER,
                       float(self.source[self.start:self.current]))

    def string(self):
        """
        Processes a string.

        A string without both '"' is an error.

        We can handle multi line strings.
        """
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
        """
        Checks for the next symbol to match the expected value.

        One token next to another may have a specific meaning while the
        fist token on its own has another.
        This compares the following token with an expected value so
        that the scanner can handle the special cases of combinations.

        Args:
            expected: str
                The expected value of the next token to be handled
                as a special case.

        Returns:
            bool: True if the next item is the expected value.
        """
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self) -> str:
        """Looks at the current character in source"""
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        """Looks at the next character in source"""
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_at_end(self) -> bool:
        """Check if the scanning is at the end of the source."""
        return self.current >= len(self.source)

    def advance(self) -> str:
        """Moves the counter by one and returns the source at the counter."""
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, tokentype: TokenType, literal: object = None):
        """
        Adds a token to the list of tokens.

        Appends the corresponding TokenType and its actual lexeme.

        Args:
            tokentype: TokenType
                The type of the token scanned

            literal: object
                ?

        Returns:
            None
        """
        text: str = self.source[self.start:self.current]
        self.tokens.append(Token(tokentype, text, literal, self.line))
