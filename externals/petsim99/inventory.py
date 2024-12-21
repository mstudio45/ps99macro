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

Tabs = {
    "Pets": {"Image": "inventory/tabs/pets", "Conf": 0.9},
    "Items": {"Image": "inventory/tabs/items", "Conf": 0.85},
    "Potions": {"Image": "inventory/tabs/potions", "Conf": 0.85},
    "Enchants": {"Image": "inventory/tabs/enchants", "Conf": 0.825}
}

class InventoryBase(Base):
    def OpenTab(self, tabName: str):
        if Tabs[tabName] == None:
            return None

        tab = Tabs[tab]
        tabBtn = None
        while tabBtn:
            PauseCheck()
            Controls.GoToCenter()
            tabBtn = Images.GetPosition(tab["Image"], confidence=tab["Conf"])
            time.sleep(0.25)
            
        Controls.Click(tabBtn)

        return True

UI = InventoryBase("Inventory", "buttons/inventory", "titles/inventory")