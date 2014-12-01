# encoding: utf-8
import math
import re
from queue import deque
from error import *


class Token:
    def __init__(self, token_type=None, lexeme='', value=None, func=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.value = value
        self.func = func


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
    'SEMICO': ['SEMICO', 'SEMICO', 0, None],
    'L_BRACKET': ['L_BRACKET', 'L_BRACKET', 0, None],
    'R_BRACKET': ['R_BRACKET', 'R_BRACKET', 0, None],
    'COMMA': ['COMMA', 'COMMA', 0, None],
    #operator
    'PLUS': ['PLUS', 'PLUS', 0, None],
    'MINUS': ['MINUS', 'MINUS', 0, None],
    'MUL': ['MUL', 'MUL', 0, None],
    'DIV': ['DIV', 'DIV', 0, None],
    'POWER': ['POWER', 'POWER', 0, None],
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
        self.re = re.compile(r'([a-zA-Z][a-zA-Z]*|[\d][\d]*[.[\d]*]?|\+|-|\*|/|\*\*|;|\(|\)|,)')
        file.close()

