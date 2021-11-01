from datetime import datetime, time, timedelta

from PyShift.workschedule.time_period import TimePeriod
from PyShift.workschedule.work_break import Break
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift_exception import PyShiftException
from PyShift.workschedule.shift_utils import ShiftUtils

##
# Class Shift is a scheduled working time period, and can include breaks.
# 
class Shift(TimePeriod):
    ##
    # Construct a shift definition
    # @param name Name of shift
    # @param description Description of shift
    # @param start Starting time of day
    # @param duration Duration of shift
    #    
    def __init__(self, name:str, description: str, start: time, duration: timedelta):
        super().__init__(name, description, start, duration)
        self.breaks = []

    ##
    # Add a break period to this shift
    # 
    # @param breakPeriod
    #           {@link Break}
    #
    def addBreak(self, breakPeriod: Break):
        if (breakPeriod not in self.breaks):
            self.breaks.append(breakPeriod)

    ##
    # Remove a break from this shift
    # 
    # @param breakPeriod
    #           {@link Break}
    #
    def removeBreak(self, breakPeriod: Break):
        if (breakPeriod in self.breaks):
            self.breaks.remove(breakPeriod)

    ##
    # Create a break for this shift
    # 
    # @param name
    #            Name of break
    # @param description
    #            Description of break
    # @param startTime
    #            Start of break
    # @param duration
    #            of break
    # @return {@link Break}
    #
    def createBreak(self, name: str, description: str, startTime: time, duration: timedelta) -> Break:
        period = Break(name, description, startTime, duration)
        self.addBreak(period)
        return period

    ##
    # Calculate the working time between the specified times of day. The shift
    # must not span midnight.
    # 
    # @param fromTime
    #            starting time
    # @param toTime
    #            Ending time
    # @return timedelta working time
    #
    def calculateWorkingTime(self, fromTime:time, toTime:time) -> timedelta:
        if (self.spansMidnight()):
            msg = Localizer.instance().messageStr("shift.spans.midnight").format(self.name, fromTime, toTime)
            raise PyShiftException(msg)
    
        return self.calculateTotalWorkingTime(fromTime, toTime, True)

    ##
    # Check to see if this shift crosses midnight
    # 
    # @return True if the shift extends over midnight, otherwise False
    #
    def spansMidnight(self) -> bool:
        startSecond = ShiftUtils.toRoundedSecond(self.startTime)
        endSecond = ShiftUtils.toRoundedSecond(self.getEndTime())
        return True if endSecond <= startSecond else False

    ##
    # Calculate the working time between the specified times of day
    # 
    # @param fromTime
    #            starting time
    # @param toTime
    #            Ending time
    # @return timedelta working time
    # @param beforeMidnight
    #            If true, and a shift spans midnight, calculate the time before
    #            midnight. Otherwise calculate the time after midnight.
    # @return timedelta working time
    #
    def calculateTotalWorkingTime(self, fromTime:time, toTime:time, beforeMidnight: bool) -> timedelta:
        startSecond = ShiftUtils.toRoundedSecond(self.startTime)
        endSecond = ShiftUtils.toRoundedSecond(self.getEndTime())
        fromSecond = ShiftUtils.toRoundedSecond(fromTime)
        toSecond = ShiftUtils.toRoundedSecond(toTime)

        delta = toSecond - fromSecond

        # check for 24 hour shift
        if (delta == 0 and fromSecond == startSecond and self.duration.total_seconds() == 86400):
            delta = 86400
    
        if (delta < 0):
            delta = 86400 + toSecond - fromSecond
    
        if (self.spansMidnight()):
            # adjust for shift crossing midnight
            if (fromSecond < startSecond and fromSecond < endSecond):
                if (not beforeMidnight):
                    fromSecond = fromSecond + 86400
            
            toSecond = fromSecond + delta
            endSecond = endSecond + 86400

        # clip seconds on edge conditions
        if (fromSecond < startSecond):
            fromSecond = startSecond
    
        if (toSecond < startSecond):
            toSecond = startSecond

        if (fromSecond > endSecond):
            fromSecond = endSecond

        if (toSecond > endSecond):
            toSecond = endSecond

        return  timedelta(seconds=(toSecond - fromSecond))
        
    ##
    # Test if the specified time falls within the shift
    # 
    # @param time Time of day
    # @return True if the time is in the shift
    #
    def isInShift(self, time: time) -> bool:
        answer = False

        start = self.startTime
        end = self.getEndTime()

        onStart = ShiftUtils.compare(time, start)
        onEnd = ShiftUtils.compare(time, end)

        timeSecond = ShiftUtils.toSecondOfDay(time)

        if (start < end):
            # shift did not cross midnight
            if (onStart >= 0 and onEnd <= 0):
                answer = True
        else:
            # shift crossed midnight, check before and after midnight
            if (timeSecond <= ShiftUtils.toSecondOfDay(end)):
                # after midnight
                answer = True
            else:
                # before midnight
                if (timeSecond >= ShiftUtils.toSecondOfDay(start)):
                    answer = True
    
        return answer

    ##
    # Calculate the total break time for the shift
    # 
    # @return duration of all breaks
    #
    def calculateBreakTime(self) -> timedelta:
        timeSum = timedelta(seconds=0)

        for b in self.breaks:
            timeSum = timeSum + b.duration
        return timeSum
    
    ##
    # a shift is a working period
    def isWorkingPeriod(self) -> bool:
        return True

    def __str__(self) -> str:
        text = super().__str__()

        if (len(self.breaks) > 0):
            text += "\n      " + str(len(self.breaks)) + " " + Localizer.instance().messageStr("breaks") + ":"
    
        for breakPeriod in self.breaks:
            text += "\n      " + str(breakPeriod)
    
        return text

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
    def __init__(self, shift: Shift, startDateTime: datetime, team):
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
        return (dateTime.compareTo(self.startDateTime) >= 0 and dateTime.compareTo(self.getEndTime()) <= 0)

    def __str__(self) -> str:
        t = Localizer.instance().messageStr("team")
        s = Localizer.instance().messageStr("shift")
        ps = Localizer.instance().messageStr("period.start")
        pe = Localizer.instance().messageStr("period.end")

        text = " " + t + ": " + self.team.name + ", " + s + ": " + self.shift.name + ", " + ps + ": " + str(self.startDateTime) + ", " + pe + ": " + str(self.getEndTime())
        return text