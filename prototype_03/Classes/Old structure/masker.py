import numpy as np
import numpy.ma as ma
from PIL.Image import Image


def replace_all_but(keep_color, input, output, new_color=(0, 0, 0)) -> np.array:
    # convenience checks
    if keep_color is not type(list):
        keep_color = list(keep_color)
    if new_color is not type(list):
        new_color = list(new_color)
    input = np.asarray(input)
    output = np.asarray(output)

    assert input.shape == output.shape
    #assert input.size == output.size

    # actual code
    mask = np.logical_not(np.all(input == keep_color, axis=-1))
    #inverted_mask = np.logical_not(mask)
    output[mask] = new_color
    #reformatted = [[tuple(i) for i in r] for r in output
    return output


if __name__ == '__main__':
    array = [[(3, 2, 5), (251, 2, 5), (3, 2, 5)],
             [(3, 2, 5), (3, 2, 5), (3, 2, 5)],
             [(3, 2, 5), (251, 2, 5), (3, 2, 5)]]
    # np_array = np.array(array)
    # print(np_array)
    # # mask = np_array.flatten()
    # nums_wanted = (251, 2, 5)
    # mask = np.all(np_array == [251, 2, 5], axis=-1)
    # print(mask)
    # inverted_mask = np.logical_not(mask)
    # print(inverted_mask)
    # np_array[inverted_mask] = [0, 0, 0]
    # print(np_array)

    array = replace_all_but(keep_color=(251, 2, 5), img_as_array=array, new_color=(0, 12, 2))
    print(array)

