from CustomProcessing import Custom
import Utility as ut
import Read as rd
from SizingImage import SizingImage as Image

class breaks(Custom.Function):
    def createImage(self):
        num = int(self.wiiuName[-1:])
        return rd.readImageSingular(self.wiiuName, f"destroy_stage_{num}", "environment", ut.size(16))