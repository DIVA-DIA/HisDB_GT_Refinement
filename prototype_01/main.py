"""
Run the prototype.
"""
from HisDB_GT_Refinement.prototype_01.Drawer import Drawer

IMG_Directory = "../EasyPIL/someImages/small_img/"
XML_Directory = "../CB55/PAGE-gt/public-test/"



if __name__ == '__main__':
    # images = ImageHolder(IMG_Directory)
    # images.display_images()
    # images.print_image_arrays()

    somePoints = [(23,112),(42,44), (33,123)]
    drawing = Drawer(300,300)
    drawing.draw_points(somePoints)
    drawing.display_drawing()

