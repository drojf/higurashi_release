# higurashi_release

This simple script creates Higurashi releases from [07th-Mod](https://github.com/07th-mod/) with close to no human interaction.
It will fetch all the latest files from the game repository and 07th-Mod server to create a zip file that can be extracted directly into the game folder or uploaded as a new release.

It currently supports all released chapters with the exception of Console Arcs.

## Prerequisites

- Python 3.6 or higher with ``requests``
  - ``pip install requests``

## How to use

Run ``py higurashi_make.py <chapterName>``

Example: ``py higurashi_make.py onikakushi``

## TODO

- ~~Test this tool on Linux~~ it works!
- Support console arcs releases
- Mac support
  - unlikely but feel free to fork and diy
- ~~Batch support~~
  - You might want to try ``for %x in (onikakushi watanagashi tatarigoroshi himatsubushi meakashi tsumihoroboshi minagoroshi matsuribayashi) do py higurashi_make.py %x`` in Windows (or the equivalent in Linux)
