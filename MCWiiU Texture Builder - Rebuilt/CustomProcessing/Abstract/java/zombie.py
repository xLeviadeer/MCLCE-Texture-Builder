from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from CodeLibs.Path import Path

class zombie(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, Path("zombie", self.wiiuName).getPath(), "entity", ut.mobsize).crop((0, 0, 64, 32))