import dearpygui.dearpygui as dpg
import os, sys
import keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import config as Config
import externals.uicode.logger as mvlogger
import externals.libs as lib

Webhook = lib.Discord()

add_logger = mvlogger.mvLogger

settings_TP_WAIT_TIME = None
settings_VIP = None
settings_WEBHOOK = None

settings_CLAIMGROUP = None
settings_CLAIMSOCIAL = None
settings_CLAIM_VIP = None

settings_CLAIMFREEDIAMONDS = None
settings_CLAIMFREEPOTIONS = None
settings_CLAIMFREE_ENCHANTS = None
settings_CLAIMFREE_ITEMS = None

settings_POTION = None
settings_FLAG = None
settings_FARM = None
settings_FARM_TOGGLE = None

settings_EGG = None
settings_HATCH_TOGGLE = None

settings_AUTORECONECT = None
def setSettings():
    Config.TP_WAIT_TIME = int(dpg.get_value(settings_TP_WAIT_TIME))
    if Config.TP_WAIT_TIME < 6:
        Config.TP_WAIT_TIME = 6

    # PET SIMULATOR 99
    Config.CLAIM_GROUP_REWARDS = dpg.get_value(settings_CLAIMGROUP)
    Config.CLAIM_SOCIAL_REWARDS = dpg.get_value(settings_CLAIMSOCIAL)
    Config.CLAIM_VIP_REWARDS = dpg.get_value(settings_CLAIM_VIP)

    Config.CLAIM_FREE_DIAMONDS = dpg.get_value(settings_CLAIMFREEDIAMONDS)
    Config.CLAIM_FREE_POTIONS = dpg.get_value(settings_CLAIMFREEPOTIONS)
    Config.CLAIM_FREE_ENCHANTS = dpg.get_value(settings_CLAIMFREE_ENCHANTS)
    Config.CLAIM_FREE_ITEMS = dpg.get_value(settings_CLAIMFREE_ITEMS)

    Config.AUTOFARM = dpg.get_value(settings_FARM_TOGGLE)
    Config.FARM = dpg.get_value(settings_FARM)
    Config.CheckAreaValid(set=True)

    Config.FLAG = dpg.get_value(settings_FLAG).lower()
    Config.CheckFlagValid(set=True)

    Config.POTION = dpg.get_value(settings_POTION).lower()
    Config.CheckPotionValid(set=True)

    Config.AUTOHATCH = dpg.get_value(settings_HATCH_TOGGLE)
    Config.EGG = dpg.get_value(settings_EGG)

    # Roblox
    if dpg.get_value(settings_AUTORECONECT).isnumeric():
        Config.AUTO_RECONNECT = int(dpg.get_value(settings_AUTORECONECT))
        Config.AUTO_RECONNECT_Calc = Config.AUTO_RECONNECT * 60
    else:
        Config.AUTO_RECONNECT = False

    Config.VIP = dpg.get_value(settings_VIP)
    if Config.VIP.lower() == "false" or Config.VIP == "False":
        Config.VIP = False

    # DISCORD
    Config.DISCORD_WEBHOOK = dpg.get_value(settings_WEBHOOK)
    if Config.DISCORD_WEBHOOK.lower() == "false":
        Config.DISCORD_WEBHOOK = False
    if str(Config.DISCORD_WEBHOOK).find("https://discord.com/api/webhooks") == -1:
        Config.log_warning("Discord webhook link is invalid. https://discord.com/api/webhooks is missing.")
        Config.DISCORD_WEBHOOK = False

    update_Values()
    Webhooks.SendWebhook(Config.EMBEDS["WebhookChanged"])
    Config.log("Config changed.")

