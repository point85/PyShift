from abc import ABC
from datetime import date, timedelta

##
# Base class for testing shift plans
# 
class BaseTest(ABC):     
    def __init__(self):
        # work schedule
        self.schedule = None
    
        # reference date for start of shift rotations
        self.referenceDate = date(2016, 10, 31)
        
        # partial test flags
        self.testToString = False
        self.testDeletions = True

    def testShifts(self, ws): 
        self.self.assertTrue(len(ws.shifts) > 0)

        for shift in ws.shifts: 
            total = shift.duration
            start = shift.startTime
            end = shift.getEndTime()

            self.assertTrue(len(shift.name) > 0)
            self.assertTrue(len(shift.description) > 0)

            self.assertTrue(total.minutes() > 0)
            self.assertTrue(shift.breaks is not None)
            self.assertTrue(start is not None)
            self.assertTrue(end is not None)

            worked = None
            spansMidnight = shift.spansMidnight()
            
            if (spansMidnight): 
                # get the interval before midnight
                worked = shift.calculateWorkingTime(start, end, True)
            else:
                worked = shift.calculateWorkingTime(start, end)

            self.assertTrue(worked == total)

            if (spansMidnight): 
                worked = shift.calculateWorkingTime(start, start, True)
            else: 
                worked = shift.calculateWorkingTime(start, start)

            # 24 hour shift on midnight is a special case
            if (total.hours() == 24): 
                self.assertTrue(worked.hours() == 24)
            else: 
                self.assertTrue(worked.hours() == 0)

            if (spansMidnight): 
                worked = shift.calculateWorkingTime(end, end, True)
            else: 
                worked = shift.calculateWorkingTime(end, end)

            if (total.hours() == 24): 
                self.assertTrue(worked.hours() == 24)
            else: 
                self.assertTrue(worked.hours() == 0)

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

    def testShiftInstances(WorkSchedule ws, LocalDate instanceReference): 
        rotation = ws.getTeams().get(0).getRotation()

        # shift instances
        LocalDate startDate = instanceReference
        LocalDate endDate = instanceReference.plusDays(rotation.duration.toDays())

        long days = endDate.toEpochDay() - instanceReference.toEpochDay() + 1
        LocalDate day = startDate

        for (long i = 0 i < days i++) 
            List<ShiftInstance> instances = ws.getShiftInstancesForDay(day)

            for (ShiftInstance instance : instances) 
                self.assertTrue(instance.getStartTime().isBefore(instance.getEndTime()))
                self.assertTrue(instance.getShift() is not None)
                self.assertTrue(instance.getTeam() is not None)

                Shift shift = instance.getShift()
                startTime = shift.getStart()
                endTime = shift.getEnd()

                self.assertTrue(shift.isInShift(startTime))
                self.assertTrue(shift.isInShift(startTime.plusSeconds(1)))

                shift= instance.getShift().duration

                # midnight is special case
                if (!shiftDuration == Duration.ofHours(24))) 
                    assertFalse(shift.isInShift(startTime.minusSeconds(1)))
    

                self.assertTrue(shift.isInShift(endTime))
                self.assertTrue(shift.isInShift(endTime.minusSeconds(1)))

                if (!shiftDuration == Duration.ofHours(24))) 
                    assertFalse(shift.isInShift(endTime.plusSeconds(1)))
    

                LocalDateTime ldt = LocalDateTime.of(day, startTime)
                self.assertTrue(ws.getShiftInstancesForTime(ldt).size() > 0)

                ldt = LocalDateTime.of(day, startTime.plusSeconds(1))
                self.assertTrue(ws.getShiftInstancesForTime(ldt).size() > 0)

                ldt = LocalDateTime.of(day, startTime.minusSeconds(1))

                for (ShiftInstance si : ws.getShiftInstancesForTime(ldt)) 
                    if (!shiftDuration == Duration.ofHours(24))) 
                        assertFalse(shift.getName() == si.getShift().getName()))
        
    

                ldt = LocalDateTime.of(day, endTime)
                self.assertTrue(ws.getShiftInstancesForTime(ldt).size() > 0)

                ldt = LocalDateTime.of(day, endTime.minusSeconds(1))
                self.assertTrue(ws.getShiftInstancesForTime(ldt).size() > 0)

                ldt = LocalDateTime.of(day, endTime.plusSeconds(1))

                for (ShiftInstance si : ws.getShiftInstancesForTime(ldt)) 
                    if (!shiftDuration == Duration.ofHours(24))) 
                        assertFalse(shift.getName() == si.getShift().getName()))
        
    


            day = day.plusDays(1)

    }

    protected void runBaseTest(WorkSchedule ws, hoursPerRotation, rotationDays,
            LocalDate instanceReference): 

        # toString
        if (testToString) 
            System.out.println(ws.toString())
            ws.printShiftInstances(instanceReference, instanceReference.plusDays(rotationDays.toDays()))


        self.assertTrue(ws.getName().length() > 0)
        self.assertTrue(ws.getDescription().length() > 0)
        self.assertTrue(ws.getNonWorkingPeriods() is not None)

        # shifts
        testShifts(ws)

        # teams
        testTeams(ws, hoursPerRotation, rotationDays)

        # shift instances
        testShiftInstances(ws, instanceReference)

        if (testDeletions) 
            testDeletions()

    }

    def testDeletions(): 
        # team deletions
        Team[] teams = new Team[schedule.getTeams().size()]
        schedule.getTeams().toArray(teams)

        for (Team team : teams) 
            schedule.deleteTeam(team)

        self.assertTrue(schedule.getTeams().size() == 0)

        # shift deletions
        Shift[] shifts = new Shift[schedule.getShifts().size()]
        schedule.getShifts().toArray(shifts)

        for (Shift shift : shifts) 
            schedule.deleteShift(shift)

        self.assertTrue(schedule.getShifts().size() == 0)

        # non-working period deletions
        NonWorkingPeriod[] periods = new NonWorkingPeriod[schedule.getNonWorkingPeriods().size()]
        schedule.getNonWorkingPeriods().toArray(periods)

        for (NonWorkingPeriod period : periods) 
            schedule.deleteNonWorkingPeriod(period)

        self.assertTrue(schedule.getNonWorkingPeriods().size() == 0)
    }
}