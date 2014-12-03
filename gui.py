# encoding: utf-8
import tkinter


class Painter:
    def __init__(self, width=1200, height=800, bg='white'):
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=width, height=height, bd=5)
        self.canvas.pack()

    def add_point(self, x, y, color, radius):
        left_top = (x-radius, y-radius)
        right_bottom = (x+radius, y+radius)
        # print(color)
        color_value = color[0]*0x10000 + color[1]*0x100 + color[0]
        color_sign = hex(color_value)[2:]
        if len(color_sign) < 6:
            tmp = ''
            for i in range(6-len(color_sign)):
                tmp += '0'
            color_sign = tmp + color_sign
        color_sign = '#' + color_sign
        # print(color_sign)
        self.canvas.create_oval(left_top[0],
                                left_top[1],
                                right_bottom[0],
                                right_bottom[1],
                                fill=color_sign,
                                width=0
                                )

    def paint_point_list(self, l: list):
        for i in l:
            self.add_point(i[0], i[1], i[2], i[3])