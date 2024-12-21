import os, time, random
import pyautogui, requests
import subprocess
import threading
from win32con import *
from discord_webhook import DiscordWebhook, DiscordEmbed
import datetime

import pyautoit as autoit

# CONFIG #
import config as Config
import externals.libs as lib

import externals.petsim99.hoverboard as Hoverboard
import externals.petsim99.inventory as Inventory
import externals.petsim99.gamepasses as GamepassBtns
import externals.petsim99.rewards as Rewards
import externals.petsim99.stats as Stats
import externals.petsim99.teleport as Teleport
import externals.StatLib.StatLib as StatLib
import ui as UI

Controls = lib.Controls()
Webhook = lib.Discord()
Roblox = lib.Roblox()
WindowsInhibitor = lib.WindowsInhibitor()
StatLibrary = StatLib.StatLib(compact=True, layout=StatLib.Layout.grid)

# TP
def GoToZone():
    Config.in_zone = False

    if Config.FARM == "VIP":
        indexcol = True
        while indexcol != None:
            indexcol = pyautogui.locateOnScreen(Config.IMGS_LOCATION + '/collection.png', confidence=0.67)
            Teleport.ResetCharacter()
            Webhooks.SendWebhook(Config.EMBEDS["ToVIP"], ss=True)
            Controls.moveToCenter()
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
            Controls.hold_key("a", 3)
            Hoverboard.equipHoverboard(v=False)

        Config.in_zone = True
        GamepassBtns.AutoFarm.Set(value=True)
        Webhooks.SendWebhook(Config.EMBEDS["FinishedToVIP"], ss=True)
    else:
        farm = str(Config.FARM)
        if farm == "1":
            Teleport.ResetCharacter()
        else:
            PetSimulator.openTP()
            fixed_zone = PetSimulator.tpToZone(Config.FARM)
            farm = str(fixed_zone)

        Hoverboard.equipHoverboard(v=False)
        if farm == "1" or farm == "2" or farm == "3" or farm == "4" or farm == "5":
            Controls.hold_key("w", 1.5)
        elif farm == "6":
            Controls.hold_key("d", 2)
        elif farm == "7" or farm == "8" or farm == "9" or farm == "10":
            Controls.hold_key("s", 2)
        elif farm == "11":
            Controls.hold_key("d", 2.5)
        elif farm == "12" or farm == "13" or farm == "14":
            Controls.hold_key("w", 2.5)
        elif farm == "15":
            Controls.hold_key("w", 1.5)
        elif farm == "16":
            Controls.hold_key("d", 2.5)
        elif farm == "17" or farm == "18" or farm == "19" or farm == "20":
            Controls.hold_key("s", 2)
        elif farm == "21":
            Controls.hold_key("d", 2.5)
        elif farm == "22" or farm == "23" or farm == "24":
            Controls.hold_key("w", 2.5)
        elif farm == "25":
            Controls.hold_key("w", 1.32)
        elif farm == "26":
            Controls.hold_key("d", 2)
        elif farm == "27" or farm == "28" or farm == "29" or farm == "30":
            Controls.hold_key("s", 2.5)
        elif farm == "31":
            Controls.hold_key("d", 2)
        elif farm == "32" or farm == "33" or farm == "34" or farm == "35" or farm == "36":
            Controls.hold_key("w", 2.5)
        elif farm == "37":
            Controls.hold_key("d", 2.5)
        elif farm == "38" or farm == "39" or farm == "40":
            Controls.hold_key("s", 2)
        elif farm == "41":
            Controls.hold_key("d", 2.5)
        elif farm == "42" or farm == "43" or farm == "44" or farm == "45" or farm == "46":
            Controls.hold_key("w", 2.5)
        elif farm == "47" or farm == "48":
            Controls.hold_key("d", 2.5)
        elif farm == "49" or farm == "50" or farm == "51":
            Controls.hold_key("s", 2)
        elif farm == "52" or farm == "53" or farm == "54":
            Controls.hold_key("s", 2.5)
        elif farm == "55" or farm == "56":
            Controls.hold_key("d", 2.5)
        elif farm == "57":
            Controls.hold_key("s", 2.5)
        elif farm == "58" or farm == "59" or farm == "60" or farm == "61" or farm == "62" or farm == "63":
            Controls.hold_key("w", 2.5)
        elif farm == "64" or farm == "65" or farm == "66":
            Controls.hold_key("d", 2.5)
        elif farm == "67":
            Controls.hold_key("s", 2.5)

        Config.in_zone = True
        GamepassBtns.AutoFarm.Set(value=False)
        GamepassBtns.AutoFarm.Set(value=True)
        Webhooks.SendWebhook(Config.EMBEDS["FinishedWalking"], ss=True)

