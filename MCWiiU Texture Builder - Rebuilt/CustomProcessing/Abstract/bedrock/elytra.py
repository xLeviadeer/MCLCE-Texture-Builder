from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from CodeLibs.Path import Path

class elytra(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, Path("armor", "elytra").getPath(), "models", ut.size(ut.mobside, (ut.mobside / 2)))