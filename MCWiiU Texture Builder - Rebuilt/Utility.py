from builtins import type as typeof
from SizingImage import SizingImage as Image
from typing import Union
from CodeLibs.Path import Path
from Read import readImageSingular
import SizingImage as si
import Global
import Global
from CodeLibs import Logger as log
from CodeLibs.Logger import print
import re

# --- utility variables --- 

singularSizeOnTexSheet = 16
mobside = 64
mobsideHalf = int(mobside / 2)
mobsize = (mobside, mobside)

# --- library of utility functions ---

def blankImage(size=singularSizeOnTexSheet, height=None, color=(0, 0, 0, 0), doResize=True):
    """
    Description:
        Generates a blank image of the input size
    ---
    Arguments:
        - size : Integer <singularTexSizeOnSheet>
            - X size
        - height : Integer <size>
            - Y size
        - color : Tuple <(0, 0, 0, 255)>
            - Determines the color of the blank image
    ---
    Returns:
        - Image
    """
    # function will account for tuples as size, only 1 value as size, having no size, too many size provided
        # all values must at least have the right type of value provided (integers)
    return Image.new("RGBA", ((((size,) * 2) if (not height) else (size, height))) if (typeof(size) is not tuple) else (size[:2] if (len(size) > 1) else size), color, doResize=doResize)

def size(size=singularSizeOnTexSheet, height=None):
    """
    Description:
        Creates a tuple that works as a size
    ---
    Arguments:
        - size : Integer <singularTexSizeOnSheet>
            - X size
        - height : Integer <size>
            - Y size
    ---
    Returns:
        - Tuple : length of 2
    """
    return (int(size),) * 2 if (not height) else (int(size), int(height))

def checkVersion(majorUpdate:int, minorVersion:int=0, direction:bool=True) -> bool:
    """
    Description: 
        Checks the current version against the input version
    ---
    Arguments:
        - majorUpdate : Integer <>
        - minorVersion : Integer <0>
            - If left empty, checks against all (the latest possible) minor version 
        - direction : Boolean <True>
            - True: checks current version is equal or higher than input
            - False: checks current version is equal or lower than input
    ---
    Returns:
        - Boolean
    """
    minorVersion = 0 if (minorVersion == None) else minorVersion # change minorVersion None to 0
    return compareVersions(Global.inputVersion, [1, majorUpdate, minorVersion], direction, inclusive=True)

def compareVersions(versionA:str, versionB:str, direction:bool=None, inclusive:bool=None) -> bool:
    """
    Description:
        Compares two versions as strings to find greater/less than 
    ---
    Arguments:
        - versionA : String <>
        - versionB : String <>
        - direction : Boolean <None>
            - None: don't check greater or less than, just check equality
            - True: check if A is greater than B
            - False: check if A is smaller than B
        - inclusive : Boolean <None>
            - None: sets to False or checks equality or set to false if direction is set
            - True: inclusive check
            - False: non-inclusive check
    ---
    Returns:
        - Boolean true or false based on the provided conditions
        - Providing only versions and no conditions checks for equality
    """
    
    # casts the items of a list to an int (from int or string) and check for invalid characters
    def castItemsToInt(lst:list):
        validCharactersPattern = r"[^\d.]" # numbers and period

        i = 0
        while (i < len(lst)):
            if isinstance(lst[i], int): pass # if int, do nothing
            elif isinstance(lst[i], str): # if string, cast to int
                # remove invalids
                lst[i] = re.sub(validCharactersPattern, "", lst[i])
                
                try: # try to cast
                    lst[i] = int(lst[i])
                except ValueError or TypeError: # casting error
                    Global.endProgram(f"can't cast value {lst[i]} in lst version list to int") 
            else:
                # not a string or int
                Global.endProgram(f"value ({lst[i]}) in version list isn't a string or int")
            i += 1
        return lst
    
    # longest value variable for later
    longestVersionLength = 0

    # make sure inputs are strings or string/int lists
    j = 0
    versions = [versionA, versionB]
    while (j < len(versions)):
        # check for string/int list
        if isinstance(versions[j], list): # cast to int
            versions[j] = castItemsToInt(versions[j])
        # check for string
        elif isinstance(versions[j], str): # create list and cast to int
            lst = str.split(versions[j], ".")
            versions[j] = castItemsToInt(lst)
        else:
            Global.endProgram("versionA or versionB isn't a string")

        # update longestVersionLength
        currLength = len(versions[j])
        if (currLength > longestVersionLength):
            longestVersionLength = currLength

        # increment
        j += 1

    # add 0's to each list if needed
    i = 0
    while (i < len(versions)):
        currLength = len(versions[i])
        if (currLength < longestVersionLength):
            extensionLength = longestVersionLength - currLength
            versions[i].extend([0] * extensionLength)
        i += 1

    # set versions list values back to the versionA/B variables
    versionA = versions[0]
    versionB = versions[1]

    # function to check an list of version numbers
    def compareLists(listA:list, listB:list, direction:bool, inclusive:bool) -> bool:
        # function to check a specific value version number
        def compareValues(valueA:int, valueB:int, direction:bool) -> bool:
            if (valueA == valueB): return None # found equal
            # check greater/less than based on direction
            if (direction == True):
                return (valueA > valueB)
            elif (direction == False):
                return (valueA < valueB)

        # go through the values of each list and compare
        for valueA, valueB in zip(listA, listB): # pairs the list for iteration
            condition = compareValues(valueA, valueB, direction) # doesn't check inclusion
            if (condition != None): # this means the current majority version already meets the condition and no further comparison is needed
                return condition
            # the values dont yet meet the condition (they are equal)
        # all values were equal 
        return inclusive # return inclusion, since we know the status of "if they are equal" we just now need to say whether or not we wanted to see that as true or false

    # change inclusive (to false) if it's none and direction is set
    if (inclusive == None) and (direction != None): 
        inclusive = False 

    # actually compare them
    if (direction == None): # check equality (as long as parameters are right)
        if (inclusive != None): # can't set inclusive if direction is None
            raise ValueError("'inclusive' can't be set if 'direction' is set to None")
        else: # find equality
            return (versionA == versionB)
    else: # non-equal comparison (doesn't mean they actually aren't equal, just to check for it)
        return compareLists(versionA, versionB, direction, inclusive)

