from PIL.Image import Image
from pathlib import Path

from PIL import ImageDraw, Image

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Mask import TextLineMasker, Masker

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Mask import Mask
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Scalable import Scalable
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.VectorGT import VectorGT
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.VectorObject import Polygon, BoundingBox


class Page(Scalable):

    def __init__(self, original: Path, pixel_gt: Path, page_gt: Path):
        """
        Initialize ground truth container.
        :param img: Original Image
        :param pixel_gt: Pixel based GT
        :param page: PAGE GT
        """
        self.original_path: Path = original
        self.pixel_gt: Path = pixel_gt
        self.page_gt: Path = page_gt
        self.original: Image = Image.open(original).convert("RGB")
        self.pixel_gt: Image = Image.open(pixel_gt).convert("RGB")
        # TODO: it would be nicer to have a PAGE or VectorBasedGT class that contains all the information text_lines, bounding_boxes,
        self.vector_gt = VectorGT(page_gt)
        self.initialize_masks()

    def draw(self, drawer : ImageDraw):
        self.vector_gt.draw(drawer)
        print("Ergänze diese Methode.")

    def initialize_masks(self):
        # TODO could be outfactored to a class called: MaskCreator
        global_mask = Mask()
        masker = Masker()
        for textlines in self.vector_gt.get_main_text_lines():
            polygon = textlines.polygon.polygon
            temp_mask: Mask = TextLineMasker(Polygon(polygon), global_mask).mask()
            global_mask = masker.union(global_mask, temp_mask)

        for comments in self.vector_gt.get_comments():
            polygon = comments.polygon.polygon
            temp_mask: Mask = TextLineMasker(Polygon(polygon), global_mask).mask()
            global_mask = masker.union(global_mask, temp_mask)

        global_mask.show()












if __name__ == '__main__':
    original = Path("../../../CB55/img/public-test/e-codices_fmb-cb-0055_0105r_max.jpg")
    pixel = Path("../../../CB55/pixel-level-gt/public-test/e-codices_fmb-cb-0055_0105r_max.png")
    page = Path("../../../CB55/PAGE-gt/public-test/e-codices_fmb-cb-0055_0105r_max.xml")

    img = Image.new("RGB", (4872, 6496))
    drawer = ImageDraw.Draw(img)

    page_01 = Page(original=original, pixel_gt=pixel, page_gt=page)

    page_01.draw(drawer)

    img.show()