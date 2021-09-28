from datetime import datetime, date, time, timedelta
from PyShift.test.base_test import BaseTest
from PyShift.workschedule.work_schedule import WorkSchedule

class TestSnapSchedule(BaseTest):

    def testLowNight(self):
        description = "Low night demand"
        schedule = WorkSchedule("Low Night Demand Plan", description)

        # 3 shifts
        day = schedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=8))
        swing = schedule.createShift("Swing", "Swing shift", time(15, 0, 0), timedelta(hours=8))
        night = schedule.createShift("Night", "Night shift", time(23, 0, 0), timedelta(hours=8))

        # Team rotation
        rotation = workSchedule.createschedule.createRotation("Low night demand", "Low night demand")
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

    def test3TeamFixed24(self):
        description = "Fire departments"
        schedule = WorkSchedule("3 Team Fixed 24 Plan", description)

        # starts at 00:00 for 24 hours
        shift = schedule.createShift("24 Hour", "24 hour shift", time(0, 0, 0), timedelta(hours=24))

        # Team rotation
        rotation = workSchedule.createschedule.createRotation("3 Team Fixed 24 Plan", "3 Team Fixed 24 Plan")
        rotation.addSegment(shift, 1, 1)
        rotation.addSegment(shift, 1, 1)
        rotation.addSegment(shift, 1, 4)

        # 3 teams
        schedule.createTeam("Team1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team2", "Second team", rotation, self.referenceDate - timedelta(days=3))
        schedule.createTeam("Team3", "Third team", rotation, self.referenceDate - timedelta(days=6))

        self.runBaseTest(schedule, timedelta(hours=72), timedelta(hours=9), self.referenceDate)

    def test549(self):
        description = "Compressed work workSchedule."
        schedule = WorkSchedule("5/4/9 Plan", description)

        # 1 starts at 07:00 for 9 hours
        day1 = schedule.createShift("Day1", "Day shift #1", time(7, 0, 0), timedelta(hours=9))

        # 2 starts at 07:00 for 8 hours
        day2 = schedule.createShift("Day2", "Day shift #2", time(7, 0, 0), timedelta(hours=8))

        # Team rotation (28 days)
        rotation = workSchedule.createschedule.createRotation("5/4/9 ", "5/4/9 ")
        rotation.addSegment(day1, 4, 0)
        rotation.addSegment(day2, 1, 3)
        rotation.addSegment(day1, 4, 3)
        rotation.addSegment(day1, 4, 2)
        rotation.addSegment(day1, 4, 0)
        rotation.addSegment(day2, 1, 2)

        # 2 teams
        schedule.createTeam("Team1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team2", "Second team", rotation, self.referenceDate - timedelta(days=14))

        self.runBaseTest(schedule, timedelta(hours=160), timedelta(days=28), self.referenceDate)

    def test9to5(self):
        description = "This is the basic 9 to 5 workSchedule plan for office employees. Every employee works 8 hrs a day from Monday to Friday."
        schedule = WorkSchedule("9 To 5 Plan", description)

        # starts at 09:00 for 8 hours
        day = schedule.createShift("Day", "Day shift", time(9, 0, 0), timedelta(hours=8))

        # Team1 rotation (5 days)
        rotation = workSchedule.createschedule.createRotation("9 To 5 ", "9 To 5 ")
        rotation.addSegment(day, 5, 2)

        # 1 team, 1 shift
        schedule.createTeam("Team", "One team", rotation, self.referenceDate)

        self.runBaseTest(schedule, timedelta(hours=40), timedelta(days=7), self.referenceDate)

    def test8Plus12(self):
        description = "This is a fast rotation plan that uses 4 teams and a combination of three 8-hr shifts on weekdays and two 12-hr shifts on weekends to provide 24/7 coverage."
        schedule = WorkSchedule("8 Plus 12 Plan", description)

        # Day shift #1, starts at 07:00 for 12 hours
        day1 = schedule.createShift("Day1", "Day shift #1", time(7, 0, 0), timedelta(hours=12))

        # Day shift #2, starts at 07:00 for 8 hours
        day2 = schedule.createShift("Day2", "Day shift #2", time(7, 0, 0), timedelta(hours=8))

        # Swing shift, starts at 15:00 for 8 hours
        swing = schedule.createShift("Swing", "Swing shift", time(15, 0, 0), timedelta(hours=8))

        # Night shift #1, starts at 19:00 for 12 hours
        night1 = schedule.createShift("Night1", "Night shift #1", time(19, 0, 0), timedelta(hours=12))

        # Night shift #2, starts at 23:00 for 8 hours
        night2 = schedule.createShift("Night2", "Night shift #2", time(23, 0, 0), timedelta(hours=8))

        # shift rotation (28 days)
        rotation = workSchedule.createschedule.createRotation("8 Plus 12", "8 Plus 12")
        rotation.addSegment(day2, 5, 0)
        rotation.addSegment(day1, 2, 3)
        rotation.addSegment(night2, 2, 0)
        rotation.addSegment(night1, 2, 0)
        rotation.addSegment(night2, 3, 4)
        rotation.addSegment(swing, 5, 2)

        # 4 teams, rotating through 5 shifts
        schedule.createTeam("Team 1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team 2", "Second team", rotation, self.referenceDate - timedelta(days=7))
        schedule.createTeam("Team 3", "Third team", rotation, self.referenceDate - timedelta(days=14))
        schedule.createTeam("Team 4", "Fourth team", rotation, self.referenceDate - timedelta(days=21))

        self.runBaseTest(schedule, timedelta(hours=168), timedelta(days=28), self.referenceDate)

    def testICUInterns(self):
        description = "This plan supports a combination of 14-hr day shift , 15.5-hr cross-cover shift , and a 14-hr night shift for medical interns. "
        description = description + "The day shift and the cross-cover shift have the same start time (7:00AM). "
        description = description + "The night shift starts at around 10:00PM and ends at 12:00PM on the next day."

        schedule = WorkSchedule("ICU Interns Plan", description)

        # Day shift #1, starts at 07:00 for 15.5 hours
        crossover = schedule.createShift("Crossover", "Day shift #1 cross-over", time(7, 0, 0),
            timedelta(hours=15) + timedelta(minutes=30))

        # Day shift #2, starts at 07:00 for 14 hours
        day = schedule.createShift("Day", "Day shift #2", time(7, 0, 0), timedelta(hours=14))

        # Night shift, starts at 22:00 for 14 hours
        night = schedule.createShift("Night", "Night shift", time(22, 0, 0), timedelta(hours=14))

        # Team1 rotation
        rotation = workSchedule.createschedule.createRotation("ICU", "ICU")
        rotation.addSegment(day, 1, 0)
        rotation.addSegment(crossover, 1, 0)
        rotation.addSegment(night, 1, 1)

        schedule.createTeam("Team 1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team 2", "Second team", rotation, self.referenceDate.minusDays(3))
        schedule.createTeam("Team 3", "Third team", rotation, self.referenceDate.minusDays(2))
        schedule.createTeam("Team 4", "Forth team", rotation, self.referenceDate.minusDays(1))

        self.runBaseTest(schedule, timedelta(minutes=2610), timedelta(days=4), self.referenceDate)

    def testDupont(self):
        description = "The DuPont 12-hour rotating shift workSchedule uses 4 teams (crews) and 2 twelve-hour shifts to provide 24/7 coverage. "
        description = description + "It consists of a 4-week cycle where each team works 4 consecutive night shifts, "
        description = description + "followed by 3 days off duty, works 3 consecutive day shifts, followed by 1 day off duty, works 3 consecutive night shifts, "
        description = description + "followed by 3 days off duty, work 4 consecutive day shift, then have 7 consecutive days off duty. "
        description = description + "Personnel works an average 42 hours per week."

        schedule = WorkSchedule("DuPont Schedule", description)

        # Day shift, starts at 07:00 for 12 hours
        day = schedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=12))

        # Night shift, starts at 19:00 for 12 hours
        night = schedule.createShift("Night", "Night shift", time(19, 0, 0), timedelta(hours=12))

        # Team1 rotation
        rotation = workSchedule.createschedule.createRotation("DuPont", "DuPont")
        rotation.addSegment(night, 4, 3)
        rotation.addSegment(day, 3, 1)
        rotation.addSegment(night, 3, 3)
        rotation.addSegment(day, 4, 7)

        schedule.createTeam("Team 1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team 2", "Second team", rotation, self.referenceDate - timedelta(days=7))
        schedule.createTeam("Team 3", "Third team", rotation, self.referenceDate - timedelta(days=14))
        schedule.createTeam("Team 4", "Forth team", rotation, self.referenceDate - timedelta(days=21))

        self.runBaseTest(schedule, timedelta(hours=168), timedelta(days=28), self.referenceDate)

    def testDNO(self):
        description = "This is a fast rotation plan that uses 3 teams and two 12-hr shifts to provide 24/7 coverage. "
        description = description + "Each team rotates through the following sequence every three days: 1 day shift, 1 night shift, and 1 day off."

        schedule = WorkSchedule("DNO Plan", description)

        # Day shift, starts at 07:00 for 12 hours
        day = schedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=12))

        # Night shift, starts at 19:00 for 12 hours
        night = schedule.createShift("Night", "Night shift", time(19, 0, 0), timedelta(hours=12))

        # rotation
        rotation = schedule.createRotation("DNO", "DNO")
        rotation.addSegment(day, 1, 0)
        rotation.addSegment(night, 1, 1)

        schedule.createTeam("Team 1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team 2", "Second team", rotation, self.referenceDate - timedelta(days=1))
        schedule.createTeam("Team 3", "Third team", rotation, self.referenceDate - timedelta(days=2))

        # rotation working time
        fromDay = date(self.referenceDate + timedelta(days=rotation.getDayCount()))
        fromDateTime = datetime.combine(fromDay, time(7, 0, 0))
        duration = schedule.calculateWorkingTime(fromDateTime, fromDateTime + timedelta(days=3))
        self.assertTrue(duration == timedelta(hours=72))

        self.runBaseTest(schedule, timedelta(hours=24), timedelta(days=3), self.referenceDate)

    def test21TeamFixed(self):
        description = "".join(["This plan is a fixed (no rotation) plan that uses 21 teams and three 8-hr shifts to provide 24/7 coverage. "
        ,"It maximizes the number of consecutive days off while still averaging 40 hours per week. "
        ,"Over a 7 week cycle, each employee has two 3 consecutive days off and is required to work 6 consecutive days on 5 of the 7 weeks. "
        ,"On any given day, 15 teams will be scheduled to work and 6 teams will be off. "
        ,"Each shift will be staffed by 5 teams so the minimum number of employees per shift is five. "])

        schedule = WorkSchedule("21 Team Fixed 8 6D Plan", description)

        # Day shift, starts at 07:00 for 8 hours
        day = schedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=8))

        # Swing shift, starts at 15:00 for 8 hours
        swing = schedule.createShift("Swing", "Swing shift", time(15, 0, 0), timedelta(hours=8))

        # Night shift, starts at 15:00 for 8 hours
        night = schedule.createShift("Night", "Night shift", time(23, 0, 0), timedelta(hours=8))

        # day rotation
        dayRotation = schedule.createRotation("Day", "Day")
        dayRotation.addSegment(day, 6, 3)
        dayRotation.addSegment(day, 5, 3)
        dayRotation.addSegment(day, 6, 2)
        dayRotation.addSegment(day, 6, 2)
        dayRotation.addSegment(day, 6, 2)
        dayRotation.addSegment(day, 6, 2)

        # swing rotation
        swingRotation = schedule.createRotation("Swing", "Swing")
        swingRotation.addSegment(swing, 6, 3)
        swingRotation.addSegment(swing, 5, 3)
        swingRotation.addSegment(swing, 6, 2)
        swingRotation.addSegment(swing, 6, 2)
        swingRotation.addSegment(swing, 6, 2)
        swingRotation.addSegment(swing, 6, 2)

        # night rotation
        nightRotation = schedule.createRotation("Night", "Night")
        nightRotation.addSegment(night, 6, 3)
        nightRotation.addSegment(night, 5, 3)
        nightRotation.addSegment(night, 6, 2)
        nightRotation.addSegment(night, 6, 2)
        nightRotation.addSegment(night, 6, 2)
        nightRotation.addSegment(night, 6, 2)

        # day teams
        schedule.createTeam("Team 1", "1st day team", dayRotation, self.referenceDate)
        schedule.createTeam("Team 2", "2nd day team", dayRotation, self.referenceDate.plusDays(7))
        schedule.createTeam("Team 3", "3rd day team", dayRotation, self.referenceDate.plusDays(14))
        schedule.createTeam("Team 4", "4th day team", dayRotation, self.referenceDate.plusDays(21))
        schedule.createTeam("Team 5", "5th day team", dayRotation, self.referenceDate.plusDays(28))
        schedule.createTeam("Team 6", "6th day team", dayRotation, self.referenceDate.plusDays(35))
        schedule.createTeam("Team 7", "7th day team", dayRotation, self.referenceDate.plusDays(42))

        # swing teams
        schedule.createTeam("Team 8", "1st swing team", swingRotation, self.referenceDate)
        schedule.createTeam("Team 9", "2nd swing team", swingRotation, self.referenceDate.plusDays(7))
        schedule.createTeam("Team 10", "3rd swing team", swingRotation, self.referenceDate.plusDays(14))
        schedule.createTeam("Team 11", "4th swing team", swingRotation, self.referenceDate.plusDays(21))
        schedule.createTeam("Team 12", "5th swing team", swingRotation, self.referenceDate.plusDays(28))
        schedule.createTeam("Team 13", "6th swing team", swingRotation, self.referenceDate.plusDays(35))
        schedule.createTeam("Team 14", "7th swing team", swingRotation, self.referenceDate.plusDays(42))

        # night teams
        schedule.createTeam("Team 15", "1st night team", nightRotation, self.referenceDate)
        schedule.createTeam("Team 16", "2nd night team", nightRotation, self.referenceDate.plusDays(7))
        schedule.createTeam("Team 17", "3rd night team", nightRotation, self.referenceDate.plusDays(14))
        schedule.createTeam("Team 18", "4th night team", nightRotation, self.referenceDate.plusDays(21))
        schedule.createTeam("Team 19", "5th night team", nightRotation, self.referenceDate.plusDays(28))
        schedule.createTeam("Team 20", "6th night team", nightRotation, self.referenceDate.plusDays(35))
        schedule.createTeam("Team 21", "7th night team", nightRotation, self.referenceDate.plusDays(42))

        self.runBaseTest(schedule, timedelta(hours=280), timedelta(days=49), self.referenceDate.plusDays(49))


    def testTwoTeam(self):
        description = "".join(["This is a fixed (no rotation) plan that uses 2 teams and two 12-hr shifts to provide 24/7 coverage. "
        ,"One team will be permanently on the day shift and the other will be on the night shift."])

        schedule = WorkSchedule("2 Team Fixed 12 Plan", description)

        # Day shift, starts at 07:00 for 12 hours
        day = schedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=12))

        # Night shift, starts at 19:00 for 12 hours
        night = schedule.createShift("Night", "Night shift", time(19, 0, 0), timedelta(hours=12))

        # Team1 rotation
        team1Rotation = schedule.createRotation("Team1", "Team1")
        team1Rotation.addSegment(day, 1, 0)

        # Team1 rotation
        team2Rotation = schedule.createRotation("Team2", "Team2")
        team2Rotation.addSegment(night, 1, 0)

        schedule.createTeam("Team 1", "First team", team1Rotation, self.referenceDate)
        schedule.createTeam("Team 2", "Second team", team2Rotation, self.referenceDate)

        self.runBaseTest(schedule, timedelta(hours=12), timedelta(days=1), self.referenceDate)


    def testPanama(self):
        description = "".join(["This is a slow rotation plan that uses 4 teams and two 12-hr shifts to provide 24/7 coverage. "
        , "The working and non-working days follow this pattern: 2 days on, 2 days off, 3 days on, 2 days off, 2 days on, 3 days off. "
        , "Each team works the same shift (day or night) for 28 days then switches over to the other shift for the next 28 days. "
        , "After 56 days, the same sequence starts over."])

        scheduleName = "Panama"
        schedule = WorkSchedule(scheduleName, description)

        # Day shift, starts at 07:00 for 12 hours
        day = schedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=12))

        # Night shift, starts at 19:00 for 12 hours
        night = schedule.createShift("Night", "Night shift", time(19, 0, 0), timedelta(hours=12))

        # rotation
        rotation = schedule.createRotation("Panama",
                "2 days on, 2 days off, 3 days on, 2 days off, 2 days on, 3 days off")
        # 2 days on, 2 off, 3 on, 2 off, 2 on, 3 off (and repeat)
        rotation.addSegment(day, 2, 2)
        rotation.addSegment(day, 3, 2)
        rotation.addSegment(day, 2, 3)
        rotation.addSegment(day, 2, 2)
        rotation.addSegment(day, 3, 2)
        rotation.addSegment(day, 2, 3)

        # 2 nights on, 2 off, 3 on, 2 off, 2 on, 3 off (and repeat)
        rotation.addSegment(night, 2, 2)
        rotation.addSegment(night, 3, 2)
        rotation.addSegment(night, 2, 3)
        rotation.addSegment(night, 2, 2)
        rotation.addSegment(night, 3, 2)
        rotation.addSegment(night, 2, 3)

        # reference date for start of shift rotations
        self.referenceDate = date(2016, 10, 31)

        schedule.createTeam("Team 1", "First team", rotation, self.referenceDate)
        schedule.createTeam("Team 2", "Second team", rotation, self.referenceDate.minusDays(28))
        schedule.createTeam("Team 3", "Third team", rotation, self.referenceDate - timedelta(days=7))
        schedule.createTeam("Team 4", "Fourth team", rotation, self.referenceDate.minusDays(35))

        self.runBaseTest(schedule, timedelta(hours=336), timedelta(days=56), self.referenceDate)