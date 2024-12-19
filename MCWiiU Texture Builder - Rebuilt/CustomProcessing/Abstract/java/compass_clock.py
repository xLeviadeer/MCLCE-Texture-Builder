from CustomProcessing import Custom
import Utility as ut
import Read as rd
from SizingImage import SizingImage as Image
import Global
import os

class compass_clock(Custom.Function):
    def createImage(self):
        # this can detect and replace missing clock textures at a variable size
        self.typeFolderPath = f"{Global.inputPath}\\{self.type}"
        textures = []
        nums = []
        greatestNum = -1
        for file in os.scandir(self.typeFolderPath): # for all files in the item directory
            if (file.is_file()):
                fileName = os.path.splitext(file.name)[0] # gets the name without an extension
                if (fileName[:-2] == f"{self.wiiuName}_"): # if the name (without the last 2 numbers) equals the self.wiiuName
                    try: # uses a full error block (with x16 handling)
                        currImage = rd.readImageSingular(self.wiiuName, file.name, self.type, ut.size(16), dox16Handling=False)
                    except rd.notx16Exception as err: # stop program, isn't to size
                        # determine final image by getting the image that the program error'd on (err.getImage()) then,
                        Global.incorrectSizeErrors.append(self.wiiuName)
                        currImage = err.getImage().resize(ut.size(16)) # resize the image as the correct size
                    except rd.notExpectedException: # (only happens in error mode) place error texture
                        Global.notExpectedErrors.append(self.wiiuName)
                        currImage = Global.notFoundImage.resize(ut.size(ut.singularSizeOnTexSheet), doResize=False)
                    # image has to be found since we are reading from it's file name

                    # append sorted (sort and append to lists)
                    try:
                        currNum = int(fileName[-2:])     
                    except ValueError:
                        continue # if cannot find number, try to continue without this texture    
                    if (greatestNum < currNum): greatestNum = currNum # set greatest number            
                    if (len(nums) == 0): # if there are yet to be names and textures
                        nums.append(currNum)
                        textures.append(currImage)
                    else: # there are already names and textures
                        def checkAllNums(): # functionized so it can be returned from
                            i = 0
                            while i < len(nums): # go through all values and sort
                                if (currNum < nums[i]): 
                                    nums.insert(i, currNum)
                                    textures.insert(i, currImage)
                                    return
                                # do nothing if it's greater
                                i += 1
                            # if the loop wasn't returned, then the currNum is the smallest value
                            nums.append(currNum)
                            textures.append(currImage)
                        checkAllNums()     
        # insert missing textures (this is the NotFound check)
        i = 0
        while i < greatestNum: # while for the amount of the last number
            if (nums[i] != i):
                startingY = (i * 16) % self.wiiuImage.height # the mod makes sure that the wiiu texture is never tried to be read outside of the wiiu texture
                currImage = self.wiiuImage.crop((0, startingY, 16, (startingY + 16)))
                nums.insert(i, i)
                textures.insert(i, currImage)
            i += 1

        # add all the textures into one texture
        finalImage = ut.blankImage(16, (len(textures) * 16))
        i = 0
        for texture in textures:
            finalImage.paste(texture, (0, i))
            i += 16
        
        # return final texture
        return finalImage