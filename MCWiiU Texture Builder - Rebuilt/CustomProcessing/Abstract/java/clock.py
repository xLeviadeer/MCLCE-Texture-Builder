from CustomProcessing import Custom

class clock(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath(
            "shared", 
            "stack_textures", 
            self.wiiuName, 
            self.type,
            self.wiiuImage, 
            True, # print recursion
            "compass_", # name
            True # pad zeros
        )