from CustomProcessing import Custom

class clock(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "compass_clock", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)