# This class is supposed to help process the poligons given
# Given a polygon, it should create the bounding box.
# Given a point, it should be able to check for whether or not it's within the polygon.
# Important: Polygons must be closed path (first and last point must be the same)
from PIL import Image, ImageDraw

# TODO: make every manipulation manipulate polygon and don't create copies of polygon such as centered_polygon. Just center it directly.

class Polygon():

    def __init__(self, polygon):
        """
        Polygon given must be closed.
        :param polygon: List of tuples [(x1,y1),(x2,y2),(x3,y3),...,(x1,y1)]
        """
        self.polygon = polygon
        self.boundary_box = BoundaryBox(polygon)

    def is_within_boundary_box(self, xy):
        pass

    def is_within_polygon(self):
        pass

    # draws a given polygon. If none is given, it will draw whatever is in the instance variable
    def _draw_polygon(self, polygon=None):
        dimensions = tuple(x + 10 for x in self.boundary_box.get_dimensions())  # expand the frame a bit
        image = Image.new("RGB", dimensions, (255, 255, 255))
        drawing = ImageDraw.Draw(image)
        color = (150, 22, 56)
        if polygon is None:
            drawing.line(self.polygon, color, width=5)
        else:
            drawing.line(polygon, color, width=5)
        image.show()

    def draw_polygon_with_boundary_box(self):

    # helper-method to make the coordinates fit the image
    def _center_polygon(self, polygon = None):
        min_x = self.boundary_box.get_min_x()
        min_y = self.boundary_box.get_min_y()
        centered_polygon = []
        if polygon is None:
            for coord in self.polygon:
                centered_polygon.append((coord[0] - min_x, coord[1] - min_y))
        else:
            for coord in polygon:
                centered_polygon.append((coord[0] - min_x, coord[1] - min_y))
        return centered_polygon


class BoundaryBox():
    _coords = None
    _dimensions = None

    def __init__(self, polygon):
        self.create_boundary_box(polygon)

    def create_boundary_box(self, polygon):
        min_x = 10000000
        max_x = 0
        min_y = 10000000
        max_y = 0
        for coord in polygon:
            if coord[0] < min_x:
                min_x = coord[0]
            elif coord[0] > max_x:
                max_x = coord[0]
            if coord[1] < min_y:
                min_y = coord[1]
            elif coord[1] > max_y:
                max_y = coord[1]

        assert min_x and max_x and min_y and max_y is not None
        assert (min_x <= max_x) and (min_y <= max_y)

        self._coords = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
        delta_x = max_x - min_x
        delta_y = max_y - min_y
        self._dimensions = (delta_x, delta_y)

    def get_boundary_box(self) -> list:
        return self._coords

    def get_dimensions(self):
        return self._dimensions

    def get_min_x(self):
        return self._coords[0][0]

    def get_min_y(self):
        return self._coords[1][1]


if __name__ == '__main__':
    polyg_1 = [(3858, 955), (3858, 961), (3865, 970), (3898, 972), (4045, 963), (4076, 972), (4130, 967), (4154, 974),
               (3858, 955)]
    polygon = Polygon(polyg_1)
    print("min_x: " + str(polygon.boundary_box.get_min_x()))
    print("min_y: " + str(polygon.boundary_box.get_min_y()))

    print(polygon._center_polygon())

    polygon._draw_polygon(polygon._center_polygon())
    polygon._draw_polygon(polygon._center_polygon(polygon.boundary_box.get_boundary_box()))
