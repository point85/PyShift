from datetime import datetime, date, time, timedelta
from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift_exception import PyShiftException 
from PyShift.workschedule.shift_utils import ShiftUtils

##
# Class TimePeriod is a named period of time with a specified duration and
# starting time of day.
# 
class TimePeriod(Named):
    # number of seconds in a day
    SECONDS_PER_DAY = 24 * 60 * 60

    ##
    # Construct a time period
    # @param name Name of period
    # @param description Description of period
    # @param startTime Starting date and time of day
    # @param duration Duration of time period
    #    
    def __init__(self, name : str, description : str, startTime : datetime, duration : timedelta):
        super().__init__(name, description)
        self.setStartTime(startTime)
        self.setDuration(duration)

    ##
    # Set duration
    # 
    # @param duration
    #            period duration as timedelta
    # 
    def setDuration(self, duration: timedelta):
        if (duration is None or duration.total_seconds() == 0):
            msg = Localizer.instance().messageStr("duration.not.defined")
            raise PyShiftException(msg)
        
        if (duration.total_seconds() > TimePeriod.SECONDS_PER_DAY):
            msg = Localizer.instance().messageStr("duration.not.allowed")
            raise PyShiftException(msg)
        
        self.duration = duration
    
    ##
    # add duration to a time of day
    # @param dayTime: time of day
    # @param duration: duration to add
    # @return new time
    #
    def timePlus(self, dayTime: time, duration: timedelta) -> time:
        # unused date portion
        start = datetime.combine(date.today(), time(hour=dayTime.hour, minute=dayTime.minute, second=dayTime.second))
        end = start + duration
        return end.time()

    ##
    # Get period end
    # 
    # @return End time of day
    #
    def getEndTime(self) -> time:
        return self.timePlus(self.startTime, self.duration)
    
    ##
    # Set period start time
    # 
    # @param startTime
    #            Starting time of day
    #
    def setStartTime(self, startTime: time):
        if (startTime is None):
            msg = Localizer.instance().messageStr("start.not.defined")
            raise PyShiftException(msg)
        
        self.startTime = startTime

    def __str__(self) -> str:
        start = Localizer.instance().messageStr("period.start") + ": " + str(self.startTime) 
        end = Localizer.instance().messageStr("period.end") + ": " + str(self.getEndTime())

        return super().__str__() + ", " + start + " (" + ShiftUtils.formatTimedelta(self.duration) + ")" + ", " + end 

