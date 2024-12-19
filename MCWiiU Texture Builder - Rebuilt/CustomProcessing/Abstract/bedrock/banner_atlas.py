from CustomProcessing import Custom
import Utility as ut
import Read as rd
import Global
from CodeLibs.Path import Path

class banner_atlas(Custom.Function):
    def createImage(self):
        patterns = [] # expects patterns of x64 size (in the right (wiiu) order)
        if (ut.checkVersion(14, direction=False)): # earlier than 1.15
            def m(value):
                return value * 64

            bannerImage = rd.readImageSingular(self.wiiuName, Path("banner", "banner").getPath(), "entity", ut.size(512))

            i = 0
            amountOfTextures = 39
            bannerTexturesPerRow = 8
            while i < amountOfTextures: # runs a specific time so it doesn't grab empty banner textures
                x = (i % bannerTexturesPerRow)
                y = (i // bannerTexturesPerRow)
                patterns.append(bannerImage.crop((m(x), m(y), (m(x) + m(1)), (m(y) + m(1)))))

                i += 1
        else: # later than 1.15 or same
            patternNames = ["base", "border", "bricks", "circle", "creeper", "cross", "curly_border", "diagonal_left", "diagonal_right", 
                            "diagonal_up_left", "diagonal_up_right", "flower", "gradient", "gradient_up", "half_horizontal", "half_horizontal_bottom",
                            "half_vertical", "half_vertical_right", "mojang", "rhombus", "skull", "small_stripes", "square_bottom_left", 
                            "square_bottom_right", "square_top_left", "square_top_right", "straight_cross", "stripe_bottom", "stripe_center",
                            "stripe_downleft", "stripe_downright", "stripe_left", "stripe_middle", "stripe_right", "stripe_top", "triangle_bottom", 
                            "triangle_top", "triangles_bottom", "triangles_top"]
            i = 0
            for name in patternNames: # stripe_downright
                currImage = ut.blankImage(ut.mobsize)
                try:
                    # sets the curr image with a black background
                    currImage = rd.readImageSingular(self.wiiuName, Path("banner", f"banner_{name}").getPath(), "entity", ut.mobsize)
                except rd.notFoundException:
                    # uses wiiu image
                    bannerTexturesPerRow = 6
                    currImage = self.wiiuImage.crop((
                        (i % bannerTexturesPerRow) * ut.TextureSpecifics.bannerSize[0],
                        (i // bannerTexturesPerRow) * ut.TextureSpecifics.bannerSize[1],
                        ((i % bannerTexturesPerRow) * ut.TextureSpecifics.bannerSize[0]) + ut.TextureSpecifics.bannerSize[0],
                        ((i // bannerTexturesPerRow) * ut.TextureSpecifics.bannerSize[1]) + ut.TextureSpecifics.bannerSize[1] ))
                except rd.notExpectedException:
                    Global.notExpectedErrors.append(self.wiiuName)
                    currImage.paste(Global.notFoundImage.resize(ut.TextureSpecifics.bannerSize)) # uses error texture as the banner size
                patterns.append(currImage)
                i += 1
        return Custom.runFunctionFromPath("shared", "banner_process", self.wiiuName, self.type, self.wiiuImage, True, patterns)