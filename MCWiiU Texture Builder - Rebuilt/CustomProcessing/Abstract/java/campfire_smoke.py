from CustomProcessing import Custom

class campfire_smoke(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath(
            "shared", 
            "stack_textures", 
            self.wiiuName, 
            "particle",
            self.wiiuImage, 
            True, 
            "big_smoke_"
        )