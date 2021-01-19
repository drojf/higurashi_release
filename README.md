# higurashi_release

This repository contains scripts used for deploying the 07th-mod Higurashi mods.

## higurashi_release.py

This simple script creates Higurashi releases from [07th-Mod](https://github.com/07th-mod/) with close to no human interaction.
It will fetch all the latest files from the game repository and 07th-Mod server to create a zip file that can be extracted directly into the game folder or uploaded as a new release.

It currently supports all released chapters with the exception of Console Arcs.

## Prerequisites

- Python 3.6 or higher with ``requests``
  - ``pip install requests``

## How to use

```bash
Usage:
        higurashi_release.py (onikakushi | watanagashi | tatarigoroshi | himatsubushi | meakashi | tsumihoroboshi | minagoroshi | matsuribayashi)
```

Example: ``python higurashi_release.py meakashi``

## TODO

- ~~Test this tool on Linux~~ it works!
- Support console arcs releases
- Mac support
  - unlikely but feel free to fork and diy
- ~~Batch support~~
  - You might want to try ``for %x in (onikakushi watanagashi tatarigoroshi himatsubushi meakashi tsumihoroboshi minagoroshi matsuribayashi) do py higurashi_make.py %x`` in Windows (or the equivalent in Linux)

## compile_higurashi_scripts

### compile_higurashi_scripts.py

This script compiles scripts for each game. It is called by the Github Actions script in each higurashi repository which automatically raises a pull request with the compiled scripts, and is not intended to be called directly from the command line. It should be called from the root of a higurashi mod github repo, as it will expect a folder called `Update` containing the scripts to be compiled.

## Prerequisites

The example github workflow file already has the prerequisites setup, but if you are running this manually you will need:

- Python 3.8 or higher
- Curl
- 7zip (script only works with `7z` at the moment, not `7za`)

### pr_workflow_example.yml

This is an example Github Actions workflow which downloads and calls the `compile_higurashi_scripts.py`, then creates a new pull request with the compiled scripts.
