import unittest
from abc import ABC

from datetime import datetime, date, timedelta
from PyShift.workschedule.shift_utils import ShiftUtils

##
# Base class for testing shift plans
# 
class BaseTest(ABC, unittest.TestCase):     
    def setUp(self):
        # work schedule
        self.schedule = None
    
        # reference date for start of shift rotations
        self.referenceDate = date(2016, 10, 31)
        
        # partial test flags
        self.testToString = True
        self.testDeletions = True

    def testShifts(self, ws): 
        self.assertTrue(len(ws.shifts) > 0)

        for shift in ws.shifts: 
            total = shift.duration
            start = shift.startTime
            end = shift.getEndTime()

            self.assertTrue(len(shift.name) > 0)
            self.assertTrue(len(shift.description) > 0)

            self.assertTrue(total.total_seconds() > 0)
            self.assertTrue(shift.breaks is not None)
            self.assertTrue(start is not None)
            self.assertTrue(end is not None)

            worked = None
            spansMidnight = shift.spansMidnight()
            
            if (spansMidnight): 
                # get the interval before midnight
                worked = shift.calculateTotalWorkingTime(start, end, True)
            else:
                worked = shift.calculateWorkingTime(start, end)

            self.assertTrue(worked == total)

            if (spansMidnight): 
                worked = shift.calculateTotalWorkingTime(start, start, True)
            else: 
                worked = shift.calculateWorkingTime(start, start)

            # 24 hour shift on midnight is a special case
            if (total.total_seconds() == 86400): 
                self.assertTrue(worked.total_seconds() == 86400)
            else: 
                self.assertTrue(worked.total_seconds() == 0)

            if (spansMidnight): 
                worked = shift.calculateTotalWorkingTime(end, end, True)
            else: 
                worked = shift.calculateWorkingTime(end, end)

            if (total.total_seconds() == 86400): 
                self.assertTrue(worked.total_seconds() == 86400)
            else: 
                self.assertTrue(worked.total_seconds() == 0)

            try: 
                t = start - timedelta(minutes=1)
                worked = shift.calculateWorkingTime(t, end)

                if (total != shift.duration):
                    self.fail("Bad working time")
    
            except:
                pass

            try: 
                t = end + timedelta(minutes=1)
                worked = shift.calculateWorkingTime(start, t)
                if (total != shift.duration): 
                    self.fail("Bad working time")
    
            except: 
                pass
            
    def testTeams(self, ws, hoursPerRotation, rotationDays): 
        self.assertTrue(len(ws.teams) > 0)

        for team in ws.teams:
            self.assertTrue(len(team.name) > 0)
            self.assertTrue(len(team.description) > 0)
            self.assertTrue(team.getDayInRotation(team.rotationStart) == 1)
            hours = team.rotation.getWorkingTime()
            self.assertTrue(hours == hoursPerRotation)
            self.assertTrue(team.getPercentageWorked() > 0.0)
            self.assertTrue(team.getRotationDuration() == rotationDays)
            self.assertTrue(team.rotationStart is not None)

            rotation = team.rotation
            self.assertTrue(rotation.duration == rotationDays)
            self.assertTrue(len(rotation.periods) > 0)
            self.assertTrue(rotation.getWorkingTime().seconds() <= rotation.duration.seconds())

        self.assertTrue(ws.nonWorkingPeriods is not None)

    def testShiftInstances(self, ws, instanceReference): 
        ONE_DAY = timedelta(days=1)
        ONE_SECOND = timedelta(seconds=1)
        
        rotation = ws.teams[0].rotation

        # shift instances
        startDate = instanceReference
        endDate = instanceReference + rotation.duration.days()

        days = ShiftUtils.toEpochDay(endDate) - ShiftUtils.toEpochDay(instanceReference) + 1
        day = startDate

        for _i in range(days):
            instances = ws.getShiftInstancesForDay(day)

            for instance in instances:
                self.assertTrue(instance.startTime < instance.getEndTime())
                self.assertTrue(instance.shift is not None)
                self.assertTrue(instance.team is not None)

                shift = instance.getShift()
                startTime = shift.startTime
                endTime = shift.getEndTime()

                self.assertTrue(shift.isInShift(startTime))
                self.assertTrue(shift.isInShift(startTime + ONE_SECOND))

                shiftDuration = instance.shift.duration

                # midnight is special case
                if (shiftDuration != timedelta(hours=24)): 
                    self.assertFalse(shift.isInShift(startTime - ONE_SECOND))
    

                self.assertTrue(shift.isInShift(endTime))
                self.assertTrue(shift.isInShift(endTime - ONE_SECOND))

                if (shiftDuration != ONE_DAY):
                    self.assertFalse(shift.isInShift(endTime + ONE_SECOND))
    
                ldt = datetime.combine(day, startTime)
                self.assertTrue(len(ws.getShiftInstancesForTime(ldt))> 0)

                ldt = datetime.combine(day, startTime + ONE_SECOND)
                self.assertTrue(len(ws.getShiftInstancesForTime(ldt))> 0)

                ldt = datetime.combine(day, startTime - ONE_SECOND)

                for si in ws.getShiftInstancesForTime(ldt):
                    if (shiftDuration != timedelta(hours=24)): 
                        self.assertFalse(shift.name == si.shift.name)

                ldt = datetime.combine(day, endTime)
                self.assertTrue(len(ws.getShiftInstancesForTime(ldt))> 0)

                ldt = datetime.combine(day, endTime - ONE_SECOND)
                self.assertTrue(len(ws.getShiftInstancesForTime(ldt)) > 0)

                ldt = datetime.combine(day, endTime + ONE_SECOND)

                for si in ws.getShiftInstancesForTime(ldt):
                    if (shiftDuration != ONE_DAY): 
                        self.assertFalse(shift.name == si.shift.name)
        
            day = day + ONE_DAY

    def runBaseTest(self, ws, hoursPerRotation, rotationDays, instanceReference): 
        # toString
        if (self.testToString): 
            print(str(ws))

            end = timedelta(days=rotationDays.days)
            ws.printShiftInstances(instanceReference, instanceReference + end)

        self.assertTrue(len(ws.name) > 0)
        self.assertTrue(len(ws.description) > 0)
        self.assertTrue(ws.nonWorkingPeriods is not None)

        # shifts
        self.testShifts(ws)

        # teams
        self.testTeams(ws, hoursPerRotation, rotationDays)

        # shift instances
        self.testShiftInstances(ws, instanceReference)

        if (self.testDeletions): 
            self.testDeletions()

    def testDeletions(self): 
        if (self.schedule is None):
            return 
        
        # team deletions
        teams = self.schedule.teams

        for team in teams: 
            self.schedule.deleteTeam(team)

        self.assertTrue(len(self.schedule.teams) == 0)

        # shift deletions
        shifts = self.schedule.shifts

        for shift in shifts:
            self.schedule.deleteShift(shift)

        self.assertTrue(len(self.schedule.shifts) == 0)

        # non-working period deletions
        periods = self.schedule.getNonWorkingPeriods()

        for period in periods:
            self.schedule.deleteNonWorkingPeriod(period)

        self.assertTrue(len(self.schedule.getNonWorkingPeriods()) == 0)
