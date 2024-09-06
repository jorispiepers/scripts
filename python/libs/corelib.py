import os
import hashlib
import platform
import subprocess
from pathlib import Path

# Detect platform
osv = platform.system()

def clearscr():
    # Clearing the Screen
    if 'Linux' in osv:
        os.system('clear')
    elif 'Windows' in osv:
        os.system('cls')

def emptyfol(pathToF):
    if len(os.listdir(pathToF)) == 0:
        return 0
    else:
        return 1

def validpath(pathToF):
    if Path(pathToF).is_dir() == True:
        return 0
    else:
        return 1

def validfile(pathToF):
    if Path(pathToF).is_file() == True:
        return 0
    else:
        return 1

def response(question):
    choice = input(question).lower()
    if choice == 'yes' or choice == 'y':
        return 1
    else:
        return 0

def calchashes(fileN):
    # BUF_SIZE is totally arbitrary,
    # change for your app!
    BUF_SIZE = 65536
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(fileN, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
        return md5.hexdigest(), sha1.hexdigest()

def getfilel(folder):
    fileL = []
    for pathToF, subDir, file in os.walk(folder):
        for fileN in file:
            fileL.append((pathToF, fileN))
    return fileL

def getsubdir(folder):
    for pathToFile, subDir, file in os.walk(folder):
        return subDir

def remover(path):
    try:
        cmd = [ 'rm', '-rf', str(path) ]
        process = subprocess.run(cmd, capture_output=True)
        return process.returncode
    except:
        pass

def compress(archiveN, archFileF):
    try:
        cmd = [ '7z', 'a', '-tzip', archiveN, archFileF ]
        process = subprocess.run(cmd, capture_output=True)
        return process.returncode
    except:
        pass

def extract(fileN, targetDir):
    try:
        cmd = [ '7z', 'x', fileN, f'-o{targetDir}', '-y' ]
        process = subprocess.run(cmd, capture_output=True)
        return process.returncode
    except:
        pass

# Make sure subfolders still exist
def createdir(directory):
    try:
        os.makedirs(directory, mode=0o777, exist_ok=True)
    except:
        print("Couldn't create directory!" )
        exit(100)

def filever(fileN):
    try:
        cmd = [ 'which', fileN ]
        process = subprocess.run(cmd, capture_output=True)
        if process.returncode == 0:
            return process.returncode
        else:
            return process.returncode
    except:
        return 2