import sys

from lexer.lexer import Lexer as lex
from lexer.lexer import TokenType

def main():
    source = "IF+-123 foo*THEN/"

    lexer = lex(source)

    token = lexer.getToken()
    # while lexer.peek() != '\0':
        # print(lexer.curChar)
        # lexer.nextChar()
    while token.type != TokenType.EOF:
        print(token.type)
        token = lexer.getToken()

main()