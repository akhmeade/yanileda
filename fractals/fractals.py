import turtle
import numpy
from PIL import Image
import crypto
from util import PythonF5Random as F5Random
from util import Permutation


def append_unique_values(image_gray, values, xcoor, ycoor):
    image_width, image_height = input_image.size
    if xcoor < image_width and ycoor < image_height:
        nval = image_gray.getpixel((xcoor, ycoor))[0]
        if nval not in values:
            values.append(nval)
        return
    return


def draw_square(tur, image_gray, values):
    tur.forward(50)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())
    tur.left(90)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())
    tur.forward(50)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())
    tur.left(90)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())
    tur.forward(50)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())
    tur.left(90)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())
    tur.forward(50)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())
    tur.left(90)
    append_unique_values(image_gray, values, tur.xcor(), tur.ycor())


def fractal_squares(tur, image_grey, values):
    tur.color('green')
    for i in range(60):
        draw_square(tur, image_grey, values)
        tur.left(i)


def tree(length, n):
    if length < (length / n):
        return
    turtle.forward(length)
    turtle.left(45)
    tree(length * 0.5, length / n)
    turtle.left(20)
    tree(length * 0.5, length / n)
    turtle.right(75)
    tree(length * 0.5, length / n)
    turtle.right(20)
    tree(length * 0.5, length / n)
    turtle.left(30)
    turtle.backward(length)
    return


def fractal_tree():
    turtle.left(90)
    turtle.backward(30)
    tree(200, 4)


def Recursive_Koch(length, depth):
    if depth == 0:
        turtle.forward(length)
        return
    Recursive_Koch(length, depth - 1)
    turtle.right(60)
    Recursive_Koch(length, depth - 1)
    Recursive_Koch(120, 0)
    Recursive_Koch(length, depth - 1)
    turtle.right(60)
    Recursive_Koch(length, depth - 1)


def fractsl_koch():
    turtle.left(90)
    turtle.backward(300)
    Recursive_Koch(10, 6)


input_image = Image.open("images/i1.jpg")
image_width, image_height = input_image.size
print('%d x %d' % (image_width, image_height))

# convert image to gray scale
image_grey = input_image.convert('LA')

pixel_values = []
tur = turtle.Turtle()
screen = turtle.Screen()
screen.screensize(image_width, image_height)
tur.penup()
tur.goto(image_width // 2, image_height // 2)
tur.pendown()

pixel_values = [5, 76, 118, 4, 6, 120, 79, 130, 2, 61, 127, 3, 19, 13, 28, 160, 137, 175, 18, 157, 169, 62, 173, 149,
                154, 166, 171, 168, 156, 80, 20, 152, 129, 16, 146, 25, 141, 176, 21, 163, 180, 7, 0, 177, 8, 189, 188,
                1, 170, 190, 147, 165, 63, 119, 167, 140, 179, 191, 135, 22, 159, 9, 148, 74, 143, 187, 50, 186]

all_pixels = list(image_grey.getdata())
#print(all_pixels)
max_value = numpy.sum(all_pixels, axis=0) // len(all_pixels)
#print(max_value[0])
fractals_cnt = 3
fractal_num = max_value[0] % fractals_cnt
#print(fractal_num)

# здесь нужно будет вызывать функцию построения фрактала fractal_num
#fractal_squares(tur, image_grey, pixel_values)
# generate initial array
print(pixel_values)

password = "Adelina123"
random = F5Random(password)
permutation = Permutation(pixel_values, random)
print(permutation.shuffled)

key1 = bytes(permutation.shuffled[:16])
print(key1)
init_vector1 = bytes(permutation.shuffled[17:33])
print(init_vector1)

# ДАЛЬШЕ НЕ РАБОТАЕТ
aes1 = AES.new(key1, AES.MODE_CBC, init_vector1)
data = 'hello world 1234'
encd = aes1.encrypt(data)

random2 = F5Random(password)
permutation2 = Permutation(pixel_values, random)
print(permutation2.shuffled)
key2 = bytes(permutation2.shuffled[:16])
print(key2)
init_vector2 = bytes(permutation2.shuffled[17:33])
print(init_vector2)

aes2 = AES.new(key2, AES.MODE_CBC, init_vector2)
decd = aes2.decrypt(encd)
print(decd)
