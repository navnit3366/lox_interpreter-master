from abc import ABC
from abc import abstractmethod


class Visitor(ABC):

    @abstractmethod
    def visit_Binary_expr(self, expr):
        pass

    @abstractmethod
    def visit_Unary_expr(self, expr):
        pass

    @abstractmethod
    def visit_Grouping_expr(self, expr):
        pass

    @abstractmethod
    def visit_Literal_expr(self, expr):
        pass

    @abstractmethod
    def visit_Conditional_expr(self, expr):
        pass
