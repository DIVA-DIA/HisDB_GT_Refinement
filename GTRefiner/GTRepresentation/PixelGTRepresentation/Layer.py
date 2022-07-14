from __future__ import annotations

from typing import Tuple, List

import numpy as np
import warnings

from PIL import Image, ImageDraw
from numpy import ma

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Drawable
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon


class Layer():
    """ The :class: Layer class is used to represent the different levels of the :class: PixelLevelGT class. It does not
    implement the :class: Scalable interface because Layer should only be instantiated once the resizing has been done.
    """

    def __init__(self, layer: np.ndarray = None, img_dim: ImageDimension = None, color=None):
        self.mode = "1"
        if color is None:
            self.color = (255, 255, 255)
        else:
            self.color = color
        self.visible = True
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
        is_empty = not np.any(other.layer)
        return Layer(np.array(np.logical_or(self.layer, other.layer), copy=True), color=self.color)

    def intersect(self, other: Layer) -> Layer:
        """ XOR of each pixel of two layers.
        :param other: Other Layer.
        :returns A new Layer."""
        assert self.layer.shape == other.layer.shape
        return Layer(np.array(np.logical_and(self.layer, other.layer), copy=True), color=self.color)

    def invert(self, other: Layer = None) -> Layer:
        if other is None:
            return Layer(np.invert(self.layer))
        else:
            return Layer(np.invert(other.layer))

    def paint_layer_on_img(self, img: Image, color=None) -> Image:
        """ Takes a base_img of mode RGB and overlays it with the layer of the current instance.
        Pixels corresponding to 0 are set to black (0,0,0). Pixels corresponding to 1 are kept.
        :param img: Image to be masked.
        :return: Masked Image with (0,0,0) where layer is 0.
        """
        if color is None:
            color = self.color
        assert img.mode == "RGB"
        assert 3 == len(self.color)
        width, height = img.size
        y_axis_len = len(self.layer)
        assert height == y_axis_len
        img_as_np_array = np.asarray(img)
        colored_layer = np.zeros((img_as_np_array.shape[0], img_as_np_array.shape[1], 3), dtype="uint8")
        # # Draw self.layer (binary) with it's color RGB mode
        # colored_layer[:, :, 0] = ma.where(self.layer, self.color[0], 0)
        # colored_layer[:, :, 1] = ma.where(self.layer, self.color[1], 0)
        # colored_layer[:, :, 2] = ma.where(self.layer, self.color[2], 0)
        # Overlay img with colored layer. The values > 0 from colored layer will overwrite the img.
        combined = np.zeros((img_as_np_array.shape[0], img_as_np_array.shape[1], 3), "uint8")
        combined[:, :, 0] = ma.where(self.layer > 0, color[0], img_as_np_array[:, :, 0])
        combined[:, :, 1] = ma.where(self.layer > 0, color[1], img_as_np_array[:, :, 1])
        combined[:, :, 2] = ma.where(self.layer > 0, color[2], img_as_np_array[:, :, 2])
        return Image.fromarray(combined)

    @classmethod
    def bin_layer_from_rgb(cls, img: Image) -> Layer:
        """ Returns a binary layer where every pixel equal to (0,0,0) is set to '0', every other is set to '1'."""
        assert img.mode == "RGB"
        img_as_array = np.asarray(img)
        np_array = np.array(np.where(np.all(img_as_array == [0, 0, 0], axis=-1), 0, 1), copy=True)
        return Layer(np_array)

    @classmethod
    def merge_and_draw(cls, layers: List[Layer], img: Image = None) -> Image:
        """ Merges a list of layers onto a Pillow :class: `Image` Image while keeping their :param
        color: attribute. If only one layer is given, it will return it as a RGB Image.
        :param layers: The first layer in the list must be the base-layer. If only one layer is given.
        :type layers: List[Layer]The base-layer contains the base-object, the object that should be represented on the final Image.
        :param img: When given, it will draw the merged layers on this image.
        :type img: Image
        :return Image: return a Pillow :class: `Image` Image with moder RGB
        """
        base_layer = layers[0]
        img_dim = layers[0].img_dim
        # Deal with special cases.
        if len(layers) == 1:
            return layers[0].img_from_layer()
        if img is not None:
            rgb_img = img
            assert rgb_img.size == img_dim.to_tuple()
        else:
            rgb_img = Image.new("RGB", size=img_dim.to_tuple())
        # Merge
        for i in range(1, len(layers)):
            # logical and with base layer
            bin_layer = layers[i].intersect(base_layer)
            # draw on img with color of layers[i]
            rgb_img = bin_layer.paint_layer_on_img(img=rgb_img)
        return rgb_img




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

    def img_from_layer(self, rgb: bool = False) -> Image:
        """
        Returns an Image from the layer.
        :param rgb: If True this class returns an RGB Pillow Image.
        :return: Return a binary image from it's mask by default
        """
        # Note: img from numpy array doesn't properly work for mode "1" (it's a bug from pillow), thus the work-around
        #   by converting it to mode "1" in a seconds step.
        # Image.fromarray(obj=self.layer, mode="L").convert(mode="1")
        if rgb is True:
            img = Image.new("RGB", size=self.img_dim.to_tuple())
            return self.paint_layer_on_img(img)
        else:
            return Image.fromarray(obj=self.layer)


if __name__ == '__main__':

    # Test layer
    bin_layer: np.ndarray = np.asarray([[0, 0, 1],
                                        [0, 1, 0]])

    img_as_np_array = np.asarray([[(12, 12, 12), (100, 100, 100), (200, 200, 200)],
                                  [(250, 250, 100), (50, 100, 100), (13, 12, 12)]])

    img = Image.fromarray(img_as_np_array, "RGB")

    img_dim: ImageDimension = ImageDimension(bin_layer.shape[1], bin_layer.shape[0])

    layer_1 = Layer(layer=bin_layer)
    layer_2 = Layer(img_dim=img_dim)

    # test intitialisation
    assert layer_1.layer is not None
    assert layer_2.layer is not None
    assert layer_1.img_dim == layer_2.img_dim
    assert layer_1.layer.shape == layer_2.layer.shape
    # show it
    layer_1.show()
    layer_2.show()

    # test falty intitialisation
    try:
        layer_3 = Layer()
    except AttributeError as e:
        assert AttributeError is e

    layer_4 = Layer(layer=bin_layer, img_dim=ImageDimension(10, 5))
