from functools import total_ordering
from .localizer import Localizer
from .shift_exception import PyShiftException

##
# Class Named represents a named object such as a Shift or Team.
# 
@total_ordering
class Named():  
    ##
    # Construct a named object
    # @param name Name of object
    # @param description Description of object  
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
        super().__init__()

    def __hash__(self) -> int:
        return hash(self.name)
        
    def __eq__(self, other) -> bool:
        if other is None or not isinstance(other, Named):
            return False
        return self.name == other.name
    
    def __lt__(self, other) -> bool:
        if other is None or not isinstance(other, Named):
            return NotImplemented
        return self.name < other.name
        
    def __str__(self) -> str:
        return self.name + " (" + self.description + ")"
    
    def setName(self, name: str):
        if (name is None):          
            msg = Localizer.instance().messageStr("name.not.defined")
            raise PyShiftException(msg)
        
        self.name = name
        
    def setDescription(self, description: str):
        self.description = description or ""        
    
    ##
    # Compare two Named objects by name
    # @param other Other named object
    # @return -1 less than, 0 if equal, and 1 if greater than by string sort
    def compareName(self, other) -> int:
        return ((self.name > other.name) - (self.name < other.name))
