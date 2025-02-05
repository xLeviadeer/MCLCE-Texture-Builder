from CustomProcessing import Custom
import Utility as ut
from Sheet import SheetExtractor
import Global
from CodeLibs.Path import Path
import SizingImage as si
from CodeLibs import Logger as log
from CodeLibs.Logger import print

# custom class imports
from CustomProcessing.Abstract.bedrock.weather_WeatherSection import WeatherSection
from CustomProcessing.Abstract.bedrock.weather_WeatherLinkTexture import WeatherLinkTexture

class weather(Custom.Function):
    def createImage(self):
        # constants (not all caps because it would be too hard to read)
        AmountOfSections = 8

        # --- obtain raindrop textures ---

        # read weather image
        weatherSheet = SheetExtractor(
            Path("weather"), 
            si.convertTuple(ut.size(4)), 
            self.wiiuName, 
            "environment", 
            (32, 32)
        )

        # extract raindrops from sheet
        linkDrops = []
        tallestTextureHeight = -1
        i = 0
        while i < weatherSheet.sizeXPos:
            # adjust for rain/snow texture size
            heightPos = 0
            chunkSize = (1, 1)
            if (self.wiiuName == "rain"):
                heightPos = 1
                chunkSize = (1, 4)

            # extract raindrops into list of rain drop link textures
            currTexture = WeatherLinkTexture(
                weatherSheet.extract((i, heightPos), chunkSize)
            )
            linkDrops.append(currTexture)

            # find tallest height
            if (currTexture.realHeight > tallestTextureHeight):
                tallestTextureHeight = currTexture.realHeight

            # increment
            i += 1

        # --- create raindrop texture ---

        # wiiu image size
        wiiuImageWidth = 64
        wiiuImageHeight = 256

        # section height
        sectionHeight = wiiuImageHeight / AmountOfSections
        if (sectionHeight % 1) != 0: # check if the division isn't an integer result (value with no decimals)
            Global.endProgram(f"AmountOfSections ({AmountOfSections}) doesn't result in an integer pixel height for sections. Choose a different amount of sections.")
        sectionHeight = int(sectionHeight) # integer cast since we know it's an int

        # blank wiiu image
        newImage = ut.blankImage(wiiuImageWidth, wiiuImageHeight)

        # split the blank image into the amount of sections with correct oversizing
        i = 0
        while i < AmountOfSections:
            print(f"section {i}/{AmountOfSections}", log.CUSTOMWEATHER)

            # append to sections
            currSection = WeatherSection(
                newImage.crop(( # the imageHeight will be cropped down further in the method for adding raindrops
                    0,
                    (i * sectionHeight),
                    wiiuImageWidth,
                    ((i * sectionHeight) + sectionHeight + si.deconvertInt(tallestTextureHeight))
                ))
            )
            
            # add drops to the image
            currSection.addRainDropsToImage(
                linkDrops, 
                tallestTextureHeight, 
                WeatherSection.getRandomAmountOfRaindrops(), 
                (i == (AmountOfSections - 1 )))

            # add the completed section to the newImage
            newImage.alpha_composite(currSection.image, (0, (i * sectionHeight)))
        
            # increment
            i += 1

        # return the completed image
        return newImage
    