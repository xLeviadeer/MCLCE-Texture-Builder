from CustomProcessing import Custom

class snow(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "weather", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)