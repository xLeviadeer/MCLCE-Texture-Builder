from CustomProcessing import Custom
import Utility as ut
import Read as rd

class kelp_top(Custom.Function):
    def createImage(self):
        debug = False
        image = Custom.runFunctionFromPath("shared", "kelp_process", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)
        if (debug == True):
            image = ut.getImageNoOpacity(image, doZeroDetection=True) # for debugging only
        return image