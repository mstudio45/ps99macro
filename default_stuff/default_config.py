from discord_webhook import DiscordWebhook, DiscordEmbed
import os

# GENERAL #
USE_WSL = False                               # makes OCR faster but hard to setup for no expert Windows users (tutorial soon)
# WSL needs to have python and these packages installed: pytorch, transformers, flask

# ROBLOX #
VIP = "" # or False
AUTO_RECONNECT = False                        # minutes or False
AUTO_RECONNECT_Calc = 60 * 60                 # DO NOT TOUCH #

# PET SIM 99 #
MAX_ZONES = 1                                # Your last unlocked zone ! REQUIRED !

HOURLY_REPORTS = True

REDEEM_GIFT_BAGS = False                       # every 1 hour, and also after claiming VIP Rewards (if )

CLAIM_GROUP_REWARDS = False
CLAIM_SOCIAL_REWARDS = False                  # Social rewards

CLAIM_FREE_DIAMONDS = False                    # zone 3, 32
CLAIM_FREE_POTIONS = False                     # zone 17
CLAIM_FREE_ENCHANTS = False                    # zone 21
CLAIM_FREE_ITEMS = False                       # zone 24
CLAIM_VIP_REWARDS = False                      # if u dont have VIP dont turn this on

AUTOFARM = False
FARM = 1                                  # VIP or zone number as int

FLAG = ""                                # False or coins, diamond, fortune, hasty, magnet

# DO NOT CHANGE potion_formats_ #
potion_formats_ = """
Potion formats:
    Potion_Upgrade | Examples: Speed_1, Coins_3     | Will only use that certain potion that has the set upgrade
    Potion_All     | Examples: Speed_All, Coins_All | Will only use that certain potion ignoring the upgrade that its using (from upgrade 1 to max upgrade)
    Potion!Upgrade | Examples: Speed!3, Coins!2     | Will only use that certain potion that is that certain upgrade or under (if the upgrade is set to 3, it will only pick that potion with upgrade 3 or lower)
"""
POTION = False                                # False or potion by one of the format

AUTOHATCH = False
EGG = "1"                                     # by the egg number (on the ground)

# DISCORD #
DISCORD_WEBHOOK = ""
DISCORD_USER_ID = ""

def getAttemptRejoining(attempts): 
    return DiscordEmbed(description="Rejoining (Attempt #" + str(attempts) + ")...", color="ED4245")
EMBEDS = { # https://pypi.org/project/discord-webhook/ -> then scroll down until you see "Webhook with Embedded Content" for the DiscordEmbed examples.
    "Starting": DiscordEmbed(description="Starting...", color="FEE75C"),
    "Started": DiscordEmbed(description="**Started!**", color="57F287"),
    "Closed": DiscordEmbed(description="**Closed!**", color="ED4245"),

    "Rejoining": DiscordEmbed(description="Rejoining...", color="ED4245"),
    "RejoiningAttempt": getAttemptRejoining, # change in the function
    "Rejoined": DiscordEmbed(description="Rejoined!", color="5865F2"),

    "WebhookChanged": DiscordEmbed(description="Webhook/Config has been changed.", color="5865F2"),

    "Paused": DiscordEmbed(description="Paused...", color="E67E22"),
    "Unpaused": DiscordEmbed(description="Unpaused!", color="57F287"),

    "ToVIP": DiscordEmbed(description="Walking to VIP...", color="5865F2"),
    "FinishedToVIP": DiscordEmbed(description="Walked to VIP!", color="5865F2"),

    "FinishedWalking": DiscordEmbed(description="Finished walking to zone!", color="5865F2"),

    "ToGroupRewards": DiscordEmbed(description="Walking to Group Rewards...", color="5865F2"),
    "FinishedToGroupRewards": DiscordEmbed(description="Walked to Group Rewards!", color="57F287"),

    "ToSocialRewards": DiscordEmbed(description="Walking to Social Rewards...", color="5865F2"),
    "FinishedToSocialRewards": DiscordEmbed(description="Walked to Social Rewards!", color="57F287"),

    "ClaimingFreeRewards": DiscordEmbed(description="Claiming rewards...", color="FEE75C"),
    "ClaimedFreeRewards": DiscordEmbed(description="Rewards claimed!", color="57F287"),

    "ToFreeDiamonds": DiscordEmbed(description="Walking to Free Diamonds...", color="5865F2"),
    "ClaimedToFreeDiamonds": DiscordEmbed(description="Claimed Free Diamonds!", color="57F287"),

    "ToFreePotions": DiscordEmbed(description="Walking to Free Potions...", color="5865F2"),
    "ClaimedToFreePotions": DiscordEmbed(description="Claimed Free Potions!", color="57F287"),

    "ToFreeEnchants": DiscordEmbed(description="Walking to Free Enchants...", color="5865F2"),
    "ClaimedToFreeEnchants": DiscordEmbed(description="Claimed Free Enchants!", color="57F287"),

    "ToFreeItems": DiscordEmbed(description="Walking to Free Items...", color="5865F2"),
    "ClaimedToFreeItems": DiscordEmbed(description="Claimed Free Items!", color="57F287"),

    "ToVIPRewards": DiscordEmbed(description="Walking to VIP Rewards...", color="5865F2"),
    "ClaimedToVIPRewards": DiscordEmbed(description="Claimed VIP Rewards!", color="57F287"),

    "PlacingFlag": DiscordEmbed(description="Placing the flag...", color="5865F2"),
    "PlacedFlag": DiscordEmbed(description="Placed the flag!", color="57F287"),
    "FailedPlacedFlag": DiscordEmbed(description="Failed to place the flag...", color="ED4245"),

    "ClaimingGiftBags": DiscordEmbed(description="Claiming gift bags...", color="5865F2"),
    "ClaimedGiftBags": DiscordEmbed(description="Claimed the gift bags!", color="57F287"),

    "UsingPotions": DiscordEmbed(description="Using potions...", color="5865F2"),
    "PotionsUsed": DiscordEmbed(description="Potions used!", color="57F287"),
}


                            # ! DO NOT TOUCH ! DO NOT TOUCH ! #
