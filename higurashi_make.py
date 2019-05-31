import os, shutil
from subprocess import call
from sys import argv

# Enables the chapter name as an argument. Example: Himatsubushi
chapterName = argv[1]

# List of supported chapters
chapterList = {
    "onikakushi" : "HigurashiEp01_Data",
    "watanagashi" : "HigurashiEp02_Data",
    "tatarigoroshi" : "HigurashiEp03_Data",
    "himatsubushi" : "HigurashiEp04_Data",
    "meakashi" : "HigurashiEp05_Data",
    "tsumihoroboshi" : "HigurashiEp06_Data"
    }

getData = chapterList.get(chapterName)

def prepareFiles():
    os.makedirs(f'{getData}/StreamingAssets')
    os.mkdir(f'{getData}/Managed')
    os.mkdir(f'{getData}/Plugins')

    call([r'aria2c', '--file-allocation=none', '--continue=true', '--retry-wait=5', '-m 0', '-x 8', '-s 8', f'https://07th-mod.com/higurashi_dlls/{chapterName}/Assembly-CSharp.dll'])
    call([r'aria2c', '--file-allocation=none', '--continue=true', '--retry-wait=5', '-m 0', '-x 8', '-s 8', f'https://07th-mod.com/misc/AVProVideo.dll'])
    call([r'aria2c', '--file-allocation=none', '--continue=true', '--retry-wait=5', '-m 0', '-x 8', '-s 8', f'https://github.com/07th-mod/{chapterName}/archive/master.zip'])
    call([r'7z', 'x', f'{chapterName}-master.zip', '-aoa'])

    os.remove(f'{chapterName}-master.zip')

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

    for folder in folders:
        try:
            shutil.move(f'{chapterName}-master/{folder}', f'{getData}/StreamingAssets')
        except:
            print(f'{folder} not found')
    
    shutil.move(f'{chapterName}-master/tips.json', getData)
    shutil.move('Assembly-CSharp.dll', f'{getData}/Managed')
    shutil.move('AVProVideo.dll', f'{getData}/Plugins')

    upperChapter = chapterName.title()
    call([r'7z', 'a', f'{upperChapter}.Voice.and.Graphics.Patch.vX.Y.Z.zip', getData])

def cleanUp():
    shutil.rmtree(f'{chapterName}-master')
    shutil.rmtree(getData)

prepareFiles()
buildPatch()
cleanUp()