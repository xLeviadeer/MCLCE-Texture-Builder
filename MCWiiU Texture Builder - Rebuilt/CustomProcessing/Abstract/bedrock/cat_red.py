from CustomProcessing import Custom
from CodeLibs.Path import Path
import Utility as ut
import Read as rd

class cat_red(Custom.Function):
    def createImage(self):
        if (ut.checkVersion(1, 14)):
            return rd.readImageSingular(self.wiiuName, Path("cat", "redtabby"), self.type, ut.size(64, 32))
        else:
            return rd.readImageSingular(self.wiiuName, Path("cat", "red"), self.type, ut.size(64, 32))