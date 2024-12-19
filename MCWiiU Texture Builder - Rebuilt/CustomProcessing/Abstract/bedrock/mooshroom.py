from CustomProcessing import Custom

class mooshroom(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("shared", "cows_process", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)