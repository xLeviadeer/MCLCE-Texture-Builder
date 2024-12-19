from CustomProcessing import Custom

class acacia__leaves_dark(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("external", "leaves_dark", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)