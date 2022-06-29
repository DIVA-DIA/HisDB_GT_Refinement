# represents all the vector objects. they must be scalable.
import operator
from typing import Tuple, List

from PIL.ImageDraw import ImageDraw

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.ImageDimension import ImageDimension
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.Interfaces.Scalable import Scalable


# It could make sense to use the ImagePath.Path object -> however, the functionalities are limited and it implies a certain risk
# of not knowin what it does
# There's a design choice between has-a and is-a in my case. I could say every geometric object is a polygon.
# -> BoundingBox extends polygon, XRegion extends BoundingBox
# OR
# I say that a BoundingBox has a Polygon. Every XRegion has Polygon and a Bounding box.
# Let's think from the clients perspective. If XRegion is a Polygon, that would mean that calling a Polygon would always
# be safe. Calling the draw method of Polygon wouldn't result in drawing an the bounding box unwantadly. However, when
# calling the draw method of an XRegion, it would draw the the x-region, the bounding-box and the polygon (assuming I call
# the super() method).
# Now let's say I want to implement a mask method. If there's a is-a relation ship, I can still choose to just return
# the masked area of the bounding_box, the polygon, or the x-region. However, I could also combine them, if I know that
# they must always be combined in the same way. However, it makes more sense to combine these polygons in a different class
# called the "Masker".
# What speaks against the implementation of is-a, is the fact that it's not transparent flexible. If you think about a car
# a maserati is a car, but it's engine is not a car. The car has an engine. You could implement it over a is-a relationship
# but this just doesn't make any sense. Especially because an engine couldn't exist without a car or a more practical example:
# if you create a list of engines, it's also a list of engine. If you iterate over that list and tell that engines to accelerate
# to change tires it could do that. But it wouldn't make any sense.
# Make has-a relationship!

class VectorObject(Scalable):

    def __init__(self, xy: List[Tuple]):
        self.xy = xy

    # TODO: Implement a BoundingBox method which creates a boundingbox for every Vector

    def draw(self, drawer: ImageDraw, outline=(255,255,255), fill = None):
        drawer.polygon(xy=self.xy, outline=outline,fill=fill)

    def resize(self, scale_factor: Tuple[float,float]):
        self.xy = [tuple(map(operator.truediv, t, scale_factor)) for t in self.xy]
        self.xy = [tuple(map(round, t)) for t in self.xy]

    def crop(self, source_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        difference = source_dim.difference(target_dim)
        if not cut_left:
            difference = (0, difference[1])
        self.xy = self._find_and_scale_points(difference)

    def _find_and_scale_points(self, difference: Tuple[float, float]):
        return [tuple(map(operator.sub, t, difference)) for t in self.xy]



class Polygon(VectorObject):

    def __init__(self, polygon: List[Tuple]):
        """
        Polygon given must be closed.
        :param polygon: List of tuples [(x1,y1),(x2,y2),(x3,y3),...,(x1,y1)]
        """
        super().__init__(polygon)


    # to allow flawless iteration over all coordinates of the polygon
    def __getitem__(self, index):
        """
        :param index: int
        :return: point as tuple (x,y) at index
        """
        return self.xy[index]

    # you intuitively solved the Liskov Substitution Problem:
    # https://stackoverflow.com/questions/6034662/python-method-overriding-does-signature-matter
    def draw(self, drawer: ImageDraw, outline=(255, 125, 0), fill=None):
        drawer.polygon(self.xy, outline=outline, fill=fill)


# TODO there should be a box  and a tetragon object, the tetragon object inherits from polygon
#   It should run test on the coordinates and ensure that their sorted (left top corner, right top corner,
#   right bottom...)

class Box(VectorObject):

    # box is not a rectangle, but a polygon with four coordinates

    def __init__(self, xy: List[Tuple]):
        super().__init__(xy)
        assert len(xy) == 4

    def get_min_x(self):
        min_x = float("inf")
        for coord in self.xy:
            if coord[0] < min_x:
                min_x = int(coord[0])
        return min_x

    def get_min_y(self):
        min_y = float("inf")
        for coord in self.xy:
            if coord[1] < min_y:
                min_y = int(coord[1])
        return min_y

    def get_max_x(self):
        max_x = 0
        for coord in self.xy:
            if coord[0] > max_x:
                max_x = int(coord[0])
        return max_x

    def get_max_y(self):
        max_y = 0
        for coord in self.xy:
            if coord[1] > max_y:
                max_y = int(coord[1])
        return max_y


class Line(VectorObject):

    # TODO: make line list of 2+ coordinates. check for segement intersection
    # Segment intersection
    # def ccw(A,B,C):
    #     return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)
    #
    # # Return true if line segments AB and CD intersect
    # def intersect(A,B,C,D):
    #     return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

    def __init__(self, xy: List[Tuple]):
        super().__init__(xy)
        self.xy.sort(key=lambda x: x[0])
        assert self.xy[0][0] < self.xy[1][0]
        assert len(xy) == 2

    def get_min_x_coord(self):
        return self.xy[0]

    def get_max_x_coord(self):
        return self.xy[1]

    def __getitem__(self, index):
        return self.xy[index]


class BoundingBox(Box):

    def __init__(self, polygon):
        super().__init__(self.getbbox(polygon=polygon))

    def getbbox(self, polygon):
        min_x = float("inf")
        max_x = 0
        min_y = float("inf")
        max_y = 0
        for coord in polygon:
            if coord[0] < min_x:
                min_x = int(coord[0])
            elif coord[0] > max_x:
                max_x = int(coord[0])
            if coord[1] < min_y:
                min_y = int(coord[1])
            elif coord[1] > max_y:
                max_y = int(coord[1])
        assert min_x and max_x and min_y and max_y is not None
        assert (min_x <= max_x) and (min_y <= max_y)
        return [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

    def draw(self, drawer: ImageDraw, outline=(0, 125, 255), fill=None):
        drawer.rectangle(xy=[(self.get_min_x(), self.get_min_y()), (self.get_max_x(), self.get_max_y())],
                         outline=outline, fill=fill)




# if __name__ == '__main__':$
#       # Shows that polygon can draw lines.
#     img = Image.new(mode="RGB", size=(50,50),color=0)
#
#     line = [(10,10),(40,40)]
#
#     drawer = ImageDraw.Draw(img)
#     drawer.polygon(xy=line)
#
#     img.show(title="hello")

