from CustomProcessing import Custom
from SizingImage import SizingImage as Image
import Utility as ut
import Read as rd
from builtins import type as typeof

class leaves_dark(Custom.Function):
    def createImage(self):
        translatedTargetImageName = self.wiiuName[:-5].replace(" ", "_") # this assumes the wiiu name will exactly match the java name, but with spaces not underscores

        baseImage = Image.new('RGBA', (16, 16), "#2c2c2cff")
        pasteImage = rd.readImageSingular(self.wiiuName, translatedTargetImageName, self.type, ut.size(16))
        pasteImage = pasteImage.convert("RGBA")
        baseImage.alpha_composite(pasteImage)

        return baseImage