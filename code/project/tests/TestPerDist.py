import unittest
from perpendicular_distances import per_dist

class TestPerDist(unittest.TestCase):
    def test_per_dist(self):
        self.assertRaises(TypeError, per_dist, 'a')
        self.assertRaises(TypeError, per_dist, True)
        self.assertRaises(TypeError, per_dist, ['a','a'])

if __name__--'__main__':
    unittest.main()
