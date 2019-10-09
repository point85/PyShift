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
    def __init__(self, name, description, start, duration):
        super().__init__(name, description, start, duration)


    def isWorkingPeriod(self):
        return True