def update_Values():
    dpg.set_value(settings_TP_WAIT_TIME, Config.TP_WAIT_TIME)

    dpg.set_value(settings_CLAIMGROUP, Config.CLAIM_GROUP_REWARDS)
    dpg.set_value(settings_CLAIMSOCIAL, Config.CLAIM_SOCIAL_REWARDS)
    dpg.set_value(settings_CLAIM_VIP, Config.CLAIM_VIP_REWARDS)

    dpg.set_value(settings_CLAIMFREEDIAMONDS, Config.CLAIM_FREE_DIAMONDS)
    dpg.set_value(settings_CLAIMFREEPOTIONS, Config.CLAIM_FREE_POTIONS)
    dpg.set_value(settings_CLAIMFREE_ENCHANTS, Config.CLAIM_FREE_ENCHANTS)
    dpg.set_value(settings_CLAIMFREE_ITEMS, Config.CLAIM_FREE_ITEMS)

    dpg.set_value(settings_FARM_TOGGLE, Config.AUTOFARM)
    dpg.set_value(settings_FARM, str(Config.FARM))
    dpg.set_value(settings_FLAG, str(Config.FLAG))
    dpg.set_value(settings_POTION, str(Config.POTION))

    dpg.set_value(settings_HATCH_TOGGLE, Config.AUTOHATCH)
    dpg.set_value(settings_EGG, str(Config.EGG))

    # Roblox
    dpg.set_value(settings_AUTORECONECT, str(Config.AUTO_RECONNECT))
    dpg.set_value(settings_VIP, str(Config.VIP))

    # DISCORD
    dpg.set_value(settings_WEBHOOK, str(Config.DISCORD_WEBHOOK))

def FarmHatchUpdated():
    if dpg.get_value(settings_FARM_TOGGLE) and dpg.get_value(settings_HATCH_TOGGLE):
        dpg.set_value(settings_FARM_TOGGLE, False)
        dpg.set_value(settings_HATCH_TOGGLE, False)

status = None
status_log = None
status_cur = None
settings = None
pauseButton = None
def pauseresume():
    global status
    Config.PAUSED = not Config.PAUSED
    dpg.set_item_label(pauseButton, (not Config.PAUSED and "Stop" or "Start") + " (F3)")
    if Config.PAUSED == False:
        dpg.set_value("main_ui_tabs", status)
    Webhooks.SendWebhook(Config.PAUSED and Config.EMBEDS["Paused"] or Config.EMBEDS["Unpaused"])
    Config.log(Config.PAUSED and "Paused" or "Unpaused")

