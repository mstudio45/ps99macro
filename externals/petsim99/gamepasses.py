import os, sys, time, pyautogui
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
import externals.petsim99
import externals.petsim99.libs.macro

import externals.libs, externals.petsim99
from externals.libs import PauseCheck
from externals.timer import Timer

Macro = externals.petsim99.libs.macro.Macro()
ConvertUtil = externals.libs.ConvertUtil()
Controls = externals.libs.Controls()
Images = externals.libs.Images()
Discord = externals.libs.Discord()

class GamepassButton():
    def __init__(self, name, imageLocation, xPos, yPos):
        self.name = name
        self.imageLocation = imageLocation
        self.xPos = xPos
        self.yPos = yPos

    def IsLocked(self):
        Controls.GoToCenter()
        locked = Images.GetPosition(self.imageLocation + 'locked', confidence=0.7)
        return locked != None

    def GetButton(self):
        button = Images.GetPosition(self.imageLocation + 'btn', confidence=0.7)
        while button == None:
            PauseCheck()
            button = Images.GetPosition(self.imageLocation + 'btn', confidence=0.7)
            time.sleep(0.1)

        return button

    def GetState(self):
        if self.IsLocked():
            return
        
        button = self.GetButton()
        Controls.Click(button, click=False)
        time.sleep(0.25)

        xCurrent, yCurrent = pyautogui.position()
        newX, newY = xCurrent + self.xPos, yCurrent - self.yPos

        averageColor = ConvertUtil.ScreenPositionToAverageColor(newX, newY, 15, 15)
        color = ConvertUtil.ColorToAverageColorString(averageColor)

        Controls.ClickXY(newX, newY, click=False)
        if color == "red":
            return False
        
        return True

    def Set(self, value=None):
        while Timer(Config.USING_UI_TIMES):
            try:
                if self.IsLocked():
                    return
                
                currentState = self.GetState()
                wantedState = value or not currentState

                if currentState != wantedState:
                    button = self.GetButton()

                    while currentState != wantedState:
                        PauseCheck()
                        Controls.Click(button)
                        Controls.GoToCenter()

                        time.sleep(0.5)
                        currentState = self.GetState()

                    Controls.GoToCenter()
                    Config.log(f"Turned the '{self.name}' gamepass {currentState and "on" or "off"}!")
            except Exception as e:
                Config.log_error(f"Failed to turn on/off the '{self.name}' gamepass: {e}")

AutoFarm = GamepassButton("Auto Farm", "buttons/autofarm/", 32, 28)
AutoTap = GamepassButton("Auto Tap", "buttons/autotap/", 20, 40)
AutoHatch = GamepassButton("Auto Hatch", "buttons/autohatch/", 45, 47)