from datetime import datetime
from typing import Optional

from .named import Named
from .localizer import Localizer


# #
# Class TeamMember represents a person assigned to a Team
# 
class TeamMember(Named):
    # #
    # Construct a team member
    # @param name Name of team member
    # @param description Description of team member
    # @param memberID Identifer (e.g. employee ID)
    # 
    def __init__(self, name: str, description: str, memberID: str):
        super().__init__(name, description)  
        
        # member identifier             
        self.memberID = memberID
        
    def __str__(self) -> str:
        ident = Localizer.instance().messageStr("member.id")

        try:
            return f"{super().__str__()}, {ident}: {self.memberID}"
        except Exception as e:
            # Log the exception if needed
            return super().__str__()   

# #
# This class provides information for adding or removing a team member for a
# team working an instance of a shift. The shift instance is identified by its
# starting date and time.
#
class TeamMemberException: 
    # #
    # Construct an exception for the shift instance at this starting date and time
    #
    def __init__(self, shiftStart: datetime):
        # start date and time of day of the shift
        self.shiftStart: datetime = shiftStart
        
        # team member to add 
        self.addition: Optional[TeamMember] = None
        
        # team member to remove
        self.removal: Optional[TeamMember] = None
        
        # reason for the change
        self.reason: Optional[str] = None  
        
    def setAddition(self, member: TeamMember, reason: str = None):
        """Set the team member to add"""
        self.addition = member
        if reason:
            self.reason = reason
    
    def setRemoval(self, member: TeamMember, reason: str = None):
        """Set the team member to remove"""
        self.removal = member
        if reason:
            self.reason = reason        
        
    def __str__(self) -> str:
        return "Shift: " + str(self.shiftStart) + ", add: " + str(self.addition) + ", remove: " +str(self.removal)              
      
    
