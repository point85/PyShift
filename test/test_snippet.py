import unittest

from datetime import time, timedelta
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule

class TestSnippet(BaseTest):           
    def testLowNight(self): 
        schedule = WorkSchedule("Low Night Demand Plan", "Low night demand")
        
        # 3 shifts
        day = schedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=8))
        swing = schedule.createShift("Swing", "Swing shift", time(15, 0, 0), timedelta(hours=8))
        night = schedule.createShift("Night", "Night shift", time(23, 0, 0), timedelta(hours=8))

        # Team rotation
        rotation = schedule.createRotation("Low night demand", "Low night demand")
        rotation.addSegment(day, 3, 0)
        rotation.addSegment(swing, 4, 3)
        rotation.addSegment(day, 4, 0)
        rotation.addSegment(swing, 3, 4)
        rotation.addSegment(day, 3, 0)
        rotation.addSegment(night, 4, 3)
        rotation.addSegment(day, 4, 0)
        rotation.addSegment(night, 3, 4)

        # 6 teams
        schedule.createTeam("Team1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team2", "Second team", rotation, self.referenceDate - timedelta(days=21))
        schedule.createTeam("Team3", "Third team", rotation, self.referenceDate - timedelta(days=7))
        schedule.createTeam("Team4", "Fourth team", rotation, self.referenceDate - timedelta(days=28))
        schedule.createTeam("Team5", "Fifth team", rotation, self.referenceDate - timedelta(days=14))
        schedule.createTeam("Team6", "Sixth team", rotation, self.referenceDate - timedelta(days=35))

        self.runBaseTest(schedule, timedelta(hours=224), timedelta(days=42), self.referenceDate)
      
if __name__ == '__main__':
    unittest.main()