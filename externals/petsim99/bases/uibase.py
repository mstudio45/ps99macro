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
from externals.timer import Timer

class Base:
    def __init__(self, name, button, title, buttonConfidence = 0.65, titleConfidence = 0.67, noButtonExit = False):
        self.name = name
        self.button = button
        self.title = title
        self.buttonConfidence = buttonConfidence
        self.titleConfidence = titleConfidence
        self.noButtonExit = noButtonExit

    def IsOpened(self):
        attempt = 0
        title = None

        while Timer(Config.USING_UI_TIMES):
            while attempt < 1 or title == None: # 2 attempts
                title = Images.GetPosition(self.title, self.titleConfidence)
                attempt += 1
                time.sleep(0.5)

        return title is not None

    def Open(self):
        if self.IsOpened() == False:
            CloseCurrentUI()

            Config.log("Opening " + self.name + "...")
            return OpenMenu(self.button, self.title, self.buttonConfidence, self.titleConfidence, self.noButtonExit)
        
        return True

    def Close(self):
        CloseCurrentUI()