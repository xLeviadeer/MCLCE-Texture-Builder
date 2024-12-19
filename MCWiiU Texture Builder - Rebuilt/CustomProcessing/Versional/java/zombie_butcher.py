from CustomProcessing import Custom

class zombie_butcher(Custom.Function):
    def createImage(self):
        cls = Custom.getClass("shared", "villager_process") # get class so,
        args = cls.getJavaArgsList() # we can get the java args from it to,
        return Custom.runFunctionFromInstance(cls(self.wiiuName, self.type, self.wiiuImage, isShared=True), True, args) # run the function