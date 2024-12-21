import os, sys, time
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
from externals.petsim99.libs.ui import *
from externals.petsim99.bases.uibase import Base
from externals.petsim99.teleport import UI as Teleport
import externals.petsim99
import externals.petsim99.libs.macro

import externals.libs
from externals.libs import PauseCheck
from externals.timer import Timer

Macro = externals.petsim99.libs.macro.Macro()
ConvertUtil = externals.libs.ConvertUtil()
Controls = externals.libs.Controls()
Images = externals.libs.Images()
Discord = externals.libs.Discord()

def IsLocked():
    Controls.GoToCenter()
    locked = Images.GetPosition('buttons/hoverboard/locked', confidence=0.7)
    return locked != None

def GetButton():
    button = Images.GetPosition('buttons/hoverboard/btn', confidence=0.7)
    while button == None:
        PauseCheck()
        button = Images.GetPosition('buttons/hoverboard/btn', confidence=0.7)
        time.sleep(0.1)

    return button

def ToggleHoverboard(value: bool = True):
    if IsLocked():
        Config.log_critical("This macro requires the hoverboard, many stuff will not work.")

    button = GetButton()
    while Config.HOVERBOARD != value:
        PauseCheck()

        time.sleep(0.1)
        Controls.Click(button)
        Controls.GoToCenter()
        Config.HOVERBOARD = not Config.HOVERBOARD
    
    Controls.GoToCenter()
    return True
