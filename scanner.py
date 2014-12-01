# encoding: utf-8
import math
import re
from error import *


class Token:
    def __init__(self, token_type=None, lexeme='', value=None, func=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.value = value
        self.func = func

    def format(self):
        return [self.token_type, self.lexeme, self.value, self.func]


TOKEN_TAB = {
    'PI': ['CONST_ID', 'PI', math.pi, None],
    'E': ['CONST_ID', 'E', math.e, None],
    'CONST_ID': ['CONST_ID', 'CONST_ID', 0, None],
    'T': ['T', 'T', 0, None],
    #func
    'SIN': ['FUNC', 'SIN', 0, math.sin],
    'COS': ['FUNC', 'COS', 0, math.cos],
    'TAN': ['FUNC', 'TAN', 0, math.tan],
    'LN': ['FUNC', 'LN', 0, math.log],
    'EXP': ['FUNC', 'EXP', 0, math.exp],
    'SQRT': ['FUNC', 'EXP', 0, math.sqrt],
    #key word
    'ORIGIN': ['ORIGIN', 'ORIGIN'],
    'SCALE': ['SCALE', 'SCALE', 0, None],
    'ROT': ['ROT', 'ROT', 0, None],
    'IS': ['IS', 'IS', 0, None],
    'FOR': ['FOR', 'FOR', 0, None],
    'FROM': ['FROM', 'FROM', 0, None],
    'TO': ['TO', 'TO', 0, None],
    'STEP': ['STEP', 'STEP', 0, None],
    'DRAW': ['DRAW', 'DRAW', 0, None],
    #symbol
    ';': ['SEMICO', 'SEMICO', 0, None],
    '(': ['L_BRACKET', 'L_BRACKET', 0, None],
    ')': ['R_BRACKET', 'R_BRACKET', 0, None],
    ',': ['COMMA', 'COMMA', 0, None],
    #operator
    '+': ['PLUS', 'PLUS', 0, None],
    '-': ['MINUS', 'MINUS', 0, None],
    '*': ['MUL', 'MUL', 0, None],
    '/': ['DIV', 'DIV', 0, None],
    '**': ['POWER', 'POWER', 0, None],
    #none
    'NONE': ['NONE', 'NONE', 0, None],
    #error
    'ERROR': ['ERROR', 'ERROR', 0, None],
}


class Scanner():
    """
    """
    def __init__(self, file_name=None):
        file = open(file_name, mode='r')
        self.text = file.read()
        file.close()
        self.re = re.compile(r'([a-zA-Z_][\w]*|[\d][\d]*[.[\d]*]?|\+|\*|//.*\n|--.*\n|-|/|\*\*|;|\(|\)|,)')
        self.elements = self.re.findall(self.text)
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

    def get_token_list(self):
        if not self.token_list:
            self._generate_token_list()
        return self.token_list
