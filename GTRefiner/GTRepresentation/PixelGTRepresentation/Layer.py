from __future__ import annotations

from typing import Tuple, List

import numpy as np
import warnings

from PIL import Image, ImageDraw
from numpy import ma

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Interfaces.GTInterfaces import Drawable


class Layer():
    """ The :class: `Layer` class is used to represent the different levels of the :class: `PixelLevelGT` class. It does not
    implement the :class: `Scalable` interface because Layer should only be instantiated once the resizing has been done.
    :param layer: binary array representing the layer
    :type layer: numpy.ndarayy
    :param img_dim: the size of the layer (static cannot be changed)
    :type img_dim: ImageDimension
    :param color: color of the layer
    :type color: tuple
    """

    def __init__(self, layer: np.ndarray = None, img_dim: ImageDimension = None, color=None):
        """Constructor Method
        """
        self.mode = "1"
        if color is None:
            self._color = (255, 255, 255)
        else:
            self._color = color
        self._visible = True
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
        """ Logical OR of each pixel of two layers. Keeps the color of the current layer.
        :param other: Other Layer.
        :type other: Layer
        :return: A new Layer.
        :rtype: Layer
        """
        assert self.layer.shape == other.layer.shape
        is_empty = not np.any(other.layer)
        return Layer(np.array(np.logical_or(self.layer, other.layer), copy=True), color=self._color)

    def intersect(self, other: Layer) -> Layer:
        """ XOR of each pixel of two layers. Keeps the color of the current layer.
        :param other: Other Layer.
        :type other: Layer
        :return: A new Layer.
        :rtype: Layer
        """
        assert self.layer.shape == other.layer.shape
        return Layer(np.array(np.logical_and(self.layer, other.layer), copy=True), color=self._color)

    def paint_layer_on_img(self, img: Image, color=None) -> Image:
        """ Takes a base_img of mode RGB and overlays it with the layer of the current instance.
        Pixels corresponding to 0 are set to black (0,0,0). Pixels corresponding to 1 are kept.
        :param img: Image to be masked.
        :return: Masked Image with (0,0,0) where layer is 0.
        """
        if color is None:
            color = self._color
        assert img.mode == "RGB"
        assert 3 == len(self._color)
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

    def paint_layer_on_img_and_keep_colors(self, img: Image, color: Tuple = None):
        """Overlay img with colored layer. The values > 0 from self.layer will overwrite the img, the rest of the
        pixels are kept as are. Make sure that the layer has a color. Color of the layer can be set with set_color() or
        the color param.
        :param img: img for the layer to be painted on.
        :type img: Image
        :param color: color in which the layer should be painted on the Image
        :type color: Image
        :return:
        :rtype:
        """

        if color is not None:
            color = color
        elif color is None:
            color = self._color
        assert img.mode == "RGB"
        width, height = img.size
        y_axis_len = len(self.layer)
        assert height == y_axis_len
        # img.show() # to debug
        img_as_np_array = np.asarray(img)
        img_as_np_array[:, :, 0] = ma.where(self.layer > 0, color[0], img_as_np_array[:, :, 0])
        img_as_np_array[:, :, 1] = ma.where(self.layer > 0, color[1], img_as_np_array[:, :, 1])
        img_as_np_array[:, :, 2] = ma.where(self.layer > 0, color[2], img_as_np_array[:, :, 2])
        new_img = Image.fromarray(img_as_np_array)
        # new_img.show() # to debug
        return new_img

    @classmethod
    def bin_layer_from_rgb(cls, img: Image) -> Layer:
        """Returns a binary layer where every pixel equal to (0,0,0) is set to '0', every other is set to '1'.
        :param img: Image to be turned into a binary layer where (0,0,0) is set to '0', every other is set to '1'
        :type img: Image
        :return: A layer corresponding to the binarized image where all black pixels (0,0,0) are set to 0 and the all
        the others are set to 1.
        :rtype: Layer
        """
        assert img.mode == "RGB"
        img_as_array = np.asarray(img)
        np_array = np.array(np.where(np.all(img_as_array == [0, 0, 0], axis=-1), 0, 1), copy=True).astype(dtype="bool")
        return Layer(np_array)

    def intersect_this_layer_with_an_rgb_img(self, img: Image) -> Image:
        """ Perform logical and of this layer with another image. For all pixels of this binary layer that are "True",
        keep the RGB pixel of the Image given.
        :param img: Image to be masked with this layer, for all pixels of this binary layer that are "True",
        keep the RGB pixel of the image given.
        :type img: Image
        :return: masked image.
        :rtype: Returns Image that has kept all its pixel wehre self.layer is "True" all others are set to (0,0,0)
        (black)
        """
        assert img.mode == "RGB"
        img_as_np_array = np.asarray(img)
        img_as_np_array[:, :, 0] = ma.where(self.layer > 0, img_as_np_array[:, :, 0], 0)
        img_as_np_array[:, :, 1] = ma.where(self.layer > 0, img_as_np_array[:, :, 1], 0)
        img_as_np_array[:, :, 2] = ma.where(self.layer > 0, img_as_np_array[:, :, 2], 0)
        return Image.fromarray(img_as_np_array)

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
            return layers[0].paint_layer_on_img_and_keep_colors(img=img)
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
            rgb_img = bin_layer.paint_layer_on_img_and_keep_colors(img=rgb_img)
        return rgb_img

    def draw(self, page_elem: Drawable):
        img: Image = self.img_from_layer()
        drawer: ImageDraw = ImageDraw.Draw(img)
        page_elem.draw(drawer=drawer, color=(1,))
        self.layer = np.asarray(img)

    def _initialize_empty_layer(self, img_dim):
        """ Initializes a layer with a given dimension :class: `ImageDimension`. Warning shape stores width and height as
        height and with while img_dim stores it as width and height.
        :param img_dim: ImageDimension
        """
        self.layer = np.zeros(shape=(img_dim.height, img_dim.width), dtype=bool)

    def show(self):
        """ Display the image
        """
        img: Image = self.img_from_layer()
        img.show()

    def img_from_layer(self, rgb: bool = False) -> Image:
        """
        Returns an Image, either binary or in RGB-mode, from the layer.
        :param rgb: If True this class returns an RGB Pillow Image, defaults to binary
        :return: Return a binary image from it's mask by default
        """
        if rgb is True:
            img = Image.new("RGB", size=self.img_dim.to_tuple())
            return self.paint_layer_on_img(img)
        else:
            return Image.fromarray(obj=self.layer)

    def set_color(self, color: Tuple):
        """ Set color of the layer.
        :param color:  Set color of the layer.
        :type color: tuple
        """
        self._color = color

    def set_visible(self, is_visible: bool):
        """ Set visibility of the layer.
        :param is_visible: Set visibility of the layer.
        :type is_visible: bool
        """
        self._visible = is_visible
