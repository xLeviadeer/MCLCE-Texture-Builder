from CustomProcessing import Custom

class enderchest(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("versional", "small_chests", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)