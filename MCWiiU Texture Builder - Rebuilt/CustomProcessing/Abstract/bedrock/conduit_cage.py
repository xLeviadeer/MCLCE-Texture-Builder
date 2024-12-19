from CustomProcessing import Custom

class conduit_cage(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "conduits", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)