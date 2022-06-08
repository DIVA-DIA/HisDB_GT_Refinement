# soll die Klassen des GT_Buildingblocks repräsentieren

# TODO: Überlege, ob es Sinn macht die Klassen als classes zu speichern. Falls ja, den Code ergänzen.

class GT_classes():
    name = None
    color = (0,0,0) # default color
    def __init__(self, name):
        self.name = name

class decoration():
    def __init__(self):
        super(self, "decoration")
