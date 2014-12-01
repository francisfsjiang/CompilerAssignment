# encoding: utf-8
from scanner import Scanner
from error import *


class Parser:
    def __init__(self, file_name):
        self.scanner = Scanner(file_name)
        self.token_list = self.scanner.get_token_list()
        self.token_pos = -1
        self.token = None
        self.node_list = []

    def start(self):
        self.fetch_token()
        while self.token.type != 'NONE':
            self.state()
            self.match_token('SEMICO')

    def match_token(self, _type=None):
        if self.token.type != _type:
            raise CEError('Syntax Error.')
        self.fetch_token()

    def fetch_token(self):
        self.token_pos += 1
        if self.token_pos >= len(self.token_list):
            raise CEError('Syntax Error.(fetch)')
        self.token = self.token_list[self.token_pos]

    def make_node(self, _type, _left, _right):
        node = Node(len(self.node_list), _type, _left, _right)
        self.node_list.append(node)

    def state(self):
        if self.token.type == 'ORIGIN':
            self.state_origin()
        elif self.token.type == 'ROT':
            self.state_rot()
        elif self.token.type == 'SCALE':
            self.state_scale()
        elif self.token.type == 'FOR':
            self.state_for()
        else:
            raise CEError('Syntax error.(statement)')

    def state_origin(self):
        pass

    def state_rot(self):
        pass

    def state_scale(self):
        pass

    def state_for(self):
        self.match_token('FOR')
        self.match_token('T')
        self.match_token('FROM')
        start_node = self.node_expression()
        self.match_token('TO')
        end_node = self.node_expression()
        self.match_token('STEP')
        stop_node = self.node_expression()
        self.match_token('DRAW')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.match_token('COMMA')
        y_node = self.node_expression()
        self.match_token('R_BRACKET')

    def node_expression(self):
        left = self.node_term()
        while self.token.type == 'PLUS' or self.token.type == 'MINUS':
            token_temp = self.token.type
            self.match_token(token_temp)
            right = self.node_term()
            left = self.make_node(token_temp, left, right)

    def node_term(self):
        pass

    def node_factor(self):
        pass

    def node_component(self):
        pass

    def node_atom(self):
        pass


class Node:
    def __init__(self, _pos, _type, _left, _right, _value):
        self.pos = _pos
        self.type = _type
        self.left = _left
        self.right = _right
        self.value = _value