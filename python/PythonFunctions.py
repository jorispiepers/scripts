# This python script is a collection of useful scripts which I have made and which are useful to me.
# The goal is to add these functions in a python import so that it can be used anywhere!
# To get started run open this url for more information: https://realpython.com/python-import/#pythons-import-path

# 1. First import function

# Checks whether IPv4 address is valid and returns IP address octets
# Input:    STRING or LIST:INT IPv4 address you wish to test
# Output:   Prints whether it is a proper IPv4 address and in case so returns a tuple of these octets.

import re

def validate_ipv4(ipv4):
    if isinstance(ipv4, str):
        regex = r"(\d+)\.(\d+)\.(\d+)\.(\d+)"
        result = re.search(regex, ipv4)
        if result is not None:
            print("The given IPv4 address {}.{}.{}.{} is correct.".format(result[1], result[2], result[3], result[4]))
            return result[1], result[2], result[3], result[4],
        else:
            print("The given IP is not a valid IPv4 address.")
    elif all(isinstance(i, int) for i in ipv4) and len(ipv4) == 4:
        print("The given IPv4 list translates into IPv4 address: {}.{}.{}.{}".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))

# 2. Second import function

# Runs factorial on a specific number through a recursive function
# Input:    INT, INT factorial number you want to test and the starting number 0
# Output:   Prints the step factorial product/ result from the number which was given for testing

def recursive_factorial(n, r):
    p = n - 1
    if n > 1:
        if (r == 0):
            print("Factorial result: {} = {} * {}".format((p * n), p, n))
            r = p * n
        else:
            print("Factorial result: {} = {} * {}".format((p * r), p, r))
            r = p * r
    else:
        return r
    recursive_factorial(p, r)

# 3. Third import function

# Runs factorial on a specific number
# Input:    INT factorial number you want to test
# Output:   Prints the step factorial product/ result from the number which was given for testing

def factorial(f):
    r = 0
    for p in range(f, 1, -1):
        p = f - 1
        if r == 0:
            print("Factorial result: {} = {} * {}".format((p * f), p, f))
            r = p * f
        else:
            print("Factorial result: {} = {} * {}".format((p * r), p, r))
            r = p * r
        f -= 1