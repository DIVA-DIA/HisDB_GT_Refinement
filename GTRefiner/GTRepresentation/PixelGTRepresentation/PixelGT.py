import operator
import numpy as np
from typing import Dict, List, Tuple, Any
from abc import abstractmethod

from PIL import ImageDraw, ImageFont, Image, ImageOps
from scipy.ndimage import gaussian_filter
from skimage.filters.thresholding import threshold_otsu, threshold_niblack, threshold_sauvola

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.Table import VisibilityTable

sigma = 3
truncate = 9

class MyImage(GroundTruth):

    @abstractmethod
    def __init__(self, img: Image):
        img_dim: ImageDimension = ImageDimension(img.size[0],img.size[1])
        super().__init__(img_dim)
        self.img: Image = img

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        """ Default resize method uses the default resizing method of Pillow with bicubic resampling and no reducing
        gap. """
        # resize base image
        scale_factor = current_dim.scale_factor(target_dim)
        target_dimension = tuple(round(operator.truediv(r, t)) for r, t in zip(current_dim.to_tuple(), scale_factor))
        self.img = self.img.resize(size=target_dimension, resample=Image.BICUBIC, box=None, reducing_gap=None)
        self.img_dim = target_dim
        assert self.img_dim.to_tuple() == self.img.size

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        """
        :param current_dim: Not used.
        :param target_dim: Target dimension.
        :param cut_left: Whether or not the left part of the image should be cut off.
        :return: None
        """
        box = self._get_crop_coordinates(target_dim=target_dim, cut_left=cut_left)
        self.img = self.img.crop(box)
        self.img_dim = target_dim
        assert self.img_dim.to_tuple() == self.img.size

    def show(self):
        self.img.show()

    def _get_crop_coordinates(self, target_dim: ImageDimension,
                              cut_left: bool) -> Tuple[Any, Any, Any, Any]:
        source_dim = ImageDimension(width=self.img.width, height=self.img.height)
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

    def binarize(self, img: Image, bin_algo: str = 'otsu', **kwargs) -> np.array:
        gray_scale = ImageOps.grayscale(img)
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


class PixelLevelGT(MyImage):

    def __init__(self, img: Image = None, img_dim: ImageDimension = None):
        """ Provides the methods and functionalities needed to resize, binarize and the pixel based groundtruth.
        :param img: Ground truth image.
        :param img_dim: If this parameter is given, this class will create a new ground truth image. Useful for creating
        a new ground truth after doing manipulations on the vector_gt.
        """
        if (img is None) and (img_dim is None):
            raise AttributeError("Either provide an image (class Image) or image dimension (ImageDimension)")
        elif img is not None:
            super().__init__(img)
            self.levels: Dict[LayoutClasses, Layer] = self._hisdb_to_bin_images()
        elif img_dim is not None:
            new_img = Image.new("RGB", size=img_dim.to_tuple())
            super().__init__(new_img)
        else:
            raise AttributeError("Either provide an image (class Image) or image dimension (ImageDimension), not both.")
        self.levels: Dict[LayoutClasses, Layer] = {}
        self._initialize_empty_px_gt()

    def resize(self, current_dim: ImageDimension, target_dim: ImageDimension):
        self.img = Image.fromarray(gaussian_filter(self.img, sigma=sigma, truncate=truncate))
        super().resize(current_dim=current_dim, target_dim=target_dim)
        self.img.convert(mode="L")
        new_images: Dict[LayoutClasses, Layer] = {}
        for key, value in self.levels.items():
            img: Image = Image.fromarray(gaussian_filter(value.layer, sigma=sigma, truncate=truncate))
            img = img.resize(size=target_dim.to_tuple(), resample=Image.BICUBIC, box=None, reducing_gap=None)
            binarized_img: np.ndarray = self.binarize(img=img)
            new_images[key] = Layer(binarized_img)
        self.levels = new_images

    def crop(self, current_dim: ImageDimension, target_dim: ImageDimension, cut_left: bool):
        #super().crop(current_dim, target_dim, cut_left)
        box = self._get_crop_coordinates(target_dim=target_dim, cut_left=cut_left)
        for key, value in self.levels.items():
            #self.levels[key].show()
            self.img = self.img.crop(box)
            self.levels[key] = Layer(np.asarray(value.img_from_layer().crop(box)))
            #self.levels[key].show()
            self.img_dim = target_dim
            assert self.img_dim == self.levels[key].img_dim


    def _initialize_empty_px_gt(self):
        for layout_class in LayoutClasses:
            self.levels[layout_class] = Layer(img_dim=self.img_dim)

    def _hisdb_to_bin_images(self) -> Dict[LayoutClasses, Layer]:
        """
        Find out the different classes that are encoded in the image and convert them to binary images.
        :return: dict of binary images Dict[LayoutClasses, Layer]
        """
        img_array = np.asarray(self.img)
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

    def get_layer(self, layout_class: LayoutClasses) -> Layer:
        """ Returns the layer with the given layout_class. """
        return self.levels[layout_class]

    def show(self):
        for l_class in self.levels:
            img = self.levels[l_class].img_from_layer()
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", int(50 * self.img_dim.to_tuple()[1]/6496))
            # draw.text((x, y),"Sample Text",(r,g,b))
            draw.text(xy=(50, 100), text=f"Key: {l_class}", fill="white", font=font)
            draw.text(xy=(50, 100 + int(60*self.img_dim.to_tuple()[1]/6496)), text=f"Image Dimension: {str(self.img.size)}", fill="white", font=font)
            img.show()

    def merged_levels(self, visibility_table: VisibilityTable = None, all_vis: bool = False) -> Layer:
        base_layer = Layer(img_dim=self.img_dim)
        if visibility_table is not None:
            for k,v in self.levels.items():
                if visibility_table[k] is True:
                    base_layer = base_layer.unite(self.levels[k])
        elif all_vis is True:
            for k, layer in self.levels.items():
                base_layer = base_layer.unite(layer)
        else:
            raise ValueError("'VisibilityTable' or 'all_vis' expected. None given.")
        return base_layer

    def __getitem__(self, item):
        return self.levels[item]


class RawImage(MyImage):

    def __init__(self, img: Image):
        super().__init__(img)

    def get_cut_side(self) -> bool:
        """
        Returns the orientation of the Page. If the page is left-oriented return true,
        if it's right-oriented return false.
        :return: bool
        """
        img_left = np.array(self.img)[:, :3, :]
        img_right = np.array(self.img)[:, -3:, :]
        amount_black_left = np.where(np.all(img_left < (10, 10, 10), axis=1))[0].size
        amount_black_right = np.where(np.all(img_right < (10, 10, 10), axis=1))[0].size

        return amount_black_left > amount_black_right

