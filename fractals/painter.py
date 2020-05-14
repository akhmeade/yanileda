#coding: utf-8

import turtle
from .worm import Worm
import re

def create_l_system(iters, axiom, rules):
    start_string = axiom
    if iters == 0:
        return axiom
    end_string = ""
    for _ in range(iters):
        end_string = "".join(rules[i] if i in rules else i for i in start_string)
        start_string = end_string

    return end_string

def draw_l_system(t, instructions, angle, distance):
    for cmd in instructions:
        if cmd == 'F':
            t.forward(distance)
        elif cmd == '+':
            t.right(angle)
        elif cmd == '-':
            t.left(angle)

class L_Systems:
    def __init__(self, fractal_number):
        if (fractal_number == 0):
            self.fractal_name = "Koch Snowflake"
            self.axiom = "F--F--F"
            self.rules = {"F": "F+F--F+F"}
            self.iterations = 7
            self.angle = 60
        if (fractal_number == 1):
            self.fractal_name = "Krystall"
            self.axiom = "F+F+F+F"
            self.rules = {"F": "FF+F++F+F"}
            self.iterations = 6
            self.angle = 90
        if (fractal_number == 2):
            self.fractal_name = "Levi curve"
            self.axiom = "F"
            self.rules = {"F": "+F--F+"}
            self.iterations = 16
            self.angle = 45
        if (fractal_number == 3):
            self.fractal_name = "Serpinskii curve"
            self.axiom = "FXF--FF--FF"
            self.rules = {"F": "FF", "X": "--FXF++FXF++FXF--"}
            self.iterations = 8
            self.angle = 60
        if (fractal_number == 4):
            self.fractal_name = "Peano-Gosper curve"
            self.axiom = "FX"
            self.rules = {"X": "X+YF++YF-FX--FXFX-YF+", "Y": "-FX+YFYF++YF+FX--FX-Y"}
            self.iterations = 6
            self.angle = 60
        if (fractal_number == 5):
            self.fractal_name = "Gilbert curve"
            self.axiom = "L"
            self.rules = {"L": "+RF-LFL-FR+", "R": "-LF+RFR+FL-"}
            self.iterations = 9
            self.angle = 90
        if (fractal_number == 6):
            self.fractal_name = "Dragon curve"
            self.axiom = "FX"
            self.rules = {"X": "X+YF+", "Y": "-FX-Y"}
            self.iterations = 16
            self.angle = 90

class Painter:
    def __init__(self):
        self.values = []
        self.turtle = Worm()
        #self.turtle = turtle.Turtle()

    def append_unique_values(self):
        w, h = self.image.size
        x_coord, y_coord = self.turtle.pos()
        if x_coord < w and y_coord < h and x_coord >= 0 and y_coord >=0 and w >0 and h>0 :
            nval = self.image.getpixel((x_coord, y_coord))[0]
            if nval not in self.values:
                self.values.append(nval)

    def fractal_elements(self, image):
        self.image = image
        self.values = []
        # print("has")


class LSystemPainter(Painter):
    def __init__(self, curve_number):
        Painter.__init__(self)
        self.l_system = L_Systems(curve_number)

    def draw_l_system(self, instructions, angle, distance):
        for cmd in instructions:
            if cmd == 'F':
                self.turtle.forward(distance)
                self.append_unique_values()
            elif cmd == '+':
                self.turtle.right(angle)
                self.append_unique_values()
            elif cmd == '-':
                self.turtle.left(angle)
                self.append_unique_values()

    def fractal_elements(self, image):
        Painter.fractal_elements(self, image)
        instructions = create_l_system(self.l_system.iterations, self.l_system.axiom,
                                       self.l_system.rules)
        self.draw_l_system(instructions, self.l_system.angle, 8)


class SquarePainter(Painter):
    def __init__(self):
        Painter.__init__(self)

    def square(self):
        for _ in range(4):
            self.turtle.forward(50)
            self.append_unique_values()
            self.turtle.left(90)
            self.append_unique_values()

    def fractal_elements(self, image):
        Painter.fractal_elements(self, image)
        for i in range(60):
            self.square()
            self.turtle.left(i)

class TreePainter(Painter):
    def __init__(self):
        Painter.__init__(self)

    def tree(self, length, n):
        if length < length / n:
            return
        self.turtle.forward(length)
        self.append_unique_values()

        self.turtle.left(45)
        self.tree(length * 0.5, length / n)

        self.turtle.left(20)
        self.tree(length * 0.5, length / n)

        self.turtle.right(75)
        self.tree(length * 0.5, length / n)

        self.turtle.right(20)
        self.tree(length * 0.5, length / n)

        self.turtle.left(30)
        self.turtle.backward(length)
        self.append_unique_values()

    def fractal_elements(self, image):
        Painter.fractal_elements(self, image)
        self.turtle.left(90)
        self.turtle.backward(30)
        self.append_unique_values()
        self.tree(200, 4)

class KochPainter(Painter):
    def __init__(self):
        Painter.__init__(self)

    def snowflake(self, length, depth):
        if depth == 0:
            self.turtle.forward(length)
            self.append_unique_values()
            return

        length /= 3.0
        self.snowflake(length, depth-1)
        self.turtle.left(60)

        self.snowflake(length, depth-1)
        self.turtle.right(120)

        self.snowflake(length, depth-1)
        self.turtle.left(60)
        self.snowflake(length, depth-1)

    def fractal_elements(self, image):
        Painter.fractal_elements(self, image)
        for i in range(100):
            print(i)
            self.snowflake(300, 4)
            self.turtle.right(120)
            self.append_unique_values()

class SerpinskyPainter(Painter):
    def __init__(self):
        Painter.__init__(self)

    def draw_sierpinski(self,length, depth):
        if depth == 0:
            for i in range(0, 3):
                self.turtle.fd(length)
                self.turtle.left(120)
        else:
            self.draw_sierpinski(length / 2, depth - 1)
            self.turtle.forward(length / 2)
            self.append_unique_values()
            self.draw_sierpinski(length / 2, depth - 1)
            self.turtle.backward(length / 2)
            self.append_unique_values()
            self.turtle.left(60)
            self.turtle.forward(length / 2)
            self.append_unique_values()
            self.turtle.right(60)
            self.draw_sierpinski(length / 2, depth - 1)
            self.turtle.left(60)
            self.turtle.backward(length / 2)
            self.append_unique_values()
            self.turtle.right(60)

    def fractal_elements(self, image):
        Painter.fractal_elements(self, image)
        self.draw_sierpinski(100,2)
        self.append_unique_values()



if __name__ == "__main__":
    # for p in (SquarePainter(), TreePainter(), KochPainter()):
    #     print(p)
    #     p.fractal_elements(1)
    f1 = open("test.txt", "r")
    f2 = open("test2.txt", "r")

    a1 = f1.readlines()
    a2 = f2.readlines()
    k = 0
    for i, (s1, s2) in enumerate(zip(a1, a2)):
        if s1[0] != "<":

            nums1 = list(map(float, re.findall('\d+\.\d', s1)))
            nums2 = list(map(float, re.findall('\d+\.\d', s2)))
            if nums1 != nums2:
                print(i, s1, s2, nums1, nums2)
                k += 1
    print(k)
