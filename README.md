# HigurashiRelease

This simple script creates Higurashi releases from [07th-Mod](https://github.com/07th-mod/) with close to 
no human interaction. It will fetch all the latest files from the game repository and 07th-Mod server to 
create a zip file that can be extracted directly into the game folder or uploaded as a new release.

It currently supports all released chapters with the exception of Console Arcs.

## Pre-requisites

> Note: these should be in your system $PATH to work.

- Python 3.5 or newer
- [7-Zip](https://www.7-zip.org/https://www.7-zip.org/)
- [aria2](https://aria2.github.io/)

Use [chocolatey](https://chocolatey.org/) on Windows or the package manager of your choice on Linux/Mac.

## TODO

- Test this tool on Linux
- Support console arcs releases
- Mac support 
    - unlikely but feel free to fork and diy
