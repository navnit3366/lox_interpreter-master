from error_handler import ErrorHandler
from token_type import *
from token import Token


class Scanner:

    def __init__(self, error_handler: ErrorHandler, source):

        self.source = source
        self.error_handler = error_handler
        self.tokens = list()

        self.start = 0
        self.current = 0
        self.line = 1

        self.keywords = {'and': TokenType.AND,
                         'class': TokenType.CLASS,
                         'else': TokenType.ELSE,
                         'false': TokenType.FALSE,
                         'for': TokenType.FOR,
                         'fun': TokenType.FUN,
                         'if': TokenType.IF,
                         'nil': TokenType.NIL,
                         'or': TokenType.OR,
                         'print': TokenType.PRINT,
                         'return': TokenType.RETURN,
                         'super': TokenType.SUPER,
                         'this': TokenType.THIS,
                         'true': TokenType.TRUE,
                         'var': TokenType.VAR,
                         'while': TokenType.WHILE}

    def scan_tokens(self):

        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):

        char = self.advance()

        if char == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ',':
            self.add_token(TokenType.COMMA)
        elif char == '.':
            self.add_token(TokenType.DOT)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == ';':
            self.add_token(TokenType.SEMICOLON)
        elif char == '*':
            self.add_token(TokenType.STAR)
        elif char == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif char == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif char == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif char == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif char == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            elif self.match('*'):
                self.skip()
            else:
                self.add_token(TokenType.SLASH)
        elif char == '?':
            self.add_token(TokenType.QUESTION)
        elif char == ':':
            self.add_token(TokenType.COLON)
        elif char == ' ' or char == '\r' or char == '\t':
            pass
        elif char == '\n':
            self.line += 1
        elif char == '"':
            self.string()
        else:
            if self.is_digit(char):
                self.number()
            elif self.is_alpha(char):
                self.identifier()
            else:
                self.error_handler.error(self.line, 'Unexpected character.')

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):

        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected):

        if self.is_at_end():
            return False

        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):

        if self.is_at_end():
            return '\0'

        return self.source[self.current]

    def string(self):

        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error_handler.error(self.line, "Unterminated String.")
            return

        self.advance()
        string_value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, string_value)

    @staticmethod
    def is_digit(char):
        return '0' <= char <= '9'

    @staticmethod
    def is_alpha(char):
        return ('a' <= char <= 'z') or ('A' <= char <= 'Z') or char == '_'

    def is_alpha_numeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)

    def identifier(self):

        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        t = TokenType.IDENTIFIER

        if text in self.keywords:
            t = self.keywords[text]

        self.add_token(t)

    def skip(self):

        while True:

            if self.is_at_end():
                break

            if self.peek() == '*' and self.peek_next() == '/':
                self.advance()
                self.advance()
                break

            if self.peek() == '\n':
                self.line += 1

            self.advance()

    # def ternary(self):

    #     while not self.match(':'):

    #         if self.is_at_end():
    #             self.error_handler.error(self.line, " Expect ':' separator after then statement in ternary operator!")
    #             return

    #         self.start = self.current
    #         self.scan_token()

    #     self.current -= 1
    #     self.add_token(TokenType.COLON)
    #     self.advance()

    def number(self):

        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))

    def peek_next(self):

        if self.current + 1 >= len(self.source):
            return '\0'

        return self.source[self.current + 1]

    def add_token(self, token_type: TokenType, literal=None):

        text = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
        