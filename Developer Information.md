# Developer Information
## How to Execute the Texture Builder From the Backend
To run the TB you must create an instance of `EntryPoint.py` in it's own file.

1. The TB will attempt to multithread if `executedFromC` is not set to `True`. Because of this the first line (besides imports) of the file must be `Global.name = str(__name__)` which is *required* to control multithreading during execution. This line must be in the file that initially runs when starting the program and nowhere else.
2. Declare an `EntryPoint` in the file to determine what settings are used during execution. 
3. Start the program from the `EntryPoint`

Cumulatively, an example looks like
```py
from EntryPoint import EntryPoint
from CodeLibs import Logger as log
import Global

# MUST BE SET AT THE BEGINNING OF MAIN FILE
Global.name = str(__name__)

# declare a new entry point
entry = EntryPoint(
    executedFromC=False,
    errorMode="error",
    useComplexProcessing=False,
    processingSize=16,
    debug=False,
    
    inputPath="C:\\my_cool_path",
    inputPathType="folder",
    inputGame="java",
    inputVersion="1.14",
    
    outputPath="C:\\my_cool_output_path",
    outputStructure="wiiu",
    outputDrive="system",

    logging=[log.CUSTOMFUNCTION],
    showTracebacks=False,
    isDirectPath=True,
    useErrorTexture=False,
    forceDumpMode=False
)

# run entry point
entry.start()
```

Each setting has the following meanings:
- `executedFromC`
    - keep false if executing from backend. controls multithreading
- `errorMode`
    - replace: attempts to build and replace textures which cannot be simply copied
    - error: places an error texture over textures which cannot be simply copied
- `processingSize`
    - controls the expected input size and output size of textures. the TB will upscale/downscale textures of incorrect sizes.
    - integers other than powers of 2 are not supported, and not tested outside of 16 - 64
- `useComplexProcessing`
    - controls whether to use complex processing for certain textures
    - complex processing can result in excessively long (upwards of 8 minutes) processing times if used with large sizes (like x64 or greater)
- `debug`
    - enables all types of logging for debugging
    - included for compadibilty with old versions of the frontend
- `inputPath`
    - filepath to the textures to be translated
- `inputPathType`
    - the type of file/folder the inputPath leads to
    - folder
    - .mcpack
    - .zip
- `inputGame`
    - the game to be translated from
    - java
    - bedrock
    - any lce format
- `inputVersion`
    - the game version of the to be translated textures
- `outputPath`
    - filepath of where to output textures
- `outputStructure`
    - the output file structure, used to determine which ConsoleWriter mode to use
    - selects a build mode (build/dump) and a console to write to
    - options for this are equal to the elements in the list under global/output_structures_\<console\>
- `outputDrive`
    - determines, when using build mode, whether to name the main file as usb or mlc
    - system
    - usb
- `logging` (optional)
    - a list of LoggerModes which would be printed
- `showTracebacks` (optional)
    - whether or not to show tracebacks for debugging
- `isDirectPath` (optional)
    - whether or not (both) inputPath and outputPath are direct paths; paths which lead to the "texture" or "textures" folder exactly.
    - controls whether the program will look for valid subfolders of texture packs to locate the texture pack contents.
- `useErrorTexture` (optional)
    - whether or not to write an error texture when a custom process cannot be found.
    - used for debgugging when adding new supportedTypes to allow the completion of execution even with missing processes.
- `forceDumpMode` (optional)
    - whether to force the program to output in dump mode regardless of the build/dump status.

