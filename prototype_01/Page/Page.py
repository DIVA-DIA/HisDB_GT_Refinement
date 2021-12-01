# This class stores the coordinates of the points given in the xml-file
# The xml file is structured as follows:
#   Textregion (Comments if the id = region_XX, Maintext if the id = region_texline)
#       Coords xxxx,yyyy xxxx,yyyy xxxx,yyyy xxxx,yyyy (Äusserste Koordinaten)
#           Textline id = (Comments if the id = comment_XX, Maintext if the id = region_texline)
#               Coords xxxx,yyyy xxxx,yyyy xxxx,yyyy ...
#               Baseline xxxx, yyyy xxxx,yyyy (Immer nur zwei)
#   Graphregion
#       Coords xxxx,yyyy xxxx,yyyy xxxx,yyyy ...

def parse_to_list(points):
    """
    :param points: string of format: "xxxx,yyyy xxxx,yyyy, ..."
    :return: list
    """
    # TODO: du könntest hier darüber schreiben, wie string concatenation am effizientesten funktioniert

    list_of_coords = []  # stores strings of coordinates in the form of "xxxx,yyyy"
    index = 0
    x, y = []
    coord = ""
    for letter in points:
        if letter.isspace():
            list_of_coords.append(coord)
            coord = ""
            index += 1
        coord = coord + letter
    return list_of_coords

class Page():
    width, height = None

    comments = []
    main_text = []
    graph_region = []


class region():
    id, custom = None

    def __init__(self, id, custom):
        """
        :param id: string, denotes the id
        :param custom: string, denotes something I don't understand
        """
        self.id = id
        self.custom = custom

class text_region(region):

    def __init__(self, id, custom):
        super.__init__(id, custom)


class graph_region(region):
    points = [()]
    def __init__(self, id, custom, points):
        super.__init__(id, custom)

    def parse_to_list(self):
        pass


