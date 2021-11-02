# PyShift
The PyShift library project manages work schedules.  A work schedule consists of one or more teams who rotate through a sequence of shift and off-shift periods of time.  The PyShift project allows breaks during shifts to be defined as well as non-working periods of time (e.g. holidays and scheduled maintenance periods) that are applicable to the entire work schedule.

## Concepts

The diagram below illustrates Business Management Systems' DNO (Day, Night, Off) work schedule with three teams and two 12-hour shifts with a 3-day rotation.  This schedule is explained in http://community.bmscentral.com/learnss/ZC/3T/c3tr12-1.

![Work Schedule Diagram](https://github.com/point85/shift/blob/master/doc/DNO.png)

*Shift*

A shift is defined with a name, description, starting time of day and duration.  An off-shift period is associated with a shift.  In the example above for Team1, there are two shifts followed by one off-shift period.  Shifts can be overlapped (typically when a handoff of duties is important such as in the nursing profession).  A rotation is a sequence of shifts and off-shift days.  The DNO rotation is Day on, Night on and Night off.  An instance of a shift has a starting date and time of day and has an associated shift definition.

*Team*

A team is defined with a name and description.  It has a rotation with a starting date.  The starting date shift will have an instance with that date and a starting time of day as defined by the shift.  The same rotation can be shared between more than one team, but with different starting times.

*Work Schedule*

A work schedule is defined with a name and description.  It has one or more teams.  Zero or more non-working periods can be defined.  A non-working period has a defined starting date and time of day and duration.  For example, the New Year's Day holiday starting at midnight for 24 hours, or three consecutive days for preventive maintenance of manufacturing equipment starting at the end of the night shift. 

After a work schedule is defined, the working time for all shifts can be computed for a defined time interval.  For example, this duration of time is the maximum available productive time as an input to the calculation of the utilization of equipment in a metric known as the Overall Equipment Effectiveness (OEE).

*Rotation*

A rotation is a sequence of working periods (segments).  Each segment starts with a shift and specifies the number of days on-shift and off-shift.  A work schedule can have more than one rotation.

*Non-Working Period*

A non-working period is a duration of time where no teams are working.  For example, a holiday or a period of time when a plant is shutdown for preventative maintenance.  A non-working period starts at a defined day and time of day and continues for the specified duration of time.

*Shift Instance*

A shift instance is the duration of time from a specified date and time of day and continues for the duration of the associated shift.  A team works this shift instance.

## Examples
The DNO schedule discussed above is defined as follows.

```python
        description = "This is a fast rotation plan that uses 3 teams and two 12-hr shifts to provide 24/7 coverage. "
        description = description + "Each team rotates through the following sequence every three days: 1 day shift, 1 night shift, and 1 day off."

        self.workSchedule = WorkSchedule("DNO Plan", description)

        # Day shift, starts at 07:00 for 12 hours
        day = self.workSchedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=12))

        # Night shift, starts at 19:00 for 12 hours
        night = self.workSchedule.createShift("Night", "Night shift", time(19, 0, 0), timedelta(hours=12))

        # rotation
        rotation = self.workSchedule.createRotation("DNO", "DNO")
        rotation.addSegment(day, 1, 0)
        rotation.addSegment(night, 1, 1)
        referenceDate = date(2021, 11, 1)

        self.workSchedule.createTeam("Team 1", "First team", rotation, referenceDate)
        self.workSchedule.createTeam("Team 2", "Second team", rotation, referenceDate - timedelta(days=1))
        self.workSchedule.createTeam("Team 3", "Third team", rotation, referenceDate - timedelta(days=2))
```
To obtain the working time over three days starting at 07:00, the following methods are called:

```python
        fromDateTime = datetime.combine(date(2021, 11, 2), time(7, 0, 0))
        duration = self.workSchedule.calculateWorkingTime(fromDateTime, fromDateTime + timedelta(days=3))
```

To obtain the shift instances for a date, the following method is called:

```python
shiftInstances = self.workSchedule.getShiftInstancesForDay(date(2021, 11, 2)) 
```

To print a work schedule, call the __str()__ method.  For example:

```python
        print(str(self.workSchedule))
```
with output:

```python		
Schedule: DNO Plan (This is a fast rotation plan that uses 3 teams and two 12-hr shifts to provide 24/7 coverage. Each team rotates through the following sequence every three days: 1 day shift, 1 night shift, and 1 day off.)
Rotation duration: 9D:0H:0M, Scheduled working time: 3D:0H:0M
Shifts: 
   (1) Day (Day shift), Start: 07:00:00 (0D:12H:0M), End: 19:00:00
   (2) Night (Night shift), Start: 19:00:00 (0D:12H:0M), End: 07:00:00
Teams: 
   (1) Team 1 (First team), Rotation start: 2021-11-01, DNO (DNO)
Rotation periods: [Day (on), Night (on), DAY_OFF (off)], Rotation duration: 3D:0H:0M, Days in rotation: 3.0, Scheduled working time: 1D:0H:0M, Percentage worked: 33.333%, Average hours worked per week: : 56.000
   (2) Team 2 (Second team), Rotation start: 2021-10-31, DNO (DNO)
Rotation periods: [Day (on), Night (on), DAY_OFF (off)], Rotation duration: 3D:0H:0M, Days in rotation: 3.0, Scheduled working time: 1D:0H:0M, Percentage worked: 33.333%, Average hours worked per week: : 56.000
   (3) Team 3 (Third team), Rotation start: 2021-10-30, DNO (DNO)
Rotation periods: [Day (on), Night (on), DAY_OFF (off)], Rotation duration: 3D:0H:0M, Days in rotation: 3.0, Scheduled working time: 1D:0H:0M, Percentage worked: 33.333%, Average hours worked per week: : 56.000
Total team coverage: : 100.00%
```

To print shift instances between two dates, the following method is called:

 ```python
self.workSchedule.printShiftInstances(date(2021, 11, 1), date(2021, 11, 3))
```
with output:

```python
Working shifts
[1] Day: 2021-11-01
   (1) Team: Team 1, Shift: Day, Start: 2021-11-01 07:00:00, End: 2021-11-01 19:00:00
   (2) Team: Team 2, Shift: Night, Start: 2021-11-01 19:00:00, End: 2021-11-02 07:00:00
[2] Day: 2021-11-02
   (1) Team: Team 3, Shift: Day, Start: 2021-11-02 07:00:00, End: 2021-11-02 19:00:00
   (2) Team: Team 1, Shift: Night, Start: 2021-11-02 19:00:00, End: 2021-11-03 07:00:00
[3] Day: 2021-11-03
   (1) Team: Team 2, Shift: Day, Start: 2021-11-03 07:00:00, End: 2021-11-03 19:00:00
   (2) Team: Team 3, Shift: Night, Start: 2021-11-03 19:00:00, End: 2021-11-04 07:00:00
```
 
For a second example, the 24/7 schedule below has two rotations for four teams in two shifts.  It is used by manufacturing companies.

```python
        self.workSchedule = WorkSchedule("Manufacturing Company - four twelves",
            "Four 12 hour alternating day/night shifts")

        # day shift, start at 07:00 for 12 hours
        day = self.workSchedule.createShift("Day", "Day shift", time(7, 0, 0), timedelta(hours=12))

        # night shift, start at 19:00 for 12 hours
        night = self.workSchedule.createShift("Night", "Night shift", time(19, 0, 0), timedelta(hours=12))

        # 7 days ON, 7 OFF
        dayRotation = self.workSchedule.createRotation("Day", "Day")
        dayRotation.addSegment(day, 7, 7)

        # 7 nights ON, 7 OFF
        nightRotation = self.workSchedule.createRotation("Night", "Night")
        nightRotation.addSegment(night, 7, 7)

        self.workSchedule.createTeam("A", "A day shift", dayRotation, date(2014, 1, 2))
        self.workSchedule.createTeam("B", "B night shift", nightRotation, date(2014, 1, 2))
        self.workSchedule.createTeam("C", "C day shift", dayRotation, date(2014, 1, 9))
        self.workSchedule.createTeam("D", "D night shift", nightRotation, date(2014, 1, 9))
```

When printed out for a week of shift instances, the output is:

```python
Schedule: Manufacturing Company - four twelves (Four 12 hour alternating day/night shifts)
Rotation duration: 56D:0H:0M, Scheduled working time: 14D:0H:0M
Shifts: 
   (1) Day (Day shift), Start: 07:00:00 (0D:12H:0M), End: 19:00:00
   (2) Night (Night shift), Start: 19:00:00 (0D:12H:0M), End: 07:00:00
Teams: 
   (1) A (A day shift), Rotation start: 2014-01-02, Day (Day)
Rotation periods: [Day (on), Day (on), Day (on), Day (on), Day (on), Day (on), Day (on), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off)], Rotation duration: 14D:0H:0M, Days in rotation: 14.0, Scheduled working time: 3D:12H:0M, Percentage worked: 25.000%, Average hours worked per week: : 42.000
   (2) B (B night shift), Rotation start: 2014-01-02, Night (Night)
Rotation periods: [Night (on), Night (on), Night (on), Night (on), Night (on), Night (on), Night (on), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off)], Rotation duration: 14D:0H:0M, Days in rotation: 14.0, Scheduled working time: 3D:12H:0M, Percentage worked: 25.000%, Average hours worked per week: : 42.000
   (3) C (C day shift), Rotation start: 2014-01-09, Day (Day)
Rotation periods: [Day (on), Day (on), Day (on), Day (on), Day (on), Day (on), Day (on), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off)], Rotation duration: 14D:0H:0M, Days in rotation: 14.0, Scheduled working time: 3D:12H:0M, Percentage worked: 25.000%, Average hours worked per week: : 42.000
   (4) D (D night shift), Rotation start: 2014-01-09, Night (Night)
Rotation periods: [Night (on), Night (on), Night (on), Night (on), Night (on), Night (on), Night (on), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off)], Rotation duration: 14D:0H:0M, Days in rotation: 14.0, Scheduled working time: 3D:12H:0M, Percentage worked: 25.000%, Average hours worked per week: : 42.000
Total team coverage: : 100.00%
Working shifts
[1] Day: 2021-11-01
   (1) Team: A, Shift: Day, Start: 2021-11-01 07:00:00, End: 2021-11-01 19:00:00
   (2) Team: B, Shift: Night, Start: 2021-11-01 19:00:00, End: 2021-11-02 07:00:00
[2] Day: 2021-11-02
   (1) Team: A, Shift: Day, Start: 2021-11-02 07:00:00, End: 2021-11-02 19:00:00
   (2) Team: B, Shift: Night, Start: 2021-11-02 19:00:00, End: 2021-11-03 07:00:00
[3] Day: 2021-11-03
   (1) Team: A, Shift: Day, Start: 2021-11-03 07:00:00, End: 2021-11-03 19:00:00
   (2) Team: B, Shift: Night, Start: 2021-11-03 19:00:00, End: 2021-11-04 07:00:00
[4] Day: 2021-11-04
   (1) Team: C, Shift: Day, Start: 2021-11-04 07:00:00, End: 2021-11-04 19:00:00
   (2) Team: D, Shift: Night, Start: 2021-11-04 19:00:00, End: 2021-11-05 07:00:00
[5] Day: 2021-11-05
   (1) Team: C, Shift: Day, Start: 2021-11-05 07:00:00, End: 2021-11-05 19:00:00
   (2) Team: D, Shift: Night, Start: 2021-11-05 19:00:00, End: 2021-11-06 07:00:00
[6] Day: 2021-11-06
   (1) Team: C, Shift: Day, Start: 2021-11-06 07:00:00, End: 2021-11-06 19:00:00
   (2) Team: D, Shift: Night, Start: 2021-11-06 19:00:00, End: 2021-11-07 07:00:00
[7] Day: 2021-11-07
   (1) Team: C, Shift: Day, Start: 2021-11-07 07:00:00, End: 2021-11-07 19:00:00
   (2) Team: D, Shift: Night, Start: 2021-11-07 19:00:00, End: 2021-11-08 07:00:00
```

For a third example, the work schedule below with one 24 hour shift over an 18 day rotation for three platoons is used by Kern County, California firefighters.

```python
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
```

When printed out for a week of shift instances, the output is:
```python
Schedule: Kern Co. (Three 24 hour alternating shifts)
Rotation duration: 54D:0H:0M, Scheduled working time: 18D:0H:0M
Shifts: 
   (1) 24 Hour (24 hour shift), Start: 07:00:00 (1D:0H:0M), End: 07:00:00
Teams: 
   (1) Red (A Shift), Rotation start: 2017-01-08, 24 Hour (2 days ON, 2 OFF, 2 ON, 2 OFF, 2 ON, 8 OFF)
Rotation periods: [24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), 24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), 24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off)], Rotation duration: 18D:0H:0M, Days in rotation: 18.0, Scheduled working time: 6D:0H:0M, Percentage worked: 33.333%, Average hours worked per week: : 56.000
   (2) Black (B Shift), Rotation start: 2017-02-01, 24 Hour (2 days ON, 2 OFF, 2 ON, 2 OFF, 2 ON, 8 OFF)
Rotation periods: [24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), 24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), 24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off)], Rotation duration: 18D:0H:0M, Days in rotation: 18.0, Scheduled working time: 6D:0H:0M, Percentage worked: 33.333%, Average hours worked per week: : 56.000
   (3) Green (C Shift), Rotation start: 2017-01-02, 24 Hour (2 days ON, 2 OFF, 2 ON, 2 OFF, 2 ON, 8 OFF)
Rotation periods: [24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), 24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), 24 Hour (on), 24 Hour (on), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off), DAY_OFF (off)], Rotation duration: 18D:0H:0M, Days in rotation: 18.0, Scheduled working time: 6D:0H:0M, Percentage worked: 33.333%, Average hours worked per week: : 56.000
Total team coverage: : 100.00%
Working shifts
[1] Day: 2021-11-01
   (1) Team: Green, Shift: 24 Hour, Start: 2021-11-01 07:00:00, End: 2021-11-02 07:00:00
[2] Day: 2021-11-02
   (1) Team: Green, Shift: 24 Hour, Start: 2021-11-02 07:00:00, End: 2021-11-03 07:00:00
[3] Day: 2021-11-03
   (1) Team: Black, Shift: 24 Hour, Start: 2021-11-03 07:00:00, End: 2021-11-04 07:00:00
[4] Day: 2021-11-04
   (1) Team: Black, Shift: 24 Hour, Start: 2021-11-04 07:00:00, End: 2021-11-05 07:00:00
[5] Day: 2021-11-05
   (1) Team: Green, Shift: 24 Hour, Start: 2021-11-05 07:00:00, End: 2021-11-06 07:00:00
[6] Day: 2021-11-06
   (1) Team: Green, Shift: 24 Hour, Start: 2021-11-06 07:00:00, End: 2021-11-07 07:00:00
[7] Day: 2021-11-07
   (1) Team: Red, Shift: 24 Hour, Start: 2021-11-07 07:00:00, End: 2021-11-08 07:00:00
```

## Project Structure
PyShift was developed in Python 3.9.7.  The unit testswere run with Python unit-test.

PyShift has the following structure:
 * '/' - doc.zip (DOxygen documentation), setup.py, README.md
 * `/workschedule` - Python source files
 * `/workschedule/locales` - .mo and .po text translation files for locales
 * `/test` - unit test Python source files 
 * `/scripts` - Windows shell script to create compiled message translation files


