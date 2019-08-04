import os, shutil
from subprocess import call
from sys import argv

# Enables the chapter name as an argument. Example: Himatsubushi
chapterName = argv[1]

# Makes sure the chapter name is lowercase
lowerChapterName = chapterName.lower()

# List of supported chapters
chapterList = {
    "onikakushi" : "HigurashiEp01_Data",
    "watanagashi" : "HigurashiEp02_Data",
    "tatarigoroshi" : "HigurashiEp03_Data",
    "himatsubushi" : "HigurashiEp04_Data",
    "meakashi" : "HigurashiEp05_Data",
    "tsumihoroboshi" : "HigurashiEp06_Data",
    "minagoroshi" : "HigurashiEp07_Data"
    }

# Takes the HigurashiEp_Data folder from the selected chapter and stores it to be used as a path
getData = chapterList.get(lowerChapterName)

def prepareFiles():
    os.makedirs(f'{getData}/StreamingAssets')
    os.mkdir(f'{getData}/Managed')
    os.mkdir(f'{getData}/Plugins')

    call([r'aria2c', '--file-allocation=none', '--continue=true', '--retry-wait=5', '-m 0', '-x 8', '-s 8', f'https://07th-mod.com/higurashi_dlls/{lowerChapterName}/Assembly-CSharp.dll'])
    call([r'aria2c', '--file-allocation=none', '--continue=true', '--retry-wait=5', '-m 0', '-x 8', '-s 8', f'https://07th-mod.com/misc/AVProVideo.dll'])
    call([r'aria2c', '--file-allocation=none', '--continue=true', '--retry-wait=5', '-m 0', '-x 8', '-s 8', f'https://github.com/07th-mod/{lowerChapterName}/archive/master.zip'])
    call([r'7z', 'x', f'{lowerChapterName}-master.zip', '-aoa'])

    os.remove(f'{lowerChapterName}-master.zip')

def buildPatch():
    # List of all folders used in releases. Dev and misc files are ignored
    folders = [
        "CG",
        "CGAlt",
        "SE",
        "voice",
        "spectrum",
        "BGM",
        "Update"
    ]

    # Iterates the list of folders above looking for valid folders in the master repo
    for folder in folders:
        try:
            shutil.move(f'{lowerChapterName}-master/{folder}', f'{getData}/StreamingAssets')
        except:
            print(f'{folder} not found')
    
    shutil.move(f'{lowerChapterName}-master/tips.json', getData)
    shutil.move('Assembly-CSharp.dll', f'{getData}/Managed')
    shutil.move('AVProVideo.dll', f'{getData}/Plugins')

    # Turns the first letter of the chapter name into uppercase for consistency when uploading a release
    upperChapter = chapterName.capitalize()
    call([r'7z', 'a', f'{upperChapter}.Voice.and.Graphics.Patch.vX.Y.Z.zip', getData])

def cleanUp():
    shutil.rmtree(f'{lowerChapterName}-master')
    shutil.rmtree(getData)

prepareFiles()
buildPatch()
cleanUp()