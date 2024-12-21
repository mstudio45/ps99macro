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
Controls = externals.libs.Controls()
Images = externals.libs.Images()
Discord = externals.libs.Discord()

# Macro info in macro.py
ZoneList = {
    1: {
        "Name": "Spawn",
        "Walking": "hoverboard:false;key_w:1.5;"
    },
    2: {
        "Name": "Colorful Forest",
        "Walking": "hoverboard:false;key_w:1.5;"
    },
    3: {
        "Name": "Castle",
        "Walking": "hoverboard:false;key_w:1.5;"
    },
    4: {
        "Name": "Green Forest",
        "Walking": "hoverboard:false;key_w:1.5;"
    },
    5: {
        "Name": "Autumn",
        "Walking": "hoverboard:false;key_w:1.5;"
    },
    6: {
        "Name": "Cherry Blossom",
        "Walking": "hoverboard:false;key_d:2"
    },
    7: {
        "Name": "Farm",
        "Walking": "hoverboard:false;key_s:2"
    },
    8: {
        "Name": "Backyard",
        "Walking": "hoverboard:false;key_s:2"
    },
    9: {
        "Name": "Misty Falls",
        "Walking": "hoverboard:false;key_s:2"
    },
    10: {
        "Name": "Mine",
        "Walking": "hoverboard:false;key_s:2"
    },
    11: {
        "Name": "Chrystal Caverns",
        "Walking": "hoverboard:false;key_s:2"
    },
    12: {
        "Name": "Dead Forest",
        "Walking": "hoverboard:false;"
    },
    13: {
        "Name": "Dark Forest",
        "Walking": "hoverboard:false;"
    },
    14: {
        "Name": "Mushroom Field",
        "Walking": "hoverboard:false;"
    },
    15: {
        "Name": "Enchanted Forest",
        "Walking": "hoverboard:false;"
    },
    16: {
        "Name": "Crimson Forest",
        "Walking": "hoverboard:false;"
    },
    17: {
        "Name": "Jungle",
        "Walking": "hoverboard:false;"
    },
    18: {
        "Name": "Jungle Temple",
        "Walking": "hoverboard:false;"
    },
    19: {
        "Name": "Oasis",
        "Walking": "hoverboard:false;"
    },
    20: {
        "Name": "Beach",
        "Walking": "hoverboard:false;"
    },
    21: {
        "Name": "Coral Reef",
        "Walking": "hoverboard:false;"
    },
    22: {
        "Name": "Shipwreck",
        "Walking": "hoverboard:false;"
    },
    23: {
        "Name": "Atlantis",
        "Walking": "hoverboard:false;"
    },
    24: {
        "Name": "Palm Beach",
        "Walking": "hoverboard:false;"
    },
    25: {
        "Name": "Tiki",
        "Walking": "hoverboard:false;"
    },
    26: {
        "Name": "Pirate Cove",
        "Walking": "hoverboard:false;"
    },
    27: {
        "Name": "Pirate Tavern",
        "Walking": "hoverboard:false;"
    },
    28: {
        "Name": "Shanty Town",
        "Walking": "hoverboard:false;"
    },
    29: {
        "Name": "Desert Village",
        "Walking": "hoverboard:false;"
    },
    30: {
        "Name": "Fossil Digsite",
        "Walking": "hoverboard:false;"
    },
    31: {
        "Name": "Desert Pyramids",
        "Walking": "hoverboard:false;"
    },
    32: {
        "Name": "Red Desert",
        "Walking": "hoverboard:false;"
    },
    33: {
        "Name": "Wild West",
        "Walking": "hoverboard:false;"
    },
    34: {
        "Name": "Grand Canyons",
        "Walking": "hoverboard:false;"
    },
    35: {
        "Name": "Safari",
        "Walking": "hoverboard:false;"
    },
    36: {
        "Name": "Mountains",
        "Walking": "hoverboard:false;"
    },
    37: {
        "Name": "Snow Village",
        "Walking": "hoverboard:false;"
    },
    38: {
        "Name": "Icy Peaks",
        "Walking": "hoverboard:false;"
    },
    39: {
        "Name": "Ice Rink",
        "Walking": "hoverboard:false;"
    },
    40: {
        "Name": "Ski Town",
        "Walking": "hoverboard:false;"
    },
    41: {
        "Name": "Hot Springs",
        "Walking": "hoverboard:false;"
    },
    42: {
        "Name": "Fire and Ice",
        "Walking": "hoverboard:false;"
    },
    43: {
        "Name": "Volcano",
        "Walking": "hoverboard:false;"
    },
    44: {
        "Name": "Obsidian Cave",
        "Walking": "hoverboard:false;"
    },
    45: {
        "Name": "Lava Forest",
        "Walking": "hoverboard:false;"
    },
    46: {
        "Name": "Underworld",
        "Walking": "hoverboard:false;"
    },
    47: {
        "Name": "Underworld Bridge",
        "Walking": "hoverboard:false;"
    },
    48: {
        "Name": "Underworld Castle",
        "Walking": "hoverboard:false;"
    },
    49: {
        "Name": "Metal Dojo",
        "Walking": "hoverboard:false;"
    },
    50: {
        "Name": "Fire Dojo",
        "Walking": "hoverboard:false;"
    },
    51: {
        "Name": "Samurai Village",
        "Walking": "hoverboard:false;"
    },
    52: {
        "Name": "Bamboo Forest",
        "Walking": "hoverboard:false;"
    },
    53: {
        "Name": "Zen Garden",
        "Walking": "hoverboard:false;"
    },
    54: {
        "Name": "Flower Field",
        "Walking": "hoverboard:false;"
    },
    55: {
        "Name": "Fairytale Meadows",
        "Walking": "hoverboard:false;"
    },
    56: {
        "Name": "Fairytale Castle",
        "Walking": "hoverboard:false;"
    },
    57: {
        "Name": "Royal Kingdom",
        "Walking": "hoverboard:false;"
    },
    58: {
        "Name": "Fairy Castle",
        "Walking": "hoverboard:false;"
    },
    59: {
        "Name": "Cozy Village",
        "Walking": "hoverboard:false;"
    },
    60: {
        "Name": "Rainbow River",
        "Walking": "hoverboard:false;"
    },
    61: {
        "Name": "Colorful Mines",
        "Walking": "hoverboard:false;"
    },
    62: {
        "Name": "Colorful Mountains",
        "Walking": "hoverboard:false;"
    },
    63: {
        "Name": "Frost Mountains",
        "Walking": "hoverboard:false;"
    },
    64: {
        "Name": "Ice Sculptures",
        "Walking": "hoverboard:false;"
    },
    65: {
        "Name": "Snowman Town",
        "Walking": "hoverboard:false;"
    },
    66: {
        "Name": "Ice Castle",
        "Walking": "hoverboard:false;"
    },
    67: {
        "Name": "Polar Express",
        "Walking": "hoverboard:false;"
    },
    68: {
        "Name": "Firefly Cold Forest",
        "Walking": "hoverboard:false;"
    },
    69: {
        "Name": "Golden Road",
        "Walking": "hoverboard:false;"
    },
    70: {
        "Name": "No Path Forest",
        "Walking": "hoverboard:false;"
    },
    71: {
        "Name": "Ancient Ruins",
        "Walking": "hoverboard:false;"
    },
    72: {
        "Name": "Runic Altar",
        "Walking": "hoverboard:false;"
    },
    73: {
        "Name": "Wizard Tower",
        "Walking": "hoverboard:false;"
    },
    74: {
        "Name": "Witch Marsh",
        "Walking": "hoverboard:false;"
    },
    75: {
        "Name": "Haunted Forest",
        "Walking": "hoverboard:false;"
    },
    76: {
        "Name": "Haunted Graveyard",
        "Walking": "hoverboard:false;"
    },
    77: {
        "Name": "Haunted Mansion",
        "Walking": "hoverboard:false;"
    },
    78: {
        "Name": "Dungeon Entrance",
        "Walking": "hoverboard:false;"
    },
    79: {
        "Name": "Dungeon",
        "Walking": "hoverboard:false;"
    },
    80: {
        "Name": "Treasure Dungeon",
        "Walking": "hoverboard:false;"
    },
    81: {
        "Name": "Empyrean Dungeon",
        "Walking": "hoverboard:false;"
    },
    82: {
        "Name": "Mythic Dungeon",
        "Walking": "hoverboard:false;"
    },
    83: {
        "Name": "Cotton Candy Forest",
        "Walking": "hoverboard:false;"
    },
    84: {
        "Name": "Gummy Forest",
        "Walking": "hoverboard:false;"
    },
    85: {
        "Name": "Chocolate Waterfall",
        "Walking": "hoverboard:false;"
    },
    86: {
        "Name": "Sweets",
        "Walking": "hoverboard:false;"
    },
    87: {
        "Name": "Toys and Blocks",
        "Walking": "hoverboard:false;"
    },
    88: {
        "Name": "Carnival",
        "Walking": "hoverboard:false;"
    },
    89: {
        "Name": "Theme Park",
        "Walking": "hoverboard:false;"
    },
    90: {
        "Name": "Clouds",
        "Walking": "hoverboard:false;"
    },
    91: {
        "Name": "Cloud Garden",
        "Walking": "hoverboard:false;"
    },
    92: {
        "Name": "Cloud Forest",
        "Walking": "hoverboard:false;"
    },
    93: {
        "Name": "Cloud Houses",
        "Walking": "hoverboard:false;"
    },
    94: {
        "Name": "Cloud Palace",
        "Walking": "hoverboard:false;"
    },
    95: {
        "Name": "Heaven Gates",
        "Walking": "hoverboard:false;"
    },
    96: {
        "Name": "Heaven",
        "Walking": "hoverboard:false;"
    },
    97: {
        "Name": "Heaven Golden Castle",
        "Walking": "hoverboard:false;"
    },
    98: {
        "Name": "Colorful Clouds",
        "Walking": "hoverboard:false;"
    },
    99: {
        "Name": "Rainbow Road",
        "Walking": "hoverboard:false;"
    },

    # Tech World
    100: {
        "Name": "Tech Spawn",
        "Walking": "hoverboard:false;"
    },
    101: {
        "Name": "Futuristic City",
        "Walking": "hoverboard:false;"
    },
    102: {
        "Name": "Hologram Forest",
        "Walking": "hoverboard:false;"
    },
    103: {
        "Name": "Robot Farm",
        "Walking": "hoverboard:false;"
    },
    104: {
        "Name": "Bit Stream",
        "Walking": "hoverboard:false;"
    },
    105: {
        "Name": "Neon Mine",
        "Walking": "hoverboard:false;"
    },
    106: {
        "Name": "Mushroom Lab",
        "Walking": "hoverboard:false;"
    },
    107: {
        "Name": "Virtual Garden",
        "Walking": "hoverboard:false;"
    },
    108: {
        "Name": "Data Tree Farm",
        "Walking": "hoverboard:false;"
    },
    109: {
        "Name": "Tech Jungle",
        "Walking": "hoverboard:false;"
    },
    110: {
        "Name": "Lava Jungle",
        "Walking": "hoverboard:false;"
    },
    111: {
        "Name": "Oasis Ruins",
        "Walking": "hoverboard:false;"
    },
    112: {
        "Name": "Future Beach",
        "Walking": "hoverboard:false;"
    },
    113: {
        "Name": "Tech Reef",
        "Walking": "hoverboard:false;"
    },
    114: {
        "Name": "Robo Pirates",
        "Walking": "hoverboard:false;"
    },
    115: {
        "Name": "Cyber Cove",
        "Walking": "hoverboard:false;"
    },
    116: {
        "Name": "Ruinic Desert",
        "Walking": "hoverboard:false;"
    },
    117: {
        "Name": "Charged Pyramids",
        "Walking": "hoverboard:false;"
    },
    118: {
        "Name": "Fallout Desert",
        "Walking": "hoverboard:false;"
    },
    119: {
        "Name": "Tech Wild West",
        "Walking": "hoverboard:false;"
    },
    120: {
        "Name": "Cuboid Canyon",
        "Walking": "hoverboard:false;"
    },
    121: {
        "Name": "Frozen Mountains",
        "Walking": "hoverboard:false;"
    },
    122: {
        "Name": "Frostbyte Forest",
        "Walking": "hoverboard:false;"
    },
    123: {
        "Name": "Forcefield Mine",
        "Walking": "hoverboard:false;"
    },
    124: {
        "Name": "Cyber Base Camp",
        "Walking": "hoverboard:false;"
    },
    125: {
        "Name": "Frosted City",
        "Walking": "hoverboard:false;"
    },
    126: {
        "Name": "Cracked Iceberg",
        "Walking": "hoverboard:false;"
    },
    127: {
        "Name": "Melted River",
        "Walking": "hoverboard:false;"
    },
    128: {
        "Name": "Nexus",
        "Walking": "hoverboard:false;"
    },
    129: {
        "Name": "Secure Coast",
        "Walking": "hoverboard:false;"
    },
    130: {
        "Name": "Nuclear Forest",
        "Walking": "hoverboard:false;"
    },
    131: {
        "Name": "Radiation Mine",
        "Walking": "hoverboard:false;"
    },
    132: {
        "Name": "Exploded Reactor",
        "Walking": "hoverboard:false;"
    },
    133: {
        "Name": "Spaceship Dock",
        "Walking": "hoverboard:false;"
    },
    134: {
        "Name": "Rocky Planet",
        "Walking": "hoverboard:false;"
    },
    135: {
        "Name": "Lunar Planet",
        "Walking": "hoverboard:false;"
    },
    136: {
        "Name": "Mars Planet",
        "Walking": "hoverboard:false;"
    },
    137: {
        "Name": "Saturn Planet",
        "Walking": "hoverboard:false;"
    },
    138: {
        "Name": "Comet Planet",
        "Walking": "hoverboard:false;"
    },
    139: {
        "Name": "Galaxy Port",
        "Walking": "hoverboard:false;"
    },
    140: {
        "Name": "Electric Garden",
        "Walking": "hoverboard:false;"
    },
    141: {
        "Name": "Mutated Forest",
        "Walking": "hoverboard:false;"
    },
    142: {
        "Name": "Neon City",
        "Walking": "hoverboard:false;"
    },
    143: {
        "Name": "Arcade Town",
        "Walking": "hoverboard:false;"
    },
    144: {
        "Name": "Robot Factory",
        "Walking": "hoverboard:false;"
    },
    145: {
        "Name": "Egg Incubator",
        "Walking": "hoverboard:false;"
    },
    146: {
        "Name": "Hi-Tech Hive",
        "Walking": "hoverboard:false;"
    },
    147: {
        "Name": "Spore Garden",
        "Walking": "hoverboard:false;"
    },
    148: {
        "Name": "UFO Forest",
        "Walking": "hoverboard:false;"
    },
    149: {
        "Name": "Alien Lab",
        "Walking": "hoverboard:false;"
    },
    150: {
        "Name": "Alien Mothership",
        "Walking": "hoverboard:false;"
    },
    151: {
        "Name": "Space Forge",
        "Walking": "hoverboard:false;"
    },
    152: {
        "Name": "Space Factory",
        "Walking": "hoverboard:false;"
    },
    153: {
        "Name": "Space Junkyard",
        "Walking": "hoverboard:false;"
    },
    154: {
        "Name": "Steampunk Alley",
        "Walking": "hoverboard:false;"
    },
    155: {
        "Name": "Steampunk Town",
        "Walking": "hoverboard:false;"
    },
    156: {
        "Name": "Steampunk Clockwork",
        "Walking": "hoverboard:false;"
    },
    157: {
        "Name": "Steampunk Airship",
        "Walking": "hoverboard:false;"
    },
    158: {
        "Name": "Circuit Board",
        "Walking": "hoverboard:false;"
    },
    159: {
        "Name": "Mothership Circuit Board",
        "Walking": "hoverboard:false;"
    },
    160: {
        "Name": "Wizard Ruins",
        "Walking": "hoverboard:false;"
    },
    161: {
        "Name": "Wizard Forest",
        "Walking": "hoverboard:false;"
    },
    162: {
        "Name": "Wizard Tech Forest",
        "Walking": "hoverboard:false;"
    },
    163: {
        "Name": "Wizard Tech Tower",
        "Walking": "hoverboard:false;"
    },
    164: {
        "Name": "Wizard Dungeon",
        "Walking": "hoverboard:false;"
    },
    165: {
        "Name": "Cyberpunk Undercity",
        "Walking": "hoverboard:false;"
    },
    166: {
        "Name": "Cyberpunk Industrial",
        "Walking": "hoverboard:false;"
    },
    167: {
        "Name": "Cyberpunk City",
        "Walking": "hoverboard:false;"
    },
    168: {
        "Name": "Cyberpunk Road",
        "Walking": "hoverboard:false;"
    },
    169: {
        "Name": "Tech Ninja Kyoto",
        "Walking": "hoverboard:false;"
    },
    170: {
        "Name": "Tech Samurai",
        "Walking": "hoverboard:false;"
    },
    171: {
        "Name": "Tech Ninja Village",
        "Walking": "hoverboard:false;"
    },
    172: {
        "Name": "Tech Ninja City",
        "Walking": "hoverboard:false;"
    },
    173: {
        "Name": "Dominus Dungeon",
        "Walking": "hoverboard:false;"
    },
    174: {
        "Name": "Dominus Vault",
        "Walking": "hoverboard:false;"
    },
    175: {
        "Name": "Dominus Lair",
        "Walking": "hoverboard:false;"
    },
    176: {
        "Name": "Holographic Powerplant",
        "Walking": "hoverboard:false;"
    },
    177: {
        "Name": "Holographic City",
        "Walking": "hoverboard:false;"
    },
    178: {
        "Name": "Holographic Forest",
        "Walking": "hoverboard:false;"
    },
    179: {
        "Name": "Holographic Mine",
        "Walking": "hoverboard:false;"
    },
    180: {
        "Name": "Dark Tech Cove",
        "Walking": "hoverboard:false;"
    },
    181: {
        "Name": "Dark Tech Ruins",
        "Walking": "hoverboard:false;"
    },
    182: {
        "Name": "Dark Tech Castle",
        "Walking": "hoverboard:false;"
    },
    183: {
        "Name": "Dark Tech Dungeon",
        "Walking": "hoverboard:false;"
    },
    184: {
        "Name": "Dark Tech Forest",
        "Walking": "hoverboard:false;"
    },
    185: {
        "Name": "Hacker Powerplant",
        "Walking": "hoverboard:false;"
    },
    186: {
        "Name": "Hacker Compound",
        "Walking": "hoverboard:false;"
    },
    187: {
        "Name": "Hacker Base",
        "Walking": "hoverboard:false;"
    },
    188: {
        "Name": "Hacker Error",
        "Walking": "hoverboard:false;"
    },
    189: {
        "Name": "Glitch Forest",
        "Walking": "hoverboard:false;"
    },
    190: {
        "Name": "Glitch City",
        "Walking": "hoverboard:false;"
    },
    191: {
        "Name": "Glitch Skyscrapers",
        "Walking": "hoverboard:false;"
    },
    192: {
        "Name": "Glitch Town",
        "Walking": "hoverboard:false;"
    },
    193: {
        "Name": "Glitch Quantum",
        "Walking": "hoverboard:false;"
    },
    194: {
        "Name": "Quantum Forest",
        "Walking": "hoverboard:false;"
    },
    195: {
        "Name": "Quantum Space Base",
        "Walking": "hoverboard:false;"
    },
    196: {
        "Name": "Quantum Galaxy",
        "Walking": "hoverboard:false;"
    },
    197: {
        "Name": "Void Atomic",
        "Walking": "hoverboard:false;"
    },
    198: {
        "Name": "Void Fracture",
        "Walking": "hoverboard:false;"
    },
    199: {
        "Name": "Void Spiral",
        "Walking": "hoverboard:false;"
    },
     200: {
        "Name": "Prison Tower",
        "Walking": "hoverboard:false;"
    },

    # Void World
    201: {
        "Name": "Prison Block",
        "Walking": "hoverboard:false;"
    },
    202: {
        "Name": "Prison Cafeteria",
        "Walking": "hoverboard:false;"
    },
    203: {
        "Name": "Prison Yard",
        "Walking": "hoverboard:false;"
    },
    204: {
        "Name": "Prison HQ",
        "Walking": "hoverboard:false;"
    },
    205: {
        "Name": "Beach Island",
        "Walking": "hoverboard:false;"
    },
    206: {
        "Name": "Ocean Island",
        "Walking": "hoverboard:false;"
    },
    207: {
        "Name": "Tiki Island",
        "Walking": "hoverboard:false;"
    },
    208: {
        "Name": "Jungle Island",
        "Walking": "hoverboard:false;"
    },
    209: {
        "Name": "Volcano Island",
        "Walking": "hoverboard:false;"
    },
    210: {
        "Name": "Hacker Matrix",
        "Walking": "hoverboard:false;"
    },
    211: {
        "Name": "Hacker Fortress",
        "Walking": "hoverboard:false;"
    },
    212: {
        "Name": "Hacker Cave",
        "Walking": "hoverboard:false;"
    },
    213: {
        "Name": "Hacker Lab",
        "Walking": "hoverboard:false;"
    },
    214: {
        "Name": "Hacker Mainframe",
        "Walking": "hoverboard:false;"
    },
    215: {
        "Name": "Dirt Village",
        "Walking": "hoverboard:false;"
    },
    216: {
        "Name": "Stone Forts",
        "Walking": "hoverboard:false;"
    },
    217: {
        "Name": "Silver City",
        "Walking": "hoverboard:false;"
    },
    218: {
        "Name": "Golden Metropolis",
        "Walking": "hoverboard:false;"
    },
    219: {
        "Name": "Diamond Mega City",
        "Walking": "hoverboard:false;"
    }
}

