from builtins import staticmethod
from datetime import datetime, date, time, timedelta
from abc import abstractstaticmethod

class ShiftUtils():
    @staticmethod
    def toEpochSecond(instant: datetime) -> int:
        # seconds from Unix epoch
        return round(datetime.timestamp(instant))

    @staticmethod
    def toEpochDay(day: date) -> int:
        instant = datetime.combine(day, time.min)
        # days from Unix epoch
        totalSeconds = datetime.timestamp(instant)
        day = int(totalSeconds/86400)
        return day
    
    @staticmethod
    def formatTimedelta(duration: timedelta):
        days, seconds = duration.days, duration.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return str(days) + "D:" + str(hours) + "H:" + str(minutes) + "M"
    
    @staticmethod
    def toSecondOfDay(dayTime : time) -> int:
        return dayTime.hour * 3600 + dayTime.minute * 60 * dayTime.second
    
    
    