## Looking to Add Support for Later Versions of Minecraft?
Reference the more in-depth walkthrough of how the TB works [here](https://github.com/xLeviadeer/MCWiiU-Texture-Builder/blob/main/Adding%20CustomProcesses.md) to help develop this program.

## Programmer Information
### Warning About Internal Paths
Paths inside of *internal only* files weren't made with the intention of being used outside of a personal environment and hence may contain specific file-paths which need to be changed in order for the method to function correctly.

### Overview
To run to the TB (texture builder), an `EntryPoint` must be declared. 
- Some examples of this can be found in `Entry_TestJava.py` and `Entry_TestBedrock.py`.
- `Entry_Program.py` is used for running the program from the frontend.
- `Entry_Internal.py` is used to execute backend functions to manage databases and check them for errors.

The TB goes through the following steps during execution
1. **Interpret** settings declared in the `EntryPoint.py`.
2. **Run** the `TextureCreator.py` which is the overall algorithm to translate/convert textures.
    - if a texture which cannot simply be copied is found, run `CustomProcessing/` on it.
3. **Export** the textures to the output folder.

### Sheets vs Abstracts
The TB classifies certain textures as "**sheets**" aka "atlases". Generally, textures which require custom processing that are part of sheets are called "external textures".

The TB classifies certain textures as "**abstract**" aka standalone textures. Abstract textures can also be sheets/atlases if the sheet/atlas contains an animation for a singular texture rather than multiple separate textures.

Both sheets and abstract textures use fundamentally different processing methods to translate hence why they aren't one and the same.

### Program Portions
The TB is divided into a few core portions
- **Frontend** - user interface
- **Backend** - processing, non-user interface
    - **Mount-end** - translating information from the frontend and checking the correctness of it.
    - **Process-end** - process the texture pack according to the databases
    - **Build-end** - proccess textures which cannot be simply copied
    - **Databases** - a set of databases to store information about texture locations and processing specifications
    - **Internal** - test functions and processes for debugging and creating databases

### The Job of Each File
#### EntryPoint.py
Module for defining settings, preparing and executing the program
#### Global.py
Stores run-time specific settings data which can be accessed anywhere in the program
#### Internal.py
*internal only*, holds all debug functions
#### Read.py
Holds functions for reading databases, images, etc.
#### Sheet.py
Sheet extraction class, used for handling (copy, pasting) parts of an image which is a sheet/atlas of multiple textures
#### SizingImage.py
Extends/Replaces PIL's Image class to allow upscaling and downscaling of images
#### SupportedTypes.py
A list of supported types and supported versions the program will run
#### Test_BracketRandom.py
*internal only*, a test file for different implementations of BracketRandom
#### TextureCreator.py
Module to create and write textures.
#### Utility.py
Random utility functions
#### base_textures/
Folder expected to contain base game textures named as `"{version}_{game}"` where the folder directly contains the contents of the "texture" or "textures" folder. Ex. `"./base_textures/1.14_java/block/grass_block.png"` would be a valid path. Contents of the `base_textures` folder aren't provided to ensure the saftey of this program. This folder also contains base game textures
#### CodeLibs > ConsoleWriter.py
Module to organize and format different output write locations.
#### CodeLibs > JsonHandler.py
Module to handle reading, parsing and casting json files.
#### CodeLibs > JsonWritable.py
Contains a class to be extended when creating a class which can be serialized to json and back
#### CodeLibs > LoadingBar.py
Module to create, close and update the LoadingBar window popup.
#### CodeLibs > Logger.py
Extends/Replaces python's `print` function to include multiple different print types which can be enabled or disabled in the `EntryPoint.py` for more effective debugging.
#### CodeLibs > Path.py
Module with class to create and manage filepaths.
#### color_signatures/
*internal only*, folder containing information about the color data of textures for creating `linked_libraries`.
#### CustomProcessing > Custom.py
Handling for locating and executing CustomProcessing file functions.
#### CustomProcessing/
Folder of custom processes for textures which cannot simply be copied separated by game and type.
- **External** - Texture which is part of a large texture sheet (atlas) but requires a rebuilding (translation) process.
- **Abstract** - Texture which is on it's own and requires a rebuilding (translation) process.
- Override - Texture which is on it's own and can replace a texture sheet (atlas).
- **Versional** - Texture which changes processing based on the version. It's important to note that Versional processes are only used if the texture isn't already External or Abstract, in which case the versional difference programming will be within the Abstract or External process.
- **None/Shared** - Inspecific (not directly related to one texture) process for processing multiple of a particular type of texture.
#### equality_libraries/
*internal only* information and databases for comparing the equality of prospective texture libraries and verified (as correct) texture libraries.
#### global/
Small databases containing information that corresponds with the Frontend for display of user options.
#### Info/
Folder containing information about the program or certain processes
#### linking_libraries/
Libraries of data regarding game textures and how to translate them between versions. Generated with assistance via `color_signatures`.
#### output/
*internal only* folder for testing output.
#### python_builder/
*internal only* folder for building the project for the Frontend.
#### resources/
*internal only* files created while making image resources for the program.

## Frontend Information
The frontend barely works and is pretty much thrown together. It's super unorganized and I can't even remember what exactly it does. It takes input from the users, ensures certain settings can only be selected if other settings are right and then executes a process over the command line to the python_builder Entry_Program.exe to translate textures.

The program is designed away from the frontend, where almost all functions are handled in the backend, meaning that anyone can develop their own frontend on top of the backend to make implementation of this program easier for custom frontends.
