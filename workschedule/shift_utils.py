from builtins import staticmethod
from datetime import datetime, date, time, timedelta

## Utility methods
#
class ShiftUtils():
    ##
    # Get the second from the Epoch for this datetime
    # @param instant Date and time of day
    # @return seconds since Epoch
    #
    @staticmethod
    def toEpochSecond(instant: datetime) -> int:
        # seconds from Unix epoch
        return round(datetime.timestamp(instant))
    ##
    # Get the day from the Epoch for this date
    # @param day Date
    # @return days since Epoch
    #
    @staticmethod
    def toEpochDay(day: date) -> int:
        instant = datetime.combine(day, time.min)
        # days from Unix epoch
        totalSeconds = datetime.timestamp(instant)
        day = int(totalSeconds/86400)
        return day
    
    ##
    # Format a timedelta for display
    # @param duration timedelta
    # @return days : hours : minutes
    #
    @staticmethod
    def formatTimedelta(duration: timedelta) -> str:
        days, seconds = duration.days, duration.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return str(days) + "D:" + str(hours) + "H:" + str(minutes) + "M"
    
    ##
    # Get the second from the day for this time
    # @param dayTime Time of day
    # @return seconds of day
    #
    @staticmethod
    def toSecondOfDay(dayTime : time) -> int:
        return dayTime.hour * 3600 + dayTime.minute * 60 + dayTime.second
    
    ##
    # Get the second from the day for this time and round it
    # @param dayTime Time of day
    # @return rounded seconds of day
    #
    @staticmethod
    def toRoundedSecond(dayTime: time) -> int:
        second = ShiftUtils.toSecondOfDay(dayTime)

        if (dayTime.microsecond > 500000):
            second = second + 1

        return second
    
    ##
    # Compare two times
    # @param firstTime First time to compare
    # @param secondTime Second time to compare
    # @return -1 if less than, 0 if equal and 1 if greater than
    #
    @staticmethod
    def compare(firstTime:  time, secondTime:  time) -> int:
        value = 0
        
        if (firstTime < secondTime):
            value = -1
        elif (firstTime > secondTime):
            value = 1
        return value

    
    
    