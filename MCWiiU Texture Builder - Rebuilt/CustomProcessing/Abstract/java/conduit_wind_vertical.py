from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from CodeLibs.Path import Path

class conduit_wind_vertical(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, Path("conduit", f"wind_vertical").getPath(), "entity", ut.size(64, 1024)).crop((0, 0, 64, 704))
        