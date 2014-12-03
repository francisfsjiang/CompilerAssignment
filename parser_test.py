# encoding: utf-8
from parser import Parser
from pprint import pprint

if __name__ == '__main__':
    paser = Parser('test_code.ce')
    paser.start_paser()
    # for i in paser.node_list:
    #     print(i)
    paser.visual_all_nodes()
    # print(paser.point_list)