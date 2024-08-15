import os
import re
import zlib
#import py7zr
import shutil
import zipfile
import hashlib
import platform
import xml.etree.ElementTree as ET

# Global vars
romDir = 'roms'
datDir = 'dats'
tosortDir = 'tosort'
packedDir = 'tosort/packed'
extractDir = 'tosort/unpacked'

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
        os.makedirs(romDir, mode=0o777, exist_ok=True)
        os.makedirs(datDir, mode=0o777, exist_ok=True)
        os.makedirs(tosortDir, mode=0o777, exist_ok=True)
        os.makedirs(packedDir, mode=0o777, exist_ok=True)
        os.makedirs(extractDir, mode=0o777, exist_ok=True)
    except:
        print("Couldn't create directories!")    
        exit(100)

def unpack_files():
    # Extracting packed files
    for pathtoFile, subDirs, packedFile in os.walk(packedDir):
        for name in packedFile:
            if name.endswith('.zip'):
                try:
                    fileName = f'./{pathtoFile}/{name}'
                    #with zipfile.ZipFile(fileName, 'r') as z:
                    print("Extracting {} into {}".format(fileName, extractDir))
                        #z.extractall(extractDir)
                    regex = r'(.*)\/(.*)\/(.*)'
                    splitff = re.search(regex, fileName)
                    print("Move execution {} to {}".format(fileName, splitff[1]))
                    #os.rename(fileName, splitff[1])
                except Exception:
                    pass
    # Extracting remaining files and cleaning up extraction folder
    for pathtoFile, subDirs, packedFile in os.walk(extractDir):
        for name in packedFile:
            if name.endswith('.zip'):
                fileName = f'./{pathtoFile}/{name}'
                try:
                    #with zipfile.ZipFile(fileName, 'r') as z:
                    print("Extracting {}".format(fileName))
                    #z.extractall(extractDir)
                    #print("Successfully extracted {} file.".format(fileName))
                    print("Removing compressed file {}".format(fileName))
                    os.remove(fileName)
                except Exception:
                    pass

#def un7zip(fileName, extractDir):
#    with py7zr.SevenZipFile(fileName, mode='r') as z:
#        z.extractall(extractDir)

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

def process_dat_file():
    try:
        for root, subdirs, datfiles in os.walk(datDir):
            # TODO folder zip etc...
            for dat in datfiles:

                tree = ET.parse(f"./{datDir}/{dat}")
                root = tree.getroot()

                # Create subfolders for rom sets in case they do not exist
                for romset in root.findall('.//header/name'):
                    if 'Linux' in osv:                    
                        linux = f"./{romDir}/{romset.text}"
                        os.makedirs(linux, mode=0o777, exist_ok=True)
                    elif 'Windows' in osv:
                        win = f".\{romDir}\{romset.text}"
                        if not os.path.exists(win):
                            os.mkdir(win)

                # Getting general file name attribute
                # for file renaming purposes
                for game in root.iter('game'):
                    for key, value in game.items():
                        if 'name' in key:
                            print("Game name: {}".format(value))
                        if 'id' in key:
                            print("Game id: {}".format(value))

                    # Getting actual file name attribute
                    for rom in game.iter('rom'):
                        for key, value in rom.items():
                            # TODO size comparison
                            if 'size' in key:
                                print("ROM size: {}".format(value))

                            # TODO compare CRC
                            if 'crc' in key:
                                print("ROM CRC: {}".format(value))

                            # TODO compare MD5
                            if 'md5' in key:
                                print("ROM MD5: {}".format(value))

                            # TODO compare SHA1
                            if 'sha1' in key:
                                print("ROM SHA1:{}".format(value))

                            # After file checks are validated rename file
                            # and put it in the appropriate folders
                            if 'name' in key:
                                print("ROM name: {}".format(value))

    except:
        print("Couldn't read dat files ...")
        exit(200)

make_dirs()
unpack_files()
process_dat_file()

