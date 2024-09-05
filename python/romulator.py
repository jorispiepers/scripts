import re
import os, sys
import xml.etree.ElementTree as ET
sys.path.append('libs')
import corelib

def extractfiles(packedDir, extDir, cleanDir):
    print('Checking if anything needs unpacking.')
    # Getting general file name attribute
    # for file renaming purposes
    for folder in toSortDirs:
        corelib.createdir(folder)

    packedFiles = corelib.getfilel(packedDir)
    if len(packedFiles) > 0:
        print('Extracting archives:\n')
        for folder, file in packedFiles:
            archive = f'./{folder}/{file}'
            # Make sure we are dealing with ZIP files
            if file.endswith('.zip') or file.endswith('.7z'):
                if corelib.validpath(archive) == 1:
                    print(f'Extracting file: {file}')
                    # In case folder does not exist, create our new ROM sub directory
                    regex = r'(.*)\.(.*)'
                    splitExt = re.search(regex, file)
                    print(f'{extDir}/{splitExt[1]}')
                    if corelib.validpath(f'{extDir}/{splitExt[1]}') == 0:
                        corelib.createdir(f'{extDir}/{splitExt[1]}')
                    # Check return code to see why the extraction failed
                    destFolder = f'{extDir}/{splitExt[1]}'
                    returnCode = corelib.extract(archive, destFolder)
                    if corelib.validpath(destFolder) == 1:
                        print(f'Extraction of file {destFolder} succeeded!')
                    else:
                        print(f'Error {returnCode}! Something went wrong with extraction of {archive}!\n')
                    toCleanDir = f'./{cleanDir}/{file}'
                    print(f'Moving file {archive} to clean up directory: {toCleanDir}')
                    os.rename(archive, toCleanDir)
        print('Extraction done!')
    else:
        print(f'Nothing to unpack in directory {packedDir}!')

    # Extracting remaining files and cleaning up extraction folder
    packedFiles = corelib.getfilel(extDir)
    if len(packedFiles) > 0:
        for folder, file in packedFiles:
            archive = f'./{folder}/{file}'
            if file.endswith('.zip') or file.endswith('.7z'):
                print(f'Extracting subfolder {folder}')
                archive = f'./{folder}/{file}'
                regex = r'(.*)\.(.*)'
                splitExt = re.search(regex, file)
                destFolder = f'{folder}/{splitExt[1]}'
                print(f'Extracting {archive} to: {destFolder}')
                if corelib.extract(archive, destFolder) == 0:
                    print(f'Removing archive file: {archive}')
                    os.remove(archive)
        print('Extraction done!\n')
    else:
        print(f'Nothing to unpack in directory {extDir}!')

