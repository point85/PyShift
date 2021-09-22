from PyShift.workschedule.time_period import TimePeriod

##
# Class DayOff represents a scheduled non-working period
# 
class DayOff(TimePeriod):

    # Construct a period of time when not working
    def __init__(self, name, description, start, duration):
        super().__init__(name, description, start, duration)

    def isWorkingPeriod(self):
        return False
