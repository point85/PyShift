from datetime import datetime, date, timedelta

from PyShift.workschedule.named import Named
from PyShift.workschedule.shift_utils import ShiftUtils
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift import ShiftInstance
from PyShift.workschedule.rotation import Rotation
from PyShift.workschedule.shift_exception import PyShiftException

##
# Class Team is a named group of individuals who rotate through a shift
# schedule.
# 
class Team(Named):
    def __init__(self, name: str, description: str, rotation: Rotation, rotationStart: date):
        super().__init__(name, description)
                
        # shift rotation days
        self.rotation = rotation
        
        # reference date for starting the rotations
        self.rotationStart = rotationStart
        
    ##
    # Get the duration of the shift rotation
    # 
    # @return Duration
    #
    def getRotationDuration(self) -> timedelta:
        return self.rotation.getDuration()
    
    ##
    # Get the shift rotation's working time as a percentage of the rotation
    # duration
    # 
    # @return Percentage
    #
    def getPercentageWorked(self) -> float:
        num = timedelta(seconds=self.rotation.getWorkingTime())
        denom = timedelta(seconds=self.getRotationDuration()) 
        return (num / denom) * 100.0
    
    ##
    # Get the average number of hours worked each week by this team
    # 
    # @return Duration of hours worked per week
    #
    def getHoursWorkedPerWeek(self) -> timedelta:
        deltaDays = timedelta(days=self.rotation.getDuration())
        secPerWeek = timedelta(seconds = self.rotation.getWorkingTime()) * (7.0 / deltaDays.days)
        return timedelta(seconds=secPerWeek)

    ##
    # Get the day number in the rotation for this local date
    # 
    # @param date
    #            LocalDate
    # @return day number in the rotation, starting at 1
    #
    def getDayInRotation(self, date: date) -> int:
        # calculate total number of days from start of rotation
        dayTo = ShiftUtils.toEpochDay(date)
        start = ShiftUtils.toEpochDay(self.rotationStart)
        deltaDays = dayTo - start

        if (deltaDays < 0):
            msg = Localizer.instance().messageStr("end.earlier.than.start").format(self.rotationStart, date)
            raise PyShiftException(msg)
        
        duration = int(self.rotation.getDuration().total_seconds())
        rotationDays = int(duration / 86400)
        
        if (rotationDays == 0):
            rotationDays = 1
            
        return (deltaDays % rotationDays) + 1

    ##
    # Get the {@link ShiftInstance} for the specified day
    # 
    # @param day
    #            Day with a shift instance
    # @return {@link ShiftInstance}
    #
    def getShiftInstanceForDay(self, day: date) -> ShiftInstance:
        instance = None
        
        #shiftRotation = self.rotation
        
        if (self.rotation.getDuration() == timedelta(seconds=0)):
            # no instance for that day
            return instance
    
        dayInRotation = self.getDayInRotation(day)

        # shift or off shift
        period = self.rotation.getPeriods()[dayInRotation - 1]

        if (period.isWorkingPeriod()):
            startDateTime = datetime(day.year(), day.month(), day.day(), period.startTime.hour(),period.startTime.minute(), period.startTime.second() )
            instance = ShiftInstance(period, startDateTime, self)

        return instance

    ##
    # Check to see if this day is a day off
    # 
    # @param day
    #            Date to check
    # @return True if a day off
    #
    def isDayOff(self, day: date) -> bool:
        dayOff = False

        dayInRotation = self.getDayInRotation(day)

        # shift or off shift
        period = self.rotation.periods[dayInRotation - 1]

        if (not period.isWorkingPeriod()):
            dayOff = True

        return dayOff

    ##
    # Calculate the schedule working time between the specified dates and times
    # 
    # @param from
    #            Starting date and time of day
    # @param to
    #            Ending date and time of day
    # @return Duration of working time
    #
    def calculateWorkingTime(self, fromTime: datetime, toTime: datetime) -> timedelta:
        if (fromTime > toTime):
            msg = Localizer.instance().messageStr("end.earlier.than.start").format(toTime, fromTime)
            raise PyShiftException(msg)
    
        timeSum = timedelta(seconds=0)

        thisDate = fromTime.date()
        thisTime = fromTime.time()
        toDate = toTime.date()
        toTime = toTime.time()
        dayCount = self.rotation.getDayCount()

        # get the working shift from yesterday
        lastShift = None

        yesterday = thisDate - timedelta(days=1)
        yesterdayInstance = self.getShiftInstanceForDay(yesterday)

        if (yesterdayInstance is not None):
            lastShift = yesterdayInstance.shift
    
        # step through each day until done
        while (thisDate < toDate):
            if (lastShift is not None and lastShift.spansMidnight()):
                # check for days in the middle of the time period
                lastDay = True if (thisDate == toDate) else False
                
                if (not lastDay or (lastDay and toTime.seconds() != 0)):
                    # add time after midnight in this day
                    afterMidnightSecond = lastShift.getEnd().toSecondOfDay()
                    fromSecond = thisTime.toSecondOfDay()

                    if (afterMidnightSecond > fromSecond):
                        timeSum = timeSum + timedelta(seconds=(afterMidnightSecond - fromSecond))

            # today's shift
            instance = self.getShiftInstanceForDay(thisDate)

            duration = None

            if (instance is not None):
                lastShift = instance.shift
                # check for last date
                if (thisDate == toDate):
                    duration = lastShift.calculateTotalWorkingTime(thisTime, toTime, True)
                else:
                    duration = lastShift.calculateTotalWorkingTime(thisTime, datetime.time().max, True)
            
                timeSum = timeSum + duration
            else:
                lastShift = None

            n = 1
            if (self.getDayInRotation(thisDate) == dayCount):
                # move ahead by the rotation count if possible
                rotationEndDate = thisDate + timedelta(days=dayCount)

                if (rotationEndDate < toDate):
                    n = dayCount
                    timeSum = timeSum + self.rotation.getWorkingTime()

            # move ahead n days starting at midnight
            thisDate = thisDate + timedelta(days=n)
            thisTime = datetime.time().min
        # end day loop

        return timeSum
    
    ##
    # Compare one team to another one
    #
    def compareTo(self, other) -> bool:
        return self.name == other.name
    
    ##
    # Build a string value for this team
    #
    def __str__(self) -> str:
        rpct = Localizer.instance().messageStr("rotation.percentage")
        rs = Localizer.instance().messageStr("rotation.start")
        avg = Localizer.instance().messageStr("team.hours")
        worked = rpct + ": %.2f" % self.getPercentageWorked()

        text = ""
        try:
            text = super().__str__() + ", " + rs + ": " + str(self.rotationStart) + ", " + str(self.rotation) + ", " + str(worked) + "%, " + str(avg) + ": " + str(self.getHoursWorkedPerWeek())
        except:
            pass
    
        return text