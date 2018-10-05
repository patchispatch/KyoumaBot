import unittest
from botutil import esPalindromo

class PalindromoTest(unittest.TestCase):
    def test_positive(self):
        text = "palinilap"
        self.assertTrue(esPalindromo(text))

    def test_negative(self):
        text = "palin"
        self.assertFalse(esPalindromo(text))