opened_rewards = 0
redeemed_giftbags = 0

last_opened_group = None
last_opened_social = None

last_opened_diamonds_3 = None
last_opened_diamonds_32 = None
last_opened_potions = None
last_opened_enchants = None
last_opened_items = None
last_opened_vip = None

last_spawned_flag = None

last_autofarm_area = None
def MainLoop(run_event):
    global redeemed_giftbags, opened_rewards, last_opened_group, last_opened_social, last_opened_diamonds_3,last_opened_diamonds_32,last_opened_potions,last_opened_enchants,last_opened_items,last_opened_vip, last_spawned_flag, last_autofarm_area

    Config.log("Main loop on!")
    Webhooks.SendWebhook(DiscordEmbed(description="Main loop on!", color="57F287"))

    while run_event.is_set():
        if Config.CLOSING == True:
            break

        if Config.PAUSED == False:
            try:
                disconnected = Roblox.checkDisconnection()

                Rewards.getRewards()
                time.sleep(1)
                if Config.CLAIM_VIP_REWARDS == True:
                    try:
                        can_go = False
                        if last_opened_vip == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_vip) > datetime.timedelta(hours=1):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_vip = datetime.datetime.now()
                            Rewards.ClaimVIPRewards()
                            Inventory.clickGiftBags()
                            Config.in_zone = False
                    except Exception as e:
                        Config.log_error("Failed to VIP rewards: " + str(e))
                        time.sleep(1)

                if Config.CLAIM_GROUP_REWARDS == True:
                    try:
                        can_go = False
                        if last_opened_group == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_group) > datetime.timedelta(days=1):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_group = datetime.datetime.now()
                            Rewards.claimGroupRewards()
                            Config.in_zone = False
                    except Exception as e:
                        Config.log_error("Failed to claim group rewards: " + str(e))
                        time.sleep(1)
                
                if Config.CLAIM_SOCIAL_REWARDS == True:
                    try:
                        can_go = False
                        if last_opened_social == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_social) > datetime.timedelta(days=1):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_social = datetime.datetime.now()
                            Rewards.claimSocialRewards()
                            Config.in_zone = False
                    except Exception as e:
                        Config.log_error("Failed to claim Social rewards: " + str(e))
                        time.sleep(1)

                if Config.CLAIM_FREE_DIAMONDS == True:
                    try:
                        can_go = False
                        if last_opened_diamonds_3 == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_diamonds_3) > datetime.timedelta(minutes=30):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_diamonds_3 = datetime.datetime.now()
                            Rewards.FreeDiamondsZone3()
                            Config.in_zone = False

                        can_go = False
                        if last_opened_diamonds_32 == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_diamonds_32) > datetime.timedelta(hours=3):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_diamonds_32 = datetime.datetime.now()
                            Rewards.FreeDiamondsZone32()
                            Config.in_zone = False
                    except Exception as e:
                        Config.log_error("Failed to claim Free Diamonds: " + str(e))
                        time.sleep(1)

                if Config.CLAIM_FREE_POTIONS == True:
                    try:
                        can_go = False
                        if last_opened_potions == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_potions) > datetime.timedelta(minutes=30):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_potions = datetime.datetime.now()
                            Rewards.FreePotions()
                            time.sleep(1)
                            Config.in_zone = False
                    except Exception as e:
                        Config.log_error("Failed to claim Free Potions: " + str(e))
                        time.sleep(1)

                if Config.CLAIM_FREE_ENCHANTS == True:
                    try:
                        can_go = False
                        if last_opened_enchants == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_enchants) > datetime.timedelta(minutes=45):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_enchants = datetime.datetime.now()
                            Rewards.FreeEnchants()
                            Config.in_zone = False
                    except Exception as e:
                        Config.log_error("Failed to claim Free Enchants: " + str(e))
                        time.sleep(1)

                if Config.CLAIM_FREE_ITEMS == True:
                    try:
                        can_go = False
                        if last_opened_items == None:
                            can_go = True
                        else:
                            if (datetime.datetime.now() - last_opened_items) > datetime.timedelta(hours=1):
                                can_go = True
                        if can_go == True:
                            Config.in_zone = False
                            last_opened_items = datetime.datetime.now()
                            Rewards.FreeItems()
                            Config.in_zone = False
                    except Exception as e:
                        Config.log_error("Failed to claim Free Enchants: " + str(e))
                        time.sleep(1)

                if disconnected == True or Config.in_zone == False or last_autofarm_area != Config.FARM:
                    GoToZone()
                    last_autofarm_area = Config.FARM
                    
                if Config.in_zone == True:
                    if Config.POTION != False:
                        try:
                            can_go = False
                            if Config.POTION_TOTAL_START == None:
                                Inventory.usePotions()
                            else:
                                if (datetime.datetime.now() - Config.POTION_TOTAL_START) > datetime.timedelta(minutes=Config.POTION_TOTAL_MINUTES):
                                    Config.POTION_TOTAL_MINUTES = 0
                                    Config.POTION_TOTAL_START = None
                                    Inventory.usePotions()
                        except Exception as e:
                            Config.log_error("Failed to use potions: " + str(e))
                            time.sleep(1)

                    if Config.FLAG != False:
                        try:
                            can_go = False
                            if last_spawned_flag == None:
                                can_go = True
                            else:
                                if (datetime.datetime.now() - last_spawned_flag) > datetime.timedelta(minutes=5):
                                    can_go = True
                            if can_go == True:
                                last_spawned_flag = datetime.datetime.now()
                                Inventory.placeFlag()
                        except Exception as e:
                            Config.log_error("Failed to spawn flag: " + str(e))
                            time.sleep(1)
            finally:
                time.sleep(0.1)

            if Config.in_zone == True:
                Config.log("Clicked in middle for Anti AFK...")
                Controls.moveToCenter()
                x,y = pyautogui.position()
                autoit.mouse_click(x=x,y=y)
                time.sleep(10)
        else:
            if Config.CLOSING == True:
                break
            time.sleep(1)

