from CustomProcessing import Custom

class cloth_2(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "cloth", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)