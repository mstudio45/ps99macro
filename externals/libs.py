import os, sys
def GetMainDir(): # this should not fail
    current_dir = os.getcwd()
    while True:
        if all(filename in os.listdir(current_dir) for filename in ["config.py", "ui.py"]):
            break
        current_dir = os.path.dirname(current_dir)
    return current_dir
sys.path.append(GetMainDir())

import time, ctypes, random, re
import datetime
import subprocess
import psutil
import pyautogui, pydirectinput
import win32api, win32gui, win32con, getpixelcolor
import mss.tools as msstools
from win32con import *
from discord_webhook import DiscordWebhook, DiscordEmbed
from mss import mss
from contextlib import contextmanager

from externals.OCR.OCRUtil import OCRUtil, Model

import config as Config
import pyautoit as autoit

# main functions #
def PauseCheck():
    if Config.PAUSED == True:
        while Config.PAUSED:
            time.sleep(0.1)

# Classes
if os.name == 'nt':
    class WindowsInhibitor:
        '''
            Prevent OS sleep/hibernate in windows; code from:
                https://github.com/h3llrais3r/Deluge-PreventSuspendPlus/blob/master/preventsuspendplus/core.py
            API documentation:
                https://msdn.microsoft.com/en-us/library/windows/desktop/aa373208(v=vs.85).aspx
        '''
        ES_CONTINUOUS = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001

        def __init__(self):
            pass

        def inhibit(self):
            ctypes.windll.kernel32.SetThreadExecutionState(
                WindowsInhibitor.ES_CONTINUOUS | \
                WindowsInhibitor.ES_SYSTEM_REQUIRED)
            Config.log("Keep alive on!")

        def uninhibit(self):
            ctypes.windll.kernel32.SetThreadExecutionState(
                WindowsInhibitor.ES_CONTINUOUS)
            Config.log("Keep alive off!")
else:
    class WindowsInhibitor:
        def __init__(self):
            pass
        def inhibit(self):
            pass
        def uninhibit(self):
            pass

class ConvertUtil:
    def __init__(self):
        self.multipliers = { 
            'k': 1e3,      
            'm': 1e6,
            'b': 1e9,

            'K': 1e3,      
            'M': 1e6,
            'B': 1e9,
        }

    def ToFloat(self, input):
        pattern = r'([0-9.]+)([bkmBKM])'

        n = 0
        s = False
        try:
            for number, suffix in re.findall(pattern, input):
                number = float(number)
                n = (number * self.multipliers[suffix])
            if n == 0:
                input = input.replace(",", "").replace(".", "")
                n = float(input)
            s = True
        except Exception as e:
            Config.log_critical("Failed to convert '" + str(input) + "' to float: " + str(e))
            s = False
        return n, s
    
    def DeltaToStr(dlt: datetime.timedelta) -> str:
        minutes, seconds = divmod(int(dlt.total_seconds()), 60)
        return f"{minutes}:{seconds:02}"

    def ScreenPositionToAverageColor(self, x, y):
        return getpixelcolor.average(x, y, 15, 15)

    def ColorToAverageColorString(self, color):
        r, g, b = color
        
        if r < 50 and g < 50 and b < 50:
            return "black"
        elif r > 205 and g > 205 and b > 205:
            return "white"
        elif g < r / 2 and b < r / 2:
            return "red"
        elif r < g / 2 and b < g / 2:
            return "green"
        elif r < b / 2 and g < b / 2:
            return "blue"
        
        return "unknown"

class OCR:
    def __init__(self):
        self.ocr = OCRUtil(wsl={"enabled": Config.USE_WSL, "keep_alive": Config.USE_WSL})
        self.ocr.logging = False
        pass

    def Shutdown(self):
        self.ocr.shutdown_wsl()

    def ReadTextFromImage(self, filename):
        if not os.path.exists(filename):
            return False, ""
        
        text = ""
        success = False
        try:
            text = self.ocr.OCR(image_path=filename, model=Model.MICROSOFT)
            success = True
        except:
            success = False

        return success, text

