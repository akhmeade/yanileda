#coding: utf-8

import math

class Worm:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
    
    def pos(self):
        return round(self.x, 2), round(self.y, 2)
    
    def get_bias(self, length):
        rad_angle = math.radians(self.angle)
        dx = length * math.cos(rad_angle)
        dy = length * math.sin(rad_angle)
        return dx, dy

    def forward(self, length):
        dx, dy = self.get_bias(length)
        self.x += dx
        self.y += dy

    def backward(self, length):
        dx, dy = self.get_bias(length)
        self.x -= dx
        self.y -= dy
    
    def left(self, angle):
        self.angle = (self.angle + angle) % 360
    
    def right(self, angle):
        self.angle = (self.angle - angle) % 360