from builtins import type as typeof
from CodeLibs import Logger as log
from CodeLibs.Logger import print
import Utility as ut
import Global
from CodeLibs import Logger as log
from CodeLibs import Json
from CodeLibs.Path import Path
from CustomProcessing.Custom import runFunctionFromPath
from CustomProcessing.Custom import formatName
from SupportedTypes import supportedTypes
from SizingImage import SizingImage as Image
import SizingImage as si
from PIL import Image as Sampling
import math
 
# --- read errors ---

class notFoundException(Exception):
    pass

class notx16Exception(Exception):
    def __init__(self, message="", image=None):
        self.image = image

        super().__init__(message)

    def getImage(self):
        return self.image

class notExpectedException(Exception):
    def __init__(self, *args: object, size = None):
        super().__init__(*args)

        if (size == None): # default position
            self.size = (ut.singularSizeOnTexSheet,) * 2
        elif (typeof(size) is not tuple) or (len(size) != 2): # custom size error checking
            print(f"invalid syntax for position argument: {size} when position requires a tuple of length 2", log.EXIT)
            Global.bar.close()
        else: # custom size
            self.size = size
    
    def getSize(self):
        return self.size

# --- read functions ---

def patchForVersion(path, type, wiiuName, doCustomProcessing:bool=True): # does everything version_patches, no other version patches
    if (wiiuName == False or wiiuName == None): return path # nothing can be done if the wiiuName isn't passed, cannot read library
    if (type == None): return path

    variablePath = path
    # set variable path (to just path or a version patch)
    if (Global.inputVersion == None): # if the version doesn't exist
        print("attempting to run version patches but no version has been set", log.EXIT)
        Global.bar.close()
    
    # try to read the version patches
    versionPatches = None
    try:
        versionPatches = Json.readFor("\\linking_libraries\\version_patches_" + Global.inputGame, ["versions", Global.inputVersion, type])
    except:
        # this can occur if the version patch (section, not just one) that's being read for doesn't exist. In this case, the program should continue to run
        # this also always occurs for bedrock since there is no version in bedrock
        return path # skips version patch

    # if the current texture (name) is in the version patches 
    if (wiiuName in versionPatches):
        patchName = versionPatches[wiiuName] # get patchName

        # check to see if any custom processing should be done
        if (patchName == True): # if the version patch needs custom processing
            if (doCustomProcessing == False): return None # does nothing but return none as a signal it didn't work
            print(f"found version patch for {wiiuName} regarding {Global.inputVersion}", log.PATCHFUNCTION)
            # passes no wiiu image
            returnImage = runFunctionFromPath("versional", formatName(wiiuName), wiiuName, type[:-9], None) # [:-9] removes the word "abstract"
            if (returnImage == None): # if there is no function found
                print(f"(could not find) or (error while processing) patch function for \"{wiiuName}\" regarding {Global.inputVersion}", log.EXIT)
                Global.bar.close()
            print(f"found patch function for \"{wiiuName}\" and ran", log.PATCHFUNCTION, 1)
            return returnImage
        elif ((patchName == False) or (patchName == None)): # if version patch doesn't follow correct format
            print(f"invalid version patch formatting for \"{wiiuName}\" regarding {Global.inputVersion}", log.EXIT)
            Global.bar.close()

        pathSections = str.split(variablePath, "\\")

        def findIndex():
            index = 0
            for section in pathSections:
                for type in supportedTypes[Global.inputGame]:
                    if (section == type):
                        return index
                index += 1

        index = findIndex()
        if (index == len(pathSections)): # checks if type was found (the index should never equal the path sections length because there would be no file to read in this case)
            print(f"could not find type when attempting to read for: {path}", log.EXIT)
            Global.bar.close()
                    
        joinedSections = '\\'.join(pathSections[:(index + 1)])
        variablePath = f"{joinedSections}\\{patchName}"
        print(f"found version patch for {wiiuName}", log.PATCHFUNCTION)
    # always return
    return variablePath

def getImage(path):
    # check if it can be found
    try: # try to read as png
        specificVariablePath = path
        if (not specificVariablePath.endswith(".png")): specificVariablePath += ".png"
        return Image.open(specificVariablePath)
    except:
        try: # try to read as tga
            specificVariablePath = path
            if (not specificVariablePath.endswith(".tga")): specificVariablePath += ".tga"
            return Image.open(specificVariablePath)
        except: # could not find, raise notFound
            raise notFoundException