class TPBase(Base):
    def GetZoneByName(self, name: str):
        for zone in ZoneList:
            if ZoneList[zone]["Name"] == name:
                return ZoneList[zone], zone
            
        return None

    def TeleportToZone(self, name: str | int, walkToZone = False):
        while Timer(Config.TELEPORT_TIMES):
            zone = None
            zoneIndex = 0
            if type(zone) == "str":
                zone, zoneIndex = self.GetZoneByName(name)
            else:
                zone, zoneIndex = ZoneList[name], name

            if zone == None:
                Config.log_critical("Zone '" + str(name) + "' doesn't exist.")
                return False
            
            Config.log("Teleporting to '" + str(name) + "'...")
            Discord.SendWebhook(Config.EMBEDS["TeleportingTo"](name))

            ClickSearchBar(self.Open)
            Controls.Type(zone.Name)

            pos_btn = None
            while pos_btn == None:
                pos_btn = Images.GetPosition("buttons/tp/best_area", 0.68)
                time.sleep(0.5)

            Controls.Click(pos_btn, False)
            
            btnFound = False
            x, y = pyautogui.position()
            y = y - 5
            while btnFound == False:
                Controls.ClickXY(x + 10, y, False)
                x = x + 10

                color = ConvertUtil.ColorToAverageColorString(ConvertUtil.ScreenPositionToAverageColor(x, y))
                if color == "green":
                    btnFound = True
                    break
                elif color == "blue":
                    if zoneIndex > 1:
                        self.TeleportToZone(zoneIndex - 1) # Go Back
                    else:
                        self.TeleportToZone(zoneIndex + 1) # Go Forwards
                    
                    self.TeleportToZone(zoneIndex) # TP afterwards
                    break
                time.sleep(0.5)
            
            time.sleep(Config.TP_WAIT_TIME)
            if walkToZone:
                Macro.Run(zone["Walking"])

            Config.log("Successfully teleported to '" + str(name) + "'!")
            Discord.SendWebhook(Config.EMBEDS["TeleportedTo"](name), ss=True)

        return True
    
    def ResetCharacter(self): # "resets" the character to spawn
        self.TeleportToZone(1)

UI = TPBase("TP", "buttons/tp/btn", "titles/tp")

def ResetCharacter():
    UI.TeleportToZone(1)