def grayscale(image, enhanceBrightness=False):
    """
    Description:
        Turns an image to grayscale
    ---
    Arguments:
        - image : Image <>
        - enhanceBrightness : Boolean <False>
            - determines whether the image should be brighened after being turned grayscale
    ---
    Returns:
        - Image
    """
    image = image.convert("RGBA")

    i = 0
    while (i < image.width):
        j = 0
        while (j < image.height):
            currPixel = image.getpixel((i, j))
            if (currPixel[3] == 0):
                j += 1
                continue
            lightness = int(currPixel[0] * 299/1000 + currPixel[1] * 587/1000 + currPixel[2] * 114/1000)
            if (enhanceBrightness):
                lightness = (lightness + 50) if ((lightness + 50) < 255) else 255 # add 50 to lightness or max it out if it's too bright
            image.putpixel((i, j), (lightness, lightness, lightness, currPixel[3])) # add them to the color image
            j += 1
        i += 1
    return image

def getOpacityTexture(image, getOpacityPortion, *, levelOfDetection = 10, doZeroDetection=False):
    """
    Description:
        Returns either the opacity portion or inverse-opacity portion of the input image
    ---
    Arguments:
        - image : Image <>
            - the input image
        - getOpacityPortion : Boolean <>
            - True: returns the opacity (clear) portion of the image
            - False: returns the inverse-opacity (visible) portion of the image
        - levelOfDetection : Integer <10>
            - the level of alpha detection up from 0 to include when defining portions of the image
        - doZeroDetection : Boolean <False>
            - determines whether invisible pixels are used when determining the opacity texture
            - using this will mean all invisible pixels are turned to white, but this also means all pixels will be accounted for, even completely invisible ones
    ---
    Returns:
        - Image
    """
    finalImage = blankImage(image.size)

    i = 0
    while (i < image.width):
        j = 0
        while (j < image.height):
            currPixel = image.getpixel((i, j))
            if (currPixel[3] == 0) and (doZeroDetection == False): # if pixel is alpha
                j += 1
                continue
            elif ((currPixel[3] < levelOfDetection) and (getOpacityPortion)): # if the pixel is very clear, but not invisible (true for getting opacity portion)
                finalImage.putpixel((i, j), (currPixel[0], currPixel[1], currPixel[2], 255)) # add the pixel, but with no opacity
            elif ((currPixel[3] > levelOfDetection) and (not getOpacityPortion)): # add the opposite (easily visible) pixels (if false)
                finalImage.putpixel((i, j), (currPixel[0], currPixel[1], currPixel[2], 255)) # add the pixel, but with no opacity

            j += 1
        i += 1

    return finalImage

