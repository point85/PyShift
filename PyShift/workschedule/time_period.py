from abc import ABC

from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer

##
# Class TimePeriod is a named period of time with a specified duration and
# starting time of day.
# 
class TimePeriod(ABC, Named):
    SECONDS_PER_DAY = 24 * 60 * 60
    
    def __init__(self, name, description, startTime, duration):
        super().__init__(name, description)
        self.setStartTime(startTime)
        self.setDuration(duration)

    ##
    # Set duration
    # 
    # @param duration
    #            period duration
    # 
    def setDuration(self, duration):
        if (duration is None or duration.total_seconds() == 0):
            msg = Localizer.instance().langStr("duration.not.defined")
            raise Exception(msg)
        
        if (duration.total_seconds() > TimePeriod.SECONDS_PER_DAY):
            msg = Localizer.instance().langStr("duration.not.allowed")
            raise Exception(msg)
        
        self.duration = duration
    
    ##
    # Get period end
    # 
    # @return End time
    #
    def getEndTime(self):
        return self.startTime + self.duration
    
    ##
    # Set period start time
    # 
    # @param startTime
    #            Start time
    #
    def setStartTime(self, startTime):
        if (startTime is None):
            msg = Localizer.instance().langStr("start.not.defined")
            raise Exception(msg)
        
        self.startTime = startTime

    def __str__(self):
        start = Localizer.instance().langStr("period.start")
        end = Localizer.instance().langStr("period.end")

        return super().str() + ", " + start + ": " + self.startTime + " (" + self.duration + ")" + ", " + end + ": " + self.getEndTime()

