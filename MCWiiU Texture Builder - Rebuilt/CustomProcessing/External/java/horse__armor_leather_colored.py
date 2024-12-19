from CustomProcessing import Custom

class horse__armor_leather_colored(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("external", "horse__armor_leather", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)