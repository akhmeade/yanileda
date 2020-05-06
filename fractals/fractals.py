import logging
import numpy as np
from PIL import Image
from f5steganography.jpeg_encoder import JpegEncoder as JpegEncoder
import hashlib
import os
import random as r
#from painter import Painter
from .painter import SquarePainter
from .painter import TreePainter
from .painter import KochPainter
from .painter import LSystemPainter

logger = logging.getLogger(__name__)

def generate_random_string(length):
    random_string = ''
    random_str_seq = "AopqrsBC@#$%^DEFabcGHIJghijKwxyzLMNdefOPQRS!&_+|*()TUVklmnWXYZ"
    for i in range(0, length):
        if i % length == 0 and i != 0:
            random_string += '-'
        random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
    return random_string

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] & (1 << shift)) >> shift

def xor(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def string_to_bin(s):
    return ''.join('{:08b}'.format(ord(c)) for c in s)


def bin_to_string(b):
    n = int(b, 2)
    return ''.join(chr(int(b[i: i + 8], 2)) for i in range(0, len(b), 8))


def round_function(x, i, k):
    k = string_to_bin(k)
    x = string_to_bin(str(x))
    res = pow((int(x, 2) * int(k, 2)), i)
    res = bin(res)

    return bin_to_string(res)


def feistel_cypher(password, message):
    ciphertext = ""
    rounds_count = 3
    n = 8
    message = [message[i: i + n] for i in range(0, len(message), n)]
    last_block_size = len(message[len(message) - 1])
    if last_block_size < 8:
        for i in range(last_block_size, 8):
            message[len(message) - 1] += " "

    key = hashlib.sha256(password.encode('latin-1')).hexdigest()
    initial_key = key
    for block in message:
        L = [""] * (rounds_count + 1)
        R = [""] * (rounds_count + 1)
        L[0] = block[0:4]
        R[0] = block[4:8]
        for i in range(1, rounds_count + 1):
            L[i] = R[i - 1]
            if i == 1:
                round_key = initial_key
            else:
                round_key = hashlib.sha256((L[i] + initial_key).encode('latin-1')).hexdigest()
            R[i] = xor(L[i - 1], round_function(R[i - 1], i, round_key))
        ciphertext += (L[rounds_count] + R[rounds_count])
    return ciphertext


def generate_key(path_to_image, password, key_size):
    image = Image.open(path_to_image)
    width, height = image.size
    logger.info('%d x %d' % (width, height))
    grey = image.convert('LA')
    pixels = list(grey.getdata())
    max_value = np.sum(pixels, axis=0) // len(pixels)
    painters = [SquarePainter(), TreePainter(), KochPainter(),
                LSystemPainter(0), LSystemPainter(1), LSystemPainter(2),
                LSystemPainter(3),LSystemPainter(4), LSystemPainter(5),
                LSystemPainter(6)]
    fractals_cnt = len(painters)
    fractal_num = max_value[0] % fractals_cnt
    print ("fractal num = ", str(fractal_num))
    painter = painters[fractal_num]
    logger.info("Chosen painter: {}".format(painter))
    painter.turtle.goto(width//2, height // 2)
    painter.fractal_elements(grey)
    pixel_values = painter.values
    result_vector = feistel_cypher(password, bytes(pixel_values).decode('latin-1'))
    key = bytes(result_vector[:key_size].encode('latin-1'))
    return key

def generate_initial_vector (path_to_image, password):
    image = Image.open(path_to_image)
    width, height = image.size
    logger.info('%d x %d' % (width, height))
    grey = image.convert('LA')
    pixels = list(grey.getdata())
    max_value = np.sum(pixels, axis=0) // len(pixels)
    painters = [SquarePainter(), TreePainter(), KochPainter(), LSystemPainter(0),
                LSystemPainter(1), LSystemPainter(2), LSystemPainter(3),
                LSystemPainter(4), LSystemPainter(5), LSystemPainter(6)]
    fractals_cnt = len(painters)
    fractal_num = max_value[0] % fractals_cnt
    painter = painters[fractal_num]
    logger.info("Chosen painter: {}".format(painter))
    painter.turtle.goto(width//2, height // 2)
    painter.fractal_elements(grey)
    pixel_values = painter.values
    result_vector = feistel_cypher(password, bytes(pixel_values).decode('latin-1'))
    return result_vector

def generate_result_key(result_vector, key_size):
    key = bytes(result_vector[:key_size].encode('latin-1'))
    binary_key = [access_bit(key, i) for i in range(len(key) * 8)]
    return binary_key

def write_key_to_file(filename, key):
    file1 = open(filename, "w")
    file1.write(''.join(str(e) for e in key))
    file1.close()


#password = generate_random_string(10)
#cnt = 0
#print(password)
#for filename in os.listdir("test_images"):
  #  file_len = open("text_files/fractals_length.txt", "w")
  #  cnt = cnt + 1
  #  txt_filename = "text_files/fractal_keys/fractal_keys_" + str(cnt)
   # init_vector = generate_initial_vector("test_images/" + filename, password)
   # print(filename, len(init_vector))
   # file_len.writelines(filename+";"+str(len(init_vector)))
  #  res_key_128 = generate_result_key(init_vector,16)
   # write_key_to_file(txt_filename+"_128.txt", res_key_128)
   # res_key_256 = generate_result_key(init_vector,32)
  #  write_key_to_file(txt_filename + "_256.txt", res_key_256)
  #  res_key_512 = generate_result_key(init_vector,64)
  #  write_key_to_file(txt_filename + "_512.txt", res_key_512)
   # res_key_1024 = generate_result_key(init_vector,128)
  #  write_key_to_file(txt_filename + "_1024.txt", res_key_1024)
   # print(filename + "done ")




if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    print(generate_key("images/lena.png", "Adelina", 16))
    # turtle.bgpic("images/lena.png")
    # turtle.bye()
    input()





