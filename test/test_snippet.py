import unittest

from datetime import time
from PyShift.test.base_test import BaseTest

class TestSnippet(BaseTest):    
    def testIt(self):
        dayTime = time.max
        seconds = dayTime.hour * 3600 + dayTime.minute * 60 + dayTime.second
        print(str(seconds))
                  
        
if __name__ == '__main__':
    unittest.main()