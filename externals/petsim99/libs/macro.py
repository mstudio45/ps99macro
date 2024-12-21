import os, sys, time

import externals.petsim99
import externals.petsim99.hoverboard
def GetMainDir(): # this should not fail
    current_dir = os.getcwd()
    while True:
        if all(filename in os.listdir(current_dir) for filename in ["config.py", "ui.py"]):
            break
        current_dir = os.path.dirname(current_dir)
    return current_dir
sys.path.append(GetMainDir())

import config as Config
# Libraries
import externals.libs
Controls = externals.libs.Controls()

"""
Macro Usage:
   Separator = ;
   Format = TYPE:SETTING
   Types:
        hoverboard (true, false) = turn on/off hoverboard
        key_[keycode] (hold time in seconds, press) = holds/presses the inputted keycode
"""

class Macro:
    def __init__(self):
        pass

    def Run(self, macro: str):
        macro = macro.lower()
        tasks = macro.split(";")

        for fullTask in tasks:
            externals.libs.PauseCheck()
            task, setting = fullTask.split(":")

            if task.startswith("key_"):
                task = task.replace("key_", "")
                if setting == "false":
                    Controls.PressKey(task)
                else:
                    Controls.HoldKey(task, float(setting))
            elif task == "hoverboard":
                if setting == "true":
                    externals.petsim99.hoverboard.ToggleHoverboard(True)
                else:
                    externals.petsim99.hoverboard.ToggleHoverboard(False)