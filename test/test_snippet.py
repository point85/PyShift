import unittest

from datetime import date, time, timedelta, datetime
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule

class TestSnippet(BaseTest):    
    def testIt(self):
        self.workSchedule = WorkSchedule("Working Time1", "Test working time")

        # shift does not cross midnight
        shiftDuration = timedelta(hours=8)
        shiftStart = time(7, 0, 0)

        shift = self.workSchedule.createShift("Work Shift1", "Working time shift", shiftStart, shiftDuration)
        shiftEnd = shift.getEndTime()

        # case #1
        duration = shift.calculateWorkingTime(time(hour=shiftStart.hour-3), time(hour=shiftStart.hour-2))
        print(str(time(hour=shiftStart.hour-3)))
        print(str(duration))
                  
        
if __name__ == '__main__':
    unittest.main()