def checkROMs(workDir, compDir, extDir, datDir):
    # Create our folders
    corelib.createdir(workDir)
    corelib.createdir(compDir)
    corelib.createdir(extDir)
    corelib.createdir(datDir)

    # Add rom subfolders conforming to dat data
    datFiles = corelib.getfilel(datDir)
    if len(datFiles) > 0:
        for datPath, datFile in datFiles:
            fullPath = f'{datPath}/{datFile}'
            if fullPath.endswith('.dat'):
                tree = ET.parse(fullPath)
                root = tree.getroot()
                for romSet in root.findall('.//header/name'):
                    # Create subfolders for rom sets in case they do not exist
                    romSetSubDir = f'{workDir}/{romSet.text}'
                    testSubDir = f'{compDir}/{romSet.text}'
                    # In case romset directory exists in complete directory we ignore extraction to these folders
                    if corelib.validpath(testSubDir) == 1:
                        if corelib.validpath(romSetSubDir) == 1:
                            corelib.createdir(romSetSubDir)
        # Rearranged for and if nesting so that it limits disk access for each romset
        # Also made sure that certain dats are no longer checked once these sets are
        # moved into complete directory
        # Go through the rom files one by one
        romList = []
        romPaths = corelib.getfilel(extDir)
        if len(romPaths) > 0:
            print(f'Yay! We have {len(romPaths)} items, from our dat files to compare against!')
            for folder, fRom in romPaths:
                fPath = f'{folder}/{fRom}'
                if corelib.validpath(fPath) == 1:
                    # Calculate SHA1 and MD5 hash for each file
                    hashes = corelib.calchashes(fPath)
                    romList.append((fPath, folder, fRom, hashes[0], hashes[1]))
            datList = []
            datFiles = corelib.getfilel(datDir)
            if len(datFiles) > 0:
                print(f'This is looking good, there are {len(datFiles)} ROM files worth checking out as well.')
                for datPath, datFile in datFiles:
                    fPath = f'{datPath}/{datFile}'
                    tree = ET.parse(fPath)
                    root = tree.getroot()
                    for romSet in root.findall('.//header/name'):
                        for game in root.iter('game'):
                            for key, value in game.items():
                                if 'name' in key:
                                    dName = value
                            # Getting actual file name attribute
                            for rom in game.iter('rom'):
                                for key, value in rom.items():
                                    if 'name' in key:
                                        dRom = value
                                    elif 'md5' in key:
                                        dMD5 = value
                                    elif 'sha1' in key:
                                        dSHA1 = value
                            datList.append((romSet.text, dName, dRom, dMD5, dSHA1))
                print('Currently checking if there are any known ROM matches against our dat files.\n')
                for fPath, path, fRom, fMD5, fSHA1 in romList:
                    for dSet, dName, dRom, dMD5, dSHA1 in datList:
                        # We got a match!
                        if fMD5 == dMD5 and fSHA1 == dSHA1:
                            print(f'Comparing {dName}\nDAT MD5 is: {dMD5} ROM MD5 is: {fMD5}\nDAT SHA1 is: {dSHA1} ROM SHA1 is: {fSHA1}\n\n')
                            # In case our new file does not yet exist and the current file name
                            # does not match our dat filename on record we rename our file!
                            if fRom != dRom:
                                renFile = f'{path}/{dRom}'
                                print(f'File Game Name is: {fRom}')
                                print(f'Dat Game Name is: {dRom}')
                                print(f'Rename ROM file: {fPath} to {renFile}\n\n')
                                # Change the ROM name to the correct file name
                                os.rename(fPath, renFile)
                                fPath = renFile
                            # In case 7zip archive does not exist and the ROM file does exist, create it
                            archFName = f'{workDir}/{dSet}/{dName}.zip'
                            print(fPath, archFName)
                            if corelib.validfile(fPath) == 0 and corelib.validfile(archFName) == 1:
                                if corelib.compress(archFName, fPath) == 0:
                                    print(f'Archive {archFName} is created.')
                            elif corelib.validfile(fPath) == 0 and corelib.validfile(archFName) == 0:
                                if corelib.compress(archFName, fPath) == 0:
                                    print(f'Added file {fPath} to archive {archFName}.')
                    if corelib.validfile(fPath) == 0:
                        os.remove(fPath)
                # Cleaning up extraction folders, to make sure we
                # are not extracting the same files again and again.
                folders = []
                for pathToFile, subdirs, files in os.walk(extDir):
                    if os.path.isdir(pathToFile):
                        folders.append(pathToFile)
                folders.sort(key=len, reverse=True)
                for folder in folders:
                    # directory exists
                    if corelib.emptyfol(folder) == 0:
                        os.rmdir(folder)
            else:
                print(f'Cannot find any DAT files in this path {datDir}.')
        else:
            print(f'Cannot find any ROM files in this path {extDir}.')
    else:
        print(f'Cannot find any DAT files in this path {datDir}.')

