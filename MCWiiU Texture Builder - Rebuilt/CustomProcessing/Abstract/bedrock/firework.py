from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd

class firework(Custom.Function):
    def createImage(self):
        bedrockImage = rd.readImageSingular(self.wiiuName, "fireworks", "entity", ut.size((ut.mobside / 2), (ut.mobside / 2)))
        finalImage = ut.blankImage(int(ut.mobside / 2))
        finalImage.paste(bedrockImage, (1, -6))
        return finalImage