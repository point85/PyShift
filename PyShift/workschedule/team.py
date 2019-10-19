from PyShift.workschedule.named import Named
from builtins import None
#from math import remainder

##
# Class Team is a named group of individuals who rotate through a shift
# schedule.
# 
class Team(Named):
    def __init__(self, name=None, description=None, rotation=None, rotationStart=None):
        super().__init__(name, description)
        
        # shift rotation days
        self.rotation = rotation
        
        # reference date for starting the rotations
        self.rotationStart = rotationStart
        
        # owning work schedule
        self.workSchedule = None

    #def getDayFrom(self):
    #    return ShiftUtils.toEpochDay(self.rotationStart)

    ##
    # Get the duration of the shift rotation
    # 
    # @return Duration
    #
    def getRotationDuration(self):
        return self.rotation.getDuration()

    ##
    # Get the shift rotation's working time as a percentage of the rotation
    # duration
    # 
    # @return Percentage
    #
    def getPercentageWorked(self):
        num = timedelta(seconds=self.rotation.getWorkingTime())
        denom = timedelta(seconds=self.getRotationDuration())
        return (num / denom) * 100

    ##
    # Get the average number of hours worked each week by this team
    # 
    # @return Duration of hours worked per week
    #
    def getHoursWorkedPerWeek(self):
        days = timedelta(days=self.rotation.getDuration())
        secPerWeek = timedelta(seconds = self.rotation.getWorkingTime()) * (7 / days)
        return timedelta(seconds=secPerWeek)

    ##
    # Get the day number in the rotation for this local date
    # 
    # @param date
    #            LocalDate
    # @return day number in the rotation, starting at 1
    #
    def getDayInRotation(self, date):
        # calculate total number of days from start of rotation
        dayTo = ShiftUtils.toEpochDay(date)
        start = ShiftUtils.toEpochDay(self.rotationStart)
        deltaDays = dayTo - start

        if (deltaDays < 0):
            msg = Localizer.instance().langStr("end.earlier.than.start").format(self.rotationStart, date)
            raise Exception(msg)
        
        rotationDays = timedelta(days=self.rotation.duration)
        dayInRotation = (deltaDays % rotationDays) + 1
        return dayInRotation

    ##
    # Get the {@link ShiftInstance} for the specified day
    # 
    # @param day
    #            Day with a shift instance
    # @return {@link ShiftInstance}
    #
    def getShiftInstanceForDay(self, day):
        instance = None
        
        shiftRotation = self.getRotation()
        
        if (shiftRotation.duration == timedelta(seconds=0)):
            # no instance for that day
            return instance
    
        dayInRotation = self.getDayInRotation(day)

        # shift or off shift
        period = shiftRotation.periods[dayInRotation - 1]

        if (period.isWorkingPeriod()):
            startDateTime = datetime(day.year(), day.month(), day.day(), period.startTime.hour(),period.startTime.minute(), period.startTime.second() )
            instance = ShiftInstance(period, startDateTime, self)

        return instance


    ##
    # Check to see if this day is a day off
    # 
    # @param day
    #            Date to check
    # @return True if a day off
    # @throws Exception
    #             Exception
    #
    boolean isDayOff(LocalDate day):

        boolean dayOff = false

        Rotation shiftRotation = getRotation()
        dayInRotation = getDayInRotation(day)

        # shift or off shift
        TimePeriod period = shiftRotation.getPeriods().get(dayInRotation - 1)

        if (!period.isWorkingPeriod()):
            dayOff = true
    

        return dayOff



    ##
    # Calculate the schedule working time between the specified dates and times
    # 
    # @param from
    #            Starting date and time of day
    # @param to
    #            Ending date and time of day
    # @return Duration of working time
    # @throws Exception
    #             exception
    #
    Duration calculateWorkingTime(LocalDateTime from, LocalDateTime to):
        if (from.isAfter(to)):
            String msg = MessageFormat.format(WorkSchedule.getMessage("end.earlier.than.start"), to, from)
            throw new Exception(msg)
    

        Duration sum = Duration.ZERO

        LocalDate thisDate = from.toLocalDate()
        LocalTime thisTime = from.toLocalTime()
        LocalDate toDate = to.toLocalDate()
        LocalTime toTime = to.toLocalTime()
        dayCount = getRotation().getDayCount()

        # get the working shift from yesterday
        Shift lastShift = null

        LocalDate yesterday = thisDate.plusDays(-1)
        ShiftInstance yesterdayInstance = getShiftInstanceForDay(yesterday)

        if (yesterdayInstance != null):
            lastShift = yesterdayInstance.getShift()
    

        # step through each day until done
        while (thisDate.compareTo(toDate) < 1):
            if (lastShift != null && lastShift.spansMidnight()):
                # check for days in the middle of the time period
                boolean lastDay = thisDate.compareTo(toDate) == 0 ? true : false
                
                if (!lastDay || (lastDay && !toTime.equals(LocalTime.MIDNIGHT))):
                    # add time after midnight in this day
                    afterMidnightSecond = lastShift.getEnd().toSecondOfDay()
                    fromSecond = thisTime.toSecondOfDay()

                    if (afterMidnightSecond > fromSecond):
                        sum = sum.plusSeconds(afterMidnightSecond - fromSecond)
                
            
        

            # today's shift
            ShiftInstance instance = getShiftInstanceForDay(thisDate)

            Duration duration = null

            if (instance != null):
                lastShift = instance.getShift()
                # check for last date
                if (thisDate.compareTo(toDate) == 0):
                    duration = lastShift.calculateWorkingTime(thisTime, toTime, true)
             else:
                    duration = lastShift.calculateWorkingTime(thisTime, LocalTime.MAX, true)
            
                sum = sum.plus(duration)
         else:
                lastShift = null
        

            n = 1
            if (getDayInRotation(thisDate) == dayCount):
                # move ahead by the rotation count if possible
                LocalDate rotationEndDate = thisDate.plusDays(dayCount)

                if (rotationEndDate.compareTo(toDate) < 0):
                    n = dayCount
                    sum = sum.plus(getRotation().getWorkingTime())
            
        

            # move ahead n days starting at midnight
            thisDate = thisDate.plusDays(n)
            thisTime = LocalTime.MIDNIGHT
     # end day loop

        return sum


    ##
    # Get the work schedule that owns this team
    # 
    # @return {@link WorkSchedule}
    #
    WorkSchedule getWorkSchedule():
        return workSchedule


    void setWorkSchedule(WorkSchedule workSchedule):
        self.workSchedule = workSchedule


    ##
    # Compare one team to another
    #
    @Override
    compareTo(Team other):
        return self.getName().compareTo(other.getName())


    ##
    # Build a string value for this team
    #
    @Override
    String toString():
        String rpct = WorkSchedule.getMessage("rotation.percentage")
        DecimalFormat df = new DecimalFormat()
        df.setMaximumFractionDigits(2)

        String rs = WorkSchedule.getMessage("rotation.start")
        String avg = WorkSchedule.getMessage("team.hours")

        String text = ""
        try:
            text = super.toString() + ", " + rs + ": " + getRotationStart() + ", " + getRotation() + ", " + rpct + ": "
                    + df.format(getPercentageWorked()) + "%" + ", " + avg + ": " + getHoursWorkedPerWeek()

     catch (Exception e):
            # ignore
    

        return text

}
