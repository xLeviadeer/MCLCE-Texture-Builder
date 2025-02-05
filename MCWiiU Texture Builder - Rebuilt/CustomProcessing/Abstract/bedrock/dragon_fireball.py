from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd

class dragon_fireball(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, "dragon_fireball", "items", ut.size(16))