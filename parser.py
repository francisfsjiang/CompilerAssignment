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

    def make_node(self, _type, _left, _right=None, _value=None):
        pos = len(self.node_list)
        node = Node(pos, _type, _left, _right)
        self.node_list.append(node)
        return pos

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
        self.match_token('ORIGIN')
        self.match_token('IS')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.visual_node(x_node)
        self.match_token('COMMA')
        y_node = self.node_expression()
        self.visual_node(y_node)
        self.match_token('R_BRACKET')

    def state_rot(self):
        self.match_token('ROT')
        self.match_token('IS')
        value_node = self.node_expression()
        self.visual_node(value_node)

    def state_scale(self):
        self.match_token('SCALE')
        self.match_token('IS')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.match_token('COMMA')
        self.visual_node(x_node)
        y_node = self.node_expression()
        self.visual_node(y_node)
        self.match_token('R_BRACKET')

    def state_for(self):
        self.match_token('FOR')
        self.match_token('T')
        self.match_token('FROM')
        start_node = self.node_expression()
        self.visual_node(start_node)
        self.match_token('TO')
        end_node = self.node_expression()
        self.visual_node(end_node)
        self.match_token('STEP')
        stop_node = self.node_expression()
        self.visual_node(stop_node)
        self.match_token('DRAW')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.visual_node(x_node)
        self.match_token('COMMA')
        y_node = self.node_expression()
        self.visual_node(y_node)
        self.match_token('R_BRACKET')

    def node_expression(self):
        left = self.node_term()
        while self.token.type == 'PLUS' or self.token.type == 'MINUS':
            token_temp = self.token.type
            self.match_token(token_temp)
            right = self.node_term()
            left = self.make_node(token_temp, left, right)
        return left

    def node_term(self):
        left = self.node_factor()
        while self.token.type == 'MUL' or self.token.type == 'DIV':
            token_temp = self.token.type
            self.match_token(token_temp)
            right = self.node_factor()
            left = self.make_node(token_temp, left, right)
        return left

    def node_factor(self):
        if self.token.type == 'PLUS' or self.token.type == 'MINUS':
            token_temp = self.token.type
            self.match_token(token_temp)
            right = self.node_factor()
            left = self.make_node('CONST_ID', 0)
            right = self.make_node(token_temp, left, right)
        else:
            right = self.node_component()
        return right

    def node_component(self):
        left = self.node_atom()
        if self.token.type == 'POWER':
            self.match_token('POWER')
            right = self.node_component()
            left = self.make_node('POWER', left, right)
        return left

    def node_atom(self):
        if self.token.type == 'CONST_ID' or self.token.type == 'T':
            self.match_token(self.token.type)

            return self.make_node(self.token.type, _value=self.token.value)
        elif self.token.type == 'FUNC':
            self.match_token('FUNC')
            self.match_token('L_BRACKET')
            tmp = self.node_expression()
            self.match_token('R_BRACKET')
        elif self.token.type == 'L_BRACKET':
            self.match_token('L_BRACKET')
            tmp = self.node_expression()
            self.match_token('R_BRACKET')
        else:
            raise CEError('Syntax Error.(atom)')
        return tmp

    def visual_node(self, pos, intent=0):
        if not pos:
            return
        node = self.node_list[pos]
        for i in range(intent):
            print('    ', end='')
        print('%5s %5s' % (node.type, node.value))
        self.visual_node(node.left)
        self.visual_node(node.right)


class Node:
    def __init__(self, _pos, _type, _left, _right, _value=None):
        self.pos = _pos
        self.type = _type
        self.left = _left
        self.right = _right
        self.value = _value