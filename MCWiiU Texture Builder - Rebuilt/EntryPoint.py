import os
import shutil
import threading
import traceback
import zipfile
import Global
import SizingImage
from CodeLibs import LoadingBar
from CodeLibs import Logger as log
from CodeLibs.Logger import print
from builtins import type as typeof
from Utility import compareVersions
from SupportedTypes import supportedVersions

# entry point class to be extended for use as different entry points
class EntryPoint():

    # init function collects values out of order
    def __init__(self,
                executedFromC,
                errorMode,
                processingSize,
                debug, # enables all print statements if true
                inputPath,
                inputPathType,
                inputGame,
                inputVersion,
                outputPath,
                outputStructureIndex,
                outputDrive,
                mainLoc=None,
                logging=None,
                isDirectPath=False, # whether or not the path is exactly the path with no excess folders or not
                showTracebacks=False,
                useErrorTexture=False) -> None:
        # function for casting with errors easily
        def cast(type:typeof, value:object, nullable:bool=False):
            errorMessage = f"could not cast variable {value} to type {type}"

            # allow nullability
            if (nullable == True):
                if (value == None):
                    return value

            # casting required (same type)
            if (type is typeof(value)):
                return value
            # casting logic for string -> boolean
            elif (type is bool) and (typeof(value) is str):
                if (value.lower() == "true"):
                    return True
                elif (value.lower() == "false"):
                    return False
                else:
                    Global.endProgram(errorMessage) 
            # casting logic for string -> int
            elif (type is int) and (typeof(value) is str):
                try:
                    return type(value)
                except ValueError:
                    Global.endProgram(errorMessage)
            else:
                Global.endProgram(errorMessage)

        # values must be the correct type (due to casting) when they exit init

        self.executedFromC = cast(bool, executedFromC)
        self.errorMode = cast(str, errorMode)
        self.processingSize = cast(int, processingSize)
        self.debug = cast(bool, debug)
        
        self.inputPath = cast(str, inputPath)
        self.inputPathType = cast(str, inputPathType)
        self.inputGame = cast(str, inputGame)
        self.inputVersion = cast(str, inputVersion)

        self.outputPath = cast(str, outputPath)
        self.outputStructureIndex = cast(int, outputStructureIndex)
        self.outputDrive = cast(str, outputDrive)

        self.mainLoc = cast(str, mainLoc, nullable=True)
        self.logging = logging # no casting on the list, logging is also not verified that items are correct
        self.isDirectPath = cast(bool, isDirectPath)
        self.showTracebacks = cast(bool, showTracebacks)
        
        Global.useErrorTexture = useErrorTexture

    # output game (index) function
    def _setOutputStructure(self):
        # the key for this match can be found in the uiInput folder under "write.json"
        match (self.outputStructureIndex):
            case 0: # wiiu port pack
                Global.outputStructure = "wiiu"
                Global.outputDump = "build"
            case 1: # wiiu mod pack
                Global.outputStructure = "modpack"
                Global.outputDump = "build"
            case 2: # dump mode
                Global.outputStructure = "wiiu"
                Global.outputDump = "dump"

    # start function will take all of the collected values from init and assign them in the correct order before executing
    def start(self):
        """
        Description:
            Starts the entry point aka runs/executes it
        """

        # IMPORTANT: running programEntry from c# specifically sets all threads to name '__main__' and hence breaks them. 
        # The following value must be set to false if running from C
        Global.executedFromC = self.executedFromC

        # set so that getMainLocWorking() works
        Global.inputPath = self.inputPath

        # doPrint and logging
        if (self.debug == True): # logging true
            log.enableAll()
        elif (self.debug == False):
            if (self.logging != None): # logging false and logging types
                for logType in self.logging:
                    log.setStatus(logType, True)
            else: # logging false and no logging types
                log.disableAll(log.EXIT)

        # check of the version is within the supported window
        if (compareVersions(self.inputVersion, supportedVersions[self.inputGame]["min"], direction=False) 
            or compareVersions(self.inputVersion, supportedVersions[self.inputGame]["max"], direction=True)):
            Global.endProgram(f"version ({self.inputVersion}) too young or old; version not within the supported versions: {".".join(map(str, supportedVersions[self.inputGame]["min"]))} to {".".join(map(str, supportedVersions[self.inputGame]["max"]))}")

        # WIIU TEXTURE GENERATION
        if (self.inputGame == "wiiu"):
            Global.inputPath = "WiiU Default"
            Global.outputPath = self.outputPath
            Global.inputGame = "wiiu"
            self._setOutputStructure()
            Global.outputDrive = self.outputDrive
            Global.mainLoc = self.mainLoc
            SizingImage.changeProcessingSize(self.processingSize)

            # has to be updated after printing is set so print() works
            Global.updateNotFoundImage()

            # multithreading block
            if Global.name == '__main__':

                # has to be imported down here (to ensure that files are read properly based on Global)
                import TextureCreator

                # runner, progressbar stuff
                class Runner(threading.Thread):
                    def __init__(selfRunner):
                        super().__init__()
                        selfRunner.start()

                    def run(selfRunner):
                        # run buildWiiu
                        try:
                            TextureCreator.generateWiiuTextures()
                        except LoadingBar.LoadingBarExitException:
                            print("the program exited safely", log.EXIT)
                            return
                        except:
                            if (self.showTracebacks == True): print(traceback.format_exc(), log.EXIT)
                            Global.bar.close("something went wrong: there was an adverse error")

                        try:
                            Global.bar.close() # will be the last thing that runs
                        except LoadingBar.LoadingBarExitException:
                            # no print for exit
                            return

                # set up the loading bar
                Global.processingLength = TextureCreator.getProcessingLengthDict("java")
                Global.bar = LoadingBar.bar(Global.processingLength["cumulative"])
                Global.bar.run(lambda: Runner())
        # TRANSLATIONAL TEXTURE GENERATION
        else:
            # definitions
            troubleLocatingErrorMessage = "Something went wrong, please try the following before contacting support with the \"help\" button\nIs your input path incorrect?\n\nERROR: pathNotFound - "
            extTempPath = f"{Global.getMainWorkingLoc()}\\extraction_temporary"

            # method which finds where input files are and extracts them
            def extractionMethod(bar):
                def fourthStep():
                    bar.stepCustom(extractionLength / 4)

                def extractTextures(inputPathType):
                    # determine readpath
                    readPath = None
                    if (inputPathType == "zip"):
                        readPath = "assets/minecraft/textures/"
                    elif (inputPathType == "mcpack"):
                        readPath = "textures/"
                    fourthStep()

                    # create folder
                    if (os.path.isdir(extTempPath)): # if directory exists
                        shutil.rmtree(extTempPath)
                    os.mkdir(extTempPath)
                    fourthStep()

                    # extract to folder
                    zip = zipfile.ZipFile(Global.inputPath) # get zip as a whole
                    for file in zip.namelist():
                        if file.startswith(readPath):
                            zip.extract(file, extTempPath)
                    fourthStep()

                    # set input path to this new location
                    Global.inputPath = extTempPath + "\\" + readPath.replace("/", "\\")
                    fourthStep()

                # determine if it's folder or pack and mount to correct location
                if (self.inputPathType == "folder"): # FOLDER
                    if (self.isDirectPath == True):
                        pass # exits the loop to continue normal processing with no changes
                    elif (self.inputGame == "java"): # JAVA FOLDER
                        # -- mount --
                        found = False

                        # if the file is already on point
                        if (Global.inputPath.split("\\")[-1] == "textures"):
                            found = True
                        else: # if the file needs to be mounted inwards
                            # for through possible options
                            inputPosibs = [
                                "assets",
                                "minecraft",
                                "textures"
                            ]
                            i = 0
                            while i < len(inputPosibs): 
                                if (os.path.isdir(Global.inputPath + "\\" + inputPosibs[i])):
                                    Global.inputPath = Global.inputPath + "\\" + str.join("\\", inputPosibs[-(len(inputPosibs) - i):])
                                    found = True
                                    break
                                i += 1
                        
                        # check if the path was found
                        if (found == False):
                            Global.endProgram(f"{troubleLocatingErrorMessage}JAVA_FOLDER")
                    elif (self.inputGame == "bedrock"): # BEDROCK FOLDER
                        # -- mount --
                        found = False

                        # if the file is already on point
                        if (Global.inputPath.split("\\")[-1] == "textures"):
                            found = True

                        # check if the folder contains textures folder
                        if (os.path.isdir(Global.inputPath + "\\textures")):
                            Global.inputPath = Global.inputPath + "\\textures"
                            found = True

                        # check if the path was found
                        if (found == False):
                            Global.endProgram(f"{troubleLocatingErrorMessage}BEDROCK_FOLDER")

                elif (self.inputPathType == ".zip"): # .ZIP
                    # check if the zip contains the textures folder
                    if (zipfile.Path(Global.inputPath, "assets/minecraft/textures/").is_dir() == False): # checks if it DOESN'T exist
                        Global.endProgram(f"{troubleLocatingErrorMessage}ZIP")

                    extractTextures("zip") # sets up the extraction temporary as the input path

                elif (self.inputPathType == ".mcpack"):
                    # check if the mcpack contains textures folder
                    if (zipfile.Path(Global.inputPath, "textures/").is_dir() == False): # checks if it DOESN'T exist
                        Global.endProgram(f"{troubleLocatingErrorMessage}MCPACK")

                    extractTextures("mcpack") # sets up the extraction temporary as the input path

                else:
                    Global.endProgram("Something went wrong, please contact support using the \"help\" button\n\nERROR: inputPathType")

            # Global is set out of order to account for loading bar requiring certain aspects of uiInput to work
            Global.outputPath = self.outputPath
            Global.inputGame = self.inputGame
            Global.inputVersion = self.inputVersion
            Global.errorMode = self.errorMode
            self._setOutputStructure()
            Global.outputDrive = self.outputDrive
            Global.mainLoc = self.mainLoc
            SizingImage.changeProcessingSize(self.processingSize)

            # has to be updated after printing is set so print() works
            Global.updateNotFoundImage()

            # multithreading block
            if Global.name == '__main__':

                import TextureCreator # has to be imported down here (to ensure that files are read properly based on uiInput)

                # runner, progressbar stuff
                class Runner(threading.Thread):
                    def __init__(selfRunner):
                        super().__init__()
                        selfRunner.start()

                    def run(selfRunner):
                        # extract stuff
                        extractionMethod(Global.bar)

                        # run buildWiiu
                        try:
                            TextureCreator.translateForAllTypes()
                        except LoadingBar.LoadingBarExitException:
                            print("the program exited safely", log.EXIT)
                            return
                        except:
                            if (self.showTracebacks == True): print(traceback.format_exc(), log.EXIT)
                            Global.bar.close("something went wrong: there was an adverse error")

                        # remove temporary extraction path if it was made
                        if (os.path.isdir(extTempPath)):
                            shutil.rmtree(extTempPath)

                        try:
                            Global.bar.close() # will be the last thing that runs
                        except LoadingBar.LoadingBarExitException:
                            # no print for exit
                            return

                # set up the loading bar
                Global.processingLength = TextureCreator.getProcessingLengthDict(Global.inputGame)
                totalLength = Global.processingLength["cumulative"]
                extractionLength = totalLength / 4
                if ((self.inputPathType == ".zip") or (self.inputPathType == ".mcpack")):
                    totalLength += extractionLength
                Global.bar = LoadingBar.bar(totalLength)
                Global.bar.run(lambda: Runner())

    # global assignment for testing only
    def testAssign(self):
        """
        Description:
            simply assigns the values to Global so that the program can continue during testing
        """

        Global.executedFromC = self.executedFromC
        Global.errorMode = self.errorMode
        SizingImage.changeProcessingSize(self.processingSize)
        
        Global.inputPath = self.inputPath 
        Global.inputGame = self.inputGame
        Global.inputVersion = self.inputVersion

        Global.outputPath = self.outputPath
        self._setOutputStructure()
        Global.outputDrive = self.outputDrive

        Global.mainLoc = self.mainLoc
        # doPrint and logging
        if (self.debug == True): # logging true
            log.enableAll()
        elif (self.debug == False):
            if (self.logging != None): # logging false and logging types
                for logType in self.logging:
                    log.setStatus(logType, True)
            else: # logging false and no logging types
                log.disableAll(log.EXIT)
