from _datetime import timedelta

from PyShift.workschedule.time_period import TimePeriod
from PyShift.workschedule.work_break import Break
from PyShift.workschedule.localizer import Localizer
from builtins import staticmethod

##
# Class Shift is a scheduled working time period, and can include breaks.
# 
# @author Kent Randall
#
#
class Shift(TimePeriod):
    def __init__(self, name, description, start, duration):
        super().__init__(name, description, start, duration)
        
        self.workSchedule = None
        self.breaks = []

    ##
    # Add a break period to this shift
    # 
    # @param breakPeriod
    #           :@link Break}
    #
    def addBreak(self, breakPeriod):
        if (breakPeriod not in self.breaks):
            self.breaks.add(breakPeriod)

    ##
    # Remove a break from this shift
    # 
    # @param breakPeriod
    #           :@link Break}
    #
    def removeBreak(self, breakPeriod):
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
    # @return:@link Break}
    #
    def createBreak(self, name, description, startTime, duration):
        period = Break(name, description, startTime, duration)
        self.addBreak(period)
        return period
    
    @staticmethod
    def secondOfDay(time):
        return time.hour()* 3600 + time.minute() * 60 + time.second()
    
    @staticmethod
    def toRoundedSecond(time):
        second = Shift.secondOfDay(time)

        if (time.microsecond() > 500000):
            second = second + 1

        return second

    ##
    # Calculate the working time between the specified times of day. The shift
    # must not span midnight.
    # 
    # @param fromTime
    #            starting time
    # @param toTime
    #            Ending time
    # @return of working time
    #
    def calculateWorkingTime(self, fromTime, toTime):
        if (self.spansMidnight()):
            msg = Localizer.instance().langStr("shift.spans.midnight").format(self.name, fromTime, toTime)
            raise Exception(msg)
    
        return self.calculateTotalWorkingTime(fromTime, toTime, True)

    ##
    # Check to see if this shift crosses midnight
    # 
    # @return True if the shift extends over midnight, otherwise False
    #
    def spansMidnight(self):
        startSecond = Shift.toRoundedSecond(self.startTime)
        endSecond = Shift.toRoundedSecond(self.getEndTime())
        return True if endSecond <= startSecond else False

    ##
    # Calculate the working time between the specified times of day
    # 
    # @param from
    #            starting time
    # @param to
    #            Ending time
    # @param beforeMidnight
    #            If true, and a shift spans midnight, calculate the time before
    #            midnight. Otherwise calculate the time after midnight.
    # @return of working time
    #
    def calculateTotalWorkingTime(self, fromTime, toTime, beforeMidnight):
        startSecond = Shift.toRoundedSecond(self.startTime)
        endSecond = Shift.toRoundedSecond(self.getEndTime())
        fromSecond = Shift.toRoundedSecond(fromTime)
        toSecond = Shift.toRoundedSecond(toTime)

        delta = toSecond - fromSecond

        # check for 24 hour shift
        if (delta == 0 and fromSecond == startSecond and self.duration.hours() == 24):
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

        duration = timedelta(seconds=(toSecond - fromSecond))
        return duration

    @staticmethod
    def compare(firstTime, secondTime):
        value = 0
        
        if (firstTime < secondTime):
            value = -1
        elif (firstTime < secondTime):
            value = 1
        return value
        
    ##
    # Test if the specified time falls within the shift
    # 
    # @param time
    #           :@link LocalTime}
    # @return True if in the shift
    #
    def isInShift(self, time):
        answer = False

        start = self.startTime
        end = self.getEndTime()

        onStart = Shift.compare(time, start)
        onEnd = Shift.compare(time, end)

        timeSecond = Shift.secondOfDay(time)

        if (start < end):
            # shift did not cross midnight
            if (onStart >= 0 and onEnd <= 0):
                answer = True
        else:
            # shift crossed midnight, check before and after midnight
            if (timeSecond <= Shift.secondOfDay(end)):
                # after midnight
                answer = True
            else:
                # before midnight
                if (timeSecond >= Shift.secondOfDay()):
                    answer = True
    
        return answer

    ##
    # Calculate the total break time for the shift
    # 
    # @return of all breaks
    #
    def calculateBreakTime(self):
        timeSum = timedelta(seconds=0)

        for b in self.breaks:
            timeSum = timeSum + b.duration
        return timeSum

    ##
    # Compare one shift to another one
    #
    def compareTo(self, other):
        return self.name == other.name

    ##
    # Build a string representation of this shift
    # 
    # @return String
    #
    def __str__(self):
        text = super().__str__()

        if (len(self.breaks) > 0):
            text += "\n      " + str(len(self.breaks)) + " " + Localizer.instance().langStr("breaks") + ":"
    
        for breakPeriod in self.breaks:
            text += "\n      " + str(breakPeriod)
    
        return text


    def isWorkingPeriod(self):
        return True


##
# Class ShiftInstance is an instance of a:@link Shift}. A shift instance is
# worked by a:@link Team}.
# 
# @author Kent Randall
#
#
class ShiftInstance: 
    def __init__(self, shift, startDateTime, team):
        # definition of the shift
        self.shift = shift
        
        # start date and time of day
        self.startDateTime = startDateTime
        
        # team working it
        self.team = team

    ##
    # Get the end date and time of day
    # 
    # @return LocalDateTime
    #
    def getEndTime(self):
        return self.startDateTime + self.shift.getDuration()

    ##
    # Compare this non-working period to another such period by start time of
    # day
    # 
    # @return -1 if less than, 0 if equal and 1 if greater than
    #
    def compareTo(self, other):
        value = 0
        
        if (self.startDateTime < other.startDateTime):
            value = -1
        elif (self.startDateTime > other.startDateTime):
            value = 1
        return value

    ##
    # Build a string representation of a shift instance
    #
    def __str__(self):
        t = Localizer.instance().langStr("team")
        s = Localizer.instance().langStr("shift")
        ps = Localizer.instance().langStr("period.start")
        pe = Localizer.instance().langStr("period.end")

        text = " " + t + ": " + self.team.name + ", " + s + ": " + self.shift.name + ", " + ps + ": " + str(self.startDateTime) + ", " + pe + ": " + str(self.getEndTime())
        return text