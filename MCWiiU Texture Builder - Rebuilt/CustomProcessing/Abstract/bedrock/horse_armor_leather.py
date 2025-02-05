from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from CodeLibs.Path import Path

class horse_armor_leather(Custom.Function):
    def createImage(self):
        return ut.getOpacityTexture(
                    rd.readImageSingular(self.wiiuName, Path("horse2", "armor", "horse_armor_leather"), "entity", ut.mobsize),
                    False if (self.wiiuName == "horse_armor_leather_1") else True,
                )