def getImageNoOpacity(image, *, doZeroDetection=False):
    """
    Description:
        Takes the input image and returns it with no opacity
    ---
    Arguments:
        - image : Image <>
        - doZeroDetection : Boolean <False>
            - determines whether invisible pixels are used when determining the texture
            - using this will mean all invisible pixels are turned to white, but this also means all pixels will be accounted for, even completely invisible ones
    ---
    Returns:
        - Image
    """
    i = 0
    while i < image.width:
        j = 0
        while j < image.height:
            currPixel = image.getpixel((i, j))
            if (currPixel[3] == 0) and (doZeroDetection == False):
                j += 1
                continue
            image.putpixel( (i, j), tuple(list(currPixel)[:3] + [255]) ) # converts pixel to list and slices it then appends a 255 (no opacity) value to it and converts it back to a tuple and pastes it back to the current pixel
            j += 1
        i += 1
    return image

def changeSingularSize(num: int):
    if (si.verifyPowerOfTwo(num, "sigularSizeOnTexSheet", overrideMinimum=8) == True): # verifies power of two and allows min of 8
        global singularSizeOnTexSheet
        singularSizeOnTexSheet = si.convertInt(num)

def getWiiuNameFromAbstract(locAddon):
    """
    Description:
        Picks the wiiu file name out of the loc addon path
    ---
    Arguments:
        - locAddon : String <>
    """
    wiiuNameKey = str.split(locAddon, "\\")
    return wiiuNameKey[len(wiiuNameKey) - 1]

def forEveryPixel(image: Image, function, useExistingImage: bool=False, imageConversionMode: str="RGBA", arguments: tuple=None) -> Image:
    """
    Description:
        Do a certain function for every pixel in an image
    ---
    Arguments:
        - image : Image <>
        - function : Function <>
            - Description:
                - Function that will be ran for each pixel of the image
            - Arguments:
                - "pixel" : Tuple
                - "x" : Integer
                - "y" : Integer 
                - "image" : Image
                - "args" : Tuple
            - Returns:
                - Tuple
        - useExistingImage : Boolean <False>
            - True: pastes changes onto a copy of the exisitng image
            - False: pastes changes onto an empty image
        - imageConversionMode : String <RGBA>
            - Sets the conversion mode for the image before it is processed
        - arguments : Tuple <>
            - A tuple for sending arguments into the program to be bassed to the function
    ---
    Returns:
        - Image
    """
    newImage = blankImage(image.size, doResize=False) if (useExistingImage == False) else image.copy() # uses the specified type of base image
    image = image.convert(imageConversionMode)

    i = 0
    while (i < image.width):
        j = 0
        while (j < image.height):
            currPixel = image.getpixel((i, j))
            newImage.putpixel((i, j), function(currPixel, i, j, image, arguments))

            j += 1
        i += 1

    return newImage

def tupleIsPosition(tup:tuple) -> bool:
    """
    Description:
        Verifies that a tuple is a position (length of 2, all ints)
    ---
    Arguments:
        - tup : Tuple <>
    ---
    Returns:
        - Boolean, true if correctly formatted
    """
    if (not isinstance(tup, tuple)): # provided tup value isn't a tuple
        return False
    if (len(tup) != 2) or any(not isinstance(value, int) for value in tup): # provided tuple isn't correctly formatted
        return False
    return True

