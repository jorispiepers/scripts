# This python script is a collection of useful scripts which I have made and which are useful to me.
# The goal is to add these functions in a python import so that it can be used anywhere!
# To get started run open this url for more information: https://realpython.com/python-import/#pythons-import-path

# 1. First import function

# Checks whether IPv4 address is valid and returns IP address octets
# Input:    STRING or LIST:INT IPv4 address you wish to test
# Output:   Prints whether it is a proper IPv4 address and in case so returns a tuple of these octets.

import re
import sys

def validate_ipv4(ipv4):
    if isinstance(ipv4, str):
        regex = r"(\d+)\.(\d+)\.(\d+)\.(\d+)"
        result = re.search(regex, ipv4)
        if result is not None:
            print("The given IPv4 address {}.{}.{}.{} is correct.".format(result[1], result[2], result[3], result[4]))
            return result[1], result[2], result[3], result[4]
        else:
            print("The given IP is not a valid IPv4 address.")
            sys.exit(1)
    elif all(isinstance(i, int) for i in ipv4) and len(ipv4) == 4:
        for octet in len(ipv4):
            if ipv4[octet] > 255:
                print("Octet {} fails on verification, this address {} is therefore not a proper IPv4 address.".format(octet, ipv4))
                sys.exit(1)
        print("The given IPv4 list translates into IPv4 address: {}.{}.{}.{}".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
        sys.exit(0)

# 2. Second import function

def bytes_to(newbytes):
    if isinstance(newbytes, int):
        if newbytes >= 1024**5: # Converts to Pebibytes
            print("The amount {} bytes translate into {} PB (Pebibytes)".format(newbytes, newbytes/ 1024**5))
            return newbytes/ 1024**5
        elif newbytes >= 1024**4: # Converts to Tebibytes
            print("The amount {} bytes translate into {} TB (Tebibytes)".format(newbytes, newbytes/ 1024**4))
            return newbytes/ 1024**4
        elif newbytes >= 1024**3: # Converts to Gibibytes
            print("The amount {} bytes translate into {} GB (Gibibytes)".format(newbytes, newbytes/ 1024**3))
            return newbytes/ 1024**3
        elif newbytes >= 1024**2: # Converts to Mebibytes
            print("The amount {} bytes translate into {} MB (Mebibytes)".format(newbytes, newbytes/ 1024**2))
            return newbytes/ 1024**2
        elif newbytes >= 1024**1: # Converts to Kibibytes
            print("The amount {} bytes translate into {} KB (Kibibytes)".format(newbytes, newbytes/ 1024**1))
            return newbytes/ 1024**1
        else:
            print("This will be {} b (bytes)".format(newbytes, newbytes))
            return newbytes

# 3. Third import function

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

# 4. Fourth import function

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
    sys.exit(0)

def seconds_toHMS(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours * 3600) // 60
    remaining_seconds = seconds - hours * 3600 - minutes * 60
    return hours, minutes, remaining_seconds

def hours_tominutes(hours):
    minutes = hours * 60
    return minutes

def hours_toseconds(hours):
    seconds = hours * 3600
    return seconds