# encoding: utf-8


class CEError(Exception):
    def __init_(self, msg):
        self.args = (msg, '123')