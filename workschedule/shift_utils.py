from builtins import staticmethod
from datetime import datetime, timedelta

class ShiftUtils():
    @staticmethod
    def toEpochSecond(instant: datetime) -> int:
        # seconds from Unix epoch
        return round(datetime.timestamp(instant))

    @staticmethod
    def toEpochDay(instant: datetime) -> int:
        # days from Unix epoch
        totalSeconds = datetime.timestamp(instant)
        day = int(totalSeconds/86400)
        remainder = totalSeconds%86400  
            
        if (remainder > 0):
            day = day + 1                 
            
        return day
    
    @staticmethod
    def formatTimedelta(duration: timedelta):
        days, seconds = duration.days, duration.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return str(days) + "D:" + str(hours) + "H:" + str(minutes) + "M"
    
    