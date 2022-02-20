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
        self.polygon = self._center_polygon(polygon)


    def is_within_polygon(self, xy):
        if not self.boundary_box.is_within_boundary_box(xy):
            return False
        else:
            self.point_in_polygon()

    def point_in_polygon(self, xy):
        """
        Raycasting Algorithm to find out whether a point is in a given polygon.
        Performs the even-odd-rule Algorithm to find out whether a point is in a given polygon.
        This runs in O(n) where n is the number of edges of the polygon.
         *
        :param polygon: an array representation of the polygon where polygon[i][0] is the x Value of the i-th point and polygon[i][1] is the y Value.
        :param point:   an array representation of the point where point[0] is its x Value and point[1] is its y Value
        :return: whether the point is in the polygon (not on the edge, just turn < into <= and > into >= for that)
        """

        # A point is in a polygon if a line from the point to infinity crosses the polygon an odd number of times
        odd = False
        # For each edge (In this case for each point of the polygon and the previous one)
        i = 0
        j = len(self.polygon) - 1
        while i < len(self.polygon) - 1:
            i = i + 1
            # If a line from the point into infinity crosses this edge
            # One point needs to be above, one below our y coordinate
            # ...and the edge doesn't cross our Y corrdinate before our x coordinate (but between our x coordinate and infinity)

            if (((self.polygon[i][1] > xy[1]) != (self.polygon[j][1] > xy[1])) and (xy[0] < (
                    (self.polygon[j][0] - self.polygon[i][0]) * (xy[1] - self.polygon[i][1]) / (self.polygon[j][1] - self.polygon[i][1])) +
                                                                                self.polygon[i][0])):
                # Invert odd
                odd = not odd
            j = i
        # If the number of crossings was odd, the point is in the polygon
        return odd

    # draws a given polygon. If none is given, it will draw whatever is in the instance variable
    def _draw_polygon(self, polygon=None):
        dimensions = tuple(x + 10 for x in self.boundary_box.get_dimensions())  # expand the frame a bit
        image = Image.new("RGB", dimensions, (255, 255, 255))
        drawing = ImageDraw.Draw(image)
        drawing.ellipse((1, 1, 4, 8), fill=(22, 22, 250))
        color = (150, 22, 56)
        if polygon is None:
            drawing.line(self.polygon, color, width=5)

        else:
            drawing.line(polygon, color, width=5)
        image.show()

    def draw_polygon_with_boundary_box(self):
        pass

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

    def __getitem__(self, index):
        """
        :param index: int
        :return: point as tuple (x,y) at index
        """
        return self.polygon[item]

class BoundaryBox():
    # you could just use the "getbox()" method
    _coords = None
    _dimensions = None

    def __init__(self, polygon):
        """
        Creates a boundary box for any polygon given. Polygon needn't be centered.
        :param polygon: list of tuples [(x1,y1),(x2,y2),(x3,y3),...,(x1,y1)]
        """
        self.create_boundary_box(polygon)

    def create_boundary_box(self, polygon):

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

        self._coords = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
        delta_x = max_x - min_x
        delta_y = max_y - min_y
        self._dimensions = (delta_x, delta_y)

    def is_within_boundary_box(self, xy):
        min_x = self.get_min_x()
        min_y = self.get_min_y()
        max_x = self.get_max_x()
        max_y = self.get_max_y()
        if xy[0] <= min_x or xy[1] <= min_y or xy[0] >= max_x or xy[1] >= max_y:
            return False
        return True

    def get_boundary_box(self) -> list:
        return self._coords

    def get_dimensions(self):
        return self._dimensions

    def get_min_x(self):
        return self._coords[0][0]

    def get_min_y(self):
        return self._coords[0][1]

    def get_max_x(self):
        return self._coords[1][0]

    def get_max_y(self):
        return self._coords[2][1]

if __name__ == '__main__':
    polyg_1 = [(3858, 955), (3858, 961), (3865, 970), (3898, 972), (4045, 963), (4076, 972), (4130, 967), (4154, 974),
               (3858, 955)]
    polygon = Polygon(polyg_1)
    print("min_x: " + str(polygon.boundary_box.get_min_x()))
    print("min_y: " + str(polygon.boundary_box.get_min_y()))

    print(polygon.polygon)

    coord_inside = (20,14)
    is_within = polygon.is_within_polygon(coord_inside)
    print("This should return true: " + str(is_within)) # should return true
    coord_outside = (1000,655)
    is_outside = polygon.is_within_polygon(coord_outside)
    print("This should return true: " + str(is_outside)) # should return false


    polygon._draw_polygon(polygon.polygon)
    # polygon._draw_polygon(polygon._center_polygon(polygon.boundary_box.get_boundary_box()))


