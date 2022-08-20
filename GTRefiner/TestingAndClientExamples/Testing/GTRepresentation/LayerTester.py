import unittest
import numpy as np
from PIL import Image
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
# TODO: Delete if not used.
class TestLayer(unittest.TestCase):

    # Test layer
    bin_layer: np.ndarray = np.asarray([[0, 0, 1],
                            [0, 1, 0]])

    img_as_np_array = np.asarray([[(12,12,12),(100,100,100),(200,200,200)],
                      [250,250,100],(50,100,100), (13,12,12)])

    img = Image.fromarray(img_as_np_array, "RGB")

    img_dim: ImageDimension = ImageDimension.img_dim_from_ndarray(bin_layer)

    def test_init(self):
        try:
            layer = Layer()
        except Exception as e:
            self.assertIsInstance(e, AttributeError)

        layer_2 = Layer(layer=self.bin_layer)
        self.assertEqual(self.img_dim, layer_2.img_dim)

        layer_3 = Layer(img_dim=self.img_dim)
        self.assertEqual(np.zeros(shape=self.img_dim.to_tuple(), dtype=bool),layer_3.layer)















if __name__ == '__main__':
    unittest.main()