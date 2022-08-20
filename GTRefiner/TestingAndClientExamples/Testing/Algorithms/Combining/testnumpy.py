import numpy as np
import numpy.ma as ma
from PIL import Image

from HisDB_GT_Refinement.GTRefiner.GTRepresentation.ImageDimension import ImageDimension
from HisDB_GT_Refinement.GTRefiner.GTRepresentation.PixelGTRepresentation.Layer import Layer


def test_numpy_any():
    np_array = np.asarray([[False, False, False],
                           [False, False, False],
                           [False, False, False]])
    print(np.any(np_array))
    assert np.any(np_array) == False

    np_array = np.asarray([[False, False, False],
                           [False, True, False],
                           [False, False, False]])
    print(np.any(np_array))
    assert np.any(np_array) == True


if __name__ == '__main__':
    test_numpy_any()

    img_as_array = np.asarray([[(0, 0, 0), (1, 0, 200), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                               [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                               [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 200), (0, 0, 0)],
                               [(0, 0, 200), (0, 200, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                               [(0, 0, 200), (0, 200, 0), (0, 200, 0), (255, 0, 0), (200, 0, 0), (0, 0, 0)],
                               ])
    another_img_as_array = np.asarray([[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                               [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                               [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (100, 0, 200), (0, 0, 0)],
                               [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
                               [(0, 0, 0), (0, 200, 0), (0, 200, 0), (255, 0, 0), (200, 0, 0), (0, 0, 0)],
                               ])
    orig_img = Image.fromarray(img_as_array.astype('uint8'), mode="RGB")
    img_dim = ImageDimension(orig_img.size[0], orig_img.size[1])
    print(img_dim)

    img_as_array = np.asarray(orig_img)

    # test layer
    base_layer = Layer(img_dim=img_dim)
    some_layer = Layer(np.asarray([[0, 0, 0, 0, 1, 1],
                                   [0, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 1, 1, 1],
                                   [0, 0, 0, 0, 0, 0],
                                   [0, 0, 1, 0, 1, 0]]))
    other_layer = Layer(np.asarray([[0, 1, 0, 0, 1, 1],
                                    [0, 1, 0, 0, 0, 0],
                                    [0, 1, 0, 0, 0, 0],
                                    [0, 1, 0, 0, 0, 0],
                                    [0, 1, 0, 0, 0, 0]]))

    # test union:
    union_layer = base_layer.unite(some_layer)
    union_layer.show() # passes :)

    intersected_layer = union_layer.intersect(other_layer)
    intersected_layer.show() # passes :)
    # new_shape = (base_layer.layer.shape[0], base_layer.layer.shape[1], 3)
    # np_array = np.zeros(new_shape, dtype="uint8")
    # # np_array = np_array.mask()
    color = np.asarray([255, 123, 56], dtype="uint8")
    # back_ground = np.asarray([0, 0, 0], dtype="uint8")
    #
    # np_array[:, :, 0] = ma.where(some_layer.layer, color[0], 0)
    # np_array[:, :, 1] = ma.where(some_layer.layer, color[1], 0)
    # np_array[:, :, 2] = ma.where(some_layer.layer, color[2], 0)
    #
    # print(np_array)
    # illustrate_np_array = Layer(np_array)
    # illustrate_np_array.show()

    combined = np.zeros(shape=(img_as_array.shape[0], img_as_array.shape[1], 3), dtype="uint8")
    print(combined)
    combined[:, :, 0] = ma.where(some_layer.layer > 0, color[0], img_as_array[:, :, 0])
    combined[:, :, 1] = ma.where(some_layer.layer > 0, color[1], img_as_array[:, :, 1])
    combined[:, :, 2] = ma.where(some_layer.layer > 0, color[2], img_as_array[:, :, 2])
    print(combined)
    combined_img = Image.fromarray(combined)

    combined_img.show()
    orig_img.show()
    #some_layer.show()


