# encoding: utf-8
import math


class Token:
    def __init__(self, token_type=None, lexeme='', value=None, func=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.value = value
        self.func = func


TOKEN_TAB = {
    'PI': Token('CONST_ID', 'PI', math.pi, None),
    'E': Token('CONST_ID', 'E', math.e, None),
    'T': Token('T', 'T', 0, None),
    'SIN': Token('FUNC', 'SIN', 0, math.sin),
    'COS': Token('FUNC', 'COS', 0, math.cos),
    'TAN': Token('FUNC', 'TAN', 0, math.tan),
    'LN': Token('FUNC', 'LN', 0, math.log),
    'EXP': Token('FUNC', 'EXP', 0, math.exp),
    'SQRT': Token('FUNC', 'EXP', 0, math.exp),
    'ORIGIN': Token('ORIGIN', 'ORIGIN', 0, None),
    'SCALE': Token('SCALE', 'SCALE', 0, None),
    'ROT': Token('ROT', 'ROT', 0, None),
    'IS': Token('IS', 'IS', 0, None),
    'FOR': Token('FOR', 'FOR', 0, None),
    'FROM': Token('FROM', 'FROM', 0, None),
    'TO': Token('TO', 'TO', 0, None),
    'STEP': Token('STEP', 'STEP', 0, None),
    'DRAW': Token('DRAW', 'DRAW', 0, None),
}


TOKEN_MAX_LEN = 500
LINE_NO = 0