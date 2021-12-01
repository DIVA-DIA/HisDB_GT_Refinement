"""
Opens the image and stores it as an numpy array.
"""
import numpy
from PIL import Image
import os


class ImageHolder():
    # Images stored as pillow Image object such that they can be displayed easily.
    images = []
    # Images stored as numpy arrays such that they can be manipulated efficiently.
    image_arrays = []

    def __init__(self, directory):
        """
        Given a directory ImageHolder reads them as images and stores them in a list of images as well as arrays.
        :param directory: string that defines the path to the directory the image/images are stored.
        """
        self.load_images(directory)

    def load_images(self, directory):
        """
        :param directory: string that defines the path to the directory the image/images are stored.
        :return:
        """
        for image in os.listdir(directory):
            rgb = Image.open(directory + image).convert("RGB")
            self.images.append(rgb)
            self.image_arrays.append(numpy.array(rgb))

    def save_images(self):
        pass

    def display_images(self):
        for img in self.images:
            Image._show(img)

    def print_image_arrays(self):
        for arr in self.image_arrays:
            print(arr)