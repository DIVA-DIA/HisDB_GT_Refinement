import numpy as np
from PIL import Image, ImageDraw


def create_color_palette(n_colors):
    # how many colors?
    segments = 2
    if (n_colors < 8): segments = 2
    elif (n_colors <= 27): segments = 3
    elif (n_colors <= 64): segments = 4
    elif (n_colors <= 125): segments = 5
    elif (n_colors <= 216): segments = 6
    elif (n_colors <= 343): segments = 7
    elif (n_colors <= 512): segments = 8
    elif (n_colors <= 729): segments = 9
    elif (n_colors <= 1000): segments = 10
    else: segments = 11
    my_range = range(segments)
    interval = int(240 / (segments - 1))
    unsorted = [tuple([x * interval, y * interval, z * interval]) for x in my_range for y in my_range for z in my_range]
    return sorted(unsorted, key=lambda tup: (tup[0],tup[1],tup[2]), reverse=True)


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
    def get_raw_palette(self, img: Image):
        return np.array(img.getpalette())

    # reshaped from one-dimensional to 2-dimensional = [[R,G,B], [R,G,B], ... ]]
    def get_reshaped_palette(self, img: Image):
            return self.get_raw_palette(img).reshape(-1, 3)

    # reduce palette to unique colors only. -> used to create GIF
    def get_unique_palette(self, img: Image):
        return np.unique(self.get_reshaped_palette(img), axis=0)

if __name__ == '__main__':
    colorpalette = ColorPalette()
    colors = create_color_palette(n_colors=1000)
    print(colors)
    print(str(len(colors)))


