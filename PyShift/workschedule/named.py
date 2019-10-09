from abc import ABC

from PyShift.workschedule.localizer import Localizer

##
# Class Named represents a named object such as a Shift or Team.
# 
class Named(ABC):    
    def __init__(self, name=None, description=None):
        self.setName(name)
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
        
    def __str__(self):
        return self.name + " (" + self.description + ")"
    
    def setName(self, name):
        if (name is None):          
            msg = Localizer.instance().langStr("name.not.defined")
            raise Exception(msg)
        
        self.name = name