def readImage(path, type, wiiuName, expectedHeight, expectedWidth=None, isAbstractRead=False):
    # base handling of ALL image reads has been transferred to this function universally

    patchType = type if (isAbstractRead == False) else f"{type}_abstract"
    variablePath = patchForVersion(path, patchType, wiiuName)
    if (typeof(variablePath) is not str): # if the return of patchForVersion is an image
        # UNSTABLE check for type, simply checks if it's not a str
        return variablePath
    image = getImage(variablePath)

    # multiplier physics & set sizes as they should be (for not expected errors)
    deconSizeOnSheet = si.deconvertInt(ut.singularSizeOnTexSheet)
    baseSize = si.baseSize if (deconSizeOnSheet >= 16) else deconSizeOnSheet
    returnSize = ((expectedWidth if (expectedWidth != None) else baseSize), expectedHeight) # happens before conversion
    returnHeight = si.convertInt(expectedHeight)
    returnWidth = si.convertInt(expectedWidth) if (expectedWidth != None) else ut.singularSizeOnTexSheet # 16

    # check width
    if (image.width != returnWidth): # width not right
        if (Global.errorMode == "error"): raise notExpectedException(size=(returnSize))
        if (Global.errorMode == "replace"):
            def resizeInContextToWidth(image):
                return image.resize((returnWidth, int(image.height * (returnWidth / image.width))), doResize=False)
            def newSize(image): # resizes a texture upwards if needed
                if (si.resizingNeeded() == False): return image # if resizing isn't needed

                i = 1
                while i <= math.log2(si.getMultiplier()):
                    if ((image.width * pow(2, i)) == returnWidth): # image width is just wrong (this check will always be false with a processing size of 16)
                        # resize the image to be the intended width
                        return resizeInContextToWidth(image)
                    i += 1
                raise notx16Exception(image=image) # not found
            image = newSize(image) # accounts for up-conversion
            if (returnWidth < image.width): # cannot be smaller if newSize was successful in resizing. Accounts for down-conversion
                image = resizeInContextToWidth(image)

    # the width must be correct at this point since there were no errors

    # check height
    if (image.height != returnHeight): # height not right
        if (Global.errorMode == "replace"): 
            if (image.height < returnHeight): # if (actual image) is smaller (than wiiu), than duplicate up
                return duplicateImageDown(image, returnWidth, returnHeight)
            elif (image.height > returnHeight): # if (actual image) is larger (than wiiu), then crop down
                return image.crop((0, 0, image.width, returnHeight), doResize=False) # crop to make sure it fits
        if (Global.errorMode == "error"): raise notExpectedException(size=(returnSize))
    
    return image # no errors found, return normally

def duplicateImageDown(startImage, expectedWidth, expectedHeight):
    image = Image.new("RGBA", (expectedWidth, expectedHeight), "#ffffff00", doResize=False) # emtpy image
                
    # go down the image, duplicating
    currPos = 0
    while (currPos < expectedHeight):
        image.paste(startImage, (0, currPos), doResize=False)

        currPos += startImage.height # iterate down
    return image

def duplicateImageRight(startImage, expectedWidth, expectedHeight):
    image = ut.blankImage(ut.size(expectedWidth, expectedHeight), doResize=False)
    
    # go to the right duplicating
    currPos = 0
    while (currPos < expectedWidth):
        image.paste(startImage, (currPos, 0), doResize=False)

        currPos += startImage.width
    return image

def readWiiuLibFor(type, travel):
    content = False
    if (type.endswith("s")): type = type[:-1] # if there's and s at the end, get rid of it
    try:
        content = Json.readFor("\\linking_libraries\\wiiu_" + type, travel)
    except:
        print(f"{type}: could not read wiiu -> {travel}", log.DEBUG)
    return content

def readLinkLibFor(game, travel):
    content = False
    try:
        content = Json.readFor("\\linking_libraries\\base_" + game, travel)
    except:
        print(f"{game}: could not read wiiu -> {travel}", log.DEBUG)
    return content

