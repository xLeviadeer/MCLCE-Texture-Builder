from CustomProcessing import Custom

class wolf_collar(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "wolf", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)