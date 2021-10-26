from datetime import datetime, date, time, timedelta
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule


class TestWorkSchedule(BaseTest):
    """
    def testExceptions(self):
        self.workSchedule = WorkSchedule("Exceptions", "Test exceptions")
        shiftDuration = timedelta(hours=24)
        time(shiftStart = time(7, 0, 0)
        shift = self.workSchedule.createShift("Test", "Test shift", time(shiftStart, shiftDuration)

        period = self.workSchedule.createNonWorkingPeriod("Non-working", "Non-working period",
                datetime.combine(date(2017, 1, 1, time(0, 0, 0), timedelta(hours=24))
    
        try:
            period.setDuration(timedelta(seconds=0))
            self.self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass
    
        try:
            period.setStartDateTime(None)
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            # same period
            self.workSchedule.createNonWorkingPeriod("Non-working", "Non-working period",
                datetime.combine(date(2017, 1, 1, time(0, 0, 0), timedelta(hours=24))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            # crosses midnight
            shift.calculateWorkingTime(time(shiftStart.hour-1, shift.getEndTime() + timedelta(hours=1))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            shift.setDuration(None)
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            shift.setDuration(timedelta(seconds=0))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            shift.setDuration(timedelta(seconds=48*3600))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            # same shift
            self.workSchedule.createShift("Test", "Test shift", time(shiftStart, shiftDuration)
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass        

        rotation = self.workSchedule.createRotation("Rotation", "Rotation")
        rotation.addSegment(shift, 5, 2)

        startRotation = date(2016, 12, 31)
        team = self.workSchedule.createTeam("Team", "Team", rotation, startRotation)

        # ok
        fromDateTime = datetime.combine(date(2017, 1, 1, time(7, 0, 0))
        toDateTime   = datetime.combine(date(2017, 2, 1, time(0, 0, 0))
                                      
        self.workSchedule.calculateWorkingTime(fromDateTime, toDateTime)
    
        try:
            # end before start
            fromDateTime = datetime.combine(date(2017, 1, 2, time(0, 0, 0))
            toDateTime   = datetime.combine(date(2017, 1, 1, time(0, 0, 0))
            self.workSchedule.calculateWorkingTime(fromDateTime, toDateTime)
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass 

        try:
            # same team
            team = self.workSchedule.createTeam("Team", "Team", rotation, startRotation)
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass 

        try:
            # date before start
            team.getDayInRotation(date(2016, 1, 1))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass 

        try:
            # end before start
            self.workSchedule.printShiftInstances(date(2017, 1, 2, date(2017, 1, 1))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass 

        try:
            # delete in-use shift
            self.workSchedule.deleteShift(shift)
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass 

        # breaks
        lunch = shift.createBreak("Lunch", "Lunch", time(12, 0, 0, timedelta(minutes=60))
        lunch.setDuration(timedelta(minutes=30))
        lunch.startTime = time(11, 30, 0)
        shift.removeBreak(lunch)
        shift.removeBreak(lunch)

        shift2 = self.workSchedule.createShift("Test2", "Test shift2", time(shiftStart, shiftDuration)
        self.assertFalse(shift == shift2)

        lunch2 = shift2.createBreak("Lunch2", "Lunch", time(12, 0, 0, timedelta(minutes=60))
        shift.removeBreak(lunch2)
        
        # ok to delete
        schedule2 = WorkSchedule("Exceptions2", "Test exceptions2")
        schedule2.name = "Schedule 2"
        schedule2.description = "a description"

        schedule2.deleteShift(shift)
        schedule2.deleteTeam(team)
        schedule2.deleteNonWorkingPeriod(period)

        # nulls
        try:
            self.workSchedule.createShift("1", "1", None, timedelta(minutes=60))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            self.workSchedule.createShift("1", "1", time(shiftStart, None)
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            self.workSchedule.createShift(None, "1", time(shiftStart, timedelta(minutes=60))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        self.assertFalse(shift == rotation)

        # hashcode()
        team.__hash__()
        teams = {}
        teams[team.name] = team
        value = teams[team.name]
        self.assertTrue(value is not None)
    
    """
    """
    def testShiftWorkingTime(self):
        self.workSchedule = WorkSchedule("Working Time1", "Test working time")

        # shift does not cross midnight
        shiftDuration = timedelta(hours=8)
        shiftStart = time(7, 0, 0)

        shift = self.workSchedule.createShift("Work Shift1", "Working time shift", shiftStart, shiftDuration)
        shiftEnd = shift.getEndTime()

        # case #1
        duration = shift.calculateWorkingTime(time(hour=shiftStart.hour-3), time(hour=shiftStart.hour-2))
        self.assertTrue(duration.total_seconds() == 0)
        workingTime = shift.calculateWorkingTime(time(hour=shiftStart.hour-3), time(hour=shiftStart.hour-3))
        self.assertTrue(workingTime.total_seconds() == 0)
    
        # case #2
        workingTime = shift.calculateWorkingTime(time(shiftStart.hour-1), time(shiftStart.hour+1))
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #3
        workingTime = shift.calculateWorkingTime(time(shiftStart.hour+1), time(shiftStart.hour+2))
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #4
        workingTime = shift.calculateWorkingTime(time(shiftEnd.hour-1), time(shiftEnd.hour+1))
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #5
        workingTime = shift.calculateWorkingTime(time(shiftEnd.hour+1), time(shiftEnd.hour+2))
        self.assertTrue(workingTime.total_seconds() == 0)
        workingTime = shift.calculateWorkingTime(time(shiftEnd.hour+1), time(shiftEnd.hour+1))
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #6
        workingTime = shift.calculateWorkingTime(time(shiftStart.hour-1), time(shiftEnd.hour+1))
        self.assertTrue(workingTime.total_seconds() == shiftDuration.total_seconds())

        # case #7
        workingTime = shift.calculateWorkingTime(time(shiftStart.hour+1), time(shiftStart.hour+1))
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #8
        workingTime = shift.calculateWorkingTime(time(shiftStart.hour), time(shiftEnd.hour))
        self.assertTrue(workingTime.total_seconds() == shiftDuration.total_seconds())

        # case #9
        workingTime = shift.calculateWorkingTime(time(shiftStart.hour), time(shiftStart.hour))
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #10
        workingTime = shift.calculateWorkingTime(shiftEnd, shiftEnd)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #11
        workingTime = shift.calculateWorkingTime(time(shiftStart.hour), time(shiftStart.hour, shiftStart.minute, shiftStart.second+1))
        self.assertTrue(workingTime.total_seconds() == 1)

        # case #12
        workingTime = shift.calculateWorkingTime(time(shiftEnd.hour-1), shiftEnd)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # 8 hr shift crossing midnight
        shiftStart = time(22, 0, 0)

        shift = self.workSchedule.createShift("Work Shift2", "Working time shift spans midnight", shiftStart, shiftDuration)
        shiftEnd = shift.getEndTime()

        # case #1
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-3), time(shiftStart.hour-2), True)
        self.assertTrue(workingTime.total_seconds() == 0)
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-3), time(shiftStart.hour-3), True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #2
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-1), time(shiftStart.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #3
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour+1), time.min, True)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #4
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour-1), time(shiftEnd.hour+1), False)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #5
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour+1), time(shiftEnd.hour+2), True)
        self.assertTrue(workingTime.total_seconds() == 0)
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour+1), time(shiftEnd.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #6
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-1), time(shiftEnd.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == shiftDuration.total_seconds())

        # case #7
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour+1), time(shiftStart.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #8
        workingTime = shift.calculateTotalWorkingTime(shiftStart, shiftEnd, True)
        self.assertTrue(workingTime.total_seconds() == shiftDuration.total_seconds())

        # case #9
        workingTime = shift.calculateTotalWorkingTime(shiftStart, shiftStart, True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #10
        workingTime = shift.calculateTotalWorkingTime(shiftEnd, shiftEnd, True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #11
        workingTime = shift.calculateTotalWorkingTime(shiftStart, time(shiftStart.hour, shiftStart.minute, shiftStart.second+1), True)
        self.assertTrue(workingTime.total_seconds() == 1)

        # case #12
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour-1), shiftEnd, False)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # 24 hr shift crossing midnight
        shiftDuration = timedelta(hours=24)
        shiftStart = time(7, 0, 0)

        shift = self.workSchedule.createShift("Work Shift3", "Working time shift", shiftStart, shiftDuration)
        shiftEnd = shift.getEndTime()

        # case #1
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-3), time(shiftStart.hour-2), False)
        self.assertTrue(workingTime.total_seconds() == 3600)
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-3), time(shiftStart.hour-3), True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #2
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-1), time(shiftStart.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #3
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour+1), time(shiftStart.hour+2), True)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #4
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour-1), time(shiftEnd.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #5
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour+1), time(shiftEnd.hour+2), True)
        self.assertTrue(workingTime.total_seconds() == 3600)
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour+1), time(shiftEnd.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #6
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour-1), time(shiftEnd.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 3600)

        # case #7
        workingTime = shift.calculateTotalWorkingTime(time(shiftStart.hour+1), time(shiftStart.hour+1), True)
        self.assertTrue(workingTime.total_seconds() == 0)

        # case #8
        workingTime = shift.calculateTotalWorkingTime(shiftStart, shiftEnd, True)
        self.assertTrue(workingTime.total_seconds() == shiftDuration.total_seconds())

        # case #9
        workingTime = shift.calculateTotalWorkingTime(shiftStart, shiftStart, True)
        self.assertTrue(workingTime.total_seconds() == shiftDuration.total_seconds())

        # case #10
        workingTime = shift.calculateTotalWorkingTime(shiftEnd, shiftEnd, True)
        self.assertTrue(workingTime.total_seconds() == shiftDuration.total_seconds())

        # case #11
        workingTime = shift.calculateTotalWorkingTime(shiftStart, time(shiftStart.hour, shiftStart.minute, shiftStart.second+1), True)
        self.assertTrue(workingTime.total_seconds() == 1)

        # case #12
        workingTime = shift.calculateTotalWorkingTime(time(shiftEnd.hour-1), shiftEnd, False)
        self.assertTrue(workingTime.total_seconds() == 3600)
    """    
    """
    def testTeamWorkingTime(self):
        self.workSchedule = WorkSchedule("Team Working Time", "Test team working time")
        shiftDuration = timedelta(hours=12)
        halfShift = timedelta(hours=6)
        shiftStart = time(7, 0, 0)

        shift = self.workSchedule.createShift("Team Shift1", "Team shift 1", shiftStart, shiftDuration)

        rotation = self.workSchedule.createRotation("Team", "Rotation")
        rotation.addSegment(shift, 1, 1)

        startRotation = date(2017, 1, 1)
        team = self.workSchedule.createTeam("Team", "Team", rotation, startRotation)
        team.rotationStart = startRotation

        # case #1
        fromDateTime = datetime.combine(startRotation, shiftStart) + timedelta(days=rotation.getDayCount())
        toDateTime = fromDateTime + timedelta(days=1)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration)

        # case #2
        toDateTime = fromDateTime + timedelta(days=2)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration)

        # case #3
        toDateTime = fromDateTime + timedelta(days=3)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + shiftDuration)

        # case #4
        toDateTime = fromDateTime + timedelta(days=4)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + shiftDuration)

        # case #5
        fromDateTime = datetime.combine(startRotation, shiftStart) + timedelta(days=rotation.getDayCount(), hours=6)
        toDateTime = fromDateTime + timedelta(days=1)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == halfShift)

        # case #6
        toDateTime = fromDateTime + timedelta(days=2)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration)

        # case #7
        toDateTime = fromDateTime + timedelta(days=3)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + halfShift)

        # case #8
        toDateTime = fromDateTime + timedelta(days=4)
        workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + shiftDuration)

        # now crossing midnight
        shiftStart = time(18, 0, 0)
        shift2 = self.workSchedule.createShift("Team Shift2", "Team shift 2", shiftStart, shiftDuration)

        rotation2 = self.workSchedule.createRotation("Case 8", "Case 8")
        rotation2.addSegment(shift2, 1, 1)

        team2 = self.workSchedule.createTeam("Team2", "Team 2", rotation2, startRotation)
        team2.rotationStart = startRotation

        # case #1
        fromDateTime = datetime.combine(startRotation, shiftStart) + timedelta(days=rotation.getDayCount())
        toDateTime = fromDateTime + timedelta(days=1)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration)

        # case #2
        toDateTime = fromDateTime + timedelta(days=2)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration)

        # case #3
        toDateTime = fromDateTime + timedelta(days=3)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + shiftDuration)

        # case #4
        toDateTime = fromDateTime + timedelta(days=4)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + shiftDuration)

        # case #5
        dayDelta = datetime.combine(startRotation, shiftStart) + timedelta(days=rotation.getDayCount())
        fromDateTime = datetime.combine(dayDelta.date(), time.max)
        toDateTime = fromDateTime + timedelta(days=1)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == halfShift)

        # case #6
        toDateTime = fromDateTime + timedelta(days=2)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration)

        # case #7
        toDateTime = fromDateTime + timedelta(days=3)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + halfShift)

        # case #8
        toDateTime = fromDateTime + timedelta(days=4)
        workingTime = team2.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(workingTime == shiftDuration + shiftDuration)
    """
    
    def testNonWorkingTime(self): 
        self.workSchedule =  WorkSchedule("Non Working Time", "Test non working time")
        localDate = date(2017, 1, 1)
        localTime = time(7, 0, 0)

        period1 = self.workSchedule.createNonWorkingPeriod("Day1", "First test day",
                datetime.combine(localDate, time.min), timedelta(hours=24))
        period2 = self.workSchedule.createNonWorkingPeriod("Day2", "First test day",
                datetime.combine(localDate, localTime) + timedelta(days=7), timedelta(hours=24))

        fromDateTime = datetime.combine(localDate, localTime)
        toDateTime = datetime.combine(localDate, time(localTime.hour+1))

        # case #1
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=1))

        # case #2
        fromDateTime = datetime.combine(localDate, localTime) - timedelta(days=1)
        toDateTime = datetime.combine(localDate, localTime) + timedelta(days=1)
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=24))

        # case #3
        fromDateTime = datetime.combine(localDate, localTime) - timedelta(days=1)
        toDateTime = datetime.combine(localDate, time(localTime.hour+1)) - timedelta(days=1)
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=0))

        # case #4
        fromDateTime = datetime.combine(localDate, localTime) + timedelta(days=1)
        toDateTime = datetime.combine(localDate, time(localTime.hour+1)) + timedelta(days=1)
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=0))

        # case #5
        fromDateTime = datetime.combine(localDate, localTime) - timedelta(days=1)
        toDateTime = datetime.combine(localDate, localTime)
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=7))

        # case #6
        fromDateTime = datetime.combine(localDate, localTime)
        toDateTime = datetime.combine(localDate, localTime) + timedelta(days=1)
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=17))

        # case #7
        fromDateTime = datetime.combine(localDate, time(hour=12))
        toDateTime = datetime.combine(localDate, time(hour=12)) + timedelta(days=7)
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=17))

        # case #8
        fromDateTime = datetime.combine(localDate, time(hour=12)) - timedelta(days=1)
        toDateTime = datetime.combine(localDate, time(hour=12)) + timedelta(days=8)
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=48))

        # case #9
        self.workSchedule.deleteNonWorkingPeriod(period1)
        self.workSchedule.deleteNonWorkingPeriod(period2)
        fromDateTime = datetime.combine(localDate, localTime)
        toDateTime = datetime.combine(localDate, time(localTime.hour+1))

        # case #10
        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=0))

        shiftDuration = timedelta(hours=8)
        shiftStart = time(7, 0, 0)

        shift = self.workSchedule.createShift("Work Shift1", "Working time shift", shiftStart, shiftDuration)

        rotation = self.workSchedule.createRotation("Case 10", "Case10")
        rotation.addSegment(shift, 1, 1)

        startRotation = date(2017, 1, 1)
        team = self.workSchedule.createTeam("Team", "Team", rotation, startRotation)
        team.rotationStart = startRotation

        period1 = self.workSchedule.createNonWorkingPeriod("Day1", "First test day", datetime.combine(localDate, time.min),
            timedelta(hours=24))

        mark = localDate + timedelta(days=rotation.getDayCount())
        fromDateTime = datetime.combine(mark, time(hour=localTime.hour-2))
        toDateTime = datetime.combine(mark, time(hour=localTime.hour-1))

        # case #11
        duration = self.workSchedule.calculateWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=0))

        # case #12
        fromDateTime = datetime.combine(localDate, shiftStart)
        toDateTime = datetime.combine(localDate, time(localTime.hour+8))

        duration = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime)
        self.assertTrue(duration == timedelta(hours=8))
    