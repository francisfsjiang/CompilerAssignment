# encoding: utf-8
import math
import re
from error import *


class Token:
    def __init__(self, token_type=None, lexeme=None, value=0., func=None):
        self.token_type = token_type
        if lexeme:
            self.lexeme = lexeme
        else:
            self.lexeme = token_type
        self.value = value
        self.func = func

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
    'SQRT': ['FUNC', 'EXP', 0, math.sqrt],
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
    #symbol
    ';': ['SEMICO'],
    '(': ['L_BRACKET'],
    ')': ['R_BRACKET'],
    ',': ['COMMA'],
    #operator
    '+': ['PLUS'],
    '-': ['MINUS'],
    '*': ['MUL'],
    '/': ['DIV'],
    '**': ['POWER'],
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
        self.re = re.compile(r'([a-zA-Z_][\w]*|[\d][\d]*[.[\d]*]?|\+|\*|//.*|--.*|-|/|\*\*|;|\(|\)|,)')
        self.elements = self.re.findall(self.text)
        print(self.elements)
        self.token_list = None

    def _generate_token_list(self):
        self.token_list = []
        for i in self.elements:
            try:
                x = float(i)
                token = Token(*TOKEN_TAB['CONST_ID'])
                token.value = x
                self.token_list.append(token)
                continue
            except ValueError:
                pass
            if i.startswith('//') or i.startswith('--'):
                continue
            i = i.upper()
            if i in TOKEN_TAB:
                self.token_list.append(Token(*TOKEN_TAB[i]))
            else:
                self.token_list.append(Token(*TOKEN_TAB['ERROR']))
        self.token_list.append(Token(*TOKEN_TAB['NONE']))

    def get_token_list(self):
        if not self.token_list:
            self._generate_token_list()
        return self.token_list
