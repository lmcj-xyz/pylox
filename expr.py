from token import Token
from abc import ABC, abstractmethod


class Expr:
    pass


class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(expr: Binary):
        pass

    @abstractmethod
    def visit_grouping_expr(expr: Grouping):
        pass

    @abstractmethod
    def visit_literal_expr(expr: Literal):
        pass

    @abstractmethod
    def visit_unary_expr(expr: Unary):
        pass



class Grouping(Expr):
    def __init__(self, expresion: Expr):
        self.expresion = expresion

    def accept(self, visitor: Visitor):
        return visitor.visit_Grouping_Expr(self)


class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor: Visitor):
        return visitor.visit_Literal_Expr(self)


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor):
        return visitor.visit_Unary_Expr(self)


