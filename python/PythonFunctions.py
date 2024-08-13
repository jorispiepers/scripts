# This python script is a collection of useful scripts which I have made and which are useful to me.
# The goal is to add these functions in a python import so that it can be used anywhere!
# To get started run open this url for more information: https://realpython.com/python-import/#pythons-import-path

# 1. First import function

# Checks whether IPv4 address is valid and returns IP address octets
# Input:    STRING or LIST:INT IPv4 address you wish to test
# Returns:   Returns an error when the IPv4 address is invalid, and returns a proper IPv4 octet list in case of success.

import re
import sys

def validate_ipv4(ipv4):
    if isinstance(ipv4, str):
        # Fail here because we found a special character
        regex = r"[^.\d]"
        if re.search(regex, ipv4):
            print("The specific IPv4 address contains letters or special characters which are not allowed.")
            return 9
        # Fail here as the IP address cannot be 0.0.0.0 or 255.255.255.255
        if ipv4 == "0.0.0.0":
            print("The IPv4 address 0.0.0.0, is not a valid IPv4 address.")
            return 8
        elif ipv4 == "255.255.255.255":
            print("The IPv4 address 255.255.255.255, is not a valid IPv4 address.")
            return 7
        regex = r"(\d+)\.(\d+)\.(\d+)\.(\d+)"
        result = re.search(regex, ipv4)
        if result is not None:
            ipv4 = [ int(result[octet + 1]) for octet in range(4) ]
            # Make sure that IPv4 octets are not above 255 or under 0 and fail in case they do
            for octet in range(len(ipv4)):
                if ipv4[octet] > 255 or ipv4[octet] <= -1:
                    print("Octet failure in address {}.{}.{}.{}.".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
                    return 6
            # Finally return back the correct IPv4 address list
            print("The given IPv4 address {}.{}.{}.{}, is correct.".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
            return ipv4[0], ipv4[1], ipv4[2], ipv4[3]
        else:
            print("The given IPv4 address {}.{}.{}.{}, is not a valid IPv4 address.".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
            return 5
    elif all(isinstance(i, int) for i in ipv4) and len(ipv4) == 4:
        # Fail here as the IP address cannot be 0.0.0.0 or 255.255.255.255
        if ipv4 == [ 0, 0, 0, 0 ]:
            print("The given IPv4 address {}.{}.{}.{}, is invalid".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
            return 4
        elif ipv4 == [ 255, 255, 255, 255 ]:
            print("The given IPv4 address {}.{}.{}.{}, is invalid".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
            return 3
        # Also make sure the IP octets are between range 0 and 255
        for octet in range(len(ipv4)):
            if ipv4[octet] >= 256 or ipv4[octet] <= -1:
                print("Octet failure in IPv4 address {}.{}.{}.{}.".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
                return 2
        # Finally return back the correct IPv4 address list
        print("The given IPv4 list translates into the IPv4 address {}.{}.{}.{}".format(ipv4[0], ipv4[1], ipv4[2], ipv4[3]))
        return ipv4
    else:
        print("The specific IPv4 address contains letters or special characters which are not allowed.")
        return 1

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

def days_toHMS(days):
    # 1 day = 24 H
    hours = days_toHours(days)
    # 1 Hour = 60 M
    minutes = days_toMinutes(days)
    # 1 Minute = 60 S
    seconds = days_toSeconds(days)
    print("The {} days equal to {} hours.".format(days, hours))
    print("The {} days equal to {} minutes.".format(days, minutes))
    print("The {} days equal to {} seconds.".format(days, seconds))
    return hours, minutes, seconds

def seconds_toHMS(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours * 3600) // 60
    remaining_seconds = seconds - hours * 3600 - minutes * 60
    return hours, minutes, remaining_seconds

def days_toHours(days):
    hours = days * 24
    return hours

def days_toMinutes(days):
    minutes = days * 1440
    return minutes

def days_toSeconds(days):
    seconds = days * 86400
    return seconds