# encoding: utf-8
from parser import Parser
from gui import Painter


def run():
    paint = Painter()
    parser = Parser('test_code.ce')
    parser.start_paser()
    paint.paint_point_list(parser.point_list)
    # return parser.point_list
    # print(parser.point_list)