def countromsindat(workDir, completeDir):
    # DATs lists for comparing both
    # DAT and complete folders
    datDict = {}
    romCount = []
    datCount = []
    # Population of the names and romset names in our lists
    print(f'Checking for complete sets in folder {workDir}')
    workDirF = corelib.getsubdir(workDir)
    if len(workDirF) > 0:
        for subDir in workDirF:
            folder = (f'./{workDir}/{subDir}')
            romFiles = corelib.getfilel(folder)
            if len(romFiles) > 0:
                romCount.append((subDir, len(romFiles)))
            datFiles = corelib.getfilel(datDir)
            for path, file in datFiles:
                tree = ET.parse(f"./{path}/{file}")
                root = tree.getroot()
                for romSet in root.findall('.//header/name'):
                    dCount = 0
                    if romSet.text == subDir:
                        for game in root.iter('game'):
                            for key, value in game.items():
                                if 'name' in key:
                                    dCount += 1
                    if dCount > 0:
                        datCount.append((romSet.text, dCount))
    for dRomSet, dCount in datCount:
        for fRomSet, fCount in romCount:
            # Move our directory
            if dRomSet == fRomSet and dCount == fCount:
                source = f'./{workDir}/{dRomSet}'
                destination = f'./{completeDir}/{dRomSet}'
                print(f'{source} -> {destination}.')
                os.rename(source, destination)

    # Checks whether you are missing some ROM's
    print(f'Checking if we are still missing any roms in folder {workDir}')
    for root, subdirs, datfiles in os.walk(datDir):
        for dat in datfiles:
            tree = ET.parse(f"./{datDir}/{dat}")
            root = tree.getroot()
            for romset in root.findall('.//header/name'):
                for game in root.iter('game'):
                    for key, value in game.items():
                        if 'name' in key:
                            datDict[value] = romset.text
    open('missing.txt', 'w').close()
    for dName, dSet in datDict.items():    
        match = 0
        for pathToFile, subDirs, romFileName in os.walk(workDir):
            for fileName in romFileName:
                regex = r'(.*)\/(.*)'
                splitFolder = re.search(regex, pathToFile)
                regex = r'(.*)\.(.*)'
                splitFile = re.search(regex, fileName)
                if dSet == splitFolder[2] and dName == splitFile[1]:
                    match = 1
        if match != 1:
            with open('missing.txt', 'a') as myfile:
                myfile.write(f'Missing ROM file {dName} from {dSet}')

# Global vars
datDir = 'dats'
romDir = [ 'roms', 'roms/work', 'roms/complete' ]
toSortDirs = [ 'tosort', 'tosort/packed', 'tosort/extracted', 'tosort/cleanup' ]

# We clear the screen
corelib.clearscr()

# Clean directory tosort/cleanup?
fileList = corelib.getfilel(toSortDirs[3])
if len(fileList) > 0:
    print('We found that the clean up directory under tosort/cleanup is not empty.')
    cleanDir = corelib.response('Do you want to remove ALL contents of this directory (default is NO) [y/N]? ')
    if cleanDir == 1:
        for folder, file in fileList:
            remove = f'./{folder}/{file}'
            if corelib.validfile(remove) == 0:
                os.remove(remove)

chkszip = corelib.filever('7z')
if chkszip == 0:
    # Here we extract the files from the packed folder
    # and move the folder to cleanup folder
    packedDir = f'./{toSortDirs[1]}'
    cleanDir = f'./{toSortDirs[3]}'
    extDir = f'./{toSortDirs[2]}'

    extractfiles(packedDir, extDir, cleanDir)
    # The meat of the script, which will check whether
    # the files match MD5 and SHA1 hash from the
    # imported DATs
    extDir = f'./{toSortDirs[2]}'
    workDir = f'./{romDir[1]}'
    compDir = f'./{romDir[2]}'
    datDir = f'./{datDir}'

    checkROMs(workDir, compDir, extDir, datDir)
    # Some management of the roms folder, we can
    # decide to move the folders we worked on to
    # the complete folder
    countromsindat(romDir[0], romDir[1])
    print('Exit script, nothing more to do.')
else:
    print('Aborting, 7zip is not installed you can install it by running: "apt/ dnf install p7zip"')