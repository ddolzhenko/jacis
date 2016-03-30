import unittest

class StubTestCase(unittest.TestCase):
    
    def setUp(self):
        self.x = 42

    def test_x_eq_42(self):
        self.assertEqual(self.x, 42, 'incorrect default size')

    def test_x_eq_52(self):
        self.assertEqual(self.x, 52, 'Not 52')
