# encoding: utf-8
import tkinter


class Painter:
    def __init__(self, width=300, height=300, bg='white'):
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=width, height=height, bd=5)
        self.canvas.pack()

    def add_point(self, x, y, radius):
        left_top = (x-radius, y-radius)
        right_bottom = (x+radius, y+radius)
        self.canvas.create_oval(left_top[0],
                                left_top[1],
                                right_bottom[0],
                                right_bottom[1],
                                fill='#000000')

    def paint_point_list(self, l: list):
        for i in l:
            self.add_point(i[0], i[1], 0.1)