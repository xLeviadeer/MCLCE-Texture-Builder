from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from CodeLibs.Path import Path

class ghast_fire(Custom.Function):
    def createImage(self):
        return ut.getImageNoOpacity(
                rd.readImageSingular(self.wiiuName, Path("ghast", "ghast_shooting").getPath(), "entity", ut.size(ut.mobside, (ut.mobside / 2)))
            )