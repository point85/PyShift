from datetime import datetime, date, time, timedelta
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule


class TestWorkSchedule(BaseTest):
    def testExceptions(self):
        self.workSchedule = WorkSchedule("Exceptions", "Test exceptions")
        shiftDuration = timedelta(hours=24)
        shiftStart = time(7, 0, 0)
        shift = self.workSchedule.createShift("Test", "Test shift", shiftStart, shiftDuration)

        period = self.workSchedule.createNonWorkingPeriod("Non-working", "Non-working period",
                datetime.combine(date(2017, 1, 1), time(0, 0, 0)), timedelta(hours=24))
    
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
                datetime.combine(date(2017, 1, 1), time(0, 0, 0)), timedelta(hours=24))
            self.fail()
        except Exception as e:
            # expected
            print(str(e))
            pass

        try:
            # crosses midnight
            shift.calculateWorkingTime(shiftStart - timedelta(hours=1), shift.getEndTime() + timedelta(hours=1))
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
            self.workSchedule.createShift("Test", "Test shift", shiftStart, shiftDuration)
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
        fromDateTime = datetime.combine(date(2017, 1, 1), time(7, 0, 0))
        toDateTime   = datetime.combine(date(2017, 2, 1), time(0, 0, 0))
                                      
        self.workSchedule.calculateWorkingTime(fromDateTime, toDateTime)
    
        try:
            # end before start
            fromDateTime = datetime.combine(date(2017, 1, 2), time(0, 0, 0))
            toDateTime   = datetime.combine(date(2017, 1, 1), time(0, 0, 0))
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
            self.workSchedule.printShiftInstances(date(2017, 1, 2), date(2017, 1, 1))
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
        lunch = shift.createBreak("Lunch", "Lunch", time(12, 0, 0), timedelta(minutes=60))
        lunch.setDuration(timedelta(minutes=30))
        lunch.startTime = time(11, 30, 0)
        shift.removeBreak(lunch)
        shift.removeBreak(lunch)

        shift2 = self.workSchedule.createShift("Test2", "Test shift2", shiftStart, shiftDuration)
        self.assertFalse(shift == shift2)

        lunch2 = shift2.createBreak("Lunch2", "Lunch", time(12, 0, 0), timedelta(minutes=60))
        shift.removeBreak(lunch2)
    