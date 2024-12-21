import sys, os, time, pyautogui
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config as Config
import externals.petsim99.main_f as PetSimulator
import externals.codes.controls as Controls
import externals.codes.webhook as Webhooks
import externals.petsim99.hoverboard as Hoverboard

imageLocation = Config.IMGS_LOCATION + "/freegifts/"
def getRewardButtonPos():
    return pyautogui.locateOnScreen(imageLocation + 'freegift.png', confidence=0.7)

def openRewardsMenu():
    PetSimulator.closeUI()
    Config.log("Opening Rewards Menu...")
    btn = getRewardButtonPos()
    Config.log_debug(btn)
    
    if btn != None:
        Controls.clickPos(btn)
        btn_e = None
        while btn_e == None:
            if Config.PAUSED == True:
                while Config.PAUSED:
                    time.sleep(1)

            Controls.moveTozero()
            btn = getRewardButtonPos()
            if btn != None:
                Controls.clickPos(btn)
            time.sleep(0.25)
            btn_e = pyautogui.locateOnScreen(Config.IMGS_LOCATION + '/free_rewards_open.png', confidence=0.67)
        Controls.moveTozero()

def CheckRewardsMenu():
    tpe = pyautogui.locateOnScreen(Config.IMGS_LOCATION + '/free_rewards_open.png', confidence=0.67)
    while tpe == None:
        openRewardsMenu()
        tpe = pyautogui.locateOnScreen(Config.IMGS_LOCATION + '/free_rewards_open.png', confidence=0.67)
        time.sleep(0.25)

def getRewards():
    PetSimulator.closeUI()
    start_time = datetime.datetime.now()
    button = getRewardButtonPos()
    Config.log("Looking for gift rewards...")
    Config.log_debug(button)

    if button != None:
        CheckRewardsMenu()
        time.sleep(0.25)
        Controls.moveToCenter()

        Config.log("Claiming rewards...")
        Webhooks.SendWebhook(Config.EMBEDS["ClaimingFreeRewards"], ss=True)

        rewards_pick = pyautogui.locateAllOnScreen(imageLocation + "redeem.png", confidence=0.8)
        rewards_pick_small = pyautogui.locateAllOnScreen(imageLocation + "redeem_small.png", confidence=0.8)
        for pick in rewards_pick:
            if Config.PAUSED == True:
                while Config.PAUSED:
                    time.sleep(1)
            Controls.clickPos(pick)
            time.sleep(0.1)
        for pick in rewards_pick_small:
            if Config.PAUSED == True:
                while Config.PAUSED:
                    time.sleep(1)
            Controls.clickPos(pick)
            time.sleep(0.1)
        
        time.sleep(1)
        Config.log("Rewards claimed!")
        Webhooks.SendWebhook(Config.EMBEDS["ClaimedFreeRewards"], ss=True)
    PetSimulator.closeUI()
    Config.USING_UI_TIMES.append(datetime.datetime.now() - start_time)

