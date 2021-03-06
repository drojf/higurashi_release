import os
import shutil
import subprocess
import sys
from sys import argv, stdout


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
    call(['curl', '-OJL', url])


class ChapterInfo:
    def __init__(self, name, episodeNumber, uiFileName):
        self.name = name
        self.episodeNumber = episodeNumber
        self.dataFolderName = f'HigurashiEp{episodeNumber:02}_Data'
        self.uiArchiveName = uiFileName


def compileScripts(chapter: ChapterInfo):
    """
    Compiles scripts for the given chapter.

    Expects:
        - to run on a Windows machine
        - Windows, Steam UI files
        - Windows, Steam base assets
    """
    baseArchiveName = f'{chapter.name}_base.7z'

    # - Download and extract the base archive for the selected game, using key
    download(f'https://07th-mod.com/misc/script_building/{baseArchiveName}')
    # Do not replace the below call with sevenZipExtract() as it would expose the 'EXTRACT_KEY'
    subprocess.call(["7z", "x", baseArchiveName, '-y', f"-p{os.environ['EXTRACT_KEY']}"], shell=isWindows())

    print(f"\n\n>> Compiling [{chapter.name}] scripts...")
    baseFolderName = f'{chapter.name}_base'

    # - Download and extract the UI archive for the selected game
    uiArchiveName = chapter.uiArchiveName
    download(f'https://07th-mod.com/rikachama/ui/{uiArchiveName}')
    sevenZipExtract(uiArchiveName, baseFolderName)

    # - Download the DLL for the selected game
    # TODO: when experimental DLL is released, don't use experimental DLL for building
    dllArchiveName = f'experimental-drojf-dll-ep{chapter.episodeNumber}.7z'
    download(f'https://github.com/drojf/higurashi-assembly/releases/latest/download/{dllArchiveName}')
    sevenZipExtract(dllArchiveName, baseFolderName)

    # - Copy the Update folder containing the scripts to be compiled to the base folder, so the game can find it
    shutil.copytree(f'Update', f'{baseFolderName}/{chapter.dataFolderName}/StreamingAssets/Update', dirs_exist_ok=True)

    # - Remove status file if it exists
    statusFilename = "higu_script_compile_status.txt"
    if os.path.exists(statusFilename):
        os.remove(statusFilename)

    # - Run the game with 'quitaftercompile' as argument
    call([f'{baseFolderName}\\HigurashiEp{chapter.episodeNumber:02}.exe', 'quitaftercompile'])

    # - Check compile status file
    if not os.path.exists(statusFilename):
        raise SystemExit("Script Compile Failed: Script compilation status file not found")

    with open(statusFilename, "r") as f:
        status = f.read().strip()
        if status != "Compile OK":
            raise SystemExit(f"Script Compile Failed: Script compilation status indicated status {status}")

    os.remove(statusFilename)

    # - Copy the CompiledScriptsUpdate folder to the expected final build dir
    shutil.copytree(f'{baseFolderName}/{chapter.dataFolderName}/StreamingAssets/CompiledUpdateScripts', f'CompiledUpdateScripts', dirs_exist_ok=True)

    # Clean up
    os.remove(uiArchiveName)
    os.remove(dllArchiveName)
    shutil.rmtree(baseFolderName)

    # Clean up base archive
    os.remove(baseArchiveName)


def main():
    if sys.version_info < (3, 8):
        raise SystemExit(f"""ERROR: This script requires Python >= 3.8 to run (you have {sys.version_info.major}.{sys.version_info.minor})!

This script uses 3.8's 'dirs_exist_ok=True' argument for shutil.copy.""")

    help = """Usage:
            compile_higurashi_scripts.py (onikakushi | watanagashi | tatarigoroshi | himatsubushi | meakashi | tsumihoroboshi | minagoroshi | matsuribayashi)
           """

    # Enables the chapter name as an argument. Example: Himatsubushi
    if len(argv) < 2:
        raise SystemExit(help)

    chapterName = argv[1]

    chapterListA = [
        ChapterInfo("onikakushi",       1, "Onikakushi-UI_5.2.2f1_win.7z"),
        ChapterInfo("watanagashi",      2, "Watanagashi-UI_5.2.2f1_win.7z"),
        ChapterInfo("tatarigoroshi",    3, "Tatarigoroshi-UI_5.4.0f1_win.7z"),
        ChapterInfo("himatsubushi",     4, "Himatsubushi-UI_5.4.1f1_win.7z"),
        ChapterInfo("meakashi",         5, "Meakashi-UI_5.5.3p3_win.7z"),
        ChapterInfo("tsumihoroboshi",   6, "Tsumihoroboshi-UI_5.5.3p3_win.7z"),
        ChapterInfo("minagoroshi",      7, "Minagoroshi-UI_5.6.7f1_win.7z"),
        ChapterInfo("matsuribayashi",   8, "Matsuribayashi-UI_2017.2.5_win.7z")
    ]

    chapterDict = dict((chapter.name, chapter) for chapter in chapterListA)

    if chapterName not in chapterDict:
        raise SystemExit(f"Error: Invalid Chapter [{chapterName}]\n\n{help}")

    chapter = chapterDict[chapterName]

    # Compile every chapter's scripts before building archives
    compileScripts(chapter)


if __name__ == "__main__":
    main()
