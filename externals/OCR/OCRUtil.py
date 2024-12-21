#
# OCRUtil.py made by upio
#
# OCRUtil.py is a python module that allows you to use OCR on images using Microsoft's TrOCR model or pytesseract.
# It also allows you to use the Microsoft model on linux using WSL.
#
# USAGE:
# from OCRUtil import OCRUtil, Model
# print(OCRUtil.OCR("ocr/ss.png", model=Model.MICROSOFT))  # returns text
# print(OCRUtil.OCR("ocr/ss.png", model=Model.PYTESSERACT))  # returns text and image
#
# You can also use the WSL version of the Microsoft model by passing wsl=True to the OCRUtil constructor.
# This will start a WSL instance and a flask server that will run the model.
# This is much faster than the non-WSL version, but it requires you to have WSL installed.
# If you don't have WSL installed, you can install it by following this guide: https://docs.microsoft.com/en-us/windows/wsl/install-win10
# If you don't want to install WSL, you can use the non-WSL version of the Microsoft model.
#
# USAGE:
# from OCRUtil import OCRUtil, Model
# ocr = OCRUtil(wsl=True)
# print(ocr.OCR("ocr/ss.png", model=Model.MICROSOFT))  # returns text
# print(ocr.OCR("ocr/ss.png", model=Model.PYTESSERACT))  # returns text and image

from threading import Thread
from typing import Union
from enum import Enum
from PIL import Image
import pytesseract
import subprocess
import requests
import time
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\tesseract.exe'

class WSL:
    def __init__(self):
        pass

    def file_exists(self,file_path: str):
        cmd = f'wsl test -f {file_path} && echo exists || echo not exists'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Error while running WSL commands\n{stderr.decode()}")
        else:
            return stdout.decode().strip() == 'exists'
    
    def run_cmd(self, cmd: str, wait: bool = False, noconsole: bool = True):
        def wrapper():
            wsl_cmd = f"wsl {cmd}"
            if noconsole:
                subprocess.run(wsl_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.run(wsl_cmd, shell=True)

        if wait:
            wrapper()
        else:
            Thread(target=wrapper).start()

    def get_file_path_from_windows_path(self,windows_path: str):
        return "/mnt/" + windows_path[0].lower() + windows_path[2:].replace("\\", "/")

class Model(Enum):
    MICROSOFT = "microsoft/trocr-large-printed"
    HUGGINGFACE_MSAPI = "microsoft/trocr-large-printed (huggingface api)"
    PYTESSERACT = "pytesseract"

class OCRUtil:
    def __init__(self,wsl={"enabled": False,"keep_alive": False},logging=False):
        self.wsl = wsl.get("enabled", False)
        self.wsl_dict = wsl
        self.logging = logging

        self.WSLInstance = WSL()
        
        self.msModel = None
        self.msProcessor = None

    def log(self,message: str):
        if self.logging:
            print(message)

    def OCR(self,image_path: str, model: Union[str, Model], **kwargs) -> str:
        """
        This function takes an image path, a model name, and additional optional arguments as input.
        Returns the text that it detects in the image, may be inaccurate.

        For faster results using the microsoft model, use linux.
        """
        model = model.value if isinstance(model, Model) else model

        if model == Model.MICROSOFT.value:
            if self.wsl:
                self.log("[INFO]: Using Microsoft model with WSL. Starting WSL Ubuntu")
                
                self.log("[INFO]: Running WSL commands")

                was_running = False
                if self.wsl_dict.get("keep_alive", False):
                    response = requests.get("http://localhost:5000") # just to check if the server is running
                    if response.status_code == 200:
                        self.log("[INFO]: Server is already running, not starting it again")
                        was_running = True
                
                if not was_running:
                    script_directory = os.path.dirname(os.path.abspath(__file__))
                    wsl_server_path = self.WSLInstance.get_file_path_from_windows_path(os.path.join(script_directory, "wslServer.py"))
                    
                    self.WSLInstance.run_cmd(f'python3 "{wsl_server_path}"',noconsole=self.logging)
                    self.log(f"[INFO]: WSL server started at {wsl_server_path}, waiting for it to start...")

                    while True:
                        time.sleep(0.25)
                        try:
                            r = requests.get("http://localhost:5000")
                            if r.text == "Linux OCR API made by upio" or r.status_code == 200:
                                break
                        except:
                            pass
                
                self.log("[INFO]: WSL server started, passing image to it...")

                response = requests.post("http://localhost:5000/ocr", files={"image": open(image_path, "rb")})
                self.log("[INFO]: Image passed to WSL server, cleaning up server...")

                if not self.wsl_dict.get("keep_alive", False):
                    self.log("[INFO]: keep_alive is False, stopping WSL server...")
                    try:
                        requests.post("http://localhost:5000/stop") # just does exit() so it's fine
                    except Exception as e:
                        self.log("[INFO]: Server cleaned up, returning text...")
                else:
                    self.log("[INFO]: keep_alive is True, not stopping WSL server...")
                
                return response.json()["text"]
            else:
                from transformers import TrOCRProcessor, VisionEncoderDecoderModel

                if self.msProcessor is None:
                    self.log("[INFO]: Initializing Microsoft processor...")
                    self.msProcessor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-printed')
                    self.log("[INFO]: Microsoft processor initialized")

                if self.msModel is None:
                    self.log("[INFO]: Initializing Microsoft model...")
                    self.msModel = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-printed')
                    self.log("[INFO]: Microsoft model initialized")
                
                self.log("[INFO]: Opening image...")
                image = Image.open(image_path)

                self.log("[INFO]: Image opened, passing to Microsoft processor...")
                pixel_values = self.msProcessor(images=image, return_tensors="pt").pixel_values

                self.log("[INFO]: Image passed to Microsoft processor, passing to Microsoft model...")
                generated_ids = self.msModel.generate(pixel_values)

                self.log("[INFO]: Image passed to Microsoft model, decoding...")
                generated_text = self.msProcessor.batch_decode(generated_ids, skip_special_tokens=True)[0]

                self.log("[INFO]: Text decoded, returning...")
                return generated_text
        elif model == Model.PYTESSERACT.value:
            add = ""
            if self.wsl:
                add = ", note that this is not gonna run on WSL"
            self.log("[INFO]: Using pytesseract" + add + "...")

            img = Image.open(image_path).convert("RGB")
            self.log("[INFO]: Image opened, passing to pytesseract with a psm of 8")

            psmLvl = kwargs.get("psm", 8)

            txt = pytesseract.image_to_string(img, config='--psm ' + str(psmLvl), output_type=pytesseract.Output.STRING)
            self.log("[INFO]: Text generated, returning...")

            return txt
        elif model == Model.HUGGINGFACE_MSAPI.value:
            API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-large-printed"
            headers = {"Authorization": "Bearer " + kwargs.get("api_key", "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")}
            
            def query(filename):
                with open(filename, "rb") as f:
                    data = f.read()
                response = requests.post(API_URL, headers=headers, data=data)
                return response.json()
            
            return query(image_path)
        else:
            raise ValueError("Invalid model name")

    def shutdown_wsl(self):
        if self.wsl:
            self.log("[INFO]: Stopping WSL server...")
            try:
                requests.post("http://localhost:5000/stop") # just does exit() so it's fine
            except Exception as e:
                self.log("[INFO]: Server stopped")
            
            return True
        else:
            return False