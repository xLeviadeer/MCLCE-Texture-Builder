from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Read as rd
from CodeLibs.Path import Path

class slime_lava(Custom.Function):
    def createImage(self):
        return ut.getImageNoOpacity(
                rd.readImageSingular(self.wiiuName, Path("slime", "magmacube").getPath(), "entity", ut.size(ut.mobside, (ut.mobside / 2))),
                doZeroDetection=True
            )