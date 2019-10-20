import unittest
from datetime import date
from datetime import datetime

class TestSnippet(unittest.TestCase):
    def testOne(self):
        dt = date.today()
        print(datetime.combine(dt, datetime.min.time()))
        print(datetime.combine(dt, datetime.max.time()))
        
        print("pi is %.2f" % 3.14159)

        
