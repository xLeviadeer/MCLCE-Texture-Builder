from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from CodeLibs.Path import Path

class banner_base(Custom.Function):
    def createImage(self):
        if (ut.checkVersion(14, direction=False)): # earlier than 1.15
            return rd.readImageSingular(self.wiiuName, Path("banner", "banner").getPath(), "entity", ut.size(512)).crop((0, 0, 64, 64))
        else:
            return rd.readImageSingular(self.wiiuName, Path("banner", "banner_base").getPath(), "entity", ut.mobsize)