from expr import Visitor, Expr, Binary


class ASTPrinter(Visitor):
    def __init__(self):
        pass

    def print(self, expr: Expr) -> str:
        return expr.accept()

    def visit_binary_expr(self, expr: Binary):
        pass
