from builtins import staticmethod
from datetime import datetime

class ShiftUtils():
    @staticmethod
    def toEpochSecond(startDate):
        # seconds from Unix epoch
        delta = startDate - datetime.datetime(1970,1,1)
        totalSeconds = int(delta).total_second
        return totalSeconds

    @staticmethod
    def toEpochDay(startDate):
        totalSeconds = ShiftUtils.toEpochSecond(startDate)
        day = totalSeconds/86400
        remainder = totalSeconds%86400  
        
        if (remainder > 0):
            day = day + 1                 
        
        return day
    