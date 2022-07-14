from typing import List

from PIL import Image, ImageDraw

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.VectorGTRepresentation.VectorObjects import Polygon, Rectangle, \
    Line, Quadrilateral

if __name__ == '__main__':
    # create some vector_objects
    vector_obj: List[Polygon] = list()
    vector_obj.append(Polygon(xy=[(15, 25), (100, 50), (250, 8), (256, 360), (200, 310), (50, 103)]))
    vector_obj.append(Rectangle([(20,50),(10,200)]))
    vector_obj.append(Quadrilateral([(21, 50), (25, 80), (150, 8), (160, 70)]))
    vector_obj.append(Line([(10, 10), (200, 200)]))
    # set dimension
    img_dim: ImageDimension = ImageDimension(width=vector_obj[0].get_max_x()+50,height=vector_obj[0].get_max_y()+50) # [0] is the biggest

    # create image and drawer
    img = Image.new("RGB",size=img_dim.to_tuple())
    drawer = ImageDraw.Draw(img)

    # draw the objects
    for obj in vector_obj:
        obj.draw(drawer)

    #show image
    img.show()

    # draw boundingboxes
    for obj in vector_obj:
        obj.get_bbox().draw(drawer)

    #show image
    img.show()

    # crop
    current_dim = img_dim.to_tuple()
    target_dim = ImageDimension(current_dim[0]-50,current_dim[1]-50)
    img = Image.new("RGB",size=target_dim.to_tuple())
    drawer = ImageDraw.Draw(img)
    for obj in vector_obj:
        obj.crop(img_dim, target_dim, cut_left=False)
        obj.draw(drawer)



    # TODO: Test cropping with a given polygon that you know how the cropped result should look like.

    #show image
    img.show()

    # resize
    target_dim = ImageDimension(150,150)
    img = Image.new("RGB",size=target_dim.to_tuple())
    drawer = ImageDraw.Draw(img)
    for obj in vector_obj:
        obj.resize(current_dim=img_dim,target_dim=target_dim)
        obj.draw(drawer)
        obj.get_bbox().draw(drawer)

    #show image
    img.show()


