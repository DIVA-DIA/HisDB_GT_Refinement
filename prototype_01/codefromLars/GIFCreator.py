# This file should provide GIF color palettes, store the information of what the different colors mean, take images as
# ndarrays and output them as GIF.
import os

import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
import cv2 as cv2
from itertools import combinations_with_replacement


class ColorPalette():
    # [0,0,0], [0, 0, 120], [0, 120, 0], [120, 0, 0] can be combined, thus all their combination (e.g [120, 120, 120]
    # are reserved.
    # [240,240,240] is a boundary pixel
    BACKGROUND = [0, 0, 0]
    MAINTEXT = [0, 0, 120]
    DECORATION = [0, 120, 0]
    COMMENT = [120, 0, 0]
    # TODO: can a boundary pixel be a comment, decoration, comment? If so, must be changed...
    BOUNDARYPIXEL = [240, 0, 0]

    def __init__(self):
        self.two_D_palette = self.init_palette()
        self.one_D_palette = self.two_d_palette_to_one_d(self.two_D_palette)

    # to 2-dimensional = [[R,G,B], [R,G,B], ... ]] with 27 levels

    def init_palette(self):
        palette = [[x * 120, y * 120, z * 120] for x in range(3) for y in range(3) for z in range(3)]
        palette_256 = palette + (256 - len(palette)) * [[0, 0, 0]]
        return palette_256

    # 1-dimensional palette of length 768 [R, G, B, R, G, B, R, G, B ...]


    def two_d_palette_to_one_d(self, palette: list):
        np_array = np.array(palette)
        flattened = np_array.flatten()
        assert len(flattened) == 768
        return flattened

    # 1-dimensional palette of length 768 [R, G, B, R, G, B, R, G, B ...]

    @staticmethod
    def get_raw_palette(self, img: Image):
        return np.array(img.getpalette())

    # reshaped from one-dimensional to 2-dimensional = [[R,G,B], [R,G,B], ... ]]

    @staticmethod
    def get_reshaped_palette(self, img: Image):
            return self.get_raw_palette(self, img).reshape(-1, 3)

    # reduce palette to unique colors only. -> used to create GIF
    @staticmethod
    def get_unique_palette(self, img: Image):
        return np.unique(self.get_reshaped_palette(self, img), axis=0)


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



