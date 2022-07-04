from __future__ import annotations
import numpy as np
import warnings

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Drawable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon


class Layer():
    """ The :class: Layer class is used to represent the different levels of the :class: PixelLevelGT class. It does not
    implement the :class: Scalable interface because Layer should only be instantiated once the resizing has been done.
    """
    mode = "1"

    # color = (255,0,0) # not used -> could come in handy for the coloring

    def __init__(self, layer: np.ndarray = None, img_dim: ImageDimension = None):
        if layer is None:
            if img_dim is None:
                raise AttributeError("layer or img_dim must have a value")
            else:
                self.img_dim: ImageDimension = img_dim
            self._initialize_empty_layer(self.img_dim)
        else:
            self.layer: np.ndarray = layer
            if img_dim is not None:
                warnings.warn("img_dim is ignored, because a base_layer has been given.", DeprecationWarning)
            self.img_dim: ImageDimension = ImageDimension(layer.shape[1], layer.shape[0])

    def unite(self, other: Layer) -> Layer:
        assert self.layer.shape == other.layer.shape
        return Layer(np.logical_or(self.layer, other.layer))

    def intersect(self, other: Layer) -> Layer:
        """ Xor gives us not A and B"""
        assert self.layer.shape == other.layer.shape
        return Layer(np.logical_and(self.layer, other.layer))

    def invert(self, other: Layer = None) -> Layer:
        if other is None:
            return Layer(np.invert(self.layer))
        else:
            return Layer(np.invert(other.layer))

    def mask(self, img: Image) -> Image:
        """ Takes a base_img of mode RGB and overlays it with the layer of the current instance.
        Pixels corresponding to 0 are set to black (0,0,0). Pixels correpsonding to 1 are kept.
        :param img: Image to be masked.
        :return: Masked Image with (0,0,0) where layer is 0.
        """
        assert img.mode == "RGB"
        img_as_array = np.asarray(img)
        black_background = np.where(img_as_array, self.layer, (0, 0, 0))
        return Image.fromarray(black_background, mode="RGB")

    def draw(self, page_elem: Drawable):
        img: Image = self.img_from_layer()
        drawer: ImageDraw = ImageDraw.Draw(img)
        page_elem.draw(drawer=drawer, color=(1,))
        self.layer = np.asarray(img)

    def _initialize_empty_layer(self, img_dim):
        """ nitializes a layer with a given dimension :class: `ImageDimension`. Warning shape stores width and height as
        height and with while img_dim stores it as width and height.
        :param img_dim: ImageDimension
        """
        self.layer = np.zeros(shape=(img_dim.height, img_dim.width), dtype=bool)

    def show(self):
        """ Display the image
        """
        img = self.img_from_layer()
        print("image mode" + str(img.mode))
        print("image shape/size" + str(img.size))
        print("self.img_dim" + str(self.img_dim))
        img.show()

    def img_from_layer(self):
        """
        Return a binary image from it's mask.
        :return: Image
        """
        # Note: img from numpy array doesn't properly work for mode "1" (it's a bug from pillow), thus the work-around
        #   by converting it to mode "1" in a seconds step.
        # Image.fromarray(obj=self.layer, mode="L").convert(mode="1")
        return Image.fromarray(obj=self.layer)


if __name__ == '__main__':
    pass
    # # Test layer
    # bin_layer: np.ndarray = np.asarray([[0, 0, 1],
    #                                     [0, 1, 0]])
    #
    # img_as_np_array = np.asarray([[(12, 12, 12), (100, 100, 100), (200, 200, 200)],
    #                               [(250, 250, 100), (50, 100, 100), (13, 12, 12)]])
    #
    # img = Image.fromarray(img_as_np_array, "RGB")
    #
    # img_dim: ImageDimension = ImageDimension(bin_layer.shape[1],bin_layer.shape[0])
    #
    # layer_1 = Layer(layer=bin_layer)
    # layer_2 = Layer(img_dim=img_dim)
    #
    # # test intitialisation
    # assert layer_1.layer is not None
    # assert layer_2.layer is not None
    # assert layer_1.img_dim == layer_2.img_dim
    # assert layer_1.layer.shape == layer_2.layer.shape
    # #show it
    # layer_1.show()
    # layer_2.show()
    #
    # # test falty intitialisation
    # try:
    #     layer_3 = Layer()
    # except AttributeError as e:
    #     assert AttributeError is e
    #
    # layer_4 = Layer(layer=bin_layer,img_dim=ImageDimension(10,5))
