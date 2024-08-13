import zlib
import os, sys
import hashlib
import platform
import xml.etree.ElementTree as ET

# Global vars
romdir = 'roms'
datdir = 'dats'
tosortdir = 'tosort'

# Detect platform
osv = platform.system()

# Clearing the Screen
if 'Linux' in osv:
    os.system('clear')
elif 'Windows' in osv:
    os.system('cls')

# make sure subfolders still exist
def make_dirs():
    try:
        osv = platform.system()
        # We are using linux
        if 'Linux' in osv:
            os.makedirs(tosortdir, mode=0o777, exist_ok=True)
            os.makedirs(romdir, mode=0o777, exist_ok=True)
            os.makedirs(datdir, mode=0o777, exist_ok=True)
        elif 'Windows' in osv:
            if not os.path.exists(romdir):
                os.mkdir(romdir)
            if not os.path.exists(datdir):
                os.mkdir(datdir)
            if not os.path.exists(tosortdir):
                os.mkdir(tosortdir)
    except:
        print("Couldn't create directories!")    
        exit(100)

def crc(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def md5(fileName):
    m = hashlib.md5()
    for eachLine in open(fileName, 'rb'):
        m.update(eachLine)
    return m.hexdigest()

def open_dat_file():
    try:
        for root, subdirs, datfiles in os.walk(datdir):
            # TODO folder zip etc...
            for dat in datfiles:

                tree = ET.parse(f"./{datdir}/{dat}")
                root = tree.getroot()

                # Create subfolders for rom sets in case they do not exist
                for romset in root.findall('.//header/name'):
                    if 'Linux' in osv:                    
                        linux = f"./{romdir}/{romset.text}"
                        os.makedirs(linux, mode=0o777, exist_ok=True)
                    elif 'Windows' in osv:
                        win = f".\{romdir}\{romset.text}"
                        if not os.path.exists(win):
                            os.mkdir(win)

                # Printing name attributes
                for game in root.iter('game'):
                    for key, value in game.items():
                        if 'name' in key:
                            print("Game name: {}".format(value))
                        if 'id' in key:
                            print("Game id: {}".format(value))

                    # Printing rom attributes
                    for rom in game.iter('rom'):
                        for key, value in rom.items():
                            if 'name' in key:
                                print("ROM name: {}".format(value))
                            if 'size' in key:
                                print("ROM size: {}".format(value))
                            if 'crc' in key:
                                print("ROM CRC: {}".format(value))
                            if 'md5' in key:
                                print("ROM MD5: {}".format(value))
                            if 'sha1' in key:
                                print("ROM SHA1:{}".format(value))

    except:
        print("Couldn't read dat files ...")
        exit(200)

make_dirs()
open_dat_file()

