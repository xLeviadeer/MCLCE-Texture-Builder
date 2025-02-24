from enum import Enum
import sys
from builtins import print as pyPrint

class _LoggerValue():
    """
    Description:
        Class to house logger status values
    ---
    Other:
        - Class is required so that Enum can have duplicate "values"
    """
    status = None
    syntax = None
    syntaxEnd = None
    isIndentable = None
    isCustom = None
    def __init__(self, status: bool, syntax: str, syntaxEnd: str="", *, isIndentable: bool=False, isCustom: bool=False):
        self.status = status
        self.syntax = syntax
        self.syntaxEnd = syntaxEnd
        self.isIndentable = isIndentable
        self.isCustom = isCustom

    def __str__(self) -> str:
        return f"{self.status}"
    
    def buildSyntax(self, message) -> str:
        return f"{self.syntax}{message}{self.syntaxEnd}"

# Logger Modes
class LoggerMode(Enum):
    """
    Description:
        List of logger type values
    """
    VERYIMPORTANT = _LoggerValue(True, "!! ") # non-exit cases, signifying importance
    IMPORTANT = _LoggerValue(True, "!  ") # non-exit cases, signifying importance
    EXIT = _LoggerValue(True, "EXITED: ") # exit cases
    ERROR = _LoggerValue(True, "---", isIndentable=True) # errors
    WARNING = _LoggerValue(True, " --", isIndentable=True) # warnings
    LOG = _LoggerValue(True, "  -", isIndentable=True) # routine logging
    DEBUG = _LoggerValue(False, "  *", isIndentable=True) # same as log but defaults as off
    NOTE = _LoggerValue(True, "   ", isIndentable=True) # used for prints like doPrint
    PLAIN = _LoggerValue(True, "") # AVOID using
    SECTION = _LoggerValue(True, "\n-----", "-----") # splits prints
    CHANNELONE = _LoggerValue(True, "    +")
    CHANNELTWO = _LoggerValue(True, "   ++")
    CHANNELTHREE = _LoggerValue(True, "  +++")
    # specials
    CUSTOMFUNCTION = _LoggerValue(False, "  *", isIndentable=True, isCustom=True)
    CUSTOMFUNCTIONRECURSION = _LoggerValue(False, "  * (", ")", isIndentable=True, isCustom=True)
    CUSTOMFUNCTIONTIMING = _LoggerValue(False, "  _*", isIndentable=True, isCustom=True)
    PATCHFUNCTION = _LoggerValue(False, "  *", isIndentable=True, isCustom=True)
    CUSTOMWEATHER = _LoggerValue(False, "  '", isIndentable=True)
    DEBUGTWO = _LoggerValue(False, "   *", isIndentable=True)
    DEBUGBRACKETRANDOM = _LoggerValue(False, "  '", isIndentable=True)

# sets mods to the module
module = sys.modules[__name__]
for item in LoggerMode:
    setattr(module, item.name, item.value)

def print(message: str="", mode: LoggerMode=LoggerMode.PLAIN, indent: int=0):
    """
    Description:
        Print to the terminal and use "logger" settings for better debugging
    ---
    Arguments:
        - mode : _LoggerMode <>
            - mode for this print to use
        - message : String <>
    ---
    Other:
        - Prints will not be made if doPrint is not set correctly in uiInput
    """
    # check if it's printable
    logMode = LoggerMode(mode)
    if logMode.value.status == True:
        message = logMode.value.buildSyntax(message)

        # check if mode is indentable
        if (LoggerMode(mode).value.isIndentable == True):
            while indent > 0:
                message = f" {message}"
                indent -= 1

        # print
        pyPrint(message)

def isEnabled(mode: LoggerMode):
    logMode = LoggerMode(mode)
    return (logMode.value.status == True)

def setStatus(mode: LoggerMode, status: bool):
    """
    Description:
        Sets the status of a LoggerMode
    ---
    Arguments:
        - mode : LoggerMode <>
        - status : Boolean <>
    """
    logMode = LoggerMode(mode)
    logMode.value.status = status # changes the value
    setattr(module, logMode.name, logMode.value) # updates the module

    # if the mode is debug, change all custom modes too
    if (logMode == LoggerMode.DEBUG):
        for item in LoggerMode:
            if (item.value.isCustom == True):
                setStatus(item.value, status)

def enableAll():
    """
    Description:
        Enables all LoggerModes
    """
    for item in LoggerMode:
        LoggerMode(item).value.status = True 
        setattr(module, item.name, item.value)

def disableAll(exception: LoggerMode=None):
    """
    Description:
        Disables all LoggerModes
    """
    for item in LoggerMode:
        if (exception != None):
            if (item == LoggerMode(exception)): # will exclude the exception
                continue
        item.value.status = False 
        setattr(module, item.name, item.value)

def debugPrint():
    for item in LoggerMode:
        pyPrint(f"{item.__str__()}: {item.value}")
