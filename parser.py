from token import Token
from expr import Expr, Binary, Unary, Literal, Grouping
from token_type import TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self._current = 0

    def expression(self) -> Expr:
        return self.equality

    def equality(self) -> Expr:
        expr: Expr = self.comparison()

        while self._match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term()

        while self._match([TokenType.GREATER,
                           TokenType.GREATER_EQUAL,
                           TokenType.LESS,
                           TokenType.LESS_EQUAL]):
            operator: Token = self._previous()
            right: Expr = self.term()
            expr: Binary(expr, operator, right)

        return expr

    def term(self) -> Expr:
        expr: Expr = self.factor()

        while self._match([TokenType.MINUS, TokenType.PLUS]):
            operator: Token = self._previous()
            right: Expr = self.factor()
            expr: Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        while self._match([TokenType.SLASH, TokenType.STAR]):
            operator: Token = self._previous()
            right: Expr = self.unary()
            expr: Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr:
        if self._match([TokenType.MINUS, TokenType.BANG]):
            operator: Token = self._previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self._match([TokenType.FALSE]):
            return Literal(False)
        elif self._match([TokenType.TRUE]):
            return Literal(True)
        elif self._match([TokenType.NIL]):
            return Literal(None)
        elif self._match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self._previous().literal)
        elif self._match([TokenType.LEFT_PAREN]):
            expr: Expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

    def _match(self, types: list[TokenType]) -> bool:
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, t: TokenType, message: str):
        if self._check(t):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, type: TokenType):
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self):
        if self._is_at_end():
            self._current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _peek(self):
        return self.tokens[self._current]

    def _previous(self):
        return self.tokens[self._current - 1]
