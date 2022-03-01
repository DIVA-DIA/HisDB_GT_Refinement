# This file should provide GIF color palettes, store the information of what the different colors mean, take images as
# ndarrays and output them as GIF.
import os

import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
import cv2 as cv2
from itertools import combinations_with_replacement

# TODO Separate the Class ColorPalette form GIFCreator


    # TODO: given an original color-palette (1D), replace every pixel of an image with the corresponding color of the
    #  target color-palette (1D) and store it as gif.
class GIFCreator():

    # somehow the color_palette get's only replaced partially...
    def create_GIF(self,path_in: Path, path_out: str, color_palette: ColorPalette):
        # load the image as rgb array
        rgb = Image.open(path_in).convert("RGB")
        rgb.show(title="Original image (before conversion)")
        img_as_array = np.asarray(rgb)
        # convert the image to an index based image
        pil_image = Image.fromarray(img_as_array).convert('P', palette=Image.ADAPTIVE, colors=256)
        palette_before = color_palette.get_raw_palette(color_palette, pil_image)
        colormap = color_palette.one_D_palette # My custom palette
        pil_image.save(path_out, save_all=True, format="GIF",
                       palette=colormap.tobytes(), duration=100, loop=0)
        # to illustrate the end-result
        rgb = Image.open(path_out).convert("RGB")
        img_as_array = np.asarray(rgb)
        pil_image = Image.fromarray(img_as_array).convert('P', palette=Image.ADAPTIVE, colors=256)
        palette_after = color_palette.get_raw_palette(color_palette, pil_image)
        print("This is original unique palette: " + str(palette_before))
        print("This is new unique palette: " + str(palette_after))
        print("Are the equal?")
        rgb.show("This is the GIF you created.")



if __name__ == '__main__':
    path_in = Path("../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0098v_max.png")
    path_out = "../Output/GIF/FirstGIF/first_GIF_02.gif"
    # #img = Image.open(fp=path, mode='RGB')
    # # img_asarray = np.asarray(img)
    #image = Image.open(path_in).convert('P', palette=Image.ADAPTIVE, colors=256)
    #image.show()
    color_palette = ColorPalette()
    # raw_palette = color_palette.get_raw_palette(color_palette, img=image)
    # reshaped_palette = color_palette.get_reshaped_palette(color_palette, img=image)
    # unique_palette = color_palette.get_unique_palette(color_palette, img=image)
    # print(raw_palette)
    # print(reshaped_palette.tobytes())
    # print(unique_palette.tobytes())


    gif_creator = GIFCreator()
    gif_creator.create_GIF(path_in, path_out, color_palette)



