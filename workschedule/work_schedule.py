from datetime import date, time, datetime, timedelta
from operator import attrgetter

from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift import Shift, ShiftInstance
from PyShift.workschedule.team import Team
from PyShift.workschedule.rotation import Rotation
from PyShift.workschedule.non_working_period import NonWorkingPeriod
from PyShift.workschedule.shift_exception import PyShiftException
from PyShift.workschedule.shift_utils import ShiftUtils

##
# Class WorkSchedule represents a named group of teams who collectively work
# one or more shifts with off-shift periods. A work schedule can have periods
# of non-working time as well as breaks.
# 
class WorkSchedule(Named):
    ##
    # Construct a work schedule
    # 
    # @param name
    #            Schedule name
    # @param description
    #            Schedule description
    #
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.teams = []
        self.shifts = []
        self.rotations = []
        self.nonWorkingPeriods = []
        
    ##
    # Remove this team from the schedule
    # 
    # @param team
    #            {@link Team}
    def deleteTeam(self, team: Team):
        if (team in self.teams):
            self.teams.remove(team)
        
    ##
    # Remove a non-working period from the schedule
    # 
    # @param period
    #            {@link NonWorkingPeriod}
    def deleteNonWorkingPeriod(self, period: NonWorkingPeriod):
        if (period in self.nonWorkingPeriods):
            self.nonWorkingPeriods.remove(period)
    
    ##
    # Get the key for sorting non-working periods    
    # @param period {@link NonWorkingPeriod}
    # @return time key 
    @staticmethod
    def getPeriodKey(period: NonWorkingPeriod) -> time:
        return period.startDateTime
    
    ##
    # Get the list of shift instances for the specified date that start during that date
    # 
    # @param day
    #            date
    # @return list of {@link ShiftInstance}
    def getShiftInstancesForDay(self, day: date) -> [ShiftInstance]:
        workingShifts = []

        # for each team see if there is a working shift
        for team in self.teams:
            instance = team.getShiftInstanceForDay(day)

            if (instance is None):
                continue
            
            # check to see if this is a non-working day
            addShift = True

            startDate = instance.startDateTime.date()

            for nonWorkingPeriod in self.nonWorkingPeriods:
                if (nonWorkingPeriod.isInPeriod(startDate)):
                    addShift = False
                    break
            
            if (addShift):
                workingShifts.append(instance)
        
        workingShifts.sort(key=attrgetter('startDateTime'))
        return workingShifts

    ##
    # Get the list of shift instances for the specified date and time of day
    # 
    # @param dateTime
    #            Date and time of day
    # @return List of {@link ShiftInstance}
    def getShiftInstancesForTime(self, dateTime: datetime) -> [ShiftInstance]:
        workingShifts = []

        # day
        candidateShifts = self.getShiftInstancesForDay(dateTime.date())

        # check time now
        for instance in candidateShifts:
            if (instance.shift.isInShift(dateTime.time())):
                workingShifts.append(instance)
        
        return workingShifts

    ##
    # Create a team
    # 
    # @param name
    #            Name of team
    # @param description
    #            description of team
    # @param rotation
    #            rotation
    # @param rotationStart 
    #            Start of rotation
    # @return {@link Team}
    #
    def createTeam(self, name: str, description: str, rotation: Rotation, rotationStart: time) -> Team:
        team = Team(name, description, rotation, rotationStart)

        if (team in self.teams):
            msg = Localizer.instance().messageStr("team.already.exists").format(name)
            raise PyShiftException(msg)
    
        self.teams.append(team)
    #    team.workSchedule = self
        return team
    
    ##
    # Create a shift
    # 
    # @param name
    #            Name of shift
    # @param description
    #            Description of shift
    # @param start
    #            start time of day
    # @param duration
    #            duration of shift
    # @return {@link Shift}
    #
    def createShift(self, name:str, description:str, start: time, duration: timedelta) -> Shift:
        shift = Shift(name, description, start, duration)

        if (shift in self.shifts):
            msg = Localizer.instance().messageStr("shift.already.exists").format(name)
            raise PyShiftException(msg)
    
        self.shifts.append(shift)
    #    shift.workSchedule = self
        return shift

    ##
    # Delete this shift
    # 
    # @param shift
    #            {@link Shift} to delete
    def deleteShift(self, shift:Shift):
        if (shift not in self.shifts):
            return
    
        # can't be in use
        for inUseShift in self.shifts:
            for team in self.teams:
                rotation = team.rotation

                for period in rotation.periods:
                    if (period == inUseShift):
                        msg = Localizer.instance().messageStr("shift.in.use").format(shift.name)
                        raise PyShiftException(msg)
                
        self.shifts.remove(shift)

    ##
    # Create a non-working period of time
    # 
    # @param name
    #            Name of period
    # @param description
    #            Description of period
    # @param startDateTime
    #            Starting date and time of day
    # @param duration
    #            Duration of period
    # @return {@link NonWorkingPeriod}
    #
    def createNonWorkingPeriod(self, name: str, description: str, startDateTime: datetime, duration: timedelta) -> NonWorkingPeriod:
        period = NonWorkingPeriod(name, description, startDateTime, duration)

        if (period in self.nonWorkingPeriods):
            msg = Localizer.instance().messageStr("nonworking.period.already.exists").format(name)
            raise PyShiftException(msg)
    
    #    period.workSchedule = self
        self.nonWorkingPeriods.append(period)        
        self.nonWorkingPeriods.sort(key=WorkSchedule.getPeriodKey)

        return period

    ##
    # Create a rotation
    # 
    # @param name        Name of rotation
    # @param description Description of rotation
    #
    # @return {@link Rotation}
    #
    def createRotation(self, name: str, description: str) -> Rotation:
        rotation = Rotation(name, description)

        if (rotation in self.rotations):
            msg = Localizer.instance().messageStr("rotation.already.exists").format(name)
            raise PyShiftException(msg)

        self.rotations.append(rotation)
    #    rotation.workSchedule = self
        return rotation

    ##
    # Get total duration of rotations across all teams.
    # 
    # @return Duration of team rotations
    #
    def getRotationDuration(self) -> timedelta:
        timeSum = timedelta()

        for team in self.teams:
            timeSum = timeSum + team.getRotationDuration()
    
        return timeSum

    ##
    # Get the total working time for all team rotations
    # 
    # @return sum of rotation working times
    #
    def getRotationWorkingTime(self) -> timedelta:
        timeSum = timedelta()

        for team in self.teams:
            timeSum = timeSum + team.rotation.getWorkingTime()
    
        return timeSum

    ##
    # Calculate the scheduled working time between the specified dates and
    # times of day. Non-working periods are removed.
    # 
    # @param fromTime
    #            Starting date and time of day
    # @param toTime
    #            Ending date and time of day
    # @return Working time duration
    #
    def calculateWorkingTime(self, fromTime: datetime, toTime: datetime) -> timedelta:
        timeSum = timedelta()

        # now add up scheduled time by team
        for team in self.teams:
            timeSum = timeSum + team.calculateWorkingTime(fromTime, toTime)
    
        # remove the non-working time
        nonWorking = self.calculateNonWorkingTime(fromTime, toTime)
        timeSum = timeSum - nonWorking

        # clip if negative
        if (timeSum.total_seconds() < 0):
            timeSum = timedelta()

        return timeSum
    
    ##
    # Calculate the non-working time between the specified dates and times of
    # day.
    # 
    # @param fromTime
    #            Starting date and time of day
    # @param toTime
    #            Ending date and time of day
    # @return Non-working time duration
    #
    def calculateNonWorkingTime(self, fromTime: datetime, toTime: datetime) -> timedelta:
        timeSum = timedelta()

        fromSeconds = ShiftUtils.toEpochSecond(fromTime)
        toSeconds = ShiftUtils.toEpochSecond(toTime)

        for period in self.nonWorkingPeriods:
            start = period.startDateTime
            startSeconds = ShiftUtils.toEpochSecond(start)

            end = period.getEndDateTime()
            endSeconds = ShiftUtils.toEpochSecond(end)

            if (fromSeconds >= endSeconds):
                # look at next period
                continue
        
            if (toSeconds <= startSeconds):
                # done with periods
                break
    
            if (fromSeconds <= endSeconds):
                # found a period, check edge conditions
                if (fromSeconds > startSeconds):
                    startSeconds = fromSeconds
            
                if (toSeconds < endSeconds):
                    endSeconds = toSeconds

                timeSum = timeSum + timedelta(seconds=(endSeconds - startSeconds))
        
            if (toSeconds <= endSeconds):
                break
            
        return timeSum

    ##
    # Print shift instances
    # 
    # @param start
    #            Starting date
    # @param end
    #            Ending date
    #
    def printShiftInstances(self, start: date, end: date):
        if (start > end):
            msg = Localizer.instance().messageStr("end.earlier.than.start").format(start, end)
            raise PyShiftException(msg)
    
        days = ShiftUtils.toEpochDay(end) - ShiftUtils.toEpochDay(start) + 1
        day = start

        print(Localizer.instance().messageStr("shifts.working"))
        for i in range(days):
            print("[" + str(i + 1) + "] " + Localizer.instance().messageStr("shifts.day") + ": " + str(day))

            instances = self.getShiftInstancesForDay(day)

            if (len(instances) == 0):
                print("   " + Localizer.instance().messageStr("shifts.non.working"))
            else:
                count = 1
                for instance in instances:
                    print("   (" + str(count) + ")" + str(instance))
                    count = count + 1
        
            day = day + timedelta(days=1)

    def __str__(self) -> str:
        sch = Localizer.instance().messageStr("schedule")
        rd = Localizer.instance().messageStr("rotation.duration") + ": " + ShiftUtils.formatTimedelta(self.getRotationDuration())
        sw = Localizer.instance().messageStr("schedule.working") + ": " + ShiftUtils.formatTimedelta(self.getRotationWorkingTime())
        sf = Localizer.instance().messageStr("schedule.shifts")
        st = Localizer.instance().messageStr("schedule.teams")
        sc = Localizer.instance().messageStr("schedule.coverage")
        sn = Localizer.instance().messageStr("schedule.non")
        stn = Localizer.instance().messageStr("schedule.total")

        text = sch + ": " + super().__str__() + "\n" + rd  + ", " + sw 

        # shifts
        text = text + "\n" + sf + ": "
        count = 1
        for shift in self.shifts:
            text = text + "\n   (" + str(count) + ") " + str(shift)
            count = count + 1
                
        # teams
        text = text + "\n" + st + ": "
        count = 1
        teamPercent = 0.0
            
        for team in self.teams:
            text = text + "\n   (" + str(count) + ") " + str(team)
            teamPercent = teamPercent + team.getPercentageWorked()
            count = count + 1
        
        fmtTeam = ": %.2f" % teamPercent
        text = text + "\n" + sc + ": " + fmtTeam + "%"

        # non-working periods
        periods = self.nonWorkingPeriods

        if (len(periods) > 0):
            text = text + "\n" + sn + ":"

            totalMinutes = timedelta()

            count = 1
            for period in periods:
                totalMinutes = totalMinutes + period.duration
                text = text + "\n   (" + str(count) + ") " + str(period)
                count = count + 1
            
            text = text + "\n" + stn + ": " + str(totalMinutes)


        return text