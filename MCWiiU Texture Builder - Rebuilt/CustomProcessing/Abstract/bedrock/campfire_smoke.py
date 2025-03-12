from CustomProcessing import Custom
from CodeLibs.Path import Path
from Sheet import SheetExtractor
import Utility as ut
import Read as rd

class campfire_smoke(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, Path("campfire_smoke"), "particle", ut.size(16, 192))