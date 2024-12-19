from CustomProcessing import Custom

class bed_colored(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("external", "beds", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)