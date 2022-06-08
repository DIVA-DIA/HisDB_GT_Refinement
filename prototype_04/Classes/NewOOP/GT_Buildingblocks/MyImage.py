# Add functionalities to the Image if the Pillow library.
# according to this stackoverflow post: https://stackoverflow.com/questions/5165317/how-can-i-extend-image-class
# the Image object should not be extended. Instead, we should use a delegating wrapper.

# TODO: Soll ich alles so implementieren, dass stets eine Kopie erstellt wird (z.B. beim Binarisieren, Reskalieren, etc.)
#   oder das Original manipulieren?
import operator
from pathlib import Path
from typing import Tuple, Any, Dict

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Scalable import Scalable
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.ImageDimension import ImageDimension
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
from skimage.filters.thresholding import threshold_otsu, threshold_niblack, threshold_sauvola

from scipy.ndimage import gaussian_filter

from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.Layer import Layer
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.GT_Buildingblocks.layout_classes import LayoutClasses


class MyImage(Scalable):
    def __init__(self, img_path: Path):
        self._img: Image = Image.open(img_path).convert("RGB")

    def resize(self, scale_factor: Tuple[float, float]):
        img_dimension: ImageDimension = self.get_dimension()
        target_dimension = tuple(round(operator.truediv(r, t)) for r, t in zip(img_dimension.to_tuple(), scale_factor))
        self._img = self._img.resize(size=target_dimension, resample=Image.BICUBIC, box=None, reducing_gap=None)

    def crop(self, target_dim: ImageDimension, cut_left: bool):
        box = self._get_crop_coordinates(target_dim=target_dim, cut_left=cut_left)
        self._img = self._img.crop(box=box)

    def get_dimension(self) -> ImageDimension:
        img_dim: ImageDimension = ImageDimension(width=self._img.size[0], height=self._img.size[1])
        return img_dim

    def show(self):
        self._img.show()

    def _get_crop_coordinates(self, target_dim: ImageDimension,
                              cut_left: bool) -> Tuple[Any, Any, Any, Any]:
        # TODO: cut_left can be determined algorithmically for RawImage, but not for PixelLevelGT
        source_dim = ImageDimension(width=self._img.width, height=self._img.height)
        if target_dim is None or cut_left is None:
            raise ValueError("target_dim or cut_left is None.")
        if cut_left:
            left = source_dim.width - target_dim.width
            upper = (source_dim.height - target_dim.height) / 2
            right = source_dim.width
            lower = target_dim.height + upper
        else:
            left = 0
            upper = (source_dim.height - target_dim.height) / 2
            right = target_dim.width
            lower = target_dim.height + upper

        return left, upper, right, lower  # left, upper, right, lower

    def binarize(self, bin_algo: str = 'otsu', **kwargs) -> np.array:
        gray_scale = ImageOps.grayscale(self._img)
        image_array = np.asarray(gray_scale)
        threshold = 0
        if bin_algo == 'otsu':
            threshold = threshold_otsu(image_array)
        elif bin_algo == 'niblack':
            threshold = threshold_niblack(image_array, **kwargs)
        elif bin_algo == 'sauvola':
            threshold = threshold_sauvola(image_array, **kwargs)
        else:
            raise ValueError('Unknown binarization algorithm')

        return image_array > threshold


class RAWImage(MyImage):

    def __init__(self, img_path: Path):
        super().__init__(img_path)

    def get_cut_side(self) -> bool:
        """
        Returns the orientation of the Page. If the page is left-oriented return true,
        if it's right-oriented return false.
        :return: bool
        """
        img_left = np.array(self._img)[:, :3, :]
        img_right = np.array(self._img)[:, -3:, :]
        amount_black_left = np.where(np.all(img_left < (10, 10, 10), axis=1))[0].size
        amount_black_right = np.where(np.all(img_right < (10, 10, 10), axis=1))[0].size

        return amount_black_left > amount_black_right


class PixelGT(MyImage):
    sigma = 3
    truncate = 9

    def __init__(self, img_path: Image):
        super().__init__(img_path)
        self.bin_images: Dict[LayoutClasses,Layer] = self._hisdb_to_bin_images()

    def resize(self, scale_factor: Tuple[float, float]):
        new_images: Dict[LayoutClasses,Layer] = {}
        for key, value in self.bin_images.items():
            self._img = Image.fromarray(gaussian_filter(value.layer, sigma=self.sigma, truncate=self.truncate))
            super().resize(scale_factor=scale_factor)
            self._img.convert(mode="L")
            new_images[key] = Layer(self.binarize())
        self.bin_images = new_images

    def draw_with_keys(self):
        """
        mahlt die Keys auf die verschiedenen Layerklassen, ohne diese zu manipulieren. Dient also nur zu illustrationszwecken.
        :return:
        """
        for key, value in self.bin_images.items():
            img = Image.fromarray(value.layer)
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 50)
            # draw.text((x, y),"Sample Text",(r,g,b))
            draw.text(xy=(50, 100), text=f"Key: {key}", fill="white", font=font)
            img.show()

    # def _hisdb_to_bin_img(self) -> np.array:
    #     img_array = np.asarray(self._img)
    #     # remove border pixels
    #     img_array_classes = img_array[:, :, 2]  # -> 1-D array: nimmt das letzte element des jeweiligen tripplets
    #     img_array_border = np.logical_not(img_array[:, :,
    #                                       0] > 0)  # -> 1D-array: macht einen binären array und stellt TRUE überall wo eine 0 in der ersten spalte (index = 0) vorkommt
    #     blue_chan_img = np.where(img_array_border, img_array_classes,
    #                              0)  # -> 1D-array: überall wo eine null steht, wird die klasse behalten, überall wo text ist, wird 0 übernommen.
    #     blue_chan_img = np.where(blue_chan_img[:, :] == 1, 0, blue_chan_img)
    #     blue_chan_img = np.where(blue_chan_img[:, :] > 0, 255, blue_chan_img)
    #     bin_image_array = np.empty(blue_chan_img.shape)
    #     bin_image_array.fill(255)
    #     # TODO: ich könnte eigentlich eine Mask-Klasse erstellen hier. Das könnte noch praktisch sein.
    #     return np.where(np.logical_not(blue_chan_img), bin_image_array, 0)

    def _hisdb_to_bin_images(self) -> Dict[LayoutClasses, Layer]:
        """
        Find out the different classes that are encoded in the image and convert them to binary images.
        :return: dict of binary images Dict[LayoutClasses, Layer]
        """
        img_array = np.asarray(self._img)
        # remove border pixels
        img_array_classes = img_array[:, :, 2]
        # 1: background, 2: comment, 4: decoration, 8: maintext
        # 6: comment + decoration, 12: maintext + decoration
        categories = np.unique(img_array_classes)[1:]
        bin_images = {}
        for category in categories:
            # remove border pixels
            array_border = np.logical_not(img_array[:, :, 0] > 0)
            blue_chan = np.where(array_border, img_array_classes, 0)

            # set pixel which are equal to category to 255
            blue_chan = np.where(blue_chan[:, :] == category, 255, 0)

            bin_images[LayoutClasses(category)] = Layer(blue_chan.astype(np.uint8))
        return bin_images



