# Add functionalities to the Image if the Pillow library.
# according to this stackoverflow post: https://stackoverflow.com/questions/5165317/how-can-i-extend-image-class
# the Image object should not be extended. Instead, we should use a delegating wrapper.

# TODO: Soll ich alles so implementieren, dass stets eine Kopie erstellt wird (z.B. beim Binarisieren, Reskalieren, etc.)
#   oder das Original manipulieren?
from pathlib import Path
from typing import Tuple, Any

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Scalable import Scalable
from HisDB_GT_Refinement.prototype_04.Classes.NewOOP.ImageDimension import ImageDimension
import numpy as np
from PIL import Image, ImageOps, ImageDraw
from skimage.filters.thresholding import threshold_otsu, threshold_niblack, threshold_sauvola

from scipy.ndimage import gaussian_filter


class MyImage(Scalable):
    def __init__(self, img: Image):
        self._img: Image = img

    def resize(self, target_dim: ImageDimension):
        self._img = self._img.resize(size=target_dim.to_tuple(), resample=Image.BICUBIC, box=None, reducing_gap=None)

    def crop(self, target_dim: ImageDimension, cut_left: bool = True):
        box = self._get_crop_coordinates(target_dim=target_dim, cut_left=cut_left)
        self._img = self._img.crop(box=box)

    def show(self):
        self._img.show()

    def _get_crop_coordinates(self, target_dim: ImageDimension,
                              cut_left) -> Tuple[Any, Any, Any, Any]:
        # TODO: cut_left could be determined algorithmically
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

    def __init__(self, img: Image):
        super().__init__(img)


class PixelGT(MyImage):
    sigma = 3
    truncate = 9

    def __init__(self, img: Image):
        super().__init__(img)


    def resize(self, target_dim: ImageDimension):
        bin_img_array = self._hisdb_to_bin_img()
        self._img = Image.fromarray(gaussian_filter(bin_img_array, sigma=self.sigma, truncate=self.truncate))
        super().resize(target_dim=target_dim)
        self._img.convert(mode="L")

    def _hisdb_to_bin_img(self) -> np.array:
        img_array = np.asarray(self._img)
        # remove border pixels
        img_array_classes = img_array[:, :, 2]  # -> 1-D array: nimmt das letzte element des jeweiligen tripplets
        img_array_border = np.logical_not(img_array[:, :,
                                          0] > 0)  # -> 1D-array: macht einen binären array und stellt TRUE überall wo eine 0 in der ersten spalte (index = 0) vorkommt
        blue_chan_img = np.where(img_array_border, img_array_classes,
                                 0)  # -> 1D-array: überall wo eine null steht, wird die klasse behalten, überall wo text ist, wird 0 übernommen.
        blue_chan_img = np.where(blue_chan_img[:, :] == 1, 0, blue_chan_img)
        blue_chan_img = np.where(blue_chan_img[:, :] > 0, 255, blue_chan_img)
        bin_image_array = np.empty(blue_chan_img.shape)
        bin_image_array.fill(255)
        # TODO: ich könnte eigentlich eine Mask-Klasse erstellen hier. Das könnte noch praktisch sein.
        return np.where(np.logical_not(blue_chan_img), bin_image_array, 0)


if __name__ == '__main__':
    target_dimension = ImageDimension(width=700, height=1500)

    original = Path("../../../CB55/img/public-test/e-codices_fmb-cb-0055_0105r_max.jpg")
    pixelGT = Path("../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0105r_max.png")
    # Test MYImage cropping (durch instanzierung von RAWImage)
    img = Image.open(original).convert("RGB")
    diva_img = RAWImage(img=img)
    diva_img.crop(target_dim=target_dimension,cut_left=False)
    diva_img.show()

    bin_img = Image.fromarray(diva_img.binarize()).show()

    # Test RAWImage Resizing
    img = Image.open(original).convert("RGB")
    diva_img = RAWImage(img=img)
    diva_img.resize(target_dimension)
    diva_img.show()

    # Test PixelGT reskalierung
    img = Image.open(pixelGT).convert("RGB")
    pixelGt = PixelGT(img)
    pixelGt.resize(target_dimension)
    pixelGt.show()