def readImageSingular(wiiuName, pathExtension, type, expectedSize, doVersionPatches=True, doPrint=False, dox16Handling=True):
        """
        Description: 
            Runs modified handling over readImage()
        ---
        Arguments:
            - wiiuName : String <>
            - pathExtension : String <>
                - Path string that extends onto <type>
            - type : String <>
            - expectedSize : Tuple <>
                - Tuple with length of 2
            - doVersionPatches : Boolean <True>
                - Determines whether version patches should be done
            - doPrint : Boolean <False>
                - Debug variable for printing the full path
        ---
        Returns:
            - Image
        ---
        Other:
            - automatically handles x16 errors
            - lets pass notFound and notExpected errors
                - these errors should either be handled or let pass
                - if errors are passed, then the entire custom-function will fail and either result in the notFound Image or the WiiU Image
        """

        # printing
        if (doPrint == True):
            print(f"{Global.inputPath}\\{type}\\{pathExtension}<.png/.tga>", log.NOTE)

        # ignores version patches
        inputName = wiiuName
        if (doVersionPatches == False):
            inputName = None

        # read image and handle x16 errors
        image = ut.blankImage(si.convertTuple(expectedSize))
        try:
            image = readImage(f"{Global.inputPath}\\{type}\\{pathExtension}", type, inputName, expectedSize[1], expectedSize[0])
        # lets notFound exception pass
        except notx16Exception as err:
            if (dox16Handling == False):
                raise notx16Exception(image=err.getImage())
            Global.incorrectSizeErrors.append(wiiuName)
            image = err.getImage().resize(expectedSize)
        # lets notExpected exception pass
        return image

def readMulticolorGrayscale(wiiuName, type, assign, names, namePath, whitePath, expectedSize, doPrint=False):
    """
    Description:
        Reads varients of an image with multiple colors, prioritizing white. Grayscale handling is left to the user.
    ---
    Arguments:
        - wiiuName : String <>
        - type : String <>
        - assign : Function <>
            - Description:
                - Processing method for images before returning
            - Arguments
                - : Image
                - : Boolean
                    - Determines whether the image should be brightened or not
            - Returns:
                - : Image
        - names : List <>
            - A list of names that can be extended to find colored textures
            - Names farther in the list have higher "prority" for use
        - namePath : String <>
            - A path to subtend names. This path already includes the input path and the type
        - whitePath : String<>
            - A path to the white priority image. This path already includes the input path and the type
        - expectedSize : Tuple <>
            - A size to use when creating and reading images
    ---
    Returns:
        - Image
    """
    finalImage = ut.blankImage(expectedSize)
    whiteFound = True # white was found

    try: # try to read the white image first and use that
        print("------ White ------") if doPrint == True else None 
        finalImage = readImageSingular(wiiuName, Path(whitePath).getPath(withFirstSlash=False), type, expectedSize, doPrint=doPrint)
    except notFoundException:
        print("------ Colors ------") if doPrint == True else None
        # run each shulker in terms of priority until one is found that can be used
        whiteFound = False

        noneFound = True
        foundNotExpectedOnly = False
        for name in names[::-1]: # in reverse order
            try:
                finalImage = readImageSingular(wiiuName, Path(f"{namePath}{name}").getPath(withFirstSlash=False), type, expectedSize, doPrint=doPrint)
                noneFound = False
                foundNotExpectedOnly = False
                break
            except notFoundException:
                pass
            except notExpectedException:
                foundNotExpectedOnly = True

        # if only an error image was found
        if (foundNotExpectedOnly):
            finalImage = Global.notFoundImage.resize(finalImage.size)

        # if nothing was found
        if (noneFound):
            raise notFoundException # uses wiiu texture

    finalImage = assign(finalImage, (not whiteFound)) # enhance brightness if white wasn't found
    return finalImage

def readWiiuImage(inWiiuAbstract, name, doResize=True):
    name = f"{name}.png" if (not name.endswith(".png")) else name
    addition = None
    match (inWiiuAbstract):
        case True: addition = "wiiu_abstract"
        case False: addition = None # exists just so what happens is obvious
        case _:
            addition = inWiiuAbstract
    image = Image.open(Path(Global.getMainWorkingLoc(), "base_textures", addition, name).getPath(withFirstSlash=False))
    
    # multiplier physics
    if (doResize == True):
        image = image.resize(image.size, Sampling.NEAREST) # multiplier is automatic

    return image
