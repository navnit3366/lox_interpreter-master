from token_type import TokenType
from visitor import Visitor
from token import Token
import Expr


class ASTPrinter(Visitor):

    def __init__(self):
        pass

    def pprint_ast(self, expr):
        return expr.accept(self)

    def parenthesize(self, name, *expressions):

        builder = f"({name}"

        for expr in expressions:
            builder += f" {expr.accept(self)}"

        builder += ")"
        return builder

    def visit_Binary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_Grouping_expr(self, expr):
        return self.parenthesize("group", expr.expression)

    def visit_Unary_expr(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_Literal_expr(self, expr):

        if expr.value is None:
            return "nil"

        return str(expr.value)

    def visit_Conditional_expr(self, expr):
        return self.parenthesize("?", expr.condition, expr.then_jump, expr.else_jump)


if __name__ == '__main__':
    expression = Expr.Binary(
        Expr.Unary(
            Token(TokenType.MINUS, '-', None, 1),
            Expr.Literal(123)
        ),
        Token(TokenType.STAR, '*', None, 1),
        Expr.Grouping(
            Expr.Literal(45.67)
        )
    )

    test = Expr.Conditional(
        Expr.Binary(
            Expr.Unary(
                Token(TokenType.IDENTIFIER, '', None, 1),
                Expr.Literal('a')
            ),
            Token(TokenType.LESS, '<', None, 1),
            Expr.Unary(
                Token(TokenType.IDENTIFIER, '', None, 1),
                Expr.Literal('b')
            )
        ),
        Expr.Unary(
            Token(TokenType.IDENTIFIER, '', None, 1),
            Expr.Literal('a')
        ),
        Expr.Unary(
            Token(TokenType.IDENTIFIER, '', None, 1),
            Expr.Literal('b')
        )
    )
    past = ASTPrinter().pprint_ast(test)
    print(past)
