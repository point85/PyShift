from datetime import datetime, timedelta, date
from operator import attrgetter

from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.day_off import DayOff
from PyShift.workschedule.shift_exception import PyShiftException
from PyShift.workschedule.shift import Shift
from PyShift.workschedule.shift_utils import ShiftUtils

##
# This class represents part of an entire rotation. The segment starts with a
# shift and includes a count of the number of days on followed by the number of
# days off.
# 
class RotationSegment():
    def __init__(self, startingShift: Shift, daysOn: int, daysOff: int, rotation):
        self.startingShift = startingShift
        self.daysOn = daysOn
        self.daysOff = daysOff
        self.rotation = rotation
        self.sequence = 0
        
    ##
    # Compare two rotation segments
    # @param other {@link RotationSegment}
    # @return -1 if starts before other, 0 is same starting times, else 1
    #
    def compareTo(self, other) -> int:
        value = 0
        if (self.sequence < other.sequence):
            value = -1
        elif (self.sequence > other.sequence):
            value = 1
        return value

##
# Class Rotation maintains a sequenced list of shift and off-shift time
# periods.
# 
class Rotation(Named):
    dayOff = None  
      
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        # RotationSegments in the rotation
        self.rotationSegments = []
        
        # list of working and non-working TimePeriods (days)
        self.periods = None
    
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
            self.rotationSegments.sort(key=attrgetter('sequence'))

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
        return timedelta(days=len(self.getPeriods()))
    
    ##
    # Get the shift rotation's total working time
    # 
    # @return timedelta of working time
    #
    def getWorkingTime(self) -> timedelta:
        workingTime = timedelta()

        for period in self.getPeriods():
            if (period.isWorkingPeriod()):
                workingTime = workingTime + period.duration
            
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
        rd = Localizer.instance().messageStr("rotation.duration") + ": " + ShiftUtils.formatTimedelta(self.getDuration())
        rda = Localizer.instance().messageStr("rotation.days") + ": " + str(self.getDuration().total_seconds() / 86400) 
        rw = Localizer.instance().messageStr("rotation.working") + ": " + ShiftUtils.formatTimedelta(self.getWorkingTime())
        rper = Localizer.instance().messageStr("rotation.periods")
        on = Localizer.instance().messageStr("rotation.on")
        off = Localizer.instance().messageStr("rotation.off")

        periods= ""

        for period in self.periods:
            if (len(periods) > 0):
                periods += ", "
            
            onOff = on if period.isWorkingPeriod() else off
            periods = periods + period.name + " (" + str(onOff) + ")"  
        
        return named + "\n" + rper + ": [" + periods + "], " + rd  + ", " + rda + ", " + rw

        