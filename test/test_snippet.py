import unittest

from datetime import time, timedelta
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule

class TestSnippet(BaseTest):              
    def testLowNight(self):         
        self.workSchedule = WorkSchedule("Low Night Demand Plan", "Low night demand")
        
        # 3 shifts
        day = self.workSchedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=8))
        swing = self.workSchedule.createShift("Swing", "Swing shift", time(15, 0, 0), timedelta(hours=8))
        night = self.workSchedule.createShift("Night", "Night shift", time(23, 0, 0), timedelta(hours=8))

        # Team rotation
        rotation = self.workSchedule.createRotation("Low night demand", "Low night demand")
        rotation.addSegment(day, 3, 0)
        rotation.addSegment(swing, 4, 3)
        rotation.addSegment(day, 4, 0)
        rotation.addSegment(swing, 3, 4)
        rotation.addSegment(day, 3, 0)
        rotation.addSegment(night, 4, 3)
        rotation.addSegment(day, 4, 0)
        rotation.addSegment(night, 3, 4)

        # 6 teams
        self.workSchedule.createTeam("Team1", "First team", rotation, self.referenceDate)
        self.workSchedule.createTeam("Team2", "Second team", rotation, self.referenceDate - timedelta(days=21))
        self.workSchedule.createTeam("Team3", "Third team", rotation, self.referenceDate - timedelta(days=7))
        self.workSchedule.createTeam("Team4", "Fourth team", rotation, self.referenceDate - timedelta(days=28))
        self.workSchedule.createTeam("Team5", "Fifth team", rotation, self.referenceDate - timedelta(days=14))
        self.workSchedule.createTeam("Team6", "Sixth team", rotation, self.referenceDate - timedelta(days=35))

        self.runBaseTest(timedelta(hours=224), timedelta(days=42))
        
if __name__ == '__main__':
    unittest.main()