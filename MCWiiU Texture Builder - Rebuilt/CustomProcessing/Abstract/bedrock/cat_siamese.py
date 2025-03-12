from CustomProcessing import Custom
from CodeLibs.Path import Path
import Utility as ut
import Read as rd

class cat_siamese(Custom.Function):
    def createImage(self):
        if (ut.checkVersion(1, 14)):
            return rd.readImageSingular(self.wiiuName, Path("cat", "siamesecat"), self.type, ut.size(64, 32))
        else:
            return rd.readImageSingular(self.wiiuName, Path("cat", "siamese"), self.type, ut.size(64, 32))