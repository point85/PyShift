from datetime import time, timedelta
from PyShift.workschedule.time_period import TimePeriod

##
# Class Break is a defined working period of time during a shift, for example lunch.
#
class Break(TimePeriod):
    ##
    # Construct a period of time for a break
    # 
    # @param name
    #            Name of break
    # @param description
    #            Description of break
    # @param start
    #            Starting time of day
    # @param duration
    #            Duration of break
    #
    def __init__(self, name: str, description: str, start: time, duration: timedelta):
        super().__init__(name, description, start, duration)

    ##
    # a break is a working period
    def isWorkingPeriod(self):
        return True