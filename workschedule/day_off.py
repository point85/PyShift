from PyShift.workschedule.time_period import TimePeriod
from datetime import timedelta, datetime

##
# Class DayOff represents a scheduled non-working period
# 
class DayOff(TimePeriod):

    # Construct a period of time when not working
    def __init__(self, name: str, description: str, start: datetime, duration: timedelta):
        super().__init__(name, description, start, duration)

    def isWorkingPeriod(self) -> bool:
        return False
