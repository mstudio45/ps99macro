import sys, os, time
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
from externals.libs import PauseCheck
from externals.timer import Timer

Controls = externals.libs.Controls()
Images = externals.libs.Images()

# Global Functions
def CloseCurrentUI():
    while Timer(Config.USING_UI_TIMES):
        close = Images.GetPosition('buttons/close', 0.7)
        if close != None:
            Controls.Click(close)

        roblox_prompt = Images.GetPosition('roblox/cancel', 0.67)
        if roblox_prompt != None:
            Controls.Click(roblox_prompt)

def ClickSearchBar(handler, clear = True):
    while Timer(Config.USING_UI_TIMES):
        handler()

        search = Images.GetPosition('buttons/search', 0.85)
        while search == None:
            PauseCheck()
            Controls.GoToCorner()
            time.sleep(0.1)
            search = Images.GetPosition('buttons/search', 0.85)
        
        for i in range(0, 2):
            Controls.Click(search)
            time.sleep(0.5)

        if clear:
            Controls.KeyDown("ctrl")
            Controls.PressKey("a")
            Controls.KeyUp("ctrl")
            
            Controls.PressKey("backspace")


def OpenMenu(button, title, buttonConfidence = 0.65, titleConfidence = 0.67, noButtonExit = False):
    while Timer(Config.USING_UI_TIMES):
        button = Images.GetPosition(button, buttonConfidence)
        title = None

        if button == None and noButtonExit:
            return False
        
        while title == None:
            PauseCheck()

            Controls.GoToCorner()
            if button == None:
                button = Images.GetPosition(button, buttonConfidence)
            else:
                Controls.Click(button)
                title = Images.GetPosition(title, titleConfidence)
            
            time.sleep(0.5)

        if button == "buttons/inventory":
            grid_btn = None
            while grid_btn == None:
                grid_btn = Images.GetPosition('inventory/grid_on', grayscale=False, confidence=0.85)
                time.sleep(0.5)
            Controls.Click(grid_btn)
    
    return True
