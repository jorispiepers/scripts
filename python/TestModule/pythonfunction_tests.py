# Testing out our scripts.
from PythonFunctions import validate_ipv4

import unittest
import shutil
import re
import os

class TestModule(unittest.TestCase):
    def test_basic(self):
       testcase1 = "10.10.10.10"
       expected = ( 10, 10, 10, 10 )
       self.assertEqual(validate_ipv4(testcase1), expected)
       testcase2 = [ 10, 10, 10, 10 ]
       expected = [ 10, 10, 10, 10 ]
       self.assertEqual(validate_ipv4(testcase2), expected)
       testcase1 = "1000.0.380.10"
       expected = 4
       self.assertEqual(validate_ipv4(testcase1), expected)
       testcase2 = [ 10, 380, 10, 10 ]
       expected = 1
       self.assertEqual(validate_ipv4(testcase2), expected)
       testcase3 = "0.0.0.0"
       expected = 5
       self.assertEqual(validate_ipv4(testcase3), expected)
       testcase4 = [ 0, 0, 0, 0 ]
       expected = 2
       self.assertEqual(validate_ipv4(testcase4), expected)

if __name__ == '__main__':
    ret = unittest.main(verbosity=2)

print(ret)
    #regex = r"([\W\w+]+)\\\w+"
    #source = os.getcwd()
    #dest = (re.search(regex, source))[1]
    #source += "\\PythonFunctions.py"
    #dest += "\\PythonFunctions.py"
    #shutil.copy(source, dest)