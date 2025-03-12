from CustomProcessing import Custom
from CodeLibs.Path import Path
import Utility as ut
import Read as rd

class cat_black(Custom.Function):
    def createImage(self):
        if (ut.checkVersion(1, 14)):
            return rd.readImageSingular(self.wiiuName, Path("cat", "tuxedo"), self.type, ut.size(64, 32))
        else:
            return rd.readImageSingular(self.wiiuName, Path("cat", "blackcat"), self.type, ut.size(64, 32))