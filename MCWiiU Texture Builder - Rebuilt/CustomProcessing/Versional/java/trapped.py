from CustomProcessing import Custom

class trapped(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("versional", "small_chests", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)