#!/usr/bin/env python
#import PIL

from PIL import Image
#from past.builtins import raw_input

from jpeg_encoder import JpegEncoder
import sys
import os
from jpeg_extract import JpegExtract
from io import StringIO
import optparse
import logging

from pathlib import Path

from datetime import datetime

logger = logging.getLogger(__name__)
# parser = optparse.OptionParser(usage="Usage: %prog [options] [args]")
# group = optparse.OptionGroup(parser, 'Jpeg f5 steganography encoder and decoder')

# group.add_option('-t', '--type', type='string', default='e',
#         help='e for encode or x for decode')
# group.add_option('-i', '--image', type='string', help='input image')
# group.add_option('-d', '--data', type='string', help='data to be embeded, only for encode')
# group.add_option('-o', '--output', type='string', help='output image name, only for encode')
# group.add_option('-p', '--password', type='string', default='abc123',
#         help='password')
# group.add_option('-c', '--comment', type='string', default='written by fengji',
#         help='comment to put in the image, only for encode')

# parser.add_option_group(group)
# parser.add_option('-q', '--quiet', action='store_true')
# parser.add_option('-v', '--verbose', action='store_true')

# options, args = parser.parse_args()
def create_output_path(input_path):
    input_path = Path(input_path)
    name = input_path.stem
    datetime_format = "%Y-%m-%d_%H-%M-%S"
    time = datetime.now().strftime(datetime_format)
    new_name = "{0}_{1}{2}".format(name, time, input_path.suffix)
    new_path = (input_path.parent / new_name).as_posix()
    return new_path

def embed_into_image(path_to_image, data, password):
    image = Image.open(path_to_image)
    output_path = create_output_path(path_to_image)
    logger.info("Image with key %s" % output_path)
    with open(output_path, "wb") as output:
        encoder = JpegEncoder(image, 80, output, comment=None)
        encoder.compress(data, password)
    image.close()

def extract_from_image(path_to_image, password):
    logger.info("extract %s %s" % (path_to_image, password))
    output = StringIO()
    with open(path_to_image, 'rb') as image:
        decoder = JpegExtract(output, password)
        image_readed = image.read()
        logger.info("extraced image len %d" % len(image_readed))
        decoder.extract(image_readed)
        result = output.getvalue()
    return result

if __name__ == "__main__":
    path = "write down the path"  
    data = "Hello world"
    password = "12345"
    embed_into_image(path, data, password)

    output_path = "output.png"
    print(extract_from_image(output_path, password))

# if __name__ == '__main__':
#     logging.basicConfig(format='%(asctime)-15s [%(name)-9s] %(message)s', 
#             level=options.quiet and logging.ERROR
#                 or options.verbose and logging.DEBUG or logging.INFO)

#     if options.image and os.path.isfile(options.image):
#         if options.type == 'e' and options.data:
#             image = Image.open(options.image)
#             data = options.data

#             if not data:
#                 print('there\'s no data to embed')
#                 sys.exit(0)

#             if not options.output:
#                 print ('you didn\'t specify the output jpeg file, if will be default output.jpg')
#                 options.output = 'output.jpg'

#             elif os.path.exists(options.output) and os.path.isfile(options.output):
#                 print ('the output file exists, do you really want to override it?')
#                 answer = raw_input('y/n: ')
#                 if answer != 'y':
#                     print ('exit')
#                     sys.exit(0)
#             output = open(options.output, 'wb')

#             encoder = JpegEncoder(image, 80, output, options.comment)
#             encoder.compress(data, options.password)
#             output.close()

#         if options.type == 'x':
#             if options.output:
#                 output = open(options.output, 'wb')
#             else:
#                 output = StringIO()
#             image = open(options.image, 'rb')
#             JpegExtract(output, options.password).extract(image.read())

#             if not options.output:
#                 print (output.getvalue())

#             image.close()
#             output.close()
#     else:
#         print ('you didn\'t give a image or the image is not there')
#         parser.print_help()