# Images
class Screenshots:
    def __init__(self):
        pass
    
    def TakeWholeScreen(self):
        with mss(with_cursor=True) as sct:
            monitor = {"top": 0, "left": 0, "width": pyautogui.size().width, "height": pyautogui.size().height}
            screenshot = sct.grab(monitor)
            return msstools.to_png(screenshot.rgb, screenshot.size)
        
    def Screenshot(self, name = "ss", returnStream = True):
        screenshot = self.TakeWholeScreen()
        filename = f"{Config.SS_LOCATION}/{name}_{random.randint(99999, 999999)}.png"

        f = open(filename, 'wb')
        f.write(screenshot)
        if returnStream == False:
            f.close()

        return returnStream and f or None, filename
    
    def ScreenshotRegion(self, region, name = "ss", returnStream = True):
        filename = f"{Config.SS_LOCATION}/{name}_{random.randint(99999, 999999)}.png"
        pyautogui.screenshot(region=region, imageFilename=filename)

        return returnStream and open(filename, 'wb') or None, filename

class Images:
    def __init__(self):
        pass

    def TempFile(self, filename):
        try:
            yield filename
        finally:
            try:
                os.remove(filename)
            except Exception as e:
                Config.log_warning(f"Failed to remove {filename}: {str(e)}")

    # we only use .pngs but just in case (extension not required)
    def GetPosition(self, filename: str, confidence, grayscale=False, extension = ".png"):
        if filename.startswith("/"):
            filename = filename[1:]
        position = pyautogui.locateOnScreen(Config.IMGS_LOCATION + "/" + filename + extension, grayscale=grayscale, confidence=confidence)
        Config.log_debug(f"Position: {filename} = {position}")
        return position
    
    def GetAllPositions(self, filename: str, confidence, grayscale=False, extension = ".png"):
        if filename.startswith("/"):
            filename = filename[1:]
        positions = pyautogui.locateAllOnScreen(Config.IMGS_LOCATION + "/" + filename + extension, grayscale=grayscale, confidence=confidence)
        Config.log_debug(f"Positions: {filename} = {positions}")
        return positions

# Main ones
class Controls:
    def __init__(self):
        pass

    # Helpers
    def GetCenterPosition():
        return int(ctypes.windll.user32.GetSystemMetrics(0) / 2), int(ctypes.windll.user32.GetSystemMetrics(1) / 2)

    # Mouse Scroll
    def Scroll(self, s = 100, type = "down"): # type = up, down, left, right
        PauseCheck()

        x, y = autoit.mouse_get_pos()
        type = type.lower()

        if type == "down" or type == "left":
            s = s * -1
        win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, s, 0)
    
    # Mouse Click and Movement
    def GoToCenter(self):
        PauseCheck()
        autoit.mouse_move(self.GetCenterPosition())
    
    def GoToCorner(self):
        PauseCheck()
        autoit.mouse_move(0, 0)

    def Click(self, position, click = True, button = "left"): # button = left, right
        PauseCheck()

        x, y = pyautogui.center(position)
        if click:
            autoit.mouse_click(button, x, y, clicks=1)
        else:
            autoit.mouse_move(x, y)
            
    def ClickXY(self, x, y, click = True, button = "left"):
        self.Click(pyautogui.position(x, y), click, button)

    def ClickCenter(self, button = "left"):
        self.Click(pyautogui.position(self.GetCenterPosition()), True, button)
        
    # Keyboard
    def KeyDown(self, key):
        for i in range(2):
            pydirectinput.keyDown(key)

    def KeyUp(self, key):
        for i in range(2):
            pydirectinput.keyUp(key)

    def HoldKey(self, key, hold_time):
        PauseCheck()

        self.KeyDown(key)

        start = time.time()
        while time.time() - start < hold_time:
            if Config.PAUSED == True:
                while Config.PAUSED:
                    hold_time = hold_time + .1
                    time.sleep(.1)

            pydirectinput.keyDown(key)

        self.KeyUp(key)

    def PressKey(self, key):
        PauseCheck()

        self.KeyDown(key)
        self.KeyUp(key)

    def Type(self, word):
        PauseCheck()

        for l in [*word]:
            self.PressKey(l)
            time.sleep(0.00005)

def FocusEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        windowText = win32gui.GetWindowText(hwnd)
        # windowHex = hex(hwnd)
        if windowText == "Roblox":
            #win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

