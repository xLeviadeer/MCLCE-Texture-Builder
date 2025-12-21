from CustomProcessing import Custom
import Read as rd
import Utility as ut
import Global

class sheep(Custom.Function):
    def createImage(self, *args):
        # get sheep images
        sheepImage = rd.readImageSingular(self.wiiuName, "sheep\\sheep", "entity", ut.size(ut.mobside, ut.mobsideHalf), doVersionPatches=False).convert("RGBA")
        sheepFurUndercoatImage = rd.readImageSingular(self.wiiuName, "sheep\\sheep_wool_undercoat", "entity", ut.size(ut.mobside, ut.mobsideHalf), doVersionPatches=False).convert("RGBA")

        # combine
        sheepImage.alpha_composite(sheepFurUndercoatImage)
        return sheepImage