def AutoReconnectLoop(run_event):
    rec_ = 0
    if Config.AUTO_RECONNECT != False:
        Config.log("Auto reconnect on!")
        Webhooks.SendWebhook(DiscordEmbed(description="Auto reconnect on!", color="57F287"))
        while run_event.is_set():
            if Config.CLOSING == True:
                break

            if Config.PAUSED == False:
                rec_ = rec_ + 1
                if rec_ >= Config.AUTO_RECONNECT_Calc:
                    rec_ = 0
                    Webhooks.SendWebhook(DiscordEmbed(description="Reconnecting ("+str(Config.AUTO_RECONNECT)+" minutes passed)...", color="5865F2"), ss=True)
                    subprocess.call("TASKKILL /F /IM RobloxPlayerBeta.exe", shell=True)
                time.sleep(1)
            else:
                if Config.CLOSING == True:
                    break
                time.sleep(1)

def calculate_hourly_average(earnings_list):
    total_earnings = sum(earnings_list)
    average_earnings_per_hour = total_earnings / len(earnings_list)
    return round(average_earnings_per_hour)

def convert_delta(dlt: datetime.timedelta) -> str:
    minutes, seconds = divmod(int(dlt.total_seconds()), 60)
    return f"{minutes}:{seconds:02}"

def FarmingHourlyReportHandler(run_event):
    if Config.HOURLY_REPORTS != False:
        while run_event.is_set():
            while Config.in_zone == False:
                time.sleep(0.1)
            start_time = datetime.datetime.now()
            while Config.in_zone == True:
                time.sleep(0.1)
            Config.FARMING_TIMES.append(datetime.datetime.now() - start_time)

