from EntryPoint import EntryPoint
from CodeLibs import Logger as log
import Global
import sys

# set the name (must be set in the entry file)
Global.name = str(__name__)

# define args easily
args = sys.argv

# declare new entry point
entry = EntryPoint(
    executedFromC=True,
    errorMode=args[6],
    processingSize=args[11],
    useComplexProcessing=args[12],
    debug=args[10],
    
    inputPath=args[1],
    inputPathType=args[4],
    inputGame=args[3],
    inputVersion=args[5],
    
    outputPath=args[2],
    outputStructure=args[7],
    outputDrive=args[8],

    logging=None, # enforces not printing
    mainLoc=args[9],
    showTracebacks=args[10], # shows tracebacks if debug is enabled
)

# run entry point
entry.start()