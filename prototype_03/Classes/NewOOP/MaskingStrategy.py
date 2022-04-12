# Responsible for providing methods to combine masks of type Mask()
from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.Mask import Mask, ShapeMask
import numpy as np
from abc import abstractmethod

from HisDB_GT_Refinement.prototype_03.Classes.NewOOP.VectorObject import Polygon, Box





# Redundant class because you can always apply union etc directly to Mask() object (no redundant memory allocation necessary)
# class MaskCollection(Scalable):
#
#     def __init__(self):
#         self.masks: List[Mask] = []
#
#     def add(self, mask: Mask):
#         self.masks.append(mask)