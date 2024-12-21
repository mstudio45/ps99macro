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

class RewardsBase(Base):
    def ClaimRewards(self):
        while Timer(Config.REWARDS_TIMES):
            Config.log("Checking gift rewards...")

            if self.Open():
                Config.log("Claiming gift rewards...")
                Discord.SendWebhook(Config.EMBEDS["ClaimingFreeRewards"], ss=True)

                rewards = [
                    Images.GetAllPositions("gifts/redeem_small", confidence=0.8),
                    Images.GetAllPositions("gifts/redeem", confidence=0.8)
                ]

                for rr in rewards:
                    for reward in rr:
                        PauseCheck()
                        Controls.Click(reward)
                        time.sleep(0.1)

                time.sleep(1)
                Config.log("Claimed gift rewards!")
                Discord.SendWebhook(Config.EMBEDS["ClaimedFreeRewards"], ss=True)

    def ClaimGroupRewards(self):
        if Config.CLAIM_GROUP_REWARDS == False:
            return True
        
        while Timer(Config.REWARDS_TIMES):
            while Timer(Config.WALKING_TIMES):
                Teleport.ResetCharacter()

                Discord.SendWebhook(Config.EMBEDS["ToGroupRewards"], ss=True)
                Controls.ClickCenter()
                time.sleep(1)
                Macro.Run("hoverboard:true;key_w:0.2;key_a:1.5;key_s:0.1;key_a:0.425")
                time.sleep(0.5)
                CloseCurrentUI()
                time.sleep(0.1)
                Macro.Run("hoverboard:true;key_w:0.925")
                Discord.SendWebhook(Config.EMBEDS["FinishedToGroupRewards"], ss=True)
                Macro.Run("hoverboard:false")
    
    def ClaimSocialRewards(self):
        if Config.CLAIM_GROUP_REWARDS == False:
            return True
        
        while Timer(Config.REWARDS_TIMES):
            while Timer(Config.WALKING_TIMES):
                Teleport.ResetCharacter()

                Discord.SendWebhook(Config.EMBEDS["ToGroupRewards"], ss=True)
                Controls.ClickCenter()
                time.sleep(1)
                Macro.Run("hoverboard:true;key_w:0.2;key_a:1.5;key_s:0.1;key_a:0.425")
                time.sleep(0.5)
                CloseCurrentUI()
                time.sleep(0.1)
                Macro.Run("hoverboard:true;key_s:0.235")
                Discord.SendWebhook(Config.EMBEDS["FinishedToGroupRewards"], ss=True)
                Macro.Run("hoverboard:false")

UI = RewardsBase("Rewards", "gifts/freegift", "titles/freegift", noButtonExit=True)