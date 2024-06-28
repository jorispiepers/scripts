# Testing out our scripts.
from PythonFunctions import validate_ipv4

import unittest
import shutil
import re
import os

class TestModule(unittest.TestCase):
    def test_basic(self):
        # Correct IP string version
        correctIP = "192.168.0.254"
        expected = ( 192, 168, 0, 254 )
        self.assertEqual(validate_ipv4(correctIP), expected)
        # Correct IP list version
        correctIP = [ 192, 168, 0, 254 ]
        expected = [ 192, 168, 0, 254 ]
        self.assertEqual(validate_ipv4(correctIP), expected)
        # Octet error IP string version
        octetError = "1920.168.38.1"
        expected = 6
        self.assertEqual(validate_ipv4(octetError), expected)
        octetError = "192.168.38.-1"
        expected = 9
        self.assertEqual(validate_ipv4(octetError), expected)
        # Octet error IP list version
        octetError = [ 192, 168, 380, 10 ]
        expected = 2
        self.assertEqual(validate_ipv4(octetError), expected)
        octetError = [ 192, 168, 38, -1 ]
        expected = 2
        self.assertEqual(validate_ipv4(octetError), expected)
        reg = "keg"
        octetError = [ 192, 168, 38, reg ]
        expected = 1
        # Invalid IPs string variant
        self.assertEqual(validate_ipv4(octetError), expected)
        outScope = "0.0.0.0"
        expected = 8
        self.assertEqual(validate_ipv4(outScope), expected)       
        outScope = "255.255.255.255"
        expected = 7
        self.assertEqual(validate_ipv4(outScope), expected)
        # Invalid IPs list variant
        outScope = [ 0, 0, 0, 0 ]
        expected = 4
        self.assertEqual(validate_ipv4(outScope), expected)
        outScope = [ 255, 255, 255, 255 ]
        expected = 3
        self.assertEqual(validate_ipv4(outScope), expected)
        days = 3
        expected = 72
        self.assertEqual(days_toHMS(days), expected)        

if __name__ == '__main__':
    ret = unittest.main()
    #regex = r"([\W\w+]+)\\\w+"
    #source = os.getcwd()
    #dest = (re.search(regex, source))[1]
    #source += "\\PythonFunctions.py"
    #dest += "\\PythonFunctions.py"
    #shutil.copy(source, dest)