import os
import re
import shutil
import hashlib
import platform
import subprocess
import xml.etree.ElementTree as ET

# Global vars
datDir = 'dats'
romDir = [ 'roms', 'roms/work', 'roms/complete' ]
toSortDirs = [ 'tosort', 'tosort/packed', 'tosort/extracted', 'tosort/cleanup' ]

# Detect platform
osv = platform.system()

def clearScreen():
    # Clearing the Screen
    if 'Linux' in osv:
        os.system('clear')
    elif 'Windows' in osv:
        os.system('cls')

# Make sure subfolders still exist
def createDir(directory):
    try:
        os.makedirs(directory, mode=0o777, exist_ok=True)
    except:
        print("Couldn't create directory!")    
        exit(100)

def extractZip(fileName, targetDir):
    cmd = ['7z', 'x', fileName, f'-o{targetDir}', '-y' ]
    process = subprocess.run(cmd, capture_output=True)
    return process.returncode

def createSevenZip(archiveName, archivingFileFolder):
    cmd = ['7z', 'a', '-tzip', archiveName, archivingFileFolder ]
    process = subprocess.run(cmd, capture_output=True)
    return process.returncode

def isEmptyFolder(pathToFolder):
    if len(os.listdir(pathToFolder)) == 0:
        return 0
    else:    
        return 1

def isValidPath(pathToFile):
    if os.path.exists(pathToFile) == False:
        return 0
    elif os.path.exists(pathToFile) == True:
        return 1

