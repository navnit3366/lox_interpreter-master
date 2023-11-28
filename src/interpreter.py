from visitor import Visitor
from error_handler import *
from token_type import *
from Expr import *


class Interpreter(Visitor):

    def __init__(self, error_handler: ErrorHandler):
        self.error_handler = error_handler

    @staticmethod
    def is_truthy(expr):

        if expr is None:
            return False
        elif type(expr) is bool:
            return expr

        return True

    @staticmethod
    def is_equal(left, right):

        if left is None and right is None:
            return True
        if left is None:
            return False

        return left == right

    @staticmethod
    def check_number_operand(operator, operand):

        if type(operand) is float:
            return

        raise LoxRunTimeError(operator, 'Operand must be a number!')

    @staticmethod
    def check_number_operands(operator, left, right):

        if type(left) is float and type(right) is float:
            return

        raise LoxRunTimeError(operator, 'Operands must be numbers!')

    @staticmethod
    def stringfy(element):

        if element is None:
            return 'nil'

        if type(element) is float:
            text = str(element)

            if text.endswith('.0'):
                text = text[:len(text) - 2]

            return text

        return str(element)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def interpret(self, expression: Expr):

        try:
            element = self.evaluate(expression)
            print(self.stringfy(element))
        except LoxRunTimeError as error:
            self.error_handler.interpreter_error(error)

    def visit_Literal_expr(self, expr: Literal):
        return expr.value

    def visit_Grouping_expr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_Unary_expr(self, expr: Unary):

        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        if expr.operator.token_type == TokenType.BANG:
            return not self.is_truthy(right)
        else:
            return None

    def visit_Binary_expr(self, expr: Binary):

        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif expr.operator.token_type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif expr.operator.token_type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif expr.operator.token_type == TokenType.PLUS:
            if type(left) is float and type(right) is float:
                return float(left) + float(right)
            if type(left) is str or type(right) is str:
                if type(left) is not bool and type(right) is not bool:
                    if isinstance(left, float) and left.is_integer():
                        left = int(left)
                    if isinstance(right, float) and right.is_integer():
                        right = int(right)
                    return str(left) + str(right)
            raise LoxRunTimeError(expr.operator, 'The two operands must be numbers or one of them must be string! (coercion)')
        elif expr.operator.token_type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif expr.operator.token_type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif expr.operator.token_type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif expr.operator.token_type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif expr.operator.token_type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.token_type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)

        return None

    def visit_Conditional_expr(self, expr: Conditional):

        condition = self.evaluate(expr.condition)
        then_jump = self.evaluate(expr.then_jump)
        else_jump = self.evaluate(expr.else_jump)

        if self.is_truthy(condition):
            return then_jump

        return else_jump
