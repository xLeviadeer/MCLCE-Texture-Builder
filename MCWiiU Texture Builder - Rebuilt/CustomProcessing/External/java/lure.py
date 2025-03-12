from CustomProcessing import Custom
import Utility as ut
import Read as rd
from CodeLibs.Path import Path

class lure(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, Path("fishing_hook").getPath(), "entity", ut.size(8))