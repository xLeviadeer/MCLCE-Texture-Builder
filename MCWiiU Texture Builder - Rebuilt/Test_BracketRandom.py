from CodeLibs.BracketRandom import Random
#from CodeLibs.BracketRandomAsList import Random
from CodeLibs.BracketRandom import NoRandomValuesAvailableException
import random
import timeit
import psutil
import os

class RegularRandom:
    def __init__(self, min:int, max:int, alreadyUsed:list=None):
        if (alreadyUsed == None):
            self.__alreadyUsed = []
        elif not isinstance(alreadyUsed, list):
            raise ValueError("input for alreadyUsed isn't a list")
        else:
            self.__alreadyUsed = alreadyUsed

        if not isinstance(min, int):
            raise ValueError("input for min isn't an int")
        self.__min = min

        if not isinstance(max, int):
            raise ValueError("input for max isn't an int")
        self.__max = max

    def getRandom(self):
        while True:
            if (len(self.__alreadyUsed) == self.__max + 1):
                raise NoRandomValuesAvailableException("no randoms were left")

            num = random.randint(self.__min, self.__max)

            if (num not in self.__alreadyUsed):
                self.__alreadyUsed.append(num)
                return num

class ChatGPTUniqueRandom:
    # chatgpt code has been modified to include alreadyUsed

    def __init__(self, min_val, max_val, alreadyUsed=None):
        if min_val > max_val:
            raise ValueError("min_val must be less than or equal to max_val")
        
        self.numbers = alreadyUsed if (alreadyUsed != None) else list(range(min_val, max_val + 1))
        random.shuffle(self.numbers)  # Shuffle to randomize order
        self.index = 0  # Pointer to track used values

    def getRandom(self):
        if self.index >= len(self.numbers):
            raise ValueError("No more unique numbers available")  # Prevent reuse

        value = self.numbers[self.index]
        self.index += 1
        return value

RegularRandom = ChatGPTUniqueRandom

process = psutil.Process(os.getpid())

MIN = 0 # min
MAX = 10000 # max
SIZEPERCENTOFPREXISTING = 0.95
RUNTIMES = None # amount of times to run (None will equal the possible values)
PLACESMOVEDFORVISUALIZATION = 5 # how many places to move the value to the left when printing
DOPRINTREGULAR = True # print regular at all
DOPRINTBRACKET = True # print bracket at all
PRINTSAMPLESTEP = 1000 # amount of space between each print; how much space between sampling a value to print (1 will print all)

possibleValues = (MAX - MIN)
if (RUNTIMES == None):
    RUNTIMES = int(possibleValues * (1 - SIZEPERCENTOFPREXISTING))
elif (RUNTIMES > possibleValues):
    raise ValueError("runtimes cannot be more than the amount of possible values")
amountOfPrints = RUNTIMES // PRINTSAMPLESTEP
if (amountOfPrints == 0): amountOfPrints = 1

times = {
    "regular": [],
    "bracket": []
}
memory = {
    "regular": [],
    "bracket": []
}

prexistingRandom = RegularRandom(MIN, MAX)
listOfRandomPrexistingValues = []
for _ in range(int(possibleValues * SIZEPERCENTOFPREXISTING)):
    listOfRandomPrexistingValues.append(prexistingRandom.getRandom())

regular = RegularRandom(MIN, MAX, listOfRandomPrexistingValues)
bracket = Random(MIN, MAX, listOfRandomPrexistingValues)

print("\n--- REGULARS ---")
for i in range(RUNTIMES):
    memoryBefore = process.memory_info().rss / pow(1024, 2)
    regularTime = timeit.timeit(regular.getRandom, number=1)
    memoryAfter = process.memory_info().rss / pow(1024, 2)
    memoryUsed = (memoryAfter - memoryBefore)
    memory["regular"].append(memoryUsed)
    times["regular"].append(regularTime)
    if ((i % PRINTSAMPLESTEP) == 0) and (DOPRINTREGULAR == True):
        print(f"regular: {(regularTime * pow(10, PLACESMOVEDFORVISUALIZATION)):.6f} time memory to complete (sample {(i // (RUNTIMES // amountOfPrints)) + 1}/{amountOfPrints})")

print("\n--- BRACKETS ---")
for i in range(RUNTIMES):
    memoryBefore = process.memory_info().rss / pow(1024, 2)
    bracketTime = timeit.timeit(bracket.getRandom, number=1)
    memoryAfter = process.memory_info().rss / pow(1024, 2)
    memoryUsed = (memoryAfter - memoryBefore)
    memory["bracket"].append(memoryUsed)
    times["bracket"].append(bracketTime)
    if ((i % PRINTSAMPLESTEP) == 0) and (DOPRINTBRACKET == True):
        print(f"bracket: {(bracketTime * pow(10, PLACESMOVEDFORVISUALIZATION)):.8f} time to complete (sample {(i // (RUNTIMES // amountOfPrints)) + 1}/{amountOfPrints})")

def avg(lst:list):
    return sum(lst) / len(lst)

print()
print(f"average regular time: {(avg(times["regular"]) * pow(10, PLACESMOVEDFORVISUALIZATION)):.6f}")
print(f"average bracket time: {(avg(times["bracket"]) * pow(10, PLACESMOVEDFORVISUALIZATION)):.6f}")

print()
print(f"average regular memory: {(avg(memory["regular"]) * pow(10, PLACESMOVEDFORVISUALIZATION)):.6f}")
print(f"average bracket memory: {(avg(memory["bracket"]) * pow(10, PLACESMOVEDFORVISUALIZATION)):.6f}")