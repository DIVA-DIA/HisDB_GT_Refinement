from HisDB_GT_Refinement.prototype_01.codefromLars.XML_handler import read_max_textline_from_file

coordinates = [(122,23),(122,3221)]

if __name__ == '__main__':
    # writePAGEfile("yolo")
    # writePAGEfile("text_region_not_provided",text_lines = "so gehts \n wieder?",text_region_coords=[(12,23),(12,44)])
    # writePAGEfile("testline.xml",coordinates,"10,49 10,232 1230,23 12,99",[("1,233,1231,12312"),("123")])

    read_max_textline_from_file("bra3.xml")

