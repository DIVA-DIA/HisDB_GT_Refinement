# runs the prototype
from pathlib import Path
import os
from PIL import Image
from typing import List
import numpy as np

from HisDB_GT_Refinement.prototype_02.Classes.PageOntoImage import overlay_img_with_xml
from HisDB_GT_Refinement.prototype_02.Classes.PixelResizer import MinorityWins, NaiveResizer, MajorityWins
from datetime import datetime

RESIZE_FACTOR = 4 # cannot be 3
RESIZING_STRATEGY = MajorityWins()


def open_images(directory: Path):
    img = []
    dir = sorted(os.listdir(directory))
    for file in dir:
        img.append(Image.open(Path(directory/file)).convert("RGB"))
    return img


# TODO it would be better to have a static resizer object which provides the method "resize()" instead of having
#  to create a new resizing object for every image
def resize_px_images(images):
    resized = []
    for img in images:
        resizer = NaiveResizer(img=img, strategy=RESIZING_STRATEGY)
        img_as_array: np.array = resizer.resize(RESIZE_FACTOR)
        resized.append(Image.fromarray(img_as_array).convert('P', palette=Image.ADAPTIVE, colors=256))
    return resized


def combine_GTs(images: Image, PAGE_gt: Path):
    pass


def save_images_as(images, OutputDirectory: Path, format: str):
    now = datetime.now().strftime("%H_%M_%S")
    i = 0
    for img in images:
        fp = "{}/picture_no_{}_{}.{}".format(OutputDirectory, i,now, format.lower())
        i = i + 1
        img.save(fp=fp)


if __name__ == '__main__':

    # input
    public_test = Path("../../CB55/img/public-test/")
    original_png = Path("../../CB55/img/public-test/")
    xml_gt = Path("../../CB55/PAGE-gt/public-test/")
    pixel_level_gt = Path("../../CB55/pixel-level-gt/public-test/")

    # output
    intermediate_result = Path("../Output/GT_1/Resized_PX_Based_GT/")
    output_path = Path("../Output/GT_1/FINAL_GT_outline_2px_strategy_majority_wins/")

    # get all images
    images = open_images(pixel_level_gt)

    # resize all pixel based images and save them as pixel_based_GT
    resized = resize_px_images(images=images)
    save_images_as(images=resized, OutputDirectory=intermediate_result, format="png")

    # get directories of the new intermediate result and
    path_to_pixel_based_gt: List[str] = sorted(os.listdir(intermediate_result))
    path_to_xml_gt: List[str] = sorted(os.listdir(xml_gt))
    assert len(path_to_pixel_based_gt) == len(path_to_xml_gt)

    # call the overlay_xml_with_img in PageOntoImage that resizes the polyons
    for i in range(len(path_to_pixel_based_gt)):
        overlay_img_with_xml(image_path=Path(intermediate_result/path_to_pixel_based_gt[i]),
                             xml_path=Path(xml_gt/path_to_xml_gt[i]), output_path=output_path,
                             resize_factor=RESIZE_FACTOR)