class Roblox:
    def __init__(self):
        self.PlaceID = 8737899170
        self.ImagesLib = Images()
        self.Discord = Discord()
        pass

    # Helpers
    def KillRoblox(self):
        subprocess.call("TASKKILL /F /IM RobloxPlayerBeta.exe", shell=True)

    def FocusRoblox(self):
        win32gui.EnumWindows(FocusEnumHandler, None)

    def GetProcessList(self):
        PList = list()
        for process in psutil.process_iter():
            PList.append(process.name())

        return PList

    def CreateLaunchProtocol(self, placeId=None, jobId=None, privServerId=None):
        if not placeId:
            return None
        
        protocol = "roblox://placeID=" + str(placeId)
        if jobId and privServerId:
            protocol = protocol + "&linkCode=" + str(privServerId)
        elif jobId and not privServerId:
            protocol = protocol + "&gameInstanceId=" + jobId
        
        return protocol
    
    def LaunchRoblox(self, kill = False):
        protocol = self.CreateLaunchProtocol(self.PlaceID, None, None)
        if Config.VIP == False:
            protocol = self.CreateLaunchProtocol(self.PlaceID, None, Config.VIP)
        
        if kill:    
            self.KillRoblox()
        os.startfile(protocol)
        Controls.GoToCenter()
    
    # Code
    def CheckDisconnection(self): # Returns if roblox was relaunched
        start_time = datetime.datetime.now()
        FirstPList = self.GetProcessList()

        disconnected = self.ImagesLib.GetPosition('/disconnected.png', 0.9)
        if disconnected != None or "RobloxPlayerBeta.exe" not in FirstPList:
            PauseCheck()
            
            attempts = 1
            waiting = True
            waitingTime = 0

            Config.log("Rejoining...")
            self.Discord.SendWebhook(Config.EMBEDS["Rejoining"], content=f"<@{Config.DISCORD_USER_ID}>", ss=True)

            self.LaunchRoblox(True)
            while waiting:
                PauseCheck()
                CurrentPList = self.GetProcessList()
                if "RobloxPlayerBeta.exe" in CurrentPList and "RobloxPlayerLauncher.exe" not in CurrentPList: # Successfully launched!
                    waiting = False
                    break
                
                waitingTime = waitingTime + 5 # loop is each 5 seconds
                if waitingTime >= 30:
                    attempts = attempts + 1
                    Config.log("Rejoining (Attempt #" + str(attempts) + ")...")
                    self.Discord.SendWebhook(Config.EMBEDS["RejoiningAttempt"](attempts), content=f"<@{Config.DISCORD_USER_ID}>", ss=True)

                    self.LaunchRoblox(True)
                    waitingTime = 0
                time.sleep(5)
            
            # Try to find inventory button
            while self.ImagesLib.GetPosition('buttons/inventory.png', 0.85) == None:
                self.FocusRoblox()
                time.sleep(1)

            Config.log("Rejoined!")
            self.Discord.SendWebhook(Config.EMBEDS["Rejoined"], ss=True)
    
            Config.OTHER_TIMES.append(datetime.datetime.now() - start_time)
            return True
        return False

class Discord:
    def __init__(self):
        self.webhook = None
        if Config.DISCORD_WEBHOOK != None:
            self.webhook = DiscordWebhook(url=Config.DISCORD_WEBHOOK, rate_limit_retry=True)

    def SendWebhook(self, embed, content="", ss=False):
        if self.webhook is None:
            return
        
        if ss:
            ssLib = Screenshots()
            f, filename = ssLib.Screenshot()
            while ssLib.TempFile(filename):
                self.webhook.add_file(file=f.read(), filename="ss.png")
                if f.closed == False:
                    f.close()
        try:
            self.webhook.content = content
            embed.set_timestamp()
            embed.set_footer(text=Config.VERSION_)
            self.webhook.add_embed(embed)

            # response = self.webhook.execute(remove_embeds=True)
        except Exception as e:
            Config.log_error(f"Failed to send webhook: {str(e)}")
        finally:
            self.webhook.content = ""
            self.webhook.remove_embeds()
            self.webhook.remove_files()