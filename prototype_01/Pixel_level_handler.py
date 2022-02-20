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


# TODO: Als erstes werde ich ein pixel-based image lesen und eine geschickte Datenstruktur entwickeln.
# TODO: Einen Algorithmus schreiben, der durch jedes Pixel im Bild durchgeht, es kategorisiert und überprüft, ob es in einem Polygon ist.


def read_pixel_level_gt(image_path: Path):
    # show original image and get unique pixels
    rgb = Image.open(image_path).convert("RGB")
    img_asarray = asarray(rgb)
    img = Image.fromarray(img_asarray, "RGB")
    img.show()

    #print("Unique pixel after processing: \n" + str(get_unique_pixels(img_asarray)))

    # illustrate all the different colors
    img_asarray = replace_color(img_asarray, [0, 0, 1],[0, 0, 0]) # set background to black
    img_asarray = replace_color(img_asarray, [0, 0, 2], [122, 0, 0]) # set comments to dark red
    img_asarray = replace_color(img_asarray, [0, 0, 4], [0, 122, 0]) # set decorations to dark green
    img_asarray = replace_color(img_asarray, [0, 0, 8], [0, 0, 122])  # set main text body to dark blue
    img_asarray = replace_color(img_asarray, [0, 0, 6], [122, 122, 0])  # comments + decoration to dark yellow
    img_asarray = replace_color(img_asarray, [0, 0, 10], [122, 0, 122])  # set main text body + comments to dark pink
    img_asarray = replace_color(img_asarray, [0, 0, 12], [0, 122, 122])  # set main text body + decoration to dark Türkis
    # img_asarray = replace_color(img_asarray, [0, 0, 12], [122, 122, 122])  # set main text body + decoration + comment to grey -> doesn't make any sense because 0,0,12 is already used

    img_asarray = replace_color(img_asarray, [128, 0, 2], [255, 0, 0]) # set comments to bright red
    img_asarray = replace_color(img_asarray, [128, 0, 4], [0, 255, 0]) # set decorations to bright green
    img_asarray = replace_color(img_asarray, [128, 0, 8], [0, 0, 255])  # set main text body to bright blue
    img_asarray = replace_color(img_asarray, [128, 0, 6], [255, 255, 0])  # comments + decoration to bright yellow
    img_asarray = replace_color(img_asarray, [128, 0, 10], [255, 0, 255])  # set main text body + comments to bright pink
    img_asarray = replace_color(img_asarray, [128, 0, 12], [0, 255, 255])  # set main text body + decoration to bright Türkis
    # img_asarray = replace_color(img_asarray, [128, 0, 12], [255, 255, 255])  # set main text body + decoration + comment to white -> doesn't make any sense because 128,0,12 is already used
    img = Image.fromarray(img_asarray, "RGB")
    img.save("Output/with_all_different_colors_02.png")
    img.show()
    print("Unique pixel after processing: \n" + str(get_unique_pixels(img_asarray)))

    print("Dimensions: " + str(img_asarray.ndim))
    print("Shape: " + str(img_asarray.shape))
    print("Array: " + str(img_asarray))
    print(rgb.getpixel((10, 23)))

    # works fine :)


def crop_image(img: Image):
    crop_area = (1500, 1500, 2000, 2000)
    cropped_img = img.crop(crop_area)
    cropped_img.show()
    cropped_img.save("Input/pixel_level_small.png")


def get_unique_pixels(img_asarray: np.ndarray):
    return np.unique(img_asarray.reshape(-1, img_asarray.shape[2]), axis=0)


def replace_color(img_asarray : np.ndarray, old_color : list, new_color : list):
    """
    Changes the color of a given pixel in an image to a given color
    :param img_asarray: RGB encoded image as array
    :param old_color: [R,G,B]
    :param new_color: [R,G,B]
    :return:
    """
    mask = np.all(img_asarray == old_color, axis=-1)
    img_asarray[mask] = new_color
    return img_asarray


if __name__ == '__main__':
    #pixel_level_gt = Path("Output/Resizing/resized02(pixel_based)_factor_by_4_minority_wins.jpg")
    pixel_level_gt = Path("../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    read_pixel_level_gt(pixel_level_gt)
