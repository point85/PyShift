
from datetime import datetime, date, timedelta
from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift_exception import PyShiftException

##
# Class NonWorkingPeriod represents named non-working, non-recurring periods.
# For example holidays and scheduled outages such as for preventive
# maintenance.
#
class NonWorkingPeriod(Named):
    ##
    # Construct a non-working period
    # @param name Name of period
    # @param description Description of period
    # @param startDateTime Starting date and time of day of period
    # @param duration Duration of period
    #
    def __init__(self, name: str, description: str, startDateTime: datetime, duration: timedelta):
        super().__init__(name, description)
        self.setStartDateTime(startDateTime)
        self.setDuration(duration)
        
    ##
    # Set period start date and time
    # 
    # @param startDateTime
    #            Period start
    #
    def setStartDateTime(self, startDateTime: datetime):
        if (startDateTime is None):
            msg = Localizer.instance().messageStr("start.not.defined")
            raise PyShiftException(msg)

        self.startDateTime = startDateTime
    
    ##
    # Get period end date and time
    # 
    # @return Period end
    #
    def getEndDateTime(self) -> datetime:
        return self.startDateTime + self.duration
    
    ##
    # Set duration
    # 
    # @param duration
    #            Duration
    #
    def setDuration(self, duration: timedelta):
        if (duration is None or duration.total_seconds() == 0):
            msg = Localizer.instance().messageStr("duration.not.defined")
            raise PyShiftException(msg)

        self.duration = duration
    
    def __str__(self) -> str:
        start = Localizer.instance().messageStr("period.start")
        end = Localizer.instance().messageStr("period.end")

        return super().__str__() + ", " + start + ": " + str(self.startDateTime) + " (" + str(self.duration) + ")" + ", " + end + ": " + str(self.getEndDateTime())
    
    ##
    # Compare two non-working periods
    # @param other {@link NonWorkingPeriod}
    # @return -1 if starts before other, 0 is same starting times, else 1
    #
    def compareTo(self, other) -> int:
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
    #
    def isInPeriod(self, day: date) -> bool:
        isInPeriod = False

        if (day >= self.startDateTime.date() and day <= self.getEndDateTime().date()):
            isInPeriod = True

        return isInPeriod