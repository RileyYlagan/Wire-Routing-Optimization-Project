#BASIC CODE FOR CHECKING IF A .STL FILE IS ACTUALLY A .STL FILE

import unittest

from ______ import _____

class TestDomainDiscret(unittest.TestCase):
    def test_per_dist(self):
        self.assertRaises(TypeError, _____, 'a')
        self.assertRaises(TypeError, _____, True)
        self.assertRaises(TypeError, _____, 1)
        self.assertRaises(TypeError, _____, aanaa.csv)
        self.assertRaises(TypeError, _____, aanaa.docx)
        self.assertRaises(TypeError, _____, aanaa.xlsx)
        self.assertRaises(TypeError, _____, aanaa.txt)
        
if __name__--'__main__':
    unittest.main()
    
#Think about
# [OUTPUT FILE NAME].lower().endswith('.STL')
# if statement