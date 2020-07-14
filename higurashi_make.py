import os, shutil, requests, zipfile
from subprocess import run
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
    "minagoroshi" : "HigurashiEp07_Data",
    "matsuribayashi" : "HigurashiEp08_Data"
    }

# Takes the HigurashiEp_Data folder from the selected chapter and stores it to be used as a path
getData = chapterList.get(lowerChapterName)

def download(url):
    r = requests.get(url, allow_redirects=True)
    filename = url.rsplit('/', 1)[1]
    open(filename, 'wb').write(r.content)

def prepareFiles():
    try:
        os.makedirs(f'{getData}/StreamingAssets')
        os.mkdir(f'{getData}/Managed')
        os.mkdir(f'{getData}/Plugins')
    except:
        pass

    download(f'https://07th-mod.com/higurashi_dlls/{lowerChapterName}/Assembly-CSharp.dll')
    download('https://07th-mod.com/misc/AVProVideo.dll')
    download(f'https://github.com/07th-mod/{lowerChapterName}/archive/master.zip')

    with zipfile.ZipFile("master.zip", "r") as zip:
        zip.extractall()
    
    os.remove('master.zip')

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
            print(f'{folder} not found (this is ok)')
    
    try:
        shutil.move(f'{lowerChapterName}-master/tips.json', getData)
    except:
        print(f'{lowerChapterName}-master/tips.json not found')
    shutil.move('Assembly-CSharp.dll', f'{getData}/Managed')
    shutil.move('AVProVideo.dll', f'{getData}/Plugins')

    # Turns the first letter of the chapter name into uppercase for consistency when uploading a release
    upperChapter = chapterName.capitalize()
    shutil.make_archive(f'{upperChapter}.Voice.and.Graphics.Patch.vX.Y.Z.zip', 'zip', getData)

def cleanUp():
    shutil.rmtree(f'{lowerChapterName}-master')
    shutil.rmtree(getData)

print("Creating folders and downloading necessary files")
prepareFiles()
print("Building the patch")
buildPatch()
print("Cleaning up the mess")
cleanUp()