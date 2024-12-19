from CustomProcessing import Custom

class chest(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("versional", "small_chests", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)