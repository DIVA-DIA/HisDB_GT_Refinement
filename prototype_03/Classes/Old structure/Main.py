# runs the prototype
from pathlib import Path
import os
from PIL import Image
from typing import List
import numpy as np
from PIL.ImageDraw import ImageDraw

from HisDB_GT_Refinement.prototype_02.Classes.PageOntoImage import overlay_img_with_xml, get_polygons_from_xml, \
    rescale_all_polygons
from HisDB_GT_Refinement.prototype_02.Classes.PixelResizer import MinorityWins, NaiveResizer, MajorityWins
import time
from datetime import datetime

from HisDB_GT_Refinement.prototype_02.Classes.masker import replace_all_but

RESIZE_FACTOR = 4  # cannot be 3
RESIZING_STRATEGY = MajorityWins()
TEXTLINE_FIll = (143, 232, 167)  # some random color I'm sure hasn't been assigned.


def open_images(directory: Path):
    img = []
    dir = sorted(os.listdir(directory))
    print(dir)
    for file in dir:
        img.append(Image.open(Path(directory / file)).convert("RGB"))
    return img


# TODO it would be better to have a static resizer object which provides the method "resize()" instead of having
#  to create a new resizing object for every image
def resize_px_images(images):
    resized = []
    for img in images:
        resizer = NaiveResizer(img=img, strategy=RESIZING_STRATEGY)
        img_as_array: np.array = resizer.resize(RESIZE_FACTOR)
        resized.append(Image.fromarray(img_as_array).convert('RGB'))
    return resized


def combine_GTs(images: Image, PAGE_gt: Path):
    pass


def save_images_as(images, OutputDirectory: Path, format: str):
    now = datetime.now().strftime("%H_%M_%S")
    i = 0
    for img in images:
        fp = "{}/picture_no_{}_{}.{}".format(OutputDirectory, i, now, format.lower())
        i = i + 1
        img.save(fp=fp)


if __name__ == '__main__':
    start = time.time()
    print("Program running")

    # input
    public_test = Path("../../../CB55/img/public-test/")
    original_png = Path("../../../CB55/img/public-test/")
    xml_gt = Path("../../../CB55/PAGE-gt/public-test/")
    pixel_level_gt = Path("../../../CB55/pixel-level-gt/public-test/")

    # output
    intermediate_result = Path("../Output/GT_1/Resized_PX_Based_GT_With_All_Pixels_Outside_Polygon_Set_To_Background/")
    output_path = Path("../../Output/GT_1/JPEG_VS_GIF/")

    # get all images
    images = open_images(pixel_level_gt)

    # get all xml paths
    path_to_xml_gt: List[str] = sorted(os.listdir(xml_gt))

    # open xml and extract the polygons in PAGEs
    PAGEs = []  # 2 D array: [[Page1][Page2][..]]
    for page in path_to_xml_gt:
        path = Path(xml_gt / page)
        polygons = get_polygons_from_xml(path)
        PAGEs.append(polygons)

    # resize all pixel based images and save them as pixel_based_GT
    resized_pixel_gt = resize_px_images(images=images)

    # resize polygons
    resized_PAGEs = []
    for page in PAGEs:
        resized_polygons = rescale_all_polygons(page, RESIZE_FACTOR)
        resized_PAGEs.append(resized_polygons)

    # fill polygons and
    PAGEs_filled_polygons = []  # list of images
    for page in resized_PAGEs:
        img = Image.new(mode="RGB", size=resized_pixel_gt[0].size)
        draw = ImageDraw(img)
        for polygon in page:
            draw.polygon(polygon, fill=TEXTLINE_FIll)
        PAGEs_filled_polygons.append(img)
        # test
        # img.show # correctly shows filled polygons

    # mask with pixel_gt so only pixel within the polygon are colored
    masked_gt = []
    for i, img in enumerate(PAGEs_filled_polygons):
        px_img = resized_pixel_gt[i]
        redrawn = replace_all_but(keep_color=TEXTLINE_FIll, input=img, output=px_img)
        img = Image.fromarray(redrawn).convert('RGB')
        # img.show() # test
        masked_gt.append(img)

    # overlay img with xml
    final_images = []
    for i, img in enumerate(masked_gt):
        new_img = overlay_img_with_xml(img, resized_PAGEs[i], output_path=output_path)
        final_images.append(img)
        # new_img.show() # test

    # save as gif
    save_images_as(final_images, output_path, "jpeg")

    # TODO: save as PAGE

    # TODO: Write J-Unit tests to test if the pixel in End-Result have been changed as desired.
    #  For testing it would be nice to have a method unique_pixel()
    #  (which can easily be implemented with color_palette ;))

    end = time.time()
    print("Programm ended in {} seconds".format((end - start)))