log = print
log_debug = print
log_warning = print
log_error = print
log_critical = print

# PS99 INFO #
HOVERBOARD = False
POTION_TOTAL_MINUTES = 0
POTION_TOTAL_START = None

# APP INFO #
UISTARTED = False
CLOSING = False
PAUSED = True
VERSION_ = "v1-dev"
in_zone = False

# ACTIONS LOG #
WALKING_TIMES = []
TELEPORT_TIMES = []
FARMING_TIMES = []
USING_UI_TIMES = []
OTHER_TIMES = []

# CODE FOR CONFIGS #
if AUTOFARM and AUTOHATCH:
    AUTOFARM = False
    AUTOHATCH = False

SS_LOCATION = os.path.join(os.getcwd(), "ss")
IMGS_LOCATION = os.path.join(os.getcwd(), "imgs")

def CheckPotionValid(set=False):
    global POTION, IMGS_LOCATION, log, log_critical, log_debug, log_error, log_warning

    potion_ = str(POTION)
    to_return = POTION
    suc = False

    if potion_.lower() == "false" or potion_ == "False":
        to_return = False
    else:
        potionName = str(POTION)

        if "_all" in potionName:
            potionName = potionName.replace("_all", "")
            if os.path.exists(IMGS_LOCATION + "/inventory/potions/" + potionName + ".txt") == False:
                log_warning("Potion '" + str(POTION) + "' doesn't exists/is not supported or the format is incorrect.")
                to_return = False
            else:
                suc = True

        elif "_" in potionName:
            if os.path.exists(IMGS_LOCATION + "/inventory/potions/" + potionName + ".png") == False:
                log_warning("Potion '" + str(POTION) + "' doesn't exists/is not supported or the format is incorrect.")
                to_return = False
            else:
                suc = True

        elif "!" in potionName:
            if os.path.exists(IMGS_LOCATION + "/inventory/potions/" + potionName.split("!")[0] + ".txt") == False:
                log_warning("Potion '" + str(POTION) + "' doesn't exists/is not supported or the format is incorrect.")
                to_return = False
            else:
                suc = True

            if os.path.exists(IMGS_LOCATION + "/inventory/potions/" + potionName.split("!")[0] + "_" + potionName.split("!")[1] + ".png") == False:
                log_warning("Potion '" + str(POTION) + "' doesn't exists/is not supported or the format is incorrect.")
                to_return = False
            else:
                suc = True   
        else:
            log_warning("Potion '" + str(POTION) + "' isn't in any of the formats.")
            to_return = False

    if set == True:
        POTION = to_return

    return suc, to_return
def CheckFlagValid(set=False):
    global FLAG, IMGS_LOCATION, log_warning

    to_return = FLAG
    suc = False

    if str(FLAG).lower() == "false" or str(FLAG) == "False":
        to_return = False
    else:
        if os.path.exists(IMGS_LOCATION + "/inventory/flags/" + str(FLAG) + ".png") == False:
            log_warning("Flag '" + str(FLAG) + "' doesn't exists/is not supported.")
            to_return = False
        else:
            suc = True

    if set == True:
        FLAG = to_return
    return suc, to_return

def CheckAreaValid(set=False):
    global FARM, IMGS_LOCATION, log_warning

    to_return = FARM
    suc = False
    if FARM == "VIP":
        return True, FARM
    
    if os.path.exists(IMGS_LOCATION + '/tp_menu/#'+str(FARM)+'.png') == False or os.path.exists(IMGS_LOCATION + '/tp_menu_safe_one/#'+str(FARM)+'.png') == False:
        log_warning("Area '" + str(FARM) + "' is not supported.")
        suc = False
        to_return = str(MAX_ZONES)
    elif os.path.exists(IMGS_LOCATION + '/tp_menu/#'+str(FARM)+'.png') == True and os.path.exists(IMGS_LOCATION + '/tp_menu_safe_one/#'+str(FARM)+'.png') == True:
        suc = True

    if set == True:
        FARM = to_return
    return suc, to_return

CheckAreaValid(set=True)
CheckFlagValid(set=True)
CheckPotionValid(set=True)