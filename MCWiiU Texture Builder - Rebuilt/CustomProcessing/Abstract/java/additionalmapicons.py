from CustomProcessing import Custom

class additionalmapicons(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "map_icons", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)