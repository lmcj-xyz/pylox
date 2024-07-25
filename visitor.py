from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(expr):
        pass

    @abstractmethod
    def visit_grouping_expr(expr):
        pass

    @abstractmethod
    def visit_literal_expr(expr):
        pass

    @abstractmethod
    def visit_unary_expr(expr):
        pass

