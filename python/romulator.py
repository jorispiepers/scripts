import os
import re
import hashlib
import platform
import subprocess
import xml.etree.ElementTree as ET

# Global vars
romDir = 'roms'
datDir = 'dats'
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

def isValidPath(pathToFile):
    if os.path.exists(pathToFile) == False:
        return 0

    if os.path.exists(pathToFile) == True:
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
    for pathToFile, subDirs, packedFile in os.walk(extractDir):
        for name in packedFile:
            zipFile = f'./{pathToFile}/{name}'
            if name.endswith('.zip'):
                zipFile = f'./{pathToFile}/{name}'
                print('Extracting {} to: {}'.format(zipFile, pathToFile))
                if extractZip(zipFile, pathToFile) == 0:
                    print('Removing zip file: {}'.format(zipFile))
                    os.remove(zipFile)

def checkROMs():
    datMD5 = 0
    datSize = 0
    datSHA1 = 0
    datName = ''
    createDir(datDir)
    createDir(romDir)

    extractDir = toSortDirs[2]
    cleanupDir = toSortDirs[3]

    for root, subdirs, datfiles in os.walk(datDir):
        for dat in datfiles:
            tree = ET.parse(f"./{datDir}/{dat}")
            root = tree.getroot()

            # Create subfolders for rom sets in case they do not exist
            for romset in root.findall('.//header/name'):
                romSubDir = f"./{romDir}/{romset.text}"
                if isValidPath(romSubDir) == 0:
                    createDir(romSubDir)

                for pathToFile, subDirs, extractedFile in os.walk(extractDir):
                    if romset.text in pathToFile: 
                        for game in root.iter('game'):
                            for key, value in game.items():
                                if 'name' in key:
                                    gameName = value

                                    # Getting actual file name attribute
                                    for rom in game.iter('rom'):
                                        for key, value in rom.items():
                                            if 'md5' in key:
                                                datMD5 = value
                                            if 'sha1' in key:
                                                datSHA1 = value
                                            if 'name' in key:
                                                datName = value
                                            if 'size' in key:
                                                datSize = value

                                        for fileName in extractedFile:
                                            romFile = f'./{pathToFile}/{fileName}'

                                            # in case the file SHA1 and and MD5 match with the DAT file, continue
                                            if isValidPath(romFile) == 1:
                                                romSize = os.stat(romFile)
                                                if romSize.st_size == int(datSize):

                                                    # Calculate file SHA1 and MD5 hash
                                                    hashes = calculatehashes(romFile)

                                                    if hashes[0] == datMD5 and hashes[1] == datSHA1:
                                                        newFileName = f'./{pathToFile}/{datName}'
                                                        print('ROM name is {} file name is {}\nDAT MD5 is: {} ROM MD5 is: {}\nDAT SHA1 is: {} ROM SHA1 is: {}\nDAT size is: {} File size is: {}\n'.format(newFileName, romFile, datMD5, hashes[0], datSHA1, hashes[1], datSize, romSize.st_size))

                                                        if fileName != datName:
                                                            print(f'Rename ROM file: {romFile} to {newFileName}\n\n')

                                                            # Change the ROM name to the correct file name
                                                            os.rename(romFile, newFileName)

                                                        # In case 7zip archive does not exist and the ROM file does exist, create it
                                                        archiveName = f'{romSubDir}/{gameName}.zip'
                                                        if isValidPath(newFileName) == 1 and isValidPath(archiveName) == 0:
                                                            if createSevenZip(archiveName, newFileName) == 0:
                                                                print('Archive {} is created.'.format(archiveName))
                                                                #os.remove(newFileName)

                                                        elif isValidPath(newFileName) == 1 and isValidPath(archiveName == 1):
                                                            if createSevenZip(archiveName, newFileName) == 0:
                                                                print('Added file {} to archive {}.'.format(newFileName, archiveName))
                                                                #os.remove(newFileName)

def countromsindat():
    datDict = {}
    romDict = {}

    for root, subdirs, datfiles in os.walk(datDir):
        for dat in datfiles:
            roms = 0
            tree = ET.parse(f"./{datDir}/{dat}")
            root = tree.getroot()
            for romset in root.findall('.//header/name'):
                for game in root.iter('game'):
                    roms += 1
            
            print(f'DATs : {romset.text} has {roms}')
            
    for pathToFile, subDirs, extractedFile in os.walk(romDir):
        for subDir in subDirs:
            fileCount = 0
            listFiles = f'./{romDir}/{subDir}/'
            for path in os.listdir(listFiles):
                if os.path.isfile(os.path.join(listFiles, path)):
                    fileCount += 1

            print(f'Files: {subDir} has {fileCount}')

clearScreen()
extractFiles()
checkROMs()
countromsindat()