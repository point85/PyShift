from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift_exception import PyShiftException

##
# Class NonWorkingPeriod represents named non-working, non-recurring periods.
# For example holidays and scheduled outages such as for preventive
# maintenance.
#
class NonWorkingPeriod(Named):
    def __init__(self, name, description, startDateTime, duration):
        super().__init__(name, description)
        self.setStartDateTime(startDateTime)
        self.setDuration(duration)
        
    ##
    # Set period start date and time
    # 
    # @param startDateTime
    #            Period start
    #
    def setStartDateTime(self, startDateTime):
        if (startDateTime is None):
            msg = Localizer.instance().langStr("start.not.defined")
            raise PyShiftException(msg)

        self.startDateTime = startDateTime
    
    ##
    # Get period end date and time
    # 
    # @return Period end
    #
    def getEndDateTime(self):
        return self.startDateTime + self.duration
    
    ##
    # Set duration
    # 
    # @param duration
    #            Duration
    #
    def setDuration(self, duration):
        if (duration is None or duration.total_seconds() == 0):
            msg = Localizer.instance().langStr("duration.not.defined")
            raise PyShiftException(msg)

        self.duration = duration
    
    def __str__(self):
        start = Localizer.instance().langStr("period.start")
        end = Localizer.instance().langStr("period.end")

        return super().str() + ", " + start + ": " + self.startDateTime + " (" + self.duration + ")" + ", " + end + ": " + self.getEndDateTime()
    
    ##
    # Compare two non-working periods
    # @param other {@link NonWorkingPeriod}
    # @return -1 if starts before other, 0 is same starting times, else 1
    #
    def compareTo(self, other):
        value = 0
        if (self.startDateTime < other.startDateTime):
            value = -1
        elif (self.startDateTime > other.startDateTime):
            value = 1
        return value
    
    ##
    # Check to see if this day is contained in the non-working period
    # 
    # @param day
    #            Date to check
    # @return True if in the non-working period
    # @throws Exception
    #             Exception
    #/
    def isInPeriod(self, day):
        isInPeriod = False

        if (day.compareTo(self.startDateTime) >= 0 and day.compareTo(self.getEndDateTime()) <= 0):
            isInPeriod = True

        return isInPeriod