# handles reads and writes of json files

import Global
import collections
import json
import ijson
from mergedeep import merge
from . import Logger as log
from CodeLibs.Logger import print
working = Global.getMainWorkingLoc()

# --- READS ---

class keyDoesntExistException(Exception):
    pass

def _split(prefix, isArray):
    """
    Description:
        Keeps periods between values that are only numbers
    """
    arr = []
    removal = []
    indexOfFirstRemoval = None
    i = -1
    for item in str.split(prefix, "."):
        if item.isdigit(): # if the string is a number
            if indexOfFirstRemoval == None: # if the index hasn't been set
                indexOfFirstRemoval = (i + 1)
            removal.append(item)
        else:
            arr.append(item) # remove from arr
        i += 1
    if (len(removal) > 0): # if any numeric was found
        arr.insert(indexOfFirstRemoval, ".".join(removal))
    if (isArray == True): # fix the "item" prefix array problem
        arr = arr[:-1]
    return arr

def _constructJson(currJson, prefix, value):
    """
    Description:
        Constructs a new dictionary element from the prefix and values and deep merges with the existing dictionary
    """
    print(f"current module: {prefix}, {value}", log.DEBUGTWO)

    newJson = {} # used for both methods
    def updateNewJson(prefixAt, value): # updates and check if the value is an array to change processing
        if (type(value) is list): # is a list
            try:
                currPair = _removeFromTopJson(currJson, prefix)
                # currPair could be found
                if (type(currPair) is list): # array already exists
                    newJson[prefixAt] = currPair + value
            except keyDoesntExistException: # currPair couldn't be found (doesn't exist yet)
                newJson[prefixAt] = value
        else: # not a list
            newJson[prefixAt] = value

    if (len(prefix) == 1): # if there are no prefixes left
        updateNewJson(prefix[0], value) # only prefix (set to value)
        merge(currJson, newJson)
        print(f"only one prefix left, returning: {currJson}", log.DEBUGTWO, 1)
        return currJson
    else:
        print("found multiple prefixes, recursing", log.DEBUGTWO)
        updateNewJson(prefix[-1:][0], value) # get last value in prefix (set to value)
        prefix = prefix[:-1] # remove from prefix
        return _constructJson(currJson, prefix, newJson)

def _filterFromJson(ijsonFile, key):
    """
    Description:
        Filters to only collect json elements that are part of the desired object
    """
    # map_key event is an object
    # otherwise, the event is the type name of an object
    finalJson = {}
    found = False
    isCurrentlyArray = False
    for prefix, event, value in ijsonFile: # for the json file
        prefixArr = _split(prefix, isCurrentlyArray)
        if (prefixArr == key): # check if it's not a map end or start and the prefix matches
            match (event):
                case "start_map":
                    found = True
                    continue # ensures that found doesn't run on the starting key
                case "start_array":
                    # the same as normal but array
                    found = True
                    isCurrentlyArray = True
                    continue
                case "end_map":
                    break # found doesn't need to be set to false because the loop is broken
                case "end_array":
                    found = False
                    continue
                case _: # the value is singular; there is only one value (a key value pair)
                    found = True
        if ((found == True)): # if it's found
            # check if the value is an invalid event before continuing
            match (event):
                case "start_map":
                    continue
                case "end_map":
                    continue
                case "map_key":
                    continue
                case "start_array":
                    isCurrentlyArray = True
                    continue
                case "end_array":
                    isCurrentlyArray = False
                    continue

            print(f"\n{prefix}, {event}, {value}", log.DEBUGTWO)
            value = value if (isCurrentlyArray == False) else [value] # change value to be in an array isCurrentlyArray is True
            finalJson = _constructJson(finalJson, prefixArr, value)
    return finalJson

def _removeFromTopJson(currJson, prefix):
    """
    Description:
        Removes values from the top of the dictionary
    """
    if (prefix[0] not in currJson):
        raise keyDoesntExistException()
    if (len(prefix) == 1): # no more keys left
        return currJson[prefix[0]] # reduce
    else: # keys left
        currJson = currJson[prefix[0]] # reduce
        prefix = prefix[1:] # update prefix
        return _removeFromTopJson(currJson, prefix)

# read whole file
def readAll(path):
    if (not path.endswith(".json")): path = path + ".json"
    with open(working + path, 'r') as file:
        return json.load(file)

# reads for a specific part of depth 
#   (legacy method, not sure if the old method is faster. The new method wont load all values in memory at once, just the needed ones. Though it adds a whole hell of a lot of processing overhead)
def readForLegacy(path, arr):
    if (not path.endswith(".json")): path = path + ".json"
    if (not isinstance(arr, collections.abc.Sequence)): print(f"readFor: \"{str(arr)}\" is not an array or string", log.EXIT); exit() # not array or string
    if (isinstance(arr, str)): arr = [arr] # if string, turn to array
    with open(working + path, 'r') as file:
        content = json.load(file)

        while len(arr) > 0:
            content = content[arr.pop(0)]
        return content

def readFor(path, arr):
    if (not path.endswith(".json")): path = path + ".json"
    if (not isinstance(arr, collections.abc.Sequence)): print(f"readFor: \"{str(arr)}\" is not an array or string", log.EXIT); exit() # not array or string
    if (isinstance(arr, str)): arr = [arr] # if string, turn to array
    with open(f"{working}{path}", 'r') as file:
        # new processing here
        content = _filterFromJson(ijson.parse(file), arr)
        content = _removeFromTopJson(content, arr)
        return content

# --- WRITES ---

def writeAll(path, content):
    """
    writes to the working directory + the specifified path
    """
    if (not path.endswith(".json")): path = path + ".json"
    with open(working + path, 'w') as file:
        file.write(json.dumps(content))

def writeAllBase(path, content):
    """
    writes to the specified path
    """
    if (not path.endswith(".json")): path = path + ".json"
    with open(path, 'w') as file:
        file.write(json.dumps(content))