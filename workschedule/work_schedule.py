from datetime import timedelta

from PyShift.workschedule.named import Named
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift import Shift
from PyShift.workschedule.team import Team
from PyShift.workschedule.rotation import Rotation
from PyShift.workschedule.non_working_period import NonWorkingPeriod
from PyShift.workschedule.shift_exception import PyShiftException
from PyShift.workschedule.shift_utils import ShiftUtils

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
    def __init__(self, name, description):
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
    def deleteTeam(self, team):
        if (team in self.teams):
            self.teams.remove(team)

    ##
    # Remove a non-working period from the schedule
    # 
    # @param period
    #            {@link NonWorkingPeriod}
    def deleteNonWorkingPeriod(self, period):
        if (period in self.nonWorkingPeriods):
            self.nonWorkingPeriods.remove(period)
            
    @staticmethod
    def getPeriodKey(shift):
        return shift.startTime
    ##
    # Get the list of shift instances for the specified date that start in that
    # date
    # 
    # @param day
    #            LocalDate
    # @return List of {@link ShiftInstance}
    def getShiftInstancesForDay(self, day):
        workingShifts = []

        # for each team see if there is a working shift
        for team in self.teams:
            instance = team.getShiftInstanceForDay(day)

            if (instance is None):
                continue
            
            # check to see if this is a non-working day
            addShift = True

            startDate = instance.getStartTime().date()

            for nonWorkingPeriod in self.nonWorkingPeriods:
                if (nonWorkingPeriod.isInPeriod(startDate)):
                    addShift = False
                    break
            
            if (addShift):
                workingShifts.append(instance)
        
        workingShifts.sort(key=WorkSchedule.getPeriodKey)
        return workingShifts

    ##
    # Get the list of shift instances for the specified date and time of day
    # 
    # @param dateTime
    #            Date and time of day
    # @return List of {@link ShiftInstance}
    def getShiftInstancesForTime(self, dateTime):
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
    #            description
    # @param rotation
    #            rotation
    # @param rotationStart 
    #            Start of rotation
    # @return {@link Team}
    def createTeam(self, name, description, rotation, rotationStart):
        team = Team(name, description, rotation, rotationStart)

        if (team in self.teams):
            msg = Localizer.instance().langStr("team.already.exists").format(name)
            raise PyShiftException(msg)
    
        self.teams.append(team)
        team.workSchedule = self
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
    #            duration
    # @return {@link Shift}
    def createShift(self, name, description, start, duration):
        shift = Shift(name, description, start, duration)

        if (shift in self.shifts):
            msg = Localizer.instance().langStr("shift.already.exists").format(name)
            raise PyShiftException(msg)
    
        self.shifts.append(shift)
        shift.workSchedule = self
        return shift

    ##
    # Delete this shift
    # 
    # @param shift
    #            {@link Shift} to delete
    def deleteShift(self, shift):
        if (shift not in self.shifts):
            return
    
        # can't be in use
        for inUseShift in self.shifts:
            for team in self.teams:
                rotation = team.rotation

                for period in rotation.periods:
                    if (period == inUseShift):
                        msg = Localizer.instance().langStr("shift.in.use").format(shift.getName())
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
    def createNonWorkingPeriod(self, name, description, startDateTime, duration):
        period = NonWorkingPeriod(name, description, startDateTime, duration)

        if (period in self.nonWorkingPeriods):
            msg = Localizer.instance().langStr("nonworking.period.already.exists").format(name)
            raise PyShiftException(msg)
    
        period.workSchedule = self
        self.nonWorkingPeriods.append(period)        
        self.nonWorkingPeriods.sort(key=WorkSchedule.getPeriodKey)

        return period

    ##
    # Create a rotation
    # 
    # @param name        Name of rotation
    # @param description Description of rotation
    # @return {@link Rotation}
    #
    def createRotation(self, name, description):
        rotation = Rotation(name, description)

        if (rotation in self.rotations):
            msg = Localizer.instance().langStr("rotation.already.exists").format(name)
            raise PyShiftException(msg)

        self.rotations.append(rotation)
        rotation.workSchedule = self
        return rotation

    ##
    # Get total duration of rotation across all teams.
    # 
    # @return Duration of rotation
    def getRotationDuration(self):
        timeSum = timedelta()

        for team in self.teams:
            timeSum = timeSum + team.getRotationDuration()
    
        return timeSum

    ##
    # Get the total working time for all team rotations
    # 
    # @return rotation working time
    def getRotationWorkingTime(self):
        timeSum = timedelta()

        for team in self.teams:
            timeSum = timeSum + team.rotation.getWorkingTime()
    
        return timeSum

    ##
    # Calculate the scheduled working time between the specified dates and
    # times of day. Non-working periods are removed.
    # 
    # @param from
    #            Starting date and time
    # @param to
    #            Ending date and time
    # @return Working time duration
    # @throws Exception
    #             exception

    def calculateWorkingTime(self, fromTime, toTime):
        timeSum = timedelta()

        # now add up scheduled time by team
        for team in self.teams:
            timeSum = timeSum + team.calculateWorkingTime(fromTime, toTime)
    
        # remove the non-working time
        nonWorking = self.calculateNonWorkingTime(fromTime, toTime)
        timeSum = timeSum - nonWorking

        # clip if negative
        if (timeSum < 0):
            timeSum = timedelta()

        return timeSum

    ##
    # Calculate the non-working time between the specified dates and times of
    # day.
    # 
    # @param from
    #            Starting date and time
    # @param to
    #            Ending date and time
    # @return Non-working time duration
    def calculateNonWorkingTime(self, fromTime, toTime):
        timeSum = timedelta()

        fromSeconds = ShiftUtils.toEpochSecond(fromTime)
        toSeconds = ShiftUtils.toEpochSecond(toTime)

        for period in self.nonWorkingPeriods:
            start = period.startTime
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

                timeSum = timeSum + (endSeconds - startSeconds)
        
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
    # @throws Exception
    #             exception

    def printShiftInstances(self, start, end):
        if (start > end):
            msg = Localizer.instance().langStr("end.earlier.than.start").format(start, end)
            raise PyShiftException(msg)
    
        days = ShiftUtils.toEpochDay(end) - ShiftUtils.toEpochDay(start) + 1
        day = start

        print(Localizer.instance().langStr("shifts.working"))
        for i in range(days):
            print("[" + str(i + 1) + "] " + Localizer.instance().langStr("shifts.day") + ": " + str(day))

            instances = self.getShiftInstancesForDay(day)

            if (len(instances) == 0):
                print("   " + Localizer.instance().langStr("shifts.non.working"))
            else:
                count = 1
                for instance in instances:
                    print("   (" + str(count) + ")" + str(instance))
                    count = count + 1
        
            day = day + timedelta(days=1)

    ##
    # Build a string value for the work schedule
    # 
    # @return String
    def __str__(self):
        sch = Localizer.instance().langStr("schedule")
        rd = Localizer.instance().langStr("rotation.duration")
        sw = Localizer.instance().langStr("schedule.working")
        sf = Localizer.instance().langStr("schedule.shifts")
        st = Localizer.instance().langStr("schedule.teams")
        sc = Localizer.instance().langStr("schedule.coverage")
        sn = Localizer.instance().langStr("schedule.non")
        stn = Localizer.instance().langStr("schedule.total")

        text = sch + ": " + super().__str__()
        try:
            text = text + "\n" + rd + ": " + self.getRotationDuration() + ", " + sw + ": " + self.getRotationWorkingTime()

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
            periods = self.getNonWorkingPeriods()

            if (len(periods) > 0):
                text = text + "\n" + sn + ":"

                totalMinutes = timedelta()

                count = 1
                for period in periods:
                    totalMinutes = totalMinutes + period.minutes()
                    text = text + "\n   (" + str(count) + ") " + str(period)
                    count = count + 1
            
                text = text + "\n" + stn + ": " + str(totalMinutes)
        
        except:
            pass

        return text
    
        ##
    # Compare one work schedule to another one
    #
    def compareTo(self, other):
        return self.name == other.name

        
    

    