#coding: utf-8
import turtle
from .worm import Worm
import re

class Painter:
    def __init__(self):
        self.values = []
        self.turtle = Worm()
        #self.turtle = turtle.Turtle()

    def append_unique_values(self):
        w, h = self.image.size
        x_coord, y_coord = self.turtle.pos()
        if x_coord < w and y_coord < h:
            nval = self.image.getpixel((x_coord, y_coord))[0]

            if nval not in self.values:
                self.values.append(nval)

    def fractal_elements(self, image):
        self.image = image
        self.values = []
        #print("has")

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

    # def koch(self, length, depth):
    #     if depth == 0:
    #         self.turtle.forward(length)
    #         return
    #     self.koch(length, depth - 1)
    #     self.turtle.right(60)
    #     self.koch(length, depth - 1)
    #     self.koch(120, 0)
    #     self.koch(length, depth - 1)
    #     self.turtle.right(60)
    #     self.koch(length, depth - 1)
    

    # def fractal_elements(self, image):
    #     Painter.fractal_elements(self, image)
    #     self.turtle.left(90)
    #     #self.turtle.backward(300)
    #     self.koch(10, 6)
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
        for i in range(3):
            print(i)
            self.snowflake(300, 4)
            self.turtle.right(120)
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
                k+=1
    print(k)