from expr import Expr, Binary, Grouping, Literal, Unary
from visitor import Visitor
from io import StringIO
from token import Token
from token_type import TokenType


class ASTPrinter(Visitor):
    def __init__(self):
        pass

    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(self,
                                 [expr.operator.lexeme, expr.left, expr.right])

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize(self, [expr.expresion])

    def visit_literal_expr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(self, [expr.operator.lexeme, expr.right])

    def parenthesize(self, name: str, exprs: list[Expr]):
        result: str = f"({name}"
        for e in exprs:
            result += f" {e.accept(self)}"
        result += ")"
        return result


def main():
    expression: Expr = Binary(
            Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67))
            )
    printer = ASTPrinter()
    print(printer.print(expression))


if __name__ == "__main__":
    main()
