#coding: utf-8

from PIL import Image

from .jpeg_encoder import JpegEncoder
import sys
import os
from .jpeg_extract import JpegExtract
from io import StringIO
import optparse
import logging

from pathlib import Path

from datetime import datetime

logger = logging.getLogger(__name__)


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
