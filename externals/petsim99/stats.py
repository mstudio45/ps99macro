import os, sys, time
import pyautogui

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
OCR = externals.libs.OCR()
Images = externals.libs.Images()
Screenshots = externals.libs.Screenshots()

def GetDiamonds():
    Config.log("Getting diamonds...")

    diamonds = Images.GetPosition("diamonds")
    if diamonds != None:
        x, y = pyautogui.center(diamonds)
        _, filename = Screenshots.ScreenshotRegion((
            int(x + 25), int(y - 30), int(200), int(50)
        ), "dia", False)

        diamonds_text, diamonds_num, success = None, None, False
        while Images.TempFile(filename):
            diamonds_text = OCR.ReadTextFromImage(filename)
            diamonds_num, success = ConvertUtil.ToFloat(diamonds_text)

        if success:
            return diamonds_text, diamonds_num, success
        else:
            time.sleep(0.25)
            return GetDiamonds()
        