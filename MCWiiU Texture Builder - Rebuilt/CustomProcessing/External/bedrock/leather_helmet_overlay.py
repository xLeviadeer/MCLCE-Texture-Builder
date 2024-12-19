from CustomProcessing import Custom

class leather_helmet_overlay(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("external", "leather_overlay", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)