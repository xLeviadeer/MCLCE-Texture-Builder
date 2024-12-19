from CustomProcessing import Custom
import Utility as ut
import Read as rd

class barrier(Custom.Function):
    def createImage(self):
        return rd.readImageSingular(self.wiiuName, "barrier", "blocks", ut.size(16))