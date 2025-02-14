from abc import ABC, abstractmethod
from typing import Callable

class JsonWritable(ABC):
    """
    Description:
        abstract class with load and save functionality and a framework for implementing classes which can be written as json
    """

    # - required value override handling -

    def __raiseNotSetMethodError(self, nameOfVariable:str):
        """
        Description:
            raises an exception for the value not being set
        """
        raise NotImplementedError(f"variable '{nameOfVariable}' was not set in the child class of JsonWritable; '{nameOfVariable}' must be set in all child classes as an instance variable")

    def __checkForOverridenGetterOrSetter(self, getterOrSetter:Callable, nameOfVariable:str):
        """
        Description:
            checks if the value exists and then attempts to get it, raising an error if not
        ---
        Arguments:
            - getterOrSetter : Method <>
                - assumes values exist in the class, checking for existence not required
            - nameOfVariable : String <>
                - the name of the backer variable
        ---
        Returns:
            - the value of the variable or otherwise returned value from the method
        """

        try:
            if (not hasattr(self, nameOfVariable)) or (getattr(self, nameOfVariable, "MISSING") == "MISSING"):
                self.__raiseNotSetMethodError(nameOfVariable)
            return getterOrSetter()
        except AttributeError:
            self.__raiseNotSetMethodError(nameOfVariable)

    # - do bypass all check - 

    __doBypassAllCheckName = "_doBypassAllCheck"

    @property
    def doBypassAllCheck(self):
        def get():
            # type check
            if not isinstance(self._doBypassAllCheck, bool):
                raise TypeError(f"value for '{self.__doBypassAllCheckName}' was not of type boolean")
            
            # no errors
            return self._doBypassAllCheck
        return self.__checkForOverridenGetterOrSetter(get, self.__doBypassAllCheckName)
    
    @doBypassAllCheck.setter
    def doBypassAllCheck(self, value):
        def set():
            raise NotImplementedError(f"'{self.__doBypassAllCheckName}' cannot be set by class instances; it should only be set directly (as '{self.__doBypassAllCheckName}') when extending the JosnWritable class")
        self.__checkForOverridenGetterOrSetter(set, self.__doBypassAllCheckName)

    # - structure variable -

    __structureName = "_structure"

    # normal getter for structure
    @property
    @abstractmethod
    def structure(self):
        def get():
            # check type of structure
            if not isinstance(self._structure, dict):
                raise TypeError(f"value for '{self.__structureName}' was not set to a dictionary")
            
            # check if value for doBypass is set (because this value depends on it)
            if (not hasattr(self, self.__doBypassAllCheckName)) or (getattr(self, self.__doBypassAllCheckName, "MISSING") == "MISSING"):
                self.__raiseNotSetMethodError(self.__doBypassAllCheckName)      

            # if bypass all is set to skip
            if (self._doBypassAllCheck == True):
                return self._structure
            else:
                # check to see if all values are accounted for
                # for every instance value self has
                for classVariableName in self.__dict__.keys():
                    # if no values in the structure dict match the current class variable name

                    # skip structure or bypass instance variable
                    if (
                        (classVariableName == self.__structureName)
                        or (classVariableName == self.__doBypassAllCheckName)
                    ): continue

                    # check all values of the structure against the class variable name
                    simplifiedName = classVariableName.replace(f"_{self.__class__.__name__}", "")
                    simplifiedNameNoUnderscores = simplifiedName.replace("_", "")
                    if all(
                            (
                                (simplifiedName != structureDictKey) 
                                and (simplifiedNameNoUnderscores != structureDictKey)
                            ) 
                            for structureDictKey in self._structure.keys()
                        ):
                        raise ValueError(f"'{self.__structureName}' doesn't contain values for all instance variables or at least one name doesn't match "
                            + "exactly between key and variable name. you can disable this check using the _doBypassAllCheck variable.\ncaught on value: "
                            + f"'{classVariableName}'")

                # return 
                return self._structure
        return self.__checkForOverridenGetterOrSetter(get, self.__structureName)

    # stop structure setter from being used 
    @structure.setter
    def structure(self, value):
        def set():
            raise NotImplementedError(f"'{self.__structureName}' cannot be set by class instances; it should only be set directly (as '{self.__structureName}') when extending the JosnWritable class")
        self.__checkForOverridenGetterOrSetter(set, self.__structureName)
