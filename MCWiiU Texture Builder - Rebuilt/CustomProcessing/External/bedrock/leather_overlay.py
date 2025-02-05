from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from SizingImage import SizingImage as Image

class leather_overlay(Custom.Function):
    def createImage(self):
        # get the respective correct image
        image = Image.new("RGBA", (ut.singularSizeOnTexSheet, ut.singularSizeOnTexSheet), "#ffffff00")
        piece = self.wiiuName.replace("leather_", "").replace("_overlay", "") # get the peice of armor
        image = rd.readImageSingular(self.wiiuName, f"leather_{piece}", "items", ut.size(16)) # read it

        # convert the image if needed and get the opacity portion of the image
        image = image.convert("RGBA")
        return ut.getOpacityTexture(image, True, levelOfDetection=40)
    