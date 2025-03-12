from CustomProcessing import Custom
from CodeLibs.Path import Path
from Sheet import SheetExtractor
import Utility as ut
import Read as rd

class campfire_smoke(Custom.Function):
    def createImage(self):
        return SheetExtractor(Path("campfire_smoke"), ut.size(16), self.wiiuName, "particle", ut.size(16, 192)).extract((0, 0))