def claimGroupRewards():
    if Config.CLAIM_GROUP_REWARDS == True:
        start_time = datetime.datetime.now()

        PetSimulator.resetChar()
        Webhooks.SendWebhook(Config.EMBEDS["ToGroupRewards"], ss=True)
        Hoverboard.equipHoverboard(v=True)
        time.sleep(1)
        Controls.clickCenter()
        time.sleep(1)
        Controls.hold_key("w", 0.2)
        time.sleep(.2)
        Controls.hold_key("a", 1.5)
        time.sleep(.2)
        Controls.hold_key("s", 0.1)
        time.sleep(.2)
        Controls.hold_key("a", 0.425)
        time.sleep(.2)
        PetSimulator.closeUI()
        time.sleep(.1)
        Controls.hold_key("w", 0.925)
        Webhooks.SendWebhook(Config.EMBEDS["FinishedToGroupRewards"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)

def ClaimVIPRewards():
    if Config.CLAIM_VIP_REWARDS == True:
        start_time = datetime.datetime.now()

        PetSimulator.resetChar()
        Webhooks.SendWebhook(Config.EMBEDS["ToVIPRewards"], ss=True)
        Hoverboard.equipHoverboard(v=True)
        time.sleep(1)
        Controls.clickCenter()
        time.sleep(1)
        Controls.hold_key("w", 0.2)
        time.sleep(.2)
        Controls.hold_key("a", 1.5)
        time.sleep(.2)
        Controls.hold_key("s", 0.1)
        time.sleep(.2)
        Controls.hold_key("a", 0.1)
        time.sleep(.2)
        PetSimulator.closeUI()
        time.sleep(.1)
        Controls.hold_key("w", 0.2)
        time.sleep(.2)
        Controls.hold_key("a", 6)
        Webhooks.SendWebhook(Config.EMBEDS["ClaimedToVIPRewards"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)

def claimSocialRewards():
    if Config.CLAIM_GROUP_REWARDS == True:
        start_time = datetime.datetime.now()

        PetSimulator.resetChar()
        Webhooks.SendWebhook(Config.EMBEDS["ToSocialRewards"], ss=True)
        Hoverboard.equipHoverboard(v=True)
        time.sleep(1)
        Controls.clickCenter()
        time.sleep(1)
        Controls.hold_key("w", 0.2)
        time.sleep(.2)
        Controls.hold_key("a", 1.5)
        time.sleep(.2)
        Controls.hold_key("s", 0.1)
        time.sleep(.2)
        Controls.hold_key("a", 0.425)
        time.sleep(.2)
        PetSimulator.closeUI()
        time.sleep(.1)
        Controls.hold_key("s", 0.235)
        Webhooks.SendWebhook(Config.EMBEDS["FinishedToSocialRewards"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)

def FreeDiamondsZone3(): # 30 min
    if Config.CLAIM_FREE_DIAMONDS == True:
        start_time = datetime.datetime.now()

        Webhooks.SendWebhook(Config.EMBEDS["ToFreeDiamonds"], ss=True)
        #PetSimulator.resetChar()
        PetSimulator.tpToZone(3)
        Hoverboard.equipHoverboard(v=True)
        Controls.clickCenter()
        time.sleep(0.5)
        Controls.hold_key("d", 0.3)
        time.sleep(.1)
        Controls.hold_key("w", 0.775)
        time.sleep(.1)
        Controls.hold_key("d", 0.75)
        Webhooks.SendWebhook(Config.EMBEDS["ClaimedToFreeDiamonds"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)

def FreeDiamondsZone32(): # 3 hod
    if Config.CLAIM_FREE_DIAMONDS == True:
        start_time = datetime.datetime.now()

        Webhooks.SendWebhook(Config.EMBEDS["ToFreeDiamonds"], ss=True)
        #PetSimulator.resetChar()
        PetSimulator.tpToZone(32)
        Hoverboard.equipHoverboard(v=True)
        Controls.clickCenter()
        time.sleep(0.5)
        Controls.hold_key("d", 0.3)
        time.sleep(.1)
        Controls.hold_key("w", 0.4)
        time.sleep(.1)
        Controls.hold_key("d", 0.75)
        Webhooks.SendWebhook(Config.EMBEDS["ClaimedToFreeDiamonds"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)

def FreePotions(): # 30 min
    if Config.CLAIM_FREE_POTIONS == True and Config.MAX_ZONES >= 17:
        start_time = datetime.datetime.now()

        Webhooks.SendWebhook(Config.EMBEDS["ToFreePotions"], ss=True)
        #PetSimulator.resetChar()
        PetSimulator.tpToZone(17)
        time.sleep(1)
        Hoverboard.equipHoverboard(v=True)
        Controls.clickCenter()
        time.sleep(0.5)
        Controls.hold_key("d", 0.5)
        time.sleep(.1)
        Controls.hold_key("s", 0.4)
        time.sleep(.1)
        Controls.hold_key("d", 0.5)
        Webhooks.SendWebhook(Config.EMBEDS["ClaimedToFreePotions"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)

def FreeEnchants(): # 45 min
    if Config.CLAIM_FREE_ENCHANTS == True and Config.MAX_ZONES >= 21:
        start_time = datetime.datetime.now()

        Webhooks.SendWebhook(Config.EMBEDS["ToFreeEnchants"], ss=True)
        #PetSimulator.resetChar()
        PetSimulator.tpToZone(21)
        time.sleep(1)
        Hoverboard.equipHoverboard(v=True)
        Controls.clickCenter()
        time.sleep(0.5)
        Controls.hold_key("w", 0.25)
        time.sleep(.1)
        Controls.hold_key("d", 2)
        time.sleep(.1)
        Controls.hold_key("s", 0.25)
        time.sleep(.1)
        Controls.hold_key("d", 0.75)
        Webhooks.SendWebhook(Config.EMBEDS["ClaimedToFreeEnchants"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)

def FreeItems(): # 45 min
    if Config.CLAIM_FREE_ITEMS == True and Config.MAX_ZONES >= 24:
        start_time = datetime.datetime.now()

        Webhooks.SendWebhook(Config.EMBEDS["ToFreeItems"], ss=True)
        #PetSimulator.resetChar()
        PetSimulator.tpToZone(24)
        time.sleep(1)
        Hoverboard.equipHoverboard(v=True)
        Controls.clickCenter()
        time.sleep(0.5)
        Controls.hold_key("d", 0.3)
        time.sleep(.1)
        Controls.hold_key("w", 0.4)
        time.sleep(.1)
        Controls.hold_key("d", 0.75)
        Webhooks.SendWebhook(Config.EMBEDS["ClaimedToFreeItems"], ss=True)
        Hoverboard.equipHoverboard(v=False)

        Config.WALKING_TIMES.append(datetime.datetime.now() - start_time)