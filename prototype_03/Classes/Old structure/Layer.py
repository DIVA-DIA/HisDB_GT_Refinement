# it makes sense to store the different information as layers that can be put together manually
# by instantiating a class of a given type the processing would automatically be made.
# Example: boundary boxes, resizing, ascender/descenders
class Layer:
    # functionalities:
    # store all xml polygons with their corresponding class
    # manipulate all polygons (resizing, boundary box,

    def __init__(self, collection: list):
        pass

class VectorLayer(Layer):

    def draw(self, img):
        pass



    pass

class PixelLayer(Layer):

    pass