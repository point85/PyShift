from builtins import staticmethod
from datetime import datetime

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
    