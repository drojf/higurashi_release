import os, shutil, requests
import subprocess
import sys
from sys import argv, exit, stdout
from colorama import Fore, Style


def isWindows():
    return sys.platform == "win32"


def call(args, **kwargs):
    print("running: {}".format(args))
    retcode = subprocess.call(args, shell=isWindows(), **kwargs)  # use shell on windows
    if retcode != 0:
        raise SystemExit(retcode)


def tryRemoveTree(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except FileNotFoundError:
        pass


def sevenZipMakeArchive(input_path, output_filename):
    tryRemoveTree(output_filename)
    call(["7z", "a", output_filename, input_path])


def sevenZipExtract(input_path, outputDir=None):
    args = ["7z", "x", input_path, '-y']
    if outputDir:
        args.append('-o' + outputDir)

    call(args)


def download(url):
    print(f"Starting download of URL: {url}")
    filename = url.rsplit('/', 1)[1]
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                stdout.flush()
    stdout.write('\n')

def compileScripts(lowerChapterName, dataFolderName, episode_number):
    # TODO: add other chapter's archive names
    chapterNameToUIFilename = {
        "onikakushi": "Onikakushi-UI_5.2.2f1_win.7z",
        "watanagashi": "",
        "tatarigoroshi": "",
        "himatsubushi": "",
        "meakashi": "",
        "tsumihoroboshi": "",
        "minagoroshi": "",
        "matsuribayashi": ""
    }

    archive_name = f'{lowerChapterName}_base.7z'
    base_folder_name = f'{lowerChapterName}_base'

    # - Download and extract the base archive for the selected game, using key
    download(f'https://07th-mod.com/misc/script_building/{archive_name}')
    # Do not replace the below call with sevenZipExtract as it would expose the 'EXTRACT_KEY'
    subprocess.call(["7z", "x", archive_name, '-y', f"-p{os.environ['EXTRACT_KEY']}"], shell=isWindows())
    os.remove(archive_name)

    # - Download and extract the UI archive for the selected game
    uiFilename = chapterNameToUIFilename[lowerChapterName]
    download(f'https://07th-mod.com/rikachama/ui/{uiFilename}')
    sevenZipExtract(uiFilename, base_folder_name)
    os.remove(uiFilename)

    # - Download the DLL for the selected game
    # TODO: when experimental DLL is released, don't use experimental DLL for building
    dllFilename = f'experimental-drojf-dll-ep{episode_number}.7z'
    download(f'https://github.com/drojf/higurashi-assembly/releases/latest/download/{dllFilename}')
    sevenZipExtract(dllFilename, base_folder_name)
    os.remove(dllFilename)

    # Download the scripts for the selected game
    scriptsFilename = 'master.zip'
    download(f'https://github.com/07th-mod/{lowerChapterName}/archive/master.zip')
    sevenZipExtract(scriptsFilename)

    # - Copy the Update folder containing the scripts to be compiled to the base folder, so the game can find it
    scriptsExtractFolder = f'{lowerChapterName}-master'
    shutil.copytree(f'{scriptsExtractFolder}/Update', f'{base_folder_name}/{dataFolderName}/StreamingAssets/Update', dirs_exist_ok=True)
    shutil.rmtree(f'{scriptsExtractFolder}')

    # - Run the game with 'quitaftercompile' as argument
    call([f'{base_folder_name}\\HigurashiEp{episode_number:02}.exe', 'quitaftercompile'])

    # - Copy the CompiledScriptsUpdate folder to the expected final build dir
    shutil.copytree(f'{base_folder_name}/{dataFolderName}/StreamingAssets/CompiledUpdateScripts', f'temp/{dataFolderName}/StreamingAssets/CompiledUpdateScripts', dirs_exist_ok=True)

    # Clean up
    shutil.rmtree(base_folder_name)


def prepareFiles(lowerChapterName, dataFolderName):
    os.makedirs(f'temp/{dataFolderName}/StreamingAssets', exist_ok=True)
    os.makedirs(f'temp/{dataFolderName}/Managed', exist_ok=True)
    os.makedirs(f'temp/{dataFolderName}/Plugins', exist_ok=True)

    download(f'https://07th-mod.com/higurashi_dlls/{lowerChapterName}/Assembly-CSharp.dll')
    print("Downloaded Unity dll")
    download('https://07th-mod.com/misc/AVProVideo.dll')
    print("Downloaded video plugin")
    download(f'https://github.com/07th-mod/{lowerChapterName}/archive/master.zip')
    print(f"Downloaded {lowerChapterName} repository")

    shutil.unpack_archive('master.zip')
    
    os.remove('master.zip')


def buildPatch(lowerChapterName, dataFolderName):
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
            shutil.move(f'{lowerChapterName}-master/{folder}', f'temp/{dataFolderName}/StreamingAssets')
        except:
            print(f'{folder} not found (this is ok)')
    
    try:
        shutil.move(f'{lowerChapterName}-master/tips.json', f'temp/{dataFolderName}')
    except:
        print(f'{lowerChapterName}-master/tips.json not found')
    shutil.move('Assembly-CSharp.dll', f'temp/{dataFolderName}/Managed')
    shutil.move('AVProVideo.dll', f'temp/{dataFolderName}/Plugins')


def makeArchive(chapterName):
    # Turns the first letter of the chapter name into uppercase for consistency when uploading a release
    upperChapter = chapterName.capitalize()
    shutil.make_archive(f'{upperChapter}.Voice.and.Graphics.Patch.vX.Y.Z', 'zip', 'temp')


def cleanUp(lowerChapterName):
    shutil.rmtree(f'{lowerChapterName}-master')
    shutil.rmtree('temp')


def main():
    if sys.version_info < (3, 8):
        raise SystemExit(f"""ERROR: This script requires Python >= 3.8 to run (you have {sys.version_info.major}.{sys.version_info.minor})!

This script uses 3.8's 'dirs_exist_ok=True' argument for shutil.copy.""")

    help = """Usage:
            higurashi_release.py (onikakushi | watanagashi | tatarigoroshi | himatsubushi | meakashi | tsumihoroboshi | minagoroshi | matsuribayashi)
           """

    # Enables the chapter name as an argument. Example: Himatsubushi
    if len(argv) < 2:
        raise SystemExit(help)

    chapterName = argv[1]

    # Makes sure the chapter name is lowercase
    lowerChapterName = chapterName.lower()

    # List of supported chapters
    chapterList = {
        "onikakushi": 1,
        "watanagashi": 2,
        "tatarigoroshi": 3,
        "himatsubushi": 4,
        "meakashi": 5,
        "tsumihoroboshi": 6,
        "minagoroshi": 7,
        "matsuribayashi": 8
    }

    if lowerChapterName in chapterList:
        # Takes the HigurashiEp_Data folder from the selected chapter and stores it to be used as a path
        episodeNumber = chapterList[lowerChapterName]
        dataFolderName = f'HigurashiEp{episodeNumber:02}_Data'

        compileScripts(lowerChapterName, dataFolderName, episodeNumber)

        print(f"{Fore.GREEN}Creating folders and downloading necessary files{Style.RESET_ALL}")
        prepareFiles(lowerChapterName, dataFolderName)

        print(f"{Fore.GREEN}Building the patch{Style.RESET_ALL}")
        buildPatch(lowerChapterName, dataFolderName)

        print(f"{Fore.GREEN}Creating Archive{Style.RESET_ALL}")
        makeArchive(chapterName)

        print(f"{Fore.GREEN}Cleaning up the mess{Style.RESET_ALL}")
        cleanUp(lowerChapterName)
    elif lowerChapterName == "-h" or "--help":
        exit(help)
    else:
        exit(help)


if __name__ == "__main__":
    main()
