from CustomProcessing import Custom
import Utility as ut
import Read as rd
import SizingImage as si 

class conduits(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, self.wiiuName, "blocks", si.deconvertTuple(self.wiiuImage.size))