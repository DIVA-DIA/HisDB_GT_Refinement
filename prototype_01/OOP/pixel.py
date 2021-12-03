# Pixel should be a class that helps to classify the pixels.
# A pixel can have multiple GT_classes (e.g be a decoration and a comment)


class Pixel():
    def __init__(self):
        self.GT_classes = {
            "main text body": False,
            "comment": False,
            "decoration": False,
        }

    # setter methods
    def set_to_main_text_body(self):
        self.GT_classes["main text body"] = True

    def set_to_comment(self):
        self.GT_classes["comment"] = True

    def set_to_decoration(self):
        self.GT_classes["decoration"] = True

    # getter methods
    def get_all_GT_classes(self):
        """
        returns the classes the Pixel belongs to
        :return: list
        """
        return [k for k, v in self.GT_classes.items() if v == True]

    def is_main_text_body(self):
        return self.GT_classes["main text body"]

    def is_comment(self):
        return self.GT_classes["comment"]

    def is_decoration(self):
        return self.GT_classes["decoration"]


if __name__ == '__main__':
    pix_1 = Pixel()
    print(pix_1.get_all_GT_classes())
    pix_1.set_to_comment()
    print(pix_1.get_all_GT_classes())
    pix_1.set_to_decoration()
    print(pix_1.get_all_GT_classes())
    print("Main text: " + str(pix_1.is_main_text_body()))
    print("Comment " + str(pix_1.is_comment()))
    print("Decoration: " + str(pix_1.is_decoration()))

