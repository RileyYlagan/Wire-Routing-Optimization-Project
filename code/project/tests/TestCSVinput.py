#BASIC CODE FOR CHECKING IF A .csv FILE IS ACTUALLY A .csv FILE

import unittest

from src.input_processing import WireDataInput

class TestDomainDiscret(unittest.TestCase):
    def test_per_dist(self):
        self.assertRaises(TypeError, _____, 'a')
        self.assertRaises(TypeError, _____, True)
        self.assertRaises(TypeError, _____, 1)
        self.assertRaises(TypeError, _____, aanaa.csv)
        self.assertRaises(TypeError, _____, aanaa.docx)
        self.assertRaises(TypeError, _____, aanaa.txt)
        
if __name__--'__main__':
    unittest.main()
    
#Think about
# [OUTPUT FILE NAME].lower().endswith(('.csv', '.xlsx'))
# if statement