def calculatehashes(fileName):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(fileName, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
        return md5.hexdigest(), sha1.hexdigest()

def getFileList(folder):
    fileList = []
    for pathToFile, subDir, file in os.walk(folder):
        for fileName in file:
            fileList.append((pathToFile, fileName))
    return fileList

def getSubDir(folder):
    for pathToFile, subDir, file in os.walk(folder):
        return subDir

def extractFiles():
    # Getting general file name attribute
    # for file renaming purposes
    for folder in toSortDirs:
        createDir(folder)

    packedDir = toSortDirs[1]
    extractDir = toSortDirs[2]
    cleanupDir = toSortDirs[3]

    for pathToFile, subDirs, fileToExtract in os.walk(packedDir):
        print('Extracting ZIP files:\n')
        for fileName in fileToExtract:
            zipFile = f'./{pathToFile}/{fileName}'

            # Make sure we are dealing with ZIP files
            if zipFile.endswith('.zip'):
                if isValidPath(zipFile) == 1:
                    print(f'Extracting file: {fileName}')

                    # In case folder does not exist, create our new ROM sub directory
                    regex = r'(.*)\.(.*)'
                    splitExt = re.search(regex, fileName)
                    print(f'{extractDir}/{splitExt[1]}')
                    if isValidPath(f'{extractDir}/{splitExt[1]}') == 0:
                        createDir(f'{extractDir}/{splitExt[1]}')

                    # Check return code to see why the extraction failed
                    destinationFolder = f'{extractDir}/{splitExt[1]}'
                    returnCode = extractZip(zipFile, destinationFolder)
                    if isValidPath(destinationFolder) == 1:
                        print(f'Extraction of file {destinationFolder} succeeded!')
                    else:
                        print(f'Error {returnCode}! Something went wrong with extraction of {zipFile}!\n')

                    toCleanupDir = f'./{cleanupDir}/{fileName}'
                    print('Moving file {} to clean up directory: {}'.format(zipFile, toCleanupDir))
                    os.rename(zipFile, toCleanupDir)

    # Extracting remaining files and cleaning up extraction folder
    for pathToFile, subDirs, fileToExtract in os.walk(extractDir):
        for fileName in fileToExtract:
            archive = f'./{pathToFile}/{fileName}'
            if fileName.endswith('.zip') or fileName.endswith('.7z'):
                print(f'Extracting subfolder {pathToFile}')
                archive = f'./{pathToFile}/{fileName}'
                # TODO test extraction sub folder so all files stay within the rom folder
                regex = r'(.*)\.(.*)'
                splitExt = re.search(regex, fileName)
                destinationFolder = f'{pathToFile}/{splitExt[1]}'
                print('Extracting {} to: {}'.format(archive, destinationFolder))

                if extractZip(archive, destinationFolder) == 0:
                    print('Removing archive file: {}'.format(archive))
                    os.remove(archive)
    
    print('Done!')

def checkROMs():
    workDir = romDir[1]
    completeDir = romDir[2]
    extractDir = toSortDirs[2]
    cleanupDir = toSortDirs[3]

    # Create our folders
    for folder in romDir:
        createDir(folder)
    createDir(datDir)

    # Create rom subfolder according to dats
    datFiles = getFileList(datDir)
    for datPath, datFile in datFiles:
        fullPath = f'{datPath}/{datFile}'
        tree = ET.parse(fullPath)
        root = tree.getroot()
        for romSet in root.findall('.//header/name'):
            # Create subfolders for rom sets in case they do not exist
            romSetSubDir = f'./{workDir}/{romSet.text}'
            testSubDir = f'./{completeDir}/{romSet.text}'
            # In case romset directory exists in complete directory we ignore extraction to these folders
            if isValidPath(testSubDir) == 0:
                if isValidPath(romSetSubDir) == 0:
                    createDir(romSetSubDir)

    # Rearranged for and if nesting so that it limits disk access for each romset
    # Also made sure that certain dats are no longer checked once these sets are
    # moved into complete directory

    # Go through the rom files one by one
    romList = []
    romPaths = getFileList(extractDir)
    for path, fRom in romPaths:
        fPath = f'./{path}/{fRom}'
        if isValidPath(fPath) == 1:
            # Calculate SHA1 and MD5 hash for each file
            hashes = calculatehashes(fPath)    
            romList.append((fPath, path, fRom, hashes[0], hashes[1]))
    
    datList = []
    datFiles = getFileList(datDir)
    for datPath, datFile in datFiles:
        fullPath = f'{datPath}/{datFile}'
        tree = ET.parse(fullPath)
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

    for fPath, path, fRom, fMD5, fSHA1 in romList:
        for dSet, dName, dRom, dMD5, dSHA1 in datList:
            # We got a match!
            if fMD5 == dMD5 and fSHA1 == dSHA1:
                print(f'Comparing {dName}\nDAT MD5 is: {dMD5} ROM MD5 is: {fMD5}\nDAT SHA1 is: {dSHA1} ROM SHA1 is: {fSHA1}\n\n')
                # In case our new file does not yet exist and the current file name
                # does not match our dat filename on record we rename our file!
                #if isValidPath(fullPath) == 1 and isValidPath(renameFile) == 0 and fRom != dRom:
                if fRom != dRom:
                    renameFile = f'./{path}/{dRom}'
                    print(f'File Game Name is: {fRom}')
                    print(f'Dat Game Name is: {dRom}')
                    print(f'Rename ROM file: {fPath} to {renameFile}\n\n')
                    # Change the ROM name to the correct file name
                    os.rename(fPath, renameFile)
                    fPath = renameFile
                
                # In case 7zip archive does not exist and the ROM file does exist, create it
                archiveFullName = f'{workDir}/{dSet}/{dName}.zip'
                if isValidPath(fPath) == 1 and isValidPath(archiveFullName) == 0:
                    if createSevenZip(archiveFullName, fPath) == 0:
                        print(f'Archive {archiveFullName} is created.'.format(archiveFullName))
                        #os.remove(fPath)
                elif isValidPath(fPath) == 1 and isValidPath(archiveFullName == 1):
                    if createSevenZip(archiveFullName, fPath) == 0:
                        print(f'Added file {fPath} to archive {archiveFullName}.')
                        #os.remove(fPath)
        
    folders = []
    for pathToFile, subdirs, files in os.walk(extractDir):
        if os.path.isdir(pathToFile):
            folders.append(pathToFile)

    folders.sort(key=len, reverse=True)
    for folder in folders:
        # directory exists
        if isEmptyFolder(folder) == 0:
            print(f'Removing empty {folder}!')
            os.rmdir(folder)

def countromsindat():
    # DATs lists for comparing both
    # DAT and complete folders
    datDict = {}
    workDir = romDir[1]
    completeDir = romDir[2]

    datCount = []
    romCount = []
    # Population of the names and romset names in our lists
    workDirF = getSubDir(workDir)
    for subDir in workDirF:
        folder = (f'./{workDir}/{subDir}')
        romFiles = getFileList(folder)
        if len(romFiles) > 0:
            romCount.append((subDir, len(romFiles)))

        datFiles = getFileList(datDir)
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
    

    """for root, subdirs, datfiles in os.walk(datDir):
        for dat in datfiles:
            tree = ET.parse(f"./{datDir}/{dat}")
            root = tree.getroot()
            for romset in root.findall('.//header/name'):
                for game in root.iter('game'):
                    for key, value in game.items():
                        if 'name' in key:
                            datDict[value] = romset.text

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
            print(f'Missing ROM file {dName} from {dSet}')"""
    
# We clear the screen
clearScreen()

# Here we extract the files from the packed folder
# and move the folder to cleanup folder
extractFiles()

# The meat of the script, which will check whether
# the files match MD5 and SHA1 hash from the
# imported DATs
checkROMs()

# Some management of the roms folder, we can
# decide to move the folders we worked on to
# the complete folder
countromsindat()