from PyShift.workschedule.time_period import TimePeriod
from datetime import timedelta, datetime

##
# Class DayOff represents a scheduled non-working period
# 
class DayOff(TimePeriod):

    ##
    # Construct a period of time when not working
    # 
    # @param name
    #            Day off name
    # @param description
    #            Day off description
    # @param start Date and time of day when period starts
    # @param duration Duration of day off
    #
    def __init__(self, name: str, description: str, start: datetime, duration: timedelta):
        super().__init__(name, description, start, duration)

    ##
    # A day off is not a working period
    def isWorkingPeriod(self) -> bool:
        return False
