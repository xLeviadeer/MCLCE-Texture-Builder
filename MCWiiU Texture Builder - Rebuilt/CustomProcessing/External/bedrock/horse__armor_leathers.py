from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd

class horse__armor_leathers(Custom.Function):
    def createImage(self):
        # get the image
        image = rd.readImageSingular(self.wiiuName, "leather_horse_armor", self.type, ut.size(16))
        
        # convert the image if needed and get the opacity portion of the image
        image = image.convert("RGBA")
        if (self.wiiuName == "horse armor_leather_colorless"):
            return ut.getOpacityTexture(image, True)
        elif (self.wiiuName == "horse armor_leather_colored"):
            return ut.getOpacityTexture(image, False)