from CustomProcessing import Custom
import Utility as ut
import Read as rd
from CodeLibs.Path import Path

class spiders(Custom.Function):
    def createImage(self):
        if (self.wiiuName == "spider_eyes"):
            return ut.getOpacityTexture(
                        rd.readImageSingular(self.wiiuName, Path("spider", "spider").getPath(), "entity", ut.size(ut.mobside, (ut.mobside / 2))),
                        True,
                    )
        else: # spider, cavespider
            textureName = "spider" if (self.wiiuName != "cavespider") else "cave_spider"
            return ut.getImageNoOpacity( 
                    rd.readImageSingular(self.wiiuName, Path("spider", textureName).getPath(), "entity", ut.size(ut.mobside, (ut.mobside / 2)))
                )