def HourlyReport(run_event):
    global opened_rewards, redeemed_giftbags

    if Config.HOURLY_REPORTS != False:
        Config.log("Hourly Report on!")
        Webhooks.SendWebhook(DiscordEmbed(description="Hourly report on!", color="57F287"))

        while run_event.is_set():
            if Config.CLOSING == True:
                break
            if Config.PAUSED == False:
                try:
                    to_remove = 0
                    diamonds_array = []
                    diamonds_array.insert(0, ("0", 0, "00:00"))

                    for idx in range(1, 7):
                        dia__a = Stats.GetDiamonds()
                        to_r = 0
                        while dia__a[0] == None:
                            dia__a = Stats.GetDiamonds()
                            to_remove = to_remove + 5
                            to_r = to_r + 5
                            time.sleep(5)

                        nowdate = datetime.datetime.now()
                        diamonds_array.insert(idx, (dia__a[0], dia__a[1], str(datetime.time(hour=nowdate.hour, minute=nowdate.minute, second=nowdate.second))))
                        Config.log_debug(str(diamonds_array))
                        if idx == 7:
                            pass
                        else:
                            for i in range(1, (600 - to_r) + 1): # get diamonds per 10 mins
                                time.sleep(1)
                                if Config.CLOSING == True:
                                    break

                    if Config.CLOSING == False:
                        Config.log_debug(str(diamonds_array))
                        filename = Config.SS_LOCATION + "/hourlyreport_"+str(random.randint(999999, 999999999))+".png"
                        firstDiamondTuple = diamonds_array.__getitem__(1)
                        lastDiamondTuple = diamonds_array.__getitem__(6)
                    
                        walkingTotal = None
                        teleportingTotal = None
                        farmingTotal = None
                        rewardsTotal = None
                        usingUITotal = None
                        otherTotal = None

                        for idx in range(len(Config.WALKING_TIMES)):
                            i = Config.WALKING_TIMES[idx]
                            if walkingTotal == None:
                                walkingTotal = i
                            else:
                                walkingTotal = walkingTotal + i

                        for idx in range(len(Config.TELEPORT_TIMES)):
                            i = Config.TELEPORT_TIMES[idx]
                            if teleportingTotal == None:
                                teleportingTotal = i
                            else:
                                teleportingTotal = teleportingTotal + i

                        for idx in range(len(Config.FARMING_TIMES)):
                            i = Config.FARMING_TIMES[idx]
                            if rewardsTotal == None:
                                rewardsTotal = i
                            else:
                                rewardsTotal = rewardsTotal + i    

                        for idx in range(len(Config.REWARDS_TIMES)):
                            i = Config.REWARDS_TIMES[idx]
                            if farmingTotal == None:
                                farmingTotal = i
                            else:
                                farmingTotal = farmingTotal + i 

                        for idx in range(len(Config.USING_UI_TIMES)):
                            i = Config.USING_UI_TIMES[idx]
                            if usingUITotal == None:
                                usingUITotal = i
                            else:
                                usingUITotal = usingUITotal + i 

                        for idx in range(len(Config.OTHER_TIMES)):
                            i = Config.OTHER_TIMES[idx]
                            if otherTotal == None:
                                otherTotal = i
                            else:
                                otherTotal = otherTotal + i 

                        if walkingTotal == None:
                            walkingTotal = datetime.timedelta(seconds=0)
                        if teleportingTotal == None:
                            teleportingTotal = datetime.timedelta(seconds=0)
                        if farmingTotal == None:
                            farmingTotal = datetime.timedelta(seconds=0)
                        if rewardsTotal == None:
                            rewardsTotal = datetime.timedelta(seconds=0)
                        if usingUITotal == None:
                            usingUITotal = datetime.timedelta(seconds=0)
                        if otherTotal == None:
                            otherTotal = datetime.timedelta(seconds=0)

                        success, img = StatLibrary.generate([
                            StatLib.StatVisualType(
                                type=StatLib.StatVisualEnum.line_chart,
                                right=False,
                                data={
                                    "x": {
                                        "data": [diamonds_array[1][2], diamonds_array[2][2], diamonds_array[3][2], diamonds_array[4][2], diamonds_array[5][2], diamonds_array[6][2]],
                                        "label": "Time"
                                    },
                                    "y": {
                                        "data": [diamonds_array[1][1][0], diamonds_array[2][1][0], diamonds_array[3][1][0], diamonds_array[4][1][0], diamonds_array[5][1][0], diamonds_array[6][1][0]],
                                        "label": "Diamonds"
                                    }
                                },
                                title=f"Diamonds ({diamonds_array[1][0]} → {diamonds_array[6][0]}) | Earned: {round(lastDiamondTuple[1][0] - firstDiamondTuple[1][0])} | Hourly Average: {calculate_hourly_average([diamonds_array[1][1][0], diamonds_array[2][1][0], diamonds_array[3][1][0], diamonds_array[4][1][0], diamonds_array[5][1][0], diamonds_array[6][1][0]])}",
                                color="#1e23b4"
                            ),
                            StatLib.StatVisualType(
                                type=StatLib.StatVisualEnum.pie_chart,
                                right=False,
                                explode=(0.1, 0, 0, 0, 0),
                                legend={
                                    "on": True,
                                    "title": "Actions"
                                },
                                data={
                                    "data": [
                                        int(farmingTotal.seconds),
                                        int(rewardsTotal.seconds),
                                        int(walkingTotal.seconds),
                                        int(teleportingTotal.seconds),
                                        int(usingUITotal.seconds),
                                        int(otherTotal.seconds)
                                    ],
                                    "labels": [
                                        f"Farming ({convert_delta(datetime.timedelta(seconds=farmingTotal.seconds))})",
                                        f"Claiming Rewards ({convert_delta(datetime.timedelta(seconds=rewardsTotal.seconds))})",
                                        f"Walking ({convert_delta(datetime.timedelta(seconds=walkingTotal.seconds))})",
                                        f"Teleporting ({convert_delta(datetime.timedelta(seconds=teleportingTotal.seconds))})",
                                        f"Using UI ({convert_delta(datetime.timedelta(seconds=usingUITotal.seconds))})",
                                        f"Other ({convert_delta(datetime.timedelta(seconds=otherTotal.seconds))})"
                                    ],
                                    "colors": ["#0353a4", "#023e7d", "#002855", "#001845", "#001233", "#000b1f"]
                                },
                                title="Actions"
                            )
                        ],savedirectory=filename,size=8)

                        description = f"""Gift bags redeemed: `{redeemed_giftbags}`"""
                        if success:
                            with open(filename, "rb") as f:
                                Webhooks.webhook.add_file(file=f.read(), filename="hr.png")
                        else:
                            description = f"""Diamonds earned: {round(lastDiamondTuple[1][0] - firstDiamondTuple[1][0])} ({diamonds_array[1][0]} → {diamonds_array[6][0]}) | Hourly Average: {calculate_hourly_average([diamonds_array[1][1][0], diamonds_array[2][1][0], diamonds_array[3][1][0], diamonds_array[4][1][0], diamonds_array[5][1][0], diamonds_array[6][1][0]])}
    Gift bags redeemed: `{redeemed_giftbags}`"""
                        
                        e = DiscordEmbed(title="Hourly Report", description=description, color="1ABC9C")
                        e.set_image(url="attachment://hr.png")
                        Webhooks.SendWebhook(e, content=f"<@{Config.DISCORD_USER_ID}>")

                        opened_rewards = 0
                        redeemed_giftbags = 0
                        to_remove = 0
                        try:
                            os.remove(filename)
                        except Exception as e:
                            Config.log_warning("Failed to remove hourly report image: " + str(e))
                except Exception as e:
                    print(e)
                    Config.log_critical("Failed to make hourly report: " + str(e))
            else:
                if Config.CLOSING == True:
                    break
                time.sleep(1)

