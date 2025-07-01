# CHD/CUE to M3U Playlist Creator

A simple but powerful Python script to automatically scan a directory for multi-disc games (e.g., for PlayStation 1), create `.m3u` playlist files, and rename the individual disc files. This is ideal for use with emulators and front-ends like RetroArch, which use `.m3u` files to handle multi-disc games seamlessly.

## The Problem it Solves

Emulators like RetroArch or DuckStation can automatically switch discs if you provide a `.m3u` playlist file. However, creating these files manually for a large collection is tedious. Furthermore, to keep your game list clean, you often want to "hide" the individual disc files (e.g., `Game (Disc 1).chd`, `Game (Disc 2).chd`) and only show the main playlist entry.

This script automates the entire process.

## Features

*   **Automatic Scanning**: Scans a folder for `.chd` and `.cue` files.
*   **Intelligent Grouping**: Identifies games with multiple discs based on their names (e.g., `(Disc 1)`, `(Disk 2)`, etc.).
*   **M3U Creation**: Generates a `.m3u` file for each multi-disc game found.
*   **File Renaming**: Renames the original disc files (e.g., `My Game (Disc 1).chd` -> `My Game (Disc 1).chd.cd1`) so that they are recognized by the emulator but hidden from the front-end's game list.
*   **Simulation Mode**: Includes a "dry run" mode to see what changes will be made without actually creating or renaming any files.
*   **Flexible Naming**: Works with common variations like `(Disc X)` and `(Disk X)`, ignoring case.

---

## How to Use

1.  **Place the Script**: Put the `chd2m3u.py` script inside your ROMs folder, or any other location.

2.  **Configure the Script**: Open `chd2m3u.py` with a text editor and modify the `CONFIGURATION` section at the top.

    ```python
    # --- CONFIGURATION ---
    # Change this line to the full path of the folder containing your games.
    # The dot "." means the same folder where the script is located.
    cartella_rom = "."

    # Set to True to simulate the operation without modifying files.
    # A "report_simulazione.txt" file will be created with the planned actions.
    # Set to False to actually perform the file creation and renaming.
    simulazione = True
    ```

    *   `cartella_rom`: The path to your games folder.
    *   `simulazione`: **It's highly recommended to run in simulation mode first (`True`)** to check the output report (`report_simulazione.txt`) and ensure everything is correct. Once you are satisfied, change it to `False` to apply the changes.

3.  **Run the Script**: Open a terminal or command prompt, navigate to the script's directory, and run it:
    ```sh
    python chd2m3u.py
    ```

---

## Example

Let's say your game folder looks like this:

**BEFORE:**
```
/PS1_GAMES
├── Final Fantasy VII (Disc 1).chd
├── Final Fantasy VII (Disc 2).chd
├── Final Fantasy VII (Disc 3).chd
├── Metal Gear Solid (Disk 1).chd
├── Metal Gear Solid (Disk 2).chd
└── Crash Bandicoot.chd
```

After running the script (with `simulazione = False`), your folder will look like this:

**AFTER:**
```
/PS1_GAMES
├── Final Fantasy VII (Disc 1).chd.cd1
├── Final Fantasy VII (Disc 2).chd.cd2
├── Final Fantasy VII (Disc 3).chd.cd3
├── Final Fantasy VII.m3u          <-- NEW
├── Metal Gear Solid (Disk 1).chd.cd1
├── Metal Gear Solid (Disk 2).chd.cd2
├── Metal Gear Solid.m3u           <-- NEW
└── Crash Bandicoot.chd            (untouched, as it's a single-disc game)
```

The content of `Final Fantasy VII.m3u` will be:
```
Final Fantasy VII (Disc 1).chd.cd1
Final Fantasy VII (Disc 2).chd.cd2
Final Fantasy VII (Disc 3).chd.cd3
```

Now, your emulator front-end will only show "Final Fantasy VII", and it will handle disc swapping automatically.

