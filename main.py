#!/usr/local/bin/python3
# encoding: utf-8
import sys
import os

from parser import Parser
from gui import Painter
from error import IEError


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ./main.py filename')
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print('%s not exists.' % sys.argv[1])
        exit(0)

    try:
        paint = Painter()
        parser = Parser(sys.argv[1])
        parser.start_paser()
        paint.paint_point_list(parser.point_list)
        paint.root.mainloop()
    except IEError as e:
        print(e)
        exit(0)
    except Exception as e:
        print('Runtime error. %s' % e)
        exit(0)
