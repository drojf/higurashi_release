import os, shutil, requests
from sys import argv, exit
from colorama import Fore, Style

help = """Usage:
        higurashi_release.py (onikakushi | watanagashi | tatarigoroshi | himatsubushi | meakashi | tsumihoroboshi | minagoroshi | matsuribayashi)
       """

# Enables the chapter name as an argument. Example: Himatsubushi
try:
    chapterName = argv[1]
except:
    exit(help)

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
        os.makedirs(f'temp/{getData}/StreamingAssets')
        os.mkdir(f'temp/{getData}/Managed')
        os.mkdir(f'temp/{getData}/Plugins')
    except:
        pass

    download(f'https://07th-mod.com/higurashi_dlls/{lowerChapterName}/Assembly-CSharp.dll')
    download('https://07th-mod.com/misc/AVProVideo.dll')
    download(f'https://github.com/07th-mod/{lowerChapterName}/archive/master.zip')

    shutil.unpack_archive('master.zip')
    
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
            shutil.move(f'{lowerChapterName}-master/{folder}', f'temp/{getData}/StreamingAssets')
        except:
            print(f'{folder} not found (this is ok)')
    
    try:
        shutil.move(f'{lowerChapterName}-master/tips.json', f'temp/{getData}')
    except:
        print(f'{lowerChapterName}-master/tips.json not found')
    shutil.move('Assembly-CSharp.dll', f'temp/{getData}/Managed')
    shutil.move('AVProVideo.dll', f'temp/{getData}/Plugins')

    # Turns the first letter of the chapter name into uppercase for consistency when uploading a release
    upperChapter = chapterName.capitalize()
    shutil.make_archive(f'{upperChapter}.Voice.and.Graphics.Patch.vX.Y.Z', 'zip', 'temp')

def cleanUp():
    shutil.rmtree(f'{lowerChapterName}-master')
    shutil.rmtree('temp')

if lowerChapterName in chapterList:
    print(f"{Fore.GREEN}Creating folders and downloading necessary files{Style.RESET_ALL}")
    prepareFiles()
    print(f"{Fore.GREEN}Building the patch{Style.RESET_ALL}")
    buildPatch()
    print(f"{Fore.GREEN}Cleaning up the mess{Style.RESET_ALL}")
    cleanUp()
elif lowerChapterName == "-h" or "--help":
    exit(help)
else:
    exit(help)
