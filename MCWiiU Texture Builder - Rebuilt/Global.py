# IMPORTANT: all variables in global must be set at startup because they have no default value and will cause errors

from CodeLibs import LoadingBar
from CodeLibs import Logger as log
from CodeLibs.Logger import print
import os
from sys import exit
from SizingImage import SizingImage as Image

# --- GENERAL SETTINGS ---

# should control the use of multithreading
executedFromC = False
def useMultithreading(): not executedFromC

# the error processing mode the program uses when an error occurs (write an error texture or replace it with the known info)
errorMode = None # replace or error

# the debugging status of the program in regards to writing error textures for unknown custom functions
useErrorTexture = None # true or false

# --- INPUT SETTINGS ---

# the input path the program will use to search for convertable files
inputPath = None 

# the game the program will assume that the input textures come from
inputGame = None # java or bedrock

# the version the program will assume that the input textures come from
inputVersion = None # version number

# --- OUTPUT SETTINGS ---

# the output path the program will use to export files to
outputPath = None

# whether or not the program will use the output file structure or dump files
outputDump = None # dump or build

# the file structure (export preset) that the program will use to write files
outputStructure = None # wiiu, modpack, (etc.)

# the usb or system location to write files to (only used if not using dump mode)
outputDrive = None # usb or sys

# --- RESOURCES ----

# name of the currentlty running thread
name = None

# an instance of the loading bar set from the entry point
bar = None
def endProgram(message:str=None): # ends the program
    if (not isinstance(bar, LoadingBar.bar)):
        print(message, log.EXIT)
        exit()
    else:
        bar.close(message)

# a list of notExpected errors
notExpectedErrors = []

# a list of incorrectSizeErrors
incorrectSizeErrors = []

# a multidimensional dictionary containing information about the current process length 
processingLength = {}

# the working directory with slight changes based on where the program is executed from
mainLoc = None
def getMainWorkingLoc():
    if (mainLoc == None):
        return os.getcwd()
    else:
        return os.getcwd() + "\\" + mainLoc

# the notFound image
notFoundImage = None
try:
    notFoundImage = Image.open(getMainWorkingLoc() + "\\base_textures\\notFound.png") # not found image
except:
    pass # do, nothing, cannot print error without creating errors
def updateNotFoundImage(): # updates the notFoundImage location
    try:
        global notFoundImage
        notFoundImage = Image.open(getMainWorkingLoc() + "\\base_textures\\notFound.png")
    except:
        print("attempt to update the notFound image failed", log.EXIT)
        try: # attempts to close the bar, but it may not exist
            bar.close()
        except:
            exit()

# the error image
    # error image is only setup to work while in wiiuEntry, debug mode
errorImage = None
try:
    errorImage = Image.open(getMainWorkingLoc() + "\\base_textures\\error.png")
except:
    pass # this will absolutely break stuff if you try to use errorImage from programEntry