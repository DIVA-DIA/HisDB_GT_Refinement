# This class serves the purpose of drawing lines on new instance pillow Image

from PIL import Image, ImageDraw
from typing import Type

COLOR = "red"


class Drawer():
    image = None

    def __init__(self, width: int, height: int):
        self.image = Image.new("RGB", (width, height))

    def draw_points(self, array: list):
        """
        Draws lines between all the points passed in the numpy array.
        :param array: numpy array of the sorts ((x1,y1),(x2,y2),...)
        :return:
        """
        print(array)
        index1 = 0
        index2 = 1
        length = len(array)
        while (index2 < length):
            self._draw_line(array[index1], array[index2], ImageDraw.Draw(self.image))
            index1 += 1
            index2 += 1

    def _draw_line(self, p1: tuple, p2: tuple, drawer: ImageDraw):
        """
        Draws a line between point 1 (p1) and point 2 (p2)
        :param p1: 2-tuple (x1,y1)
        :param p2: 2-tuple (x2,y2)$
        :param drawer: ImageDraw object to draw the line
        :return:
        """
        drawer.line((p1,p2), fill=COLOR, width=1)

    def draw_polygon(self, polygon):
        drawer = ImageDraw.Draw(self.image)
        drawer.polygon(polygon, fill =(255, 128,0), outline =(255, 128,0))


    def display_drawing(self):
        self.image.show()
