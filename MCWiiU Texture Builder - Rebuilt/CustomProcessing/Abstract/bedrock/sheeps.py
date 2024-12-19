from CustomProcessing import Custom
import Utility as ut
import Read as rd
from CodeLibs.Path import Path

class sheeps(Custom.Function):
    def createImage(self):
        sheepImage = rd.readImageSingular(self.wiiuName, Path("sheep", "sheep").getPath(), "entity", ut.mobsize)
        if (self.wiiuName == "sheep"):
            return ut.getImageNoOpacity(sheepImage.crop((0, 0, 64, 32)))
        else: # sheep fur
            return sheepImage.crop((0, 32, 64, 64))