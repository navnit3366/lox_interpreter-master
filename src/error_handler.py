from token import Token
from token_type import TokenType


class ParseError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)


class LoxRunTimeError(RuntimeError):
    def __init__(self, token_type: Token, message):
        super().__init__(message)
        self.token_type = token_type


class ErrorHandler:

    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def error(self, line, message):
        self.report(line, '', message)

    def parser_error(self, token: Token, msg):

        if token.token_type == TokenType.EOF:
            self.report(token.line, ' at end', msg)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", msg)

    def interpreter_error(self, error: LoxRunTimeError):

        print(str(error) + '\n[line ' + str(error.token_type.line) + ']')
        self.had_runtime_error = True

    def report(self, line, where, message):

        print('[Line ' + str(line) + '] Error' + where + ': ' + message)
        self.had_error = True
