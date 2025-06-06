from datetime import datetime, date, time, timedelta
from typing import List

from PyShift.workschedule.named import Named
from PyShift.workschedule.shift_utils import ShiftUtils
from PyShift.workschedule.localizer import Localizer
from PyShift.workschedule.shift_instance import ShiftInstance
from PyShift.workschedule.rotation import Rotation
from PyShift.workschedule.shift_exception import PyShiftException
from PyShift.workschedule.team_member import TeamMember
from PyShift.workschedule.team_member import TeamMemberException

##
# Class Team is a named group of individuals who rotate through a shift
# schedule.
# 
class Team(Named):
    ##
    # Construct a team
    # @param name Name of team
    # @param description Description of team
    # @param rotation {@link Rotation} of this team
    # @param rotationStart Date that the rotation starts for this team
    # 
    def __init__(self, name: str, description: str, rotation: Rotation, rotationStart: date):
        super().__init__(name, description)
                
        # shift rotation days
        self.rotation = rotation
        
        # reference date for starting the rotations
        self.rotationStart = rotationStart
        
        # assigned members
        self.assignedMembers = []
        
        # member exceptions
        self.memberExceptions = []
        
        # team member exception cache by shift instance start
        self.exceptionCache = None

    ##
    # Get the duration of the shift rotation
    # 
    # @return Duration as timedelta
    #
    def getRotationDuration(self) -> timedelta:
        return self.rotation.getDuration()
    
    ##
    # Get the shift rotation's working time as a percentage of the rotation
    # duration
    # 
    # @return Percentage worked
    #
    def getPercentageWorked(self) -> float:
        working = self.rotation.getWorkingTime()
        num = timedelta(seconds=working.total_seconds())
        
        rotationDuration = self.getRotationDuration()
        denom = timedelta(seconds=rotationDuration.total_seconds()) 
        
        return (num / denom) * 100.0
    
    ##
    # Get the average number of hours worked each week by this team
    # 
    # @return average hours worked per week
    #
    def getAverageHoursWorkedPerWeek(self) -> float:
        deltaDays = self.rotation.getDuration().total_seconds() / 86400
        hours = self.rotation.getWorkingTime().total_seconds() / 3600
        
        hoursPerWeek = (hours * 7.0) / deltaDays
        return hoursPerWeek

    ##
    # Get the day number in the rotation for this date
    # 
    # @param day
    #            date
    # @return day number in the rotation, starting at 1
    #
    def getDayInRotation(self, day: date) -> int:
        # calculate total number of days from start of rotation
        dayTo = ShiftUtils.toEpochDay(day)
        start = ShiftUtils.toEpochDay(self.rotationStart)
        deltaDays = dayTo - start

        if (deltaDays < 0):
            msg = Localizer.instance().messageStr("end.earlier.than.start").format(self.rotationStart, day)
            raise PyShiftException(msg)
        
        duration = int(self.rotation.getDuration().total_seconds())
        rotationDays = int(duration / 86400)
        
        if (rotationDays == 0):
            rotationDays = 1
            
        return (deltaDays % rotationDays) + 1

    ##
    # Get the {@link ShiftInstance} for the specified day
    # 
    # @param day
    #            date with a shift instance
    # @return {@link ShiftInstance}
    #
    def getShiftInstanceForDay(self, day: date) -> ShiftInstance:
        shiftInstance = None
        
        #shiftRotation = self.rotation
        
        if (self.rotation.getDuration() == timedelta(seconds=0)):
            # no shiftInstance for that day
            return shiftInstance
    
        dayInRotation = self.getDayInRotation(day)

        # shift or off shift
        period = self.rotation.getPeriods()[dayInRotation - 1]

        if (period.isWorkingPeriod()):
            startDateTime = datetime(day.year, day.month, day.day, hour=period.startTime.hour, minute=period.startTime.minute, second=period.startTime.second)
            shiftInstance = ShiftInstance(period, startDateTime, self)

        return shiftInstance

    ##
    # Check to see if this day is a day off
    # 
    # @param day
    #            date to check
    # @return True if a day off
    #
    def isDayOff(self, day: date) -> bool:
        dayOff = False

        dayInRotation = self.getDayInRotation(day)

        # shift or off shift
        period = self.rotation.periods[dayInRotation - 1]

        if (not period.isWorkingPeriod()):
            dayOff = True

        return dayOff

    ##
    # Calculate the team working time between the specified dates and times of day
    # 
    # @param fromTime
    #            Starting date and time of day
    # @param toTime
    #            Ending date and time of day
    # @return Duration of working time as timedelta
    #
    def calculateWorkingTime(self, fromTime: datetime, toTimeOfDay: datetime) -> timedelta:
        if (fromTime > toTimeOfDay):
            msg = Localizer.instance().messageStr("end.earlier.than.start").format(toTimeOfDay, fromTime)
            raise PyShiftException(msg)
    
        timeSum = timedelta(seconds=0)

        thisDate = fromTime.date()
        thisTime = fromTime.time()
        toDate = toTimeOfDay.date()
        toTimeOfDay = toTimeOfDay.time()
        dayCount = self.rotation.getDayCount()

        # get the working shift from yesterday
        lastShift = None

        yesterday = thisDate - timedelta(days=1)
        yesterdayInstance = self.getShiftInstanceForDay(yesterday)

        if (yesterdayInstance is not None):
            lastShift = yesterdayInstance.shift
    
        # step through each day until done
        while (thisDate <= toDate):
            if (lastShift is not None and lastShift.spansMidnight()):
                # check for days in the middle of the time period
                lastDay = True if (thisDate == toDate) else False
                
                if (not lastDay or (lastDay and toTimeOfDay != time.min)):
                    # add time after midnight in this day
                    afterMidnightSecond = ShiftUtils.toSecondOfDay(lastShift.getEndTime())
                    fromSecond = ShiftUtils.toSecondOfDay(thisTime)

                    if (afterMidnightSecond > fromSecond):
                        timeSum = timeSum + timedelta(seconds=(afterMidnightSecond - fromSecond))

            # today's shift
            instance = self.getShiftInstanceForDay(thisDate)

            duration = None

            if (instance is not None):
                lastShift = instance.shift
                # check for last date
                if (thisDate == toDate):
                    duration = lastShift.calculateTotalWorkingTime(thisTime, toTimeOfDay, True)
                else:
                    duration = lastShift.calculateTotalWorkingTime(thisTime, time.max, True)
            
                timeSum = timeSum + duration
            else:
                lastShift = None

            n = 1
            if (self.getDayInRotation(thisDate) == dayCount):
                # move ahead by the rotation count if possible
                rotationEndDate = thisDate + timedelta(days=dayCount)

                if (rotationEndDate < toDate):
                    n = dayCount
                    timeSum = timeSum + self.rotation.getWorkingTime()

            # move ahead n days starting at midnight
            thisDate = thisDate + timedelta(days=n)
            thisTime = time.min
        # end day loop

        return timeSum
    
    def __str__(self) -> str:
        rpct = Localizer.instance().messageStr("rotation.percentage")
        rs = Localizer.instance().messageStr("rotation.start") + ": " + str(self.rotationStart) 
        avg = Localizer.instance().messageStr("team.hours")
        members = Localizer.instance().messageStr("team.members")
                
        worked = rpct + ": %.3f" % self.getPercentageWorked()
        
        r = self.rotation.__str__()
        hrs = ": %.3f" % self.getAverageHoursWorkedPerWeek()

        text = ""
        try:
            text = super().__str__() + ", " + rs + ", " + r + ", " + worked + "%, " + avg + ": " + hrs + "\n" + members
            
            for member in self.assignedMembers:
                text += "\n\t" + member
        except:
            pass
    
        return text

    ##
    # Add a member to this team
    # 
    # @param member {@link TeamMember} to add
    #
    def addMember(self, member: TeamMember):
        if (member not in self.assignedMembers):
            self.assignedMembers.append(member)

    ##
    # Remove a member from this team
    # 
    # @param member {@link TeamMember} to remove
    #
    def removeMember(self, member: TeamMember):
        if (member in self.assignedMembers):
            self.assignedMembers.remove(member)

    ##
    # True if member is assigned to this team
    #
    def hasMember(self, member: TeamMember) -> bool:
        return (member in self.assignedMembers)
    
    ##
    # Add a member exception to this team
    # 
    # @param memberException {@link TeamMemberException} to add
    #
    def addMemberException(self, memberException: TeamMemberException):
        self.memberExceptions.append(memberException)

    ##
    # Remove a member exception from this team
    # 
    # @param memberException {@link TeamMemberException} to remove
    #
    def removeMemberException(self, memberException: TeamMemberException):
            self.memberExceptions.remove(memberException)
         
    def buildMemberCache(self):
        if (self.exceptionCache is None):
            # create it
            self.exceptionCache = {}

        self.exceptionCache.clear()

        for tme in self.memberExceptions:
            self.exceptionCache[tme.shiftStart] = tme
            
    ##
    # Build a list of team members for the specified shift start
    # 
    # @param shiftStart Shift instance starting date and time
    # @return List of [@link TeamMember]
    #
    def getMembers(self, shiftStart: datetime) -> List[TeamMember]:
        members = []

        # build the cache if not already done
        self.buildMemberCache()

        # assigned to the team
        for member in self.assignedMembers:
            members.append(member)

        # any exceptions?
        if shiftStart in self.exceptionCache:
            tme = self.exceptionCache[shiftStart]
            
            if (tme.addition is not None):
                members.append(tme.addition)

            if (tme.removal is not None):
                members.remove(tme.removal)

        return members
    