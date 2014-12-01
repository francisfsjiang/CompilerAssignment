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


def get_token_by_id(id, value=0.):
    token = Token(*TOKEN_TAB[id])
    token.value = value
    return token


class Scanner():
    """
    """
    def __init__(self, file_name=None):
        file = open(file_name, mode='r')
        self.stream = deque(file.read())
        self.token_buffer = ''
        self.line_no = 0
        file.close()

    def _get_char(self):
        if len(self.stream):
        return self.stream.popleft()

    def _back_char(self, char):
        self.stream.appendleft(char)

    def _add_token_buffer(self, char):
        self.token_buffer += char

    def _empty_token_buffer(self):
        self.token_buffer = ''

    def _is_eof(self):
        if len(self.stream) == 0:
            return True
        else:
            return False

    def _judge_key_token(self, id):
        if id in TOKEN_TAB:
            return get_token_by_id(id)
        return get_token_by_id('ERROR', value=self.line_no)

    def _clean_stream(self):
        """
        clean the space, tab, enter, EOF in the stream
        :return:
        """
        while True:
            if self._is_eof():
                return get_token_by_id('NONE')
            char = self._get_char()
            if char == '\n':
                self.line_no += 1
            if not char.isspace():
                self._back_char(char)

    def get_token(self):
        self._empty_token_buffer()
        char = self._get_char()
        self._add_token_buffer(char)

        if char.isalpha():  #ID
            while True:
                char = self._get_char()
                if char.isalnum():
                    self._add_token_buffer(char)
                else:
                    break
            self._back_char(char)
            return get_token_by_id(self.token_buffer)
        elif char.isdigit():  #digit
            while True:
                char = self._get_char()
                if char.isdigit():
                    self._add_token_buffer(char)
                else:
                    break
            if char == '.':
                self._add_token_buffer(char)
                while True:
                    char = self._get_char()
                    if char.isdigit():
                        self._add_token_buffer(char)
                    else:
                        break
            self._back_char(char)
            return get_token_by_id('CONST', value=float(self.token_buffer))
        else:  #operator
            if char == ';':
                return get_token_by_id('SEMICO')
            elif char == '(':
                return get_token_by_id('L_BRACKET')
            elif char == ')':
                return get_token_by_id('R_BRACKET')
            elif char == ',':
                return get_token_by_id('COMMMA')
            elif char == '+':
                return get_token_by_id('PLUS')
            elif char == '-':
                return get_token_by_id('MINUS')
            elif char == '/':
                char = self._get_char()
                if char == '/'
                    while char != '\n' and self.stream