def startUI():
    global add_logger,pauseButton,status,status_log,status_cur,settings, settings_VIP,settings_WEBHOOK,settings_FARM,settings_FARM_TOGGLE,settings_EGG,settings_HATCH_TOGGLE,settings_AUTORECONECT, settings_CLAIMGROUP, settings_CLAIMSOCIAL, settings_CLAIMFREEDIAMONDS, settings_CLAIMFREEPOTIONS, settings_CLAIMFREE_ENCHANTS, settings_CLAIMFREE_ITEMS, settings_CLAIM_VIP, settings_FLAG, settings_POTION,settings_TP_WAIT_TIME

    if Config.UISTARTED == True:
        return
    Config.UISTARTED = True
    keyboard.add_hotkey("f3", pauseresume)

    dpg.create_context()
    dpg.create_viewport(title='Pet Simualtor 99 Macro | ' + str(Config.VERSION_) + ' | mstudio45', width=835, height=315)
    with dpg.window(label="Main", width=800, height=250, pos=[10, 10], no_close=True):
        with dpg.tab_bar(tag="main_ui_tabs"):
            with dpg.tab(label="Main", tracked=True) as statusmenu:
                pauseButton = dpg.add_button(label="Start (F3)", callback=pauseresume)
            with dpg.tab(label="Status", tracked=True) as statusmenu:
                status = statusmenu
                status_cur = dpg.add_text("Current Status: None")
                status_log = add_logger(parent=statusmenu)
            with dpg.tab(label="Settings") as settinggroup:
                settings = settinggroup
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Set Config (save soon)", callback=setSettings)
                    dpg.add_button(label="Update", callback=update_Values)

                dpg.add_text("Invalid stuff may break the app.")
                dpg.add_text("Some settings will show a warning in the 'Status' tab if they are not correct.")
                with dpg.tab_bar():
                    with dpg.tab(label="General", tracked=True):
                        settings_TP_WAIT_TIME = dpg.add_input_text(label="Teleport Wait Time", default_value=Config.TP_WAIT_TIME)

                    with dpg.tab(label="Pet Simulator 99", tracked=True):
                        with dpg.tab_bar():
                            with dpg.tab(label="Rewards", tracked=True):
                                settings_CLAIMGROUP = dpg.add_checkbox(label="Claim Group Rewards", default_value=Config.CLAIM_GROUP_REWARDS)
                                settings_CLAIMSOCIAL = dpg.add_checkbox(label="Claim Social Rewards", default_value=Config.CLAIM_SOCIAL_REWARDS)
                                settings_CLAIM_VIP = dpg.add_checkbox(label="Claim VIP Rewards", default_value=Config.CLAIM_VIP_REWARDS)
                
                            with dpg.tab(label="Free Rewards", tracked=True):
                                settings_CLAIMFREEDIAMONDS = dpg.add_checkbox(label="Claim Free Diamonds", default_value=Config.CLAIM_FREE_DIAMONDS)
                                settings_CLAIMFREEPOTIONS = dpg.add_checkbox(label="Claim Free Potions", default_value=Config.CLAIM_FREE_POTIONS)
                                settings_CLAIMFREE_ENCHANTS = dpg.add_checkbox(label="Claim Free Enchants", default_value=Config.CLAIM_FREE_ENCHANTS)
                                settings_CLAIMFREE_ITEMS = dpg.add_checkbox(label="Claim Free Items", default_value=Config.CLAIM_FREE_ITEMS)

                            with dpg.tab(label="Auto Farm", tracked=True):
                                settings_FARM_TOGGLE = dpg.add_checkbox(label="Auto Farm", default_value=Config.AUTOFARM, callback=FarmHatchUpdated, user_data="farm")
                                settings_FARM = dpg.add_input_text(label="Farm Area (VIP or 1-50)", default_value=str(Config.FARM))
                                settings_FLAG = dpg.add_input_text(label="Flag (False or Flag Name)", default_value=str(Config.FLAG))
                                settings_POTION = dpg.add_input_text(label="Potion (False or Potion)", default_value=str(Config.POTION))
                                dpg.add_text(Config.potion_formats_)

                            with dpg.tab(label="Auto Hatch", tracked=True):
                                settings_HATCH_TOGGLE = dpg.add_checkbox(label="Auto Hatch", default_value=Config.AUTOHATCH, callback=FarmHatchUpdated, user_data="hatch")
                                settings_EGG = dpg.add_input_text(label="Egg (egg number thats on ground)", default_value=str(Config.EGG))

                    with dpg.tab(label="Roblox", tracked=True):
                        settings_VIP = dpg.add_input_text(label="Private Server Link (False or link)", default_value=Config.VIP)
                        settings_AUTORECONECT = dpg.add_input_text(label="Auto Reconnect (in minutes, False or int)", default_value=str(Config.AUTO_RECONNECT))

                    with dpg.tab(label="Discord", tracked=True):
                        settings_WEBHOOK = dpg.add_input_text(label="Discord Webhook (False or VIP link)", default_value=Config.DISCORD_WEBHOOK)
            with dpg.tab(label="Credits"):
                dpg.add_text(f"Created by mstudio45 | {Config.VERSION_}")
                dpg.add_text(f"Last PS99 update supported: Update 3")

                with dpg.tab_bar():
                    with dpg.tab(label="Contributors", tracked=True):
                        dpg.add_text("OCR, StatLib - upio_real")
                    with dpg.tab(label="Testers", tracked=True):
                        dpg.add_text("Master Oogway")
                        dpg.add_text("AlperSocial")

    def log(text=""):
        text = str(text)
        print(text)
        dpg.set_value(status_cur, "Current Status: " + text)
        status_log.log_info(text)

    def log_debug(text=""):
        text = str(text)
        print(text)
        dpg.set_value(status_cur, "Current Status: [DEBUG] " + text)
        status_log.log_debug(text)

    def log_warning(text=""):    
        text = str(text)
        print(text)
        dpg.set_value(status_cur, "Current Status: [WARN] " + text)
        status_log.log_warning(text)

    def log_error(text=""):    
        text = str(text)
        print(text)
        dpg.set_value(status_cur, "Current Status: [ERROR] " + text)
        status_log.log_error(text)

    def log_critical(text=""):    
        text = str(text)
        print(text)
        dpg.set_value(status_cur, "Current Status: [CRITICAL] " + text)
        status_log.log_critical(text)

    Config.log = log
    Config.log_debug = log_debug
    Config.log_warning = log_warning
    Config.log_error = log_error
    Config.log_critical = log_critical

    Config.log("UI started.")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        if Config.CLOSING == True:
            break
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
    Config.CLOSING = True
    print("UI Closed.")
