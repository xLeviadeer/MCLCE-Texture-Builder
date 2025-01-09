import Logger as log
from Logger import print
import random
from typing import Union

class NoRandomValuesAvailableException(Exception):
    pass

class RandomAlreadyUsedExeption(Exception):
    pass

class Random():
    # amountUsed
    # __min
    # __max
    # __brackets

    def __init__(self, __min:int=0, __max:int=1, clsOrUsedNums=None):
            """
            Description:
                Creates a random class for bracket based randomization using a list of already used values
            ---
            Arguments:
                - __min : Integer <0>
                    - sets a default __min to use, inclusive
                - __max : Integer <0>
                    - sets a default __max to use, inclusive
                - clsOrUsedNums : Random, Tuple or List <>
                    - must be either a Random class or Tuple or List
                    - Random: creates a new class using the provided one (copies)
                    - Tuple or List: creates a new class using the provided values; removes values not within __min/__max
                    - None: creates a new class with no prexisting values
            """

                    # set value for __min
            
            print("SETTING UP CLASS", log.DEBUGBRACKETRANDOM)

            # self executed default
            self.__selfExecuted = False

            # set value for __min
            if isinstance(__min, int):
                self.__min = __min
            else:
                raise TypeError(f"could not create class Random based on provided value for __min of (incorrect) type {type(__min)}")
            
            # set value for __max
            if isinstance(__max, int):
                self.__max = __max
            else:
                raise TypeError(f"could not create class Random based on provided value for __max of (incorrect) type {type(__max)}")

            # check bounding of __min/__max
            if (self.__min >= self.__max):
                raise ValueError("__min value is the same or greater than the __max value; __min must be less than the __max")

            # determine what type of value clsOrUsedNums is
            if isinstance(clsOrUsedNums, Random): # if class, copy
                self.amountUsed = clsOrUsedNums.amountUsed
                self.__brackets = clsOrUsedNums.__brackets
            elif isinstance(clsOrUsedNums, tuple) or isinstance(clsOrUsedNums, list): # if list/tuple, create brackets
                if all(isinstance(value, int) for value in clsOrUsedNums):
                    # -- prepare values --

                    # set empty brackets and amountUsed value
                    self.__brackets = {}
                    self.amountUsed = len(clsOrUsedNums)

                    # prune unwanted values (diplciates, out of range)
                    used = set(clsOrUsedNums) # remove duplicates, convert to set
                    used = [num for num in used if ((self.__min <= num) and (num <= self.__max))] # remove values that are out of range and convert to list
                    used = sorted(list(used)) # sort list

                    # -- create brackets from used numbers --

                    # for every used number
                    i = 1
                    buildIndex = 0
                    buildValue = 0
                    while i < len(used): # runs 1 extra time to include __max
                        # define curr and last
                        currNum = used[i]
                        lastNum = used[i - 1]

                        # check differences and act accordingly
                        currDifference = (currNum - lastNum)
                        print(f"i as {i} where currDifference is {currDifference} of set ({lastNum}, {currNum})", log.DEBUGBRACKETRANDOM)
                        if (currDifference <= 1):
                            print("found 1 or less difference", log.DEBUGBRACKETRANDOM, 1)
                            if (buildValue == 0):
                                print(f"build value was 0, changing index to {i}", log.DEBUGBRACKETRANDOM, 2)
                                buildIndex = lastNum
                            buildValue += 1
                            print(f"build value: {buildValue}", log.DEBUGBRACKETRANDOM, 1)
                        else:
                            if (buildValue != 0):
                                print(f"passed bracket, setting {buildIndex} to value {buildValue + 1}", log.DEBUGBRACKETRANDOM, 1)
                                self.__brackets[buildIndex] = buildValue + 1 # + 1 to include the initial value, not just length addon
                                buildValue = 0
                            print(f"found standalone index, setting {currNum} to 1", log.DEBUGBRACKETRANDOM, 1)
                            self.__brackets[lastNum if (i == 1) else currNum] = 1

                        # increment
                        i += 1

                    # once completed loop
                    if (buildValue != 0): # if the last value was part of an exclusion bracket
                        print(f"final bracket, setting {buildIndex} to value {buildValue}", log.DEBUGBRACKETRANDOM)
                        self.__brackets[buildIndex] = buildValue + 1 # + 1 to include the initial value, not just length addon
                else:
                    raise TypeError(f"could not create class Random because all values in the ...UsedNums are not ints")
            elif (clsOrUsedNums == None): # if none, blank
                self.amountUsed = 0
                self.__brackets = {}
            else:
                raise TypeError(f"could not create class Random based on provided value for clsOrUsedNums of (incorrect) type {type(clsOrUsedNums)}")

    def _alreadyUsedInBracket(self, num):
        for index, value in self.__brackets.items():
            if (index <= num) and (num <= (index + value - 1)):
                return True
        return False

    def addUsedValues(self, usedValues:Union[int, tuple]):
        """
        Description:
            adds a value or a tuple of multiple values to the list of unavailable values
        ---
        Arguments
            - usedValues : Integer or Tuple <>
                - a single or tuple of values to add
        """
        
        print("ADDING USED VALUES", log.DEBUGBRACKETRANDOM)
        print(f"bracket before: {self.__brackets}", log.DEBUGBRACKETRANDOM, 1)

        # turn int into tuple for processing
        if isinstance(usedValues, int):
            usedValues = (usedValues, )

        # for each number used
        for num in usedValues:
            # errors about type and range for tupled nums
            if not isinstance(num, int):
                raise TypeError(f"the provided value (of type {type(num)}) {num} is not an int")
            if (num < self.__min) or (num > self.__max):
                raise ValueError(f"the provided value {num} is not in range (above or below the __min or __max)")
            if (self.__selfExecuted == False):
                if self._alreadyUsedInBracket(num):
                    raise RandomAlreadyUsedExeption(f"the provided value ({num}) has already been used")
            
            # update amount used
            self.amountUsed += 1

            # update brackets
            bracketsAsItems = list(self.__brackets.items()) # convert brackets to a list of tuples
            for i in range(len(bracketsAsItems) + 1):
                # prev, curr and next
                prevItem = bracketsAsItems[i - 1] if (i != 0) else (self.__min - 3, 2) # use normal except first value is __min - 3 (always ignored)
                currItem = bracketsAsItems[i] if (i < len(bracketsAsItems)) else (self.__max + 3, 2) # use normal except last value is __max + 3 (always ignored)
                # rename values for easier use
                prevIndex = prevItem[0]
                prevValue = prevItem[1]
                nextIndex = currItem[0]
                nextValue = currItem[1]
                
                # check to ensure we are in the right area before proceeding (skips all incorrect positions)
                if (prevIndex > num) or (nextIndex < num): continue # curr must be greater and prev must be smaller
                print(f"found correct position ({prevIndex}, {nextIndex})", log.DEBUGBRACKETRANDOM, 1)

                # get checks and apply to self.__brackets accordingly
                lowerCheck = ((num - (prevIndex + prevValue - 1)) <= 1) # includes prevValue to accurately check distance
                    # (-1 to correct their weird adding 1 stuff from earlier)
                higherCheck = ((nextIndex - num) <= 1)
                # if prev and next indexes are within a difference of 1
                if lowerCheck and higherCheck: # merge higher and lower together
                    print("running lower and higher logic", log.DEBUGBRACKETRANDOM, 1)
                    self.__brackets[prevIndex] = prevValue + nextValue + 1 # grow the lower bracket by the higher bracket value + 1
                    if (nextIndex in self.__brackets.keys()): # check to make sure its in the dict bc of __max
                        del self.__brackets[nextIndex] # remove higher bracket
                elif lowerCheck: # merge with lower
                    print("running lower logic", log.DEBUGBRACKETRANDOM, 1)
                    self.__brackets[prevIndex] = prevValue + 1 # grow the lower bracket by 1
                elif higherCheck: # merge with higher
                    print("running higher logic", log.DEBUGBRACKETRANDOM, 1)
                    self.__brackets[nextIndex - 1] = nextValue + 1 # create a new bracket one below the higher bracket and set it to the higher bracket value + 1
                    if (nextIndex in self.__brackets.keys()): # check to make sure its in the dict bc of __max
                        del self.__brackets[nextIndex] # remove the higher bracket
                else: # standalone
                    print("running standalone logic", log.DEBUGBRACKETRANDOM, 1)
                    self.__brackets[num] = 1 # create a new bracket with value 1

                # break, because we found and applied the value
                break

        # sort dictionary after additions
        self.__brackets = dict(sorted(self.__brackets.items()))
        # no return because brackets is directly updated
        print(f"bracket after: {self.__brackets}", log.DEBUGBRACKETRANDOM, 1)

    def getRandom(self):
        """
        Description:
            gets a new random value using brackets based on the used values
        ---
        Returns:
            - a random Integer in the specified range which has not already been chosen before
        """
        
        print("GETTING RANDOM", log.DEBUGBRACKETRANDOM)

        # find ranges
        rangeOfValues = (self.__max - self.__min)
        amountOfAvailableValues = rangeOfValues - self.amountUsed

        # if the first bracket is the size of all possible randoms (which means it's the only value)
        if (self.__min in self.__brackets): # only check if the __min is in the brackets
            if (self.__brackets[self.__min] == (rangeOfValues + 1)): # +1 to account for the weird stuff you do with 1 (as 0) when creating brackets
                raise NoRandomValuesAvailableException("there are no available random values left; all random values have been exhausted")

        # find a random number of the right weight
        randomValueWithMinOffset = random.randint(0, amountOfAvailableValues) + self.__min

        # find an available random value
        availableValue = randomValueWithMinOffset
        print(f"selected prospective available value of {availableValue}", log.DEBUGBRACKETRANDOM)
        for index, value in self.__brackets.items(): # for every element in the dict
            if (index > availableValue): # break if the prospective available value is smaller than the first item in brackets
                break
            print(f"running for {index}: {value}", log.DEBUGBRACKETRANDOM)

            # offset the value based on the current bracket
            availableValue += value
            print(f"curr prospective of {availableValue}", log.DEBUGBRACKETRANDOM, 1)

            # break if not in brackets dict (dont continue offsetting)
            if not self._alreadyUsedInBracket(availableValue):
                break

        # update used and brackets with the found number (disables the double-check of alreadyUsedInBracket temporarily)
        print(f"selected final available value of {availableValue}", log.DEBUGBRACKETRANDOM)
        self.__selfExecuted = True
        self.addUsedValues(availableValue)
        self.__selfExecuted = False

        # return
        return availableValue
    
    def fill(self, length:int=None):
        """
        Description
            returns a list filled with the remaining and non repeating values
        ---
        Arguments:
            - length : Integer <None>
                - None: creates a list of size of all remaining values
                - Integer: creates a list of the provided length; length must be less than the amount of remaining values
        ---
        Returns:
            - list filled with non repeating values in random order
        """

        # remaining
        amountOfRemainingValues = ((self.__max - self.__min) - self.amountUsed) + 1

        # logic for length
        if not isinstance(length, int) and (length != None):
            raise ValueError("provided 'length' value was not an int")
        amountToGenerate = amountOfRemainingValues if (length == None) else length

        # generate fill list
        lst = []
        for _ in range(amountToGenerate):
            lst.append(self.getRandom())
        return lst