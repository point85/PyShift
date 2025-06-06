from datetime import datetime
from typing import TYPE_CHECKING

#from PyShift.workschedule.team import Team
from PyShift.workschedule.shift import Shift
from PyShift.workschedule.localizer import Localizer

if TYPE_CHECKING:
    from PyShift.workschedule.team import Team

##
# Class ShiftInstance is an instance of a {@link Shift}. A shift instance is
# worked by a {@link Team}.
#
class ShiftInstance: 
    ##
    # Construct an instance of a shift
    # @param shift {@link Shift} definition
    # @param startDateTime Starting date and time of day
    # @param team {link Team} working the shift instance
    def __init__(self, shift: Shift, startDateTime: datetime, team: 'Team'):   
        # definition of the shift instance
        self.shift = shift
        
        # start date and time of day
        self.startDateTime = startDateTime
        
        # team working it
        self.team = team

    ##
    # Get the ending date and time of day
    # 
    # @return datetime when shift ends
    #
    def getEndTime(self) -> datetime:
        return self.startDateTime + self.shift.duration

    ##
    # Compare this shift to another such period by start date and time of
    # day
    #
    # @param other Other shift instance
    # 
    # @return -1 if less than, 0 if equal and 1 if greater than
    #
    def compareTo(self, other) -> int:
        value = 0
        
        if (self.startDateTime < other.startDateTime):
            value = -1
        elif (self.startDateTime > other.startDateTime):
            value = 1
        return value
    
    ##
    # Determine if this time falls within the shift instance period
    # 
    # @param dateTime Date and time to check
    # @return True if the specified time is in this shift instance
    #
    def isInShiftInstance(self, dateTime: datetime) -> bool:
        return (dateTime >= self.startDateTime and dateTime <= self.getEndTime())

    def __str__(self) -> str:
        t = Localizer.instance().messageStr("team")
        s = Localizer.instance().messageStr("shift")
        ps = Localizer.instance().messageStr("period.start")
        pe = Localizer.instance().messageStr("period.end")
        members = Localizer.instance().messageStr("team.members")

        text = " " + t + ": " + self.team.name + ", " + s + ": " + self.shift.name + ", " + ps + ": " + str(self.startDateTime) + ", " + pe + ": " + str(self.getEndTime()) + "\n" + members
        
        for member in self.team.getMembers(self.startDateTime):
            text += "\n\t" + str(member)

        return text