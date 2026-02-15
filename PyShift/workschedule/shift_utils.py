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
        return round(instant.timestamp())
    
    ##
    # Get the day from the Epoch for this date
    # @param day Date
    # @return days since Epoch
    #
    @staticmethod
    def toEpochDay(day: date) -> int:
        # Use UTC to avoid timezone issues
        epoch = date(1970, 1, 1)
        return (day - epoch).days
    
    ##
    # Format a timedelta for display
    # @param duration timedelta
    # @return days : hours : minutes : seconds
    #
    @staticmethod
    def formatTimedelta(duration: timedelta) -> str:
        days = duration.days
        total_seconds = duration.seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{days}D:{hours}H:{minutes}M:{seconds}S"
    
    ##
    # Get the second from the day for this time
    # @param dayTime Time of day
    # @return seconds of day
    #
    @staticmethod
    def toSecondOfDay(dayTime: time) -> int:
        return dayTime.hour * 3600 + dayTime.minute * 60 + dayTime.second
    
    ##
    # Get the second from the day for this time and round it
    # @param dayTime Time of day
    # @return rounded seconds of day
    #
    @staticmethod
    def toRoundedSecond(dayTime: time) -> int:
        second = ShiftUtils.toSecondOfDay(dayTime)
        
        # Standard rounding: >= 500000 microseconds rounds up
        if dayTime.microsecond >= 500000:
            second = second + 1
        
        return second
    
    ##
    # Compare two times
    # @param firstTime First time to compare
    # @param secondTime Second time to compare
    # @return -1 if less than, 0 if equal and 1 if greater than
    #
    @staticmethod
    def compare(firstTime: time, secondTime: time) -> int:
        if firstTime < secondTime:
            return -1
        elif firstTime > secondTime:
            return 1
        return 0