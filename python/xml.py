import re
import os

os.system('cls')

with open("example.xml") as file:
    fileopen = file.read()
    for line in fileopen:
        print(line)
    # Open first tag
    tagopen = r""

    # Search for other sub tags

    # Look for closing tag
    tagclose = r""