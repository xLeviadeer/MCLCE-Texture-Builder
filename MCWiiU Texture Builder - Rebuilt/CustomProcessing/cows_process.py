from CustomProcessing import Custom
import Utility as ut
import Read as rd
import Global

class cows_process(Custom.Function):
    def createImage(self, args):
        # select correct texture
        fileName = "cow"
        if (self.wiiuName == "mooshroom"):
            if (Global.inputGame == "java"):
                if (ut.checkVersion(13, 2, direction=False)): # check for 13 or less
                    fileName = "mooshroom"
                else:
                    fileName = "red_mooshroom"
            elif (Global.inputGame == "bedrock"):
                fileName = "mooshroom"
            else:
                Global.endProgram("cows_process could not find inputGame")

        # read image
        image = rd.readImageSingular(self.wiiuName, f"cow\\{fileName}", "entity", ut.size(ut.mobside, (ut.mobside / 2)))

        # move and resize
        portionImage = image.crop((52, 0, 64, 7)) # get udders
        image.paste(ut.blankImage(12, 7), (52, 0)) # erase
        image.paste(portionImage.crop((0, 1, 6, 7)), (53, 2)) # udder bottom
        image.paste(portionImage.crop((0, 1, 1, 7)), (52, 2)) # udder left
        image.paste(portionImage.crop((5, 1, 6, 7)), (59, 2)) # udder right
        image.paste(portionImage.crop((1, 0, 12, 1)), (54, 1)) # udder top (bottom)
        image.paste(portionImage.crop((1, 0, 12, 1)), (54, 0)) # udder top (bottom)

        return image