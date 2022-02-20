"""
Run the prototype.
"""
from HisDB_GT_Refinement.prototype_01.Drawer import Drawer

IMG_Directory = "../EasyPIL/someImages/small_img/"
XML_Directory = "../CB55/PAGE-gt/public-test/"

from pathlib import Path
from PIL import Image


if __name__ == '__main__':
    # images = ImageHolder(IMG_Directory)
    # images.display_images()
    # images.print_image_arrays()

    somePoints = [(23,112),(42,44), (33,123), (23,112)]
    drawing = Drawer(300,300)
    drawing.draw_points(somePoints)
    #drawing.display_drawing()
    drawing.draw_polygon(somePoints)
    drawing.display_drawing()

    # # generates a white background
    # source_img_path = Path("../CB55/img/public-test/e-codices_fmb-cb-0055_0098v_max.jpg")
    # source_img = Image.open(source_img_path)
    # blank_image = Image.new("RGB",source_img.size, "white")
    # blank_image.save(Path("Input/White_Background.jpg"))



