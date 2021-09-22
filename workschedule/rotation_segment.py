
##
# This class represents part of an entire rotation. The segment starts with a
# shift and includes a count of the number of days on followed by the number of
# days off.
# 
class RotationSegment():
    def __init__(self, startingShift, daysOn, daysOff, rotation):
        self.startingShift = startingShift
        self.daysOn = daysOn
        self.daysOff = daysOff
        self.rotation = rotation
        self.sequence = 0
        
    ##
    # Compare two rotation segments
    # @param other {@link RotationSegment}
    # @return -1 if starts before other, 0 is same starting times, else 1
    #
    def compareTo(self, other):
        value = 0
        if (self.sequence < other.sequence):
            value = -1
        elif (self.sequence > other.sequence):
            value = 1
        return value