from PyShift.workschedule.named import Named

##
# Class WorkSchedule represents a named group of teams who collectively work
# one or more shifts with off-shift periods. A work schedule can have periods
# of non-working time.
# 
class WorkSchedule(Named):
    ##
    # Construct a work schedule
    # 
    # @param name
    #            Schedule name
    # @param description
    #            Schedule description
    # @throws Exception
    #             exception
    def __init__(self, name=None, description=None):
        super().__init__(name, description)
    

    