class SheetExtractor():
    def __init__(self, 
                imagePathOrSize:Union[Image, Path, tuple[int, int]],
                subImageSize:tuple,
                wiiuName:str=None,
                type:str=None,
                expectedSize:tuple=None,
                doVersionPatches:bool=True,
                doPrint:bool=False,
                dox16Handling:bool=True):
        """
        Description:
            Creates a class holding an image in sheet format which can be used to non-destructively extract sub-images from
        ---
        Arguments:
            - imagePathOrSize : Image, Path or Tuple <>
                - an Image, Path or tuple of ints length 2 variable which the sheet originates from or determines the size of the image
            - subImageSize : Tuple <>
                - must be a tuple of length 2
                - determines the size of sub-images on the sheet
                - is NOT required to be exactly sized to the sheet (sub-images can be cut off at the edges)
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
        """        
        # verify or try to read image
        image = None
        if tupleIsPosition(imagePathOrSize): # size tuple
            image = blankImage(imagePathOrSize)
        elif isinstance(imagePathOrSize, Path): # path
            if any(value is None for value in (wiiuName, type, expectedSize)): 
                Global.endProgram("attempting to read image from path (in SheetExtrator) but required parameters have not been set for reading")
            image = readImageSingular(wiiuName, imagePathOrSize.getPath(), type, expectedSize, doVersionPatches=doVersionPatches, doPrint=doPrint, dox16Handling=dox16Handling)
        elif isinstance(imagePathOrSize, Image): # image
            image = imagePathOrSize
        else: 
            Global.endProgram("the provided imageOrPath was not an image or a path")
        self.sheet = image

        # check formatting of subImageSize
        if (not tupleIsPosition(subImageSize)):
            Global.endProgram("subImageSize (of SheetExtractor) isn't a tuple of the correct format")
        self.sizeX = subImageSize[0]
        self.sizeY = subImageSize[1]        

    def _tuplePositionCheck(self, pos) -> None:
        if (not tupleIsPosition(pos)):
            Global.endProgram("provided value isn't a tuple of the correct format")

    def _intCheck(self, value) -> None:
        if (not isinstance(value, int)):
            Global.endProgram("the provided value isn't an int")

    def getPixelXOf(self, x:int) -> int:
        """
        Description:
            gets the pixel position based on assuming the provided value is an x value
        ---
        Arguments:
            - x : int <>
        ---
        Returns:
            - integer, pixel position
        """
        self._intCheck(x)
        return self.sizeX * x
    
    def getPixelYOf(self, y:int) -> int:
        """
        Description:
            gets the pixel position based on assuming the provided value is a y value
        ---
        Arguments:
            - y : int <>
        ---
        Returns:
            - integer, pixel position
        """
        self._intCheck(y)
        return self.sizeY * y

    def getPixelPositionOf(self, pos:tuple) -> tuple[int, int]:
        """
        Description:
            gets the pixel position of the provided sheet position
        ---
        Arguments:
            - pos : Tuple <>
                - must be a position tuple (length 2, ints only)
        ---
        Returns
            - Tuple of form (int, int)
        """
        self._tuplePositionCheck(pos)
        return (self.getPixelXOf(pos[0]), self.getPixelYOf(pos[1]))

    def extract(self, pos:tuple) -> Image:
        """
        Description:
            Extracts an image out of the sheet from the given position
        ---
        Arugments:
            - pos : Tuple <>
                - must be a position tuple (length 2, ints only)
        ---
        Returns:
            - Image
        """
        # check pos format and get positions
        pixelPos = self.getPixelPositionOf(pos)

        # check if position is inside of the sheet
        if (pixelPos > self.sheet.size):
            raise ValueError("provided pos results in a pixel position outside of the image sheet")

        # define crop outer edge
        cropEdge = [(pixelPos[0] + self.sizeX), (pixelPos[1] + self.sizeY)]
        # check if the crop is inside of the sheet and crop down
        if (cropEdge[0] > self.sheet.width): cropEdge[0] = self.sheet.width
        if (cropEdge[1] > self.sheet.height): cropEdge[1] = self.sheet.height
        # define crop box
        cropBox = pixelPos + tuple(cropEdge)

        # crop and return image
        return self.sheet.crop(cropBox)

    def insert(self, pos:tuple, image:Image, isDestructive:bool=True) -> Union[None, Image]:
        """
        Description:
            Inserts an image onto the sheet at the given position
        ---
        Arugments:
            - pos : Tuple <>
                - must be a position tuple (length 2, ints only)
            - image : Image <>
            - isDestructive : Bool <False>
                - True: returns none and inserts the image onto the stored sheet
                - False: returns the new image instead of inserting on the stored sheet
        """
        # check pos format and get positions
        pixelPos = self.getPixelPositionOf(pos)

        # check if position is inside of the sheet
        if (pixelPos > self.sheet.size):
            raise ValueError("provided pos results in a pixel position outside of the image sheet")
        
        # check if the image is an image
        if (not isinstance(image, Image)):
            Global.endProgram("image value was not an Image")

        # insertion based on destructive status
        if (isDestructive == True):
            self.sheet.paste(image, pixelPos)
        else:
            sheet = self.sheet.copy()
            sheet.paste(image, pixelPos)
            return sheet

    def getSheet(self) -> Image:
        """
        Description:
            Returns the sheet image
        ---
        Returns:
            - Image, sheet image
        """
        return self.sheet