run_event = threading.Event()
def __main_handler():
    WindowsInhibitor.inhibit()

    run_event.set()
    t1 = threading.Thread(target=MainLoop, args=[run_event])
    t2 = threading.Thread(target=AutoReconnectLoop, args=[run_event])
    t3 = threading.Thread(target=HourlyReport, args=[run_event])
    uiThread = threading.Thread(target=UI.startUI)

    uiThread.start()
    time.sleep(.5)

    try:
        while Config.UISTARTED == False:
            time.sleep(1)
        v = requests.get("https://raw.githubusercontent.com/mstudio45/ps99macro/main/data/v").text.replace("\n", "")
        if Config.VERSION_ != str(v):
            Config.log_warning("You are using an outdated version (" + Config.VERSION_ + "). Latest version: " + str(v) + ".")
    except:
        Config.log_critical("Failed to check new update...")

    t1.start()
    t2.start()
    t3.start()

    Webhooks.SendWebhook(Config.EMBEDS["Starting"])
    try:
        while True:
            time.sleep(.1)
            if Config.CLOSING == True:
                break
    finally:
        Config.CLOSING = True
        print("Attempting to close threads...")
        run_event.clear()
        WindowsInhibitor.uninhibit()
        t1.join()
        print("Main Loop closed.")
        t2.join()
        print("Auto Reconnect Loop closed.")
        t3.join()
        print("Hourly Reports closed.")
        uiThread.join()
        print("Closed!")
        Webhooks.SendWebhook(Config.EMBEDS["Closed"])

if __name__ == '__main__':
    __main_handler()
