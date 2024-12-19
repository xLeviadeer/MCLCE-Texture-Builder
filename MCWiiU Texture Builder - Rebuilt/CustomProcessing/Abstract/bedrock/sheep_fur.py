from CustomProcessing import Custom

class sheep_fur(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "sheeps", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)