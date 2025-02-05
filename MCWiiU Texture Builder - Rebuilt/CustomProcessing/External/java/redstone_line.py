from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from SizingImage import SizingImage as Image

class redstone_line(Custom.Function):
    def createImage(self):
        image = rd.readImageSingular(self.wiiuName, "redstone_dust_line0", self.type, ut.size(16))
        image = image.rotate(90)

        return image