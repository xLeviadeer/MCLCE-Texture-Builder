from CustomProcessing import Custom

class rain(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "weather", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)