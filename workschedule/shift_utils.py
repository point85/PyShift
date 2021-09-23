from builtins import staticmethod
import datetime

class ShiftUtils():
    @staticmethod
    def toEpochSecond(startDate):
        # seconds from Unix epoch
        deltaDays = startDate - datetime.date(1970,1,1)
        totalSeconds = int(deltaDays.total_seconds())
        return totalSeconds

    @staticmethod
    def toEpochDay(startDate):
        totalSeconds = ShiftUtils.toEpochSecond(startDate)
        day = int(totalSeconds/86400)
        remainder = totalSeconds%86400  
        
        if (remainder > 0):
            day = day + 1                 
        
        return day
    