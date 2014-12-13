# encoding: utf-8
from scanner import Scanner
from math import cos, sin
from error import *


class Parser:
    def __init__(self, file_name):
        self.scanner = Scanner(file_name)
        self.token_list = self.scanner.get_token_list()
        self.token_pos = -1
        self.token = None
        self.node_list = []

        #global_value
        self.global_origin = (0, 0)
        self.global_scale = (1, 1)
        self.global_rot = 0
        self.global_t = 0

        #point_list
        self.point_list = []

        #root nodes
        self.root_nodes = []

    def start_paser(self):
        self.fetch_token()
        while self.token.token_type != 'NONE':
            self.state()
            self.match_token('SEMICO')

    def match_token(self, _type=None):
        if self.token.token_type != _type:
            if _type == 'SEMICO':
                line_no = self.token_list[self.token_pos-1].line_no
            else:
                line_no = self.token.line_no
            raise IEError('@%d: Syntax error.(Except %s here)' % (line_no, _type))
        self.fetch_token()

    def fetch_token(self):
        self.token_pos += 1
        if self.token_pos >= len(self.token_list):
            raise IEError('@%d: Syntax error.(Statement uncompleted)' % self.token.line_no)
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
            raise IEError('@%d: Syntax error.(Statement Not Found)' % self.token.line_no)

    def state_origin(self):
        self.match_token('ORIGIN')
        self.match_token('IS')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.root_nodes.append(x_node)
        self.eval_node(x_node)
        self.match_token('COMMA')
        y_node = self.node_expression()
        self.root_nodes.append(y_node)
        self.eval_node(y_node)
        self.match_token('R_BRACKET')

        #eval
        x_value = self.eval_node(x_node)
        y_value = self.eval_node(y_node)
        self.global_origin = (x_value, y_value)

    def state_rot(self):
        self.match_token('ROT')
        self.match_token('IS')
        value_node = self.node_expression()
        self.root_nodes.append(value_node)
        self.eval_node(value_node)

        value = self.eval_node(value_node)
        self.global_rot = value

    def state_scale(self):
        self.match_token('SCALE')
        self.match_token('IS')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.root_nodes.append(x_node)
        self.match_token('COMMA')
        self.eval_node(x_node)
        y_node = self.node_expression()
        self.root_nodes.append(y_node)
        self.eval_node(y_node)
        self.match_token('R_BRACKET')

        #eval
        x_value = self.eval_node(x_node)
        y_value = self.eval_node(y_node)
        self.global_scale = (x_value, y_value)

    def state_for(self):
        self.match_token('FOR')
        self.match_token('T')
        self.match_token('FROM')
        start_node = self.node_expression()
        self.root_nodes.append(start_node)
        # self.eval_node(start_node)
        self.match_token('TO')
        end_node = self.node_expression()
        self.root_nodes.append(end_node)
        # self.eval_node(end_node)
        self.match_token('STEP')
        step_node = self.node_expression()
        self.root_nodes.append(step_node)
        # self.eval_node(step_node)
        self.match_token('DRAW')
        self.match_token('L_BRACKET')
        x_node = self.node_expression()
        self.root_nodes.append(x_node)
        self.match_token('COMMA')
        y_node = self.node_expression()
        self.node_list.append(y_node)
        self.match_token('R_BRACKET')

        color_flag = False
        if self.token.token_type == 'COLOR':
            color_flag = True
            self.match_token('COLOR')
            self.match_token('L_BRACKET')
            color_r_node = self.node_expression()
            self.root_nodes.append(color_r_node)
            self.match_token('COMMA')
            color_g_node = self.node_expression()
            self.root_nodes.append(color_g_node)
            self.match_token('COMMA')
            color_b_node = self.node_expression()
            self.root_nodes.append(color_b_node)
            self.match_token('R_BRACKET')

        radius_flag = False
        if self.token.token_type == 'RADIUS':
            radius_flag = True
            self.match_token('RADIUS')
            radius_node = self.node_expression()
            self.root_nodes.append(radius_node)

        #eval
        start_value = self.eval_node(start_node)
        end_value = self.eval_node(end_node)
        step_value = self.eval_node(step_node)
        i = start_value
        while True:
            self.global_t = i
            x_value = self.eval_node(x_node)
            y_value = self.eval_node(y_node)

            if color_flag:
                color_r_value = self.eval_node(color_r_node)
                color_g_value = self.eval_node(color_g_node)
                color_b_value = self.eval_node(color_b_node)
                color_value = (int(color_r_value), int(color_g_value), int(color_b_value))
            else:
                color_value = (0x00, 0x00, 0x00)

            if radius_flag:
                radius_value = self.eval_node(radius_node)
            else:
                radius_value = 1

            step_value = self.eval_node(step_node)
            self.add_point(x_value, y_value, color_value, radius_value)
            i += step_value
            if i > end_value:
                break

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
            left = self.make_node('POWER', left, right, func=token.func)
        return left

    def node_atom(self):
        if self.token.token_type == 'CONST_ID' or self.token.token_type == 'T':
            tmp_type = self.token.token_type
            tmp_value = self.token.value
            self.match_token(self.token.token_type)
            node = self.make_node(tmp_type, value=tmp_value)
            return node

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
            raise IEError('@%d: Syntax error.(Unexpected symbol)' % self.token.line_no)
        return node

    def visual_all_nodes(self):
        for i in self.root_nodes:
            self.visual_node(i)

    def visual_node(self, pos, intent=0):
        if pos is None:
            return
        node = self.node_list[pos]
        for i in range(intent):
            print('    ', end='')
        print('%s %5s %10s' % (node.token_type, node.value, node.func))
        if not node.func or type(node.func) == type('str'):
            self.visual_node(node.left, intent + 1)
        self.visual_node(node.right, intent + 1)

    def eval_node(self, pos):
        node = self.node_list[pos]
        if node.token_type == 'CONST_ID':
            return node.value
        if node.token_type == 'T':
            node.value = self.global_t
            return self.global_t
        elif node.token_type == 'FUNC':
            right_value = self.eval_node(node.right)
            node.value = node.func(right_value)
            return node.value
        elif node.token_type in ['PLUS', 'MINUS', 'MUL', 'DIV', 'POWER']:
            left_value = self.eval_node(node.left)
            right_value = self.eval_node(node.right)
            node.value = getattr(float(left_value), node.func)(right_value)
            return node.value

    def add_point(self, x, y, color_value, radius):
        local_x, local_y = x, y
        local_x, local_y = local_x*self.global_scale[0], local_y*self.global_scale[1]
        temp_x = local_x*cos(self.global_rot) + local_y*sin(self.global_rot)
        temp_y = local_x*sin(self.global_rot) + local_y*cos(self.global_rot)
        local_x, local_y = temp_x, temp_y
        local_x += self.global_origin[0]
        local_y += self.global_origin[1]
        self.point_list.append((local_x, local_y, color_value, radius))


class Node:
    def __init__(self, pos, token_type, left=None, right=None, value=None, func=None):
        self.pos = pos
        self.token_type = token_type
        self.left = left
        self.right = right
        self.value = value
        self.func = func

    def __str__(self):
        return str(self.pos) + ' ' + str(self.left) + ' ' + str(self.right) + ' ' +\
            self.token_type + ' ' + str(self.value) + ' ' + str(self.func)