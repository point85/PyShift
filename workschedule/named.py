from abc import ABC

from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift_exception import PyShiftException

##
# Class Named represents a named object such as a Shift or Team.
# 
class Named(ABC):    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
        super().__init__()

    def __hash__(self):
        return hash(str(self.name))
        
    def __eq__(self, other):
        answer = False
    
        if (other is not None and isinstance(other, Named)):
            # same name
            if (self.name == other.name):
                answer = True
        return answer
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name     
        
    def __str__(self):
        return self.name + " (" + self.description + ")"
    
    def setName(self, name):
        if (name is None):          
            msg = Localizer.instance().langStr("name.not.defined")
            raise PyShiftException(msg)
        
        self.name = name
