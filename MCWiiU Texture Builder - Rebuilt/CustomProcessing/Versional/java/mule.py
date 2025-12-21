from CustomProcessing import Custom

class mule(Custom.Function):
    def createImage(self, *args):
        return Custom.runFunctionFromPath("shared", "horse_process", self.wiiuName, self.type, self.wiiuImage, True, "mule")