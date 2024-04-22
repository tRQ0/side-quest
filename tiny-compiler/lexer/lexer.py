import enum
import sys

class Lexer:
    def __init__(self, source) -> None:
        self.source = source + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    def nextChar(self):
        self.curPos += 1
        self.len = len(self.source)
        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        if self.curPos+1 >= len(self.source):
            return '\0'
        
        return self.source[self.curPos + 1]

    def abort(self, message):
        sys.exit('Lexical error: ' + message)

    def skipWhiteLines(self):
        while self.curChar == ' ' or self.curChar == '\r' or self.curChar == '\t':
            self.nextChar()

    def skipComments(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()
                
    def getToken(self):
        token = None
        self.skipWhiteLines()
        self.skipComments()

        if self.curChar.isalpha():                 
            startPos = self.curPos
            while self.peek().isalpha():
                self.nextChar()
            
            tokenText = self.source[startPos : self.curPos + 1]
            keyword = Token.checkIfKeyword(tokenText)
            if keyword == None:
                token = Token(tokenText, TokenType.IDENT)
            else:
                token = Token(tokenText, keyword)
        elif self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '>':
            token = Token(self.curChar, TokenType.GT)
            if self.peek() == '=':
                lastChar =  self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
        elif self.curChar == '<':
            token = Token(self.curChar, TokenType.LT)
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
            token = Token(self.curChar, TokenType.LTEQ)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(self.curChar, TokenType.NOTEQ)
        elif self.curChar == '=':
            token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)
        elif self.curChar == '\"':
            self.nextChar()
            startPos = self.curPos
            while self.curChar != '\"':
                if self.curChar == '\r' or self.curChar == '\\' or self.curChar == '\n' or self.curChar == '%':
                    self.abort('invalid character in string')
                self.nextChar()
            tokenText = self.source[startPos : self.curPos + 1]    
            token = Token(tokenText, TokenType.STRING)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.curChar == '.':
                self.nextChar()
                if self.peek().isdigit():
                    self.abort('illegal character in number') 
                while self.peek().isdigit():
                    self.nextChar()
            tokenText = self.source[startPos : self.curPos + 1]
            token = Token(tokenText, TokenType.NUMBER)
        else:
            self.abort("Unknown token: " + self.curChar)

        self.nextChar()
        return token

class Token:
    def __init__(self, token, tokenType):
        self.text = token
        self.type = tokenType
        
    @staticmethod
    def checkIfKeyword(text):
        for type in TokenType:
            if type.name == text and type.value >= 100 and type.value < 200:
                return type
        return None
        
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
