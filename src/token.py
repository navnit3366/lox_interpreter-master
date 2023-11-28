from token_type import TokenType


class Token:

    def __init__(self, token_type: TokenType, lexeme, literal, line):

        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def show(self):

        return ''.join(str(self.token_type) + '' + str(self.lexeme) + '' + self.literal)
