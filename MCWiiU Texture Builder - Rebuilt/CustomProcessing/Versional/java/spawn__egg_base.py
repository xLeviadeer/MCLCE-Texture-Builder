from CustomProcessing import Custom
import Read as rd
import Global

class spawn__egg_base(Custom.Function):
    def createImage(self): return rd.readWiiuImage(False, f"{Global.getLayerGame()}_item").crop((144, 144, 160, 160))