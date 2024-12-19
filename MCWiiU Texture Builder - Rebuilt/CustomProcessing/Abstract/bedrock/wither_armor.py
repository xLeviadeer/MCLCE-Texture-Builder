from CustomProcessing import Custom
import Utility as ut
import Read as rd
from CodeLibs.Path import Path

class wither_armor(Custom.Function):
    def createImage(self):
        path = Path("wither_boss")
        if (ut.checkVersion(14)): # 1.14 or newer
            path.append("wither_armor_white")
        else:
            path.append("wither_armor")
        return rd.readImageSingular(self.wiiuName, path.getPath(), "entity", ut.mobsize)