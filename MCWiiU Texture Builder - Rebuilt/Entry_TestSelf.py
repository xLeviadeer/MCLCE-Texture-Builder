from EntryPoint import EntryPoint
from CodeLibs import Logger as log
import Global

# set the name (must be set in the entry file)
Global.name = str(__name__)

# declare new entry point
entry = EntryPoint(
    executedFromC=False,
    errorMode="replace",
    processingSize=16,
    useComplexProcessing=True,
    debug=False,
    
    inputPath="",
    inputPathType="folder",
    inputGame="wiiu",
    inputVersion="1.13.2",
    
    outputPath="F:\\Coding\\B- LeRe\\MCWiiU-Texture-Builder\\MCWiiU Texture Builder - Rebuilt\\output",
    outputStructureIndex=0,
    outputDrive="system",

    logging=[],
    showTracebacks=False,
    isDirectPath=True,
    useErrorTexture=False,
    forceDumpMode=True
)

# run entry point
entry.start()