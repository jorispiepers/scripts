# Testing out our scripts.
from PythonFunctions import validate_ipv4

import unittest
import shutil
import re
import os

class TestModule(unittest.TestCase):
    def test_basic(self):
       correctIP = "192.168.100.10"
       expected = ( 192, 168, 100, 10 )
       self.assertEqual(validate_ipv4(correctIP), expected)
       correctIP = [ 10, 10, 0, 0 ]
       expected = [ 10, 10, 0, 0 ]
       self.assertEqual(validate_ipv4(correctIP), expected)
       octetError = "1920.168.38.1"
       expected = 4
       self.assertEqual(validate_ipv4(octetError), expected)
       octetError = [ 192, 168, 380, 10 ]
       expected = 1
       self.assertEqual(validate_ipv4(octetError), expected)
       outScope = "0.0.0.0"
       expected = 5
       self.assertEqual(validate_ipv4(outScope), expected)
       outScope = [ 0, 0, 0, 0 ]
       expected = 2
       self.assertEqual(validate_ipv4(outScope), expected)
       outScope = "255.255.255.255"
       expected = 5
       self.assertEqual(validate_ipv4(outScope), expected)
       outScope = [ 255, 255, 255, 255 ]
       expected = 2
       self.assertEqual(validate_ipv4(outScope), expected)

if __name__ == '__main__':
    ret = unittest.main(verbosity=2)

print(ret)
    #regex = r"([\W\w+]+)\\\w+"
    #source = os.getcwd()
    #dest = (re.search(regex, source))[1]
    #source += "\\PythonFunctions.py"
    #dest += "\\PythonFunctions.py"
    #shutil.copy(source, dest)