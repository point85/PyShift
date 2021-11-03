import unittest

from datetime import date, time, timedelta
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule

class TestSnippet(BaseTest):    
    def testIt(self):
        # Kern Co, CA
        self.workSchedule = WorkSchedule("Kern Co.", "Three 24 hour alternating shifts")

        # shift, start 07:00 for 24 hours
        shift = self.workSchedule.createShift("24 Hour", "24 hour shift", time(7, 0, 0), timedelta(hours=24))

        # 2 days ON, 2 OFF, 2 ON, 2 OFF, 2 ON, 8 OFF
        rotation = self.workSchedule.createRotation("24 Hour", "2 days ON, 2 OFF, 2 ON, 2 OFF, 2 ON, 8 OFF")
        rotation.addSegment(shift, 2, 2)
        rotation.addSegment(shift, 2, 2)
        rotation.addSegment(shift, 2, 8)

        self.workSchedule.createTeam("Red", "A Shift", rotation, date(2017, 1, 8))
        self.workSchedule.createTeam("Black", "B Shift", rotation, date(2017, 2, 1))
        self.workSchedule.createTeam("Green", "C Shift", rotation, date(2017, 1, 2))
        
        print(str(self.workSchedule))
        self.workSchedule.printShiftInstances(date(2021, 11, 1), date(2021, 11, 7))

                  
        
if __name__ == '__main__':
    unittest.main()