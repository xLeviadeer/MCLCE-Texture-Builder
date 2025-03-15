from CustomProcessing import Custom

class bat(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("shared", "bat_process", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)