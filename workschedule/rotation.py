from datetime import datetime, timedelta, date

from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.day_off import DayOff
from PyShift.workschedule.rotation_segment import RotationSegment 
from PyShift.workschedule.shift_exception import PyShiftException
from PyShift.workschedule.shift import Shift

##
# Class Rotation maintains a sequenced list of shift and off-shift time
# periods.
# 
class Rotation(Named):
    dayOff = None  
      
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.rotationSegments = []
        self.periods = []
    
    @staticmethod    
    def getDayOff() -> DayOff:
        if (Rotation.dayOff is None):
            midnight = datetime.combine(date.today(), datetime.min.time())
            dayOff = DayOff("DAY_OFF", "24 hour off period", midnight, timedelta(hours=24))
        return dayOff
    
    ##
    # Get the shifts and off-shifts in the rotation
    # 
    # @return List of periods
    #
    def getPeriods(self) -> []:
        if (self.periods is None):
            self.periods = []
            
            # sort by sequence number
            self.rotationSegments.sort(key=RotationSegment.compareTo)

            for segment in self.rotationSegments:
                # add the on days
                if (segment.startingShift is not None):
                    for _i in range(segment.daysOn):
                        self.periods.append(segment.startingShift)

                # add the off days
                for _i in range(segment.daysOff):
                    self.periods.append(Rotation.getDayOff())

        return self.periods
    
    ##
    # Get the number of days in the rotation
    # 
    # @return Day count
    #
    def getDayCount(self) -> int:
        return len(self.periods)

    ##
    # Get the duration of this rotation
    # 
    # @return timedelta
    #
    def getDuration(self) -> timedelta:
        return timedelta(days=len(self.periods))
    
    ##
    # Get the shift rotation's total working time
    # 
    # @return timedelta of working time
    #
    def getWorkingTime(self) -> timedelta:
        workingTime = timedelta()

        for period in self.periods:
            if (period.isWorkingPeriod()):
                workingTime = workingTime.plus(period.getDuration())
            
        
        return workingTime

    ##
    # Add a working period to this rotation. A working period starts with a
    # shift and specifies the number of days on and days off
    # 
    # @param startingShift
    #           {@link Shift} that starts the period
    # @param daysOn
    #            Number of days on shift
    # @param daysOff
    #            Number of days off shift
    # @return {@link RotationSegment}
    #
    def addSegment(self, startingShift: Shift, daysOn: int, daysOff: int) -> RotationSegment:
        if (startingShift is None):
            msg = Localizer.instance().messageStr("no.starting.shift")
            raise PyShiftException(msg)
        
        segment = RotationSegment(startingShift, daysOn, daysOff, self)
        self.rotationSegments.append(segment)
        segment.sequence = len(self.rotationSegments)
        return segment
    
    def compareTo(self, other):
        return self.name == other.name
    

    ##
    # Build a string representation of this rotation
    #
    def __str__(self) -> str:
        named = super().__str__()
        rd = Localizer.instance().messageStr("rotation.duration")
        rda = Localizer.instance().messageStr("rotation.days")
        rw = Localizer.instance().messageStr("rotation.working")
        rper = Localizer.instance().messageStr("rotation.periods")
        on = Localizer.instance().messageStr("rotation.on")
        off = Localizer.instance().messageStr("rotation.off")

        periods= ""

        for period in self.periods:
            if (len(periods) > 0):
                periods = periods + ", "
            
            onOff = on if period.isWorkingPeriod() else off
            periods = periods + period.name + " (" + str(onOff) + ")"  

        return named + "\n" + rper + ": [" + periods+ "], " + rd + ": " + self.getDuration() + ", " + rda + ": " + timedelta(days=self.getDuration()) + ", " + rw + ": " + self.getWorkingTime()

        