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

    def start_paser(self):
        self.fetch_token()
        while self.token.token_type != 'NONE':
            self.state()
            self.match_token('SEMICO')

    def match_token(self, _type=None):
        if self.token.token_type != _type:
            raise CEError('Syntax Error.')
        self.fetch_token()

    def fetch_token(self):
        self.token_pos += 1
        if self.token_pos >= len(self.token_list):
            raise CEError('Syntax Error.(fetch)')
        self.token = self.token_list[self.token_pos]

    def make_node(self, token_type, left=None, right=None, value=None, func=None):
        pos = len(self.node_list)
        node = Node(pos, token_type, left, right, value, func)
        self.node_list.append(node)
        return pos

    def state(self):
        if self.token.token_type == 'ORIGIN':
            self.state_origin()
        elif self.token.token_type == 'ROT':
            self.state_rot()
        elif self.token.token_type == 'SCALE':
            self.state_scale()
        elif self.token.token_type == 'FOR':
            self.state_for()
        else:
            raise CEError('Syntax error.(statement)')

    def state_origin(self):
        self.match_token('ORIGIN')
        self.match_token('IS')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()

        self.eval_node(x_node)
        self.match_token('COMMA')
        y_node = self.node_expression()
        self.eval_node(y_node)
        self.match_token('R_BRACKET')

    def state_rot(self):
        self.match_token('ROT')
        self.match_token('IS')
        value_node = self.node_expression()
        self.eval_node(value_node)

    def state_scale(self):
        self.match_token('SCALE')
        self.match_token('IS')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.match_token('COMMA')
        self.eval_node(x_node)
        y_node = self.node_expression()
        self.eval_node(y_node)
        self.match_token('R_BRACKET')

    def state_for(self):
        self.match_token('FOR')
        self.match_token('T')
        self.match_token('FROM')
        start_node = self.node_expression()
        self.eval_node(start_node)
        self.match_token('TO')
        end_node = self.node_expression()
        self.eval_node(end_node)
        self.match_token('STEP')
        step_node = self.node_expression()
        self.eval_node(step_node)
        self.match_token('DRAW')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.eval_node(x_node)
        self.match_token('COMMA')
        y_node = self.node_expression()
        self.eval_node(y_node)
        self.match_token('R_BRACKET')

    def node_expression(self):
        left = self.node_term()
        while self.token.token_type == 'PLUS' or self.token.token_type == 'MINUS':
            token = self.token
            self.match_token(token.token_type)
            right = self.node_term()
            left = self.make_node(token.token_type, left, right, func=token.func)
        return left

    def node_term(self):
        left = self.node_factor()
        while self.token.token_type == 'MUL' or self.token.token_type == 'DIV':
            token = self.token
            self.match_token(token.token_type)
            right = self.node_factor()
            left = self.make_node(token.token_type, left, right, func=token.func)
        return left

    def node_factor(self):
        if self.token.token_type == 'PLUS' or self.token.token_type == 'MINUS':
            token = self.token
            self.match_token(token.token_type)
            right = self.node_factor()
            left = self.make_node('CONST_ID', value=0)
            right = self.make_node(token.token_type, left, right, func=token.func)
        else:
            right = self.node_component()
        return right

    def node_component(self):
        left = self.node_atom()
        if self.token.token_type == 'POWER':
            token = self.token
            self.match_token('POWER')
            right = self.node_component()
            left = self.make_node('POWER', left, right, value=token.func)
        return left

    def node_atom(self):
        if self.token.token_type == 'CONST_ID' or self.token.token_type == 'T':
            tmp_type = self.token.token_type
            tmp_value = self.token.value
            self.match_token(self.token.token_type)

            return self.make_node(tmp_type, value=tmp_value)
        elif self.token.token_type == 'FUNC':
            tmp_token = self.token
            self.match_token('FUNC')
            self.match_token('L_BRACKET')
            inner_node = self.node_expression()
            self.match_token('R_BRACKET')
            node = self.make_node('FUNC', func=tmp_token.func, right=inner_node)
        elif self.token.token_type == 'L_BRACKET':
            self.match_token('L_BRACKET')
            node = self.node_expression()
            self.match_token('R_BRACKET')
        else:
            raise CEError('Syntax Error.(atom)')
        return node

    def visual_node(self, pos, intent=0):
        if pos is None:
            return
        node = self.node_list[pos]
        for i in range(intent):
            print('    ', end='')
        print('%s %5s %10s' % (node.type, node.value, node.func))
        if not node.func or type(node.func) == type('str'):
            self.visual_node(node.left, intent + 1)
        self.visual_node(node.right, intent + 1)

    def eval_node(self, pos):
        node = self.node_list[pos]
        if node.token_type == 'CONST_ID':
            return node.value
        elif node.token_type == 'FUNC':
            right_value = self.eval_node(node.right)
            node.value = node.func(right_value)
            return node.value
        elif node.token_type in ['PLUS', 'MINUS', 'MUL', 'DIV', 'POWER']:
            left_value = self.eval_node(node.left)
            right_value = self.eval_node(node.right)
            node.value = getattr(left_value, node.func)
            return node.value


class Node:
    def __init__(self, pos, token_type, left=None, right=None, value=None, func=None):
        self.pos = pos
        self.type = token_type
        self.left = left
        self.right = right
        self.value = value
        self.func = func