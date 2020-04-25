#import turtle
import numpy as np
from PIL import Image

from .util import PythonF5Random as F5Random
from .util import Permutation
from .painter import SquarePainter
from .painter import TreePainter
from .painter import KochPainter

import logging
import turtle
logger = logging.getLogger(__name__)
# turtle.tracer(False)


def generate_key(path_to_image, password, key_size):
    image = Image.open(path_to_image)
    width, height = image.size
    logger.info('%d x %d' % (width, height))

    grey = image.convert('LA')
    pixels = list(grey.getdata())

    max_value = np.sum(pixels, axis=0) // len(pixels)

    painters = [SquarePainter(), TreePainter(), KochPainter()]

    fractals_cnt = len(painters)
    fractal_num = max_value[0] % fractals_cnt

    painter = painters[fractal_num]
    logger.info("Chosen painter: {}".format(painter))
    painter.turtle.goto(width//2, height // 2)
    painter.fractal_elements(grey)
    pixel_values = painter.values

    # print(len(pixel_values))

    random = F5Random(password)
    permutation = Permutation(pixel_values, random)
    print(permutation.shuffled)

    key1 = bytes(permutation.shuffled[:key_size])
    #print(key1, len(key1))
    return key1


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    print(generate_key("images/lena.png", "Adelina", 16))
    # turtle.bgpic("images/lena.png")
    # turtle.bye()
    input()

# input_image = Imag
# e.open("images/i1.jpg")

# image_width, image_height = input_image.size
# print('%d x %d' % (image_width, image_height))

# # convert image to gray scale
# image_grey = input_image.convert('LA')

# #pixel_values = []
# #tur = turtle.Turtle()
# #screen = turtle.Screen()
# #screen.screensize(image_width, image_height)
# #tur.penup()
# #tur.goto(image_width // 2, image_height // 2)
# #tur.pendown()

# # pixel_values_1 = set([5, 76, 118, 4, 6, 120, 79, 130, 2, 61, 127, 3, 19, 13, 28, 160, 137, 175, 18, 157, 169, 62, 173, 149,
# #                 154, 166, 171, 168, 156, 80, 20, 152, 129, 16, 146, 25, 141, 176, 21, 163, 180, 7, 0, 177, 8, 189, 188,
# #                 1, 170, 190, 147, 165, 63, 119, 167, 140, 179, 191, 135, 22, 159, 9, 148, 74, 143, 187, 50, 186])

# all_pixels = list(image_grey.getdata())
# #print(all_pixels)
# max_value = numpy.sum(all_pixels, axis=0) // len(all_pixels)
# #print(max_value[0])
# fractals_cnt = 3
# fractal_num = max_value[0] % fractals_cnt
# #print(fractal_num)
# painter = painter.SquarePainter()
# painter.turtle.goto(image_width // 2, image_height // 2)
# painter.fractal_elements(image_grey)
# pixel_values = painter.values

# # здесь нужно будет вызы
# # вать функцию построения фрактала fractal_num
# #fractal_squares(tur, image_grey, pixel_values)
# # generate initial array
# #print(pixel_values)
# print(len(pixel_values))


# password = "Adelina"
# random = F5Random(password)
# permutation = Permutation(pixel_values, random)
# print(permutation.shuffled)

# key1 = bytes(permutation.shuffled[:16])
# print(key1)
# init_vector1 = bytes(permutation.shuffled[17:33])
# print(init_vector1)

# # ДАЛЬШЕ НЕ РАБОТАЕТ
# aes1 = AES.new(key1, AES.MODE_CBC, init_vector1)
# data = 'hello world'
# encd = aes1.encrypt(data)

# random2 = F5Random(password)
# permutation2 = Permutation(pixel_values, random)
# print(permutation2.shuffled)
# key2 = bytes(permutation2.shuffled[:16])
# print(key2)
# init_vector2 = bytes(permutation2.shuffled[17:33])
# print(init_vector2)

# aes2 = AES.new(key2, AES.MODE_CBC, init_vector2)
# decd = aes2.decrypt(encd)
# print(decd)
