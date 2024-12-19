from CustomProcessing import Custom

class trapped_double(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("versional", "large_chests", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)