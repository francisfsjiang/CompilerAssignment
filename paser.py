# encoding: utf-8
from scanner import Scanner


class Parser:
    def __init__(self, file_name):
        self.scanner = Scanner(file_name)
        self.token_list = self.scanner.get_token_list()
        self.tree = []

    def program(self):
        pass

    def state(self):
        pass

    def state_origin(self):
        pass

    def state_rot(self):
        pass

    def state_scale(self):
        pass

    def state_for(self):
        pass

    def node_expression(self):
        pass

    def node_term(self):
        pass

    def node_factor(self):
        pass

    def node_component(self):
        pass

    def node_atom(self):
        pass