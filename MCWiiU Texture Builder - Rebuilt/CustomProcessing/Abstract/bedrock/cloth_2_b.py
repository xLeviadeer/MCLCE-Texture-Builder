from CustomProcessing import Custom

class cloth_2_b(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "cloth", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)