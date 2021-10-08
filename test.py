import unittest
from os import listdir
import MyRLike_parse

class TestParser(unittest.TestCase):
    def testValidProgram(self):
        self.assertEqual(MyRLike_parse.main('tests/parser/valid1.txt'), "Valid tokens and sintax")

if __name__ == '__main__':
    unittest.main()