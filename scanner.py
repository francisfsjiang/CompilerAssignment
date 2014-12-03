# encoding: utf-8
import math
import re
from error import *


def fib(n):
    n = int(n)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a = 0
        b = 1
        for i in range(n-1):
            a, b = b, a+b
        return b


class Token:
    def __init__(self, token_type=None, lexeme=None, value=0., func=None):
        self.token_type = token_type
        if lexeme:
            self.lexeme = lexeme
        else:
            self.lexeme = token_type
        self.value = value
        self.func = func
        self.line_no = 0

    def __str__(self):
        return '%10s %10s %10.4f %20s \t %d' % (self.token_type, self.lexeme, self.value, self.func, self.line_no)

    def format(self):
        return [self.token_type, self.lexeme, self.value, self.func]


TOKEN_TAB = {
    'PI': ['CONST_ID', 'PI', math.pi],
    'E': ['CONST_ID', 'E', math.e],
    'CONST_ID': ['CONST_ID', 'CONST_ID'],
    'T': ['T', 'T'],
    #func
    'SIN': ['FUNC', 'SIN', 0, math.sin],
    'COS': ['FUNC', 'COS', 0, math.cos],
    'TAN': ['FUNC', 'TAN', 0, math.tan],
    'LN': ['FUNC', 'LN', 0, math.log],
    'EXP': ['FUNC', 'EXP', 0, math.exp],
    'SQRT': ['FUNC', 'SQRT', 0, math.sqrt],
    'FIB': ['FUNC', 'FIB', 0, fib],
    #key word
    'ORIGIN': ['ORIGIN'],
    'SCALE': ['SCALE'],
    'ROT': ['ROT'],
    'IS': ['IS'],
    'FOR': ['FOR'],
    'FROM': ['FROM'],
    'TO': ['TO'],
    'STEP': ['STEP'],
    'DRAW': ['DRAW'],
    'COLOR': ['COLOR'],
    'RADIUS': ['RADIUS'],
    #symbol
    ';': ['SEMICO'],
    '(': ['L_BRACKET'],
    ')': ['R_BRACKET'],
    ',': ['COMMA'],
    #operator
    '+': ['PLUS', 'PLUS', 0, '__add__'],
    '-': ['MINUS', 'MINUS', 0, '__sub__'],
    '*': ['MUL', 'MUL', 0, '__mul__'],
    '/': ['DIV', 'DIV', 0, '__truediv__'],
    '**': ['POWER', 'POWER', 0, '__pow__'],
    #none
    'NONE': ['NONE'],
    #error
    'ERROR': ['ERROR'],
}


class Scanner:
    """
    """
    def __init__(self, file_name=None):
        file = open(file_name, mode='r')
        self.text = file.read()
        file.close()
        self.re = re.compile(
            r'(//.*|--.*|[a-zA-Z_][\w]*|[\d][\d]*[.[\d]*]?|\+|\*\*|-|/|\*|;|\(|\)|,|\n)'
        )
        self.elements = self.re.findall(self.text)
        # print(self.elements)
        self.token_list = None
        self.line_no = 1

    def _generate_token_list(self):
        self.token_list = []
        for i in self.elements:
            if i.startswith('//') or i.startswith('--'):
                continue
            if i == '\n':
                self.line_no += 1
                continue
            try:
                x = float(i)
                token = Token(*TOKEN_TAB['CONST_ID'])
                token.value = x
                token.line_no = self.line_no
                self.token_list.append(token)
                continue
            except ValueError:
                pass
            i = i.upper()
            if i in TOKEN_TAB:
                token = Token(*TOKEN_TAB[i])
            else:
                token = Token(*TOKEN_TAB['ERROR'])
            token.line_no = self.line_no
            self.token_list.append(token)
        token = Token(*TOKEN_TAB['NONE'])
        token.line_no = self.line_no
        self.token_list.append(token)

    def get_token_list(self):
        if not self.token_list:
            self._generate_token_list()
        return self.token_list


