import unittest

from datetime import date, time, timedelta, datetime
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule

class TestSnippet(BaseTest):    
    def testTwoTeam(self):
        description = "".join(["This is a fixed (no rotation) plan that uses 2 teams and two 12-hr shifts to provide 24/7 coverage. "
        ,"One team will be permanently on the day shift and the other will be on the night shift."])

        self.workSchedule = WorkSchedule("2 Team Fixed 12 Plan", description)

        # Day shift, starts at 07:00 for 12 hours
        day = self.workSchedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=12))

        # Night shift, starts at 19:00 for 12 hours
        night = self.workSchedule.createShift("Night", "Night shift", time(19, 0, 0), timedelta(hours=12))

        # Team1 rotation
        team1Rotation = self.workSchedule.createRotation("Team1", "Team1")
        team1Rotation.addSegment(day, 1, 0)

        # Team1 rotation
        team2Rotation = self.workSchedule.createRotation("Team2", "Team2")
        team2Rotation.addSegment(night, 1, 0)

        self.workSchedule.createTeam("Team 1", "First team", team1Rotation, self.referenceDate)
        self.workSchedule.createTeam("Team 2", "Second team", team2Rotation, self.referenceDate)
        
        # specific checks
        fromDateTime = datetime.combine(self.laterDate, self.laterTime)
        toDateTime = datetime.combine(self.laterDate + timedelta(days=28), self.laterTime)
        
        for team in self.workSchedule.teams:
            workingTime = team.calculateWorkingTime(fromDateTime, toDateTime)
            print("Team: " + team.name + " WT: " + str(workingTime))
        
        workingTime = self.workSchedule.calculateWorkingTime(fromDateTime, toDateTime);
        nonWorkingTime = self.workSchedule.calculateNonWorkingTime(fromDateTime, toDateTime);
        self.assertTrue(workingTime.total_seconds() == 1320 * 3600);
        self.assertTrue(nonWorkingTime.total_seconds() == 0);
        
        self.assertTrue(self.workSchedule.getRotationDuration().total_seconds() == 48 * 3600)
        self.assertTrue(self.workSchedule.getRotationWorkingTime().total_seconds() == 24 * 3600)
        
        for team in self.workSchedule.teams:
            self.assertTrue(team.rotation.getDuration().total_seconds() == 24 * 3600)
            self.assertAlmostEqual(team.getPercentageWorked(), 50.00, 2)
            self.assertTrue(team.rotation.getWorkingTime().total_seconds() == 12 * 3600)
            self.assertAlmostEqual(team.getAverageHoursWorkedPerWeek(), 84.0, 1)

        self.runBaseTest(timedelta(hours=12), timedelta(days=1))
                  
        
if __name__ == '__main__':
    unittest.main()