from CustomProcessing import Custom

class horse_markings_blackdots(Custom.Function):
    def createImage(self, *args):
        return Custom.runFunctionFromPath("shared", "horse_process", self.wiiuName, self.type, self.wiiuImage, True, "horse_markings_blackdots")