from CustomProcessing import Custom
import Read as rd
import Utility as ut

class glint(Custom.Function):
    def createImage(self):
        # resize image to half size
        image = rd.readImageSingular(self.wiiuName, "enchanted_item_glint", "misc", ut.size(128))
        return image.resize(ut.size(64))