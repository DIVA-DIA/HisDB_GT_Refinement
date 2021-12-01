# 30. Nov. 21
# This class is supposed to read the png files that represent the pixel-level-gt
# According to the website: https://diuf.unifr.ch/main/hisdoc/icdar2017-hisdoc-layout-comp#6 the four classes are stored as:
#       RGB=0b00...1000=0x000008: main text body
#       RGB=0b00...0100=0x000004: decoration
#       RGB=0b00...0010=0x000002: comment
#       RGB=0b00...0001=0x000001: background (out of page)
#           --> These are all black colors. The difference can't be noticed by eye.
# Combinations of these are possible:
#       main text body+comment : 0b...1000 | 0b...0010 = 0b...1010 = 0x00000A
#       main text body+decoration : 0b...1000 | 0b...0100 = 0b...1100 = 0x00000C
#       comment +decoration : 0b...0010 | 0b...0100 = 0b...0110 = 0x000006
# Boundary pixels are represented as
# For the boundary pixel, we use the red RGB value:
#       RGB=0b10...0000=0x800000 : boundary pixel (to be combined with one of the classe, expect background)
# For example a boundary comment is represented as:
#       boundary+comment=0b10...0000|0b00...0010=0b10...0010=0x800002
#           --> The difference can't be noticed by eye
# Using the get_unique_pixels() method I found out that there are these combinations present in ...0055_0098_max.png
# [[  0   0   1]
#  [  0   0   2]
#  [  0   0   4]
#  [  0   0   6] -> decoration & comment
#  [  0   0   8]
#                -> appearantly there is no  main text body & comment in this picture
#  [  0   0  12] -> main text body & decoration
#  [128   0   2] -> boundary pixel & comment
#  [128   0   4] -> boundary pixel & decoration
#  [128   0   6] -> boundary pixel & comment & decoration
#  [128   0   8] -> boundary pixel & main text body
#                -> appearantly there is no boundary pixel & main text body & comment in this picture
#  [128   0  12]] -> boundary pixel & main-text-body & decoration

from pathlib import Path
from PIL import Image
from numpy import asarray
import numpy as np

# TODO: Als erstes werde ich ein pixel-base image lesen und eine geschickte Datenstruktur entwickeln.


def read_pixel_level_gt(image_path :Path):
    # store png as numpy array
    # go through the numpy array and store the different colors
    rgb = Image.open(image_path).convert("RGB")
    img_asarray = asarray(rgb)
    print(img_asarray.ndim)
    print(img_asarray.shape)



    # for height in img_asarray:
    #     for width in height:
    #         if width.any()
    #         else:
    #             unique_pixels.append(width)

    print(get_unique_pixels(img_asarray))

    print(rgb.getpixel((10,23)))


def get_unique_pixels(img_asarray : np.ndarray):
    return np.unique(img_asarray.reshape(-1, img_asarray.shape[2]), axis=0)






if __name__ == '__main__':
    pixel_level_gt = Path("../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    read_pixel_level_gt(pixel_level_gt)