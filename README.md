# 521158S-NLP-project

This repository contains the work done by project group 6 for natural language processing (521158S) course at University of Oulu.

## Project description

In short, we try to analyze hotel reviews with sentiment analyzers and some other tools etc etc. 

## Implementation

We wrote most of the scripts in python which can be found in the scripts directory. The project was split into multiple semi-independent tasks so there's one or multiple scripts for each task. The project additionally contains a GUI and another script (batch this time) to wrap it all together nice and tidy.

### GUI

One of the requirements was to implement a GUI for the project. This was done using Qt 5.14.1 (mingw 7.3.0 x64) on Windows 10. Technically, it should be possible to compile the project for linux and macOS too but that's not tested and there could be issues.

When running the gui it's important to run each step in correct order. Additionally, it's important to ensure that all the required python modules are installed. There are no checks whatsoever to ensure that everything necessary is installed therefore please check below for the required modules. Required Python version is 3.6 or newer (tested with 3.8.3). Python.exe is expected to be in PATH environment variable when using the GUI.

Additionally in one of the steps we're using SentiStrength which requires java to be installed and added to PATH environment variable. We used java 8 when testing the project.

To build the GUI:

mkdir gui_build && cd gui_build
qmake ..\gui
mingw32-make

To run the GUI:

gui.exe -s [path_to_scripts_dir] -d [path_to_data_dir]

where scripts_dir is the directory containing the scripts within the repository and data_dir is the directory containing the data.

### Batch script

We also implemented a batch script to run each step of the project without GUI as a backup plan if there's any trouble running GUI. It's fairly simple and also doubles as a list to show what is done in each step. To run the script all you need to do is to CD to the repository root directory and run run_scripts.bat. Running the script literally in any other directory will fail horribly.

The same requirements as for the GUI apply. Running the script may take up to few minutes so please be patient.

PROTIP: redirect the output to a file. There's going to be lots of it. 

### (Potentially incomplete) list of required Python modules
- textstat
- matplotlib
- empath
- pandas
- nltk
- sklearn
- csv
- sys
- time
- getopt
- numpy
- collections

May save you a couple of minutes to install these all before trying to run the scripts.
