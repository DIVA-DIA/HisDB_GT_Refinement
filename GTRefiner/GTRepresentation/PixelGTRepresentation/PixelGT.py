from typing import Dict, List
from abc import abstractmethod

from PIL import ImageDraw, ImageFont

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.GroundTruth import GroundTruth
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.LayoutClasses import LayoutClasses
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer


class MyImage(GroundTruth):

    @abstractmethod
    def __init__(self, img_dim: ImageDimension):
        super().__init__(img_dim)


class PixelLevelGT(MyImage):

    def __init__(self, img_dim: ImageDimension):
        super().__init__(img_dim)
        self.levels: Dict[LayoutClasses, Layer] = {}
        self._initialize_empty_px_gt()

    def _initialize_empty_px_gt(self):
        for layout_class in LayoutClasses:
            self.levels[layout_class] = Layer(img_dim=self.img_dim)

    def get_layer(self, layout_class: LayoutClasses) -> Layer:
        """ Returns the layer with the given layout_class. """
        return self.levels[layout_class]

    def show(self):
        for l_class in self.levels:
            img = self.levels[l_class].img_from_layer()
            draw = ImageDraw.Draw(img)
            # font = ImageFont.truetype(<font-file>, <font-size>)
            font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 50)
            # draw.text((x, y),"Sample Text",(r,g,b))
            draw.text(xy=(50, 100), text=f"Key: {l_class}", fill="white", font=font)
            img.show()


class RawImage(MyImage):
    pass
