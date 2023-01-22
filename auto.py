import os
import time
try:
    import threading
    import subprocess
    import base64
    import cv2
    import random
    import numpy as np
    import requests
except:
    os.system("pip install requests")
    os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
    os.system("pip install numpy")
import threading
import subprocess
import base64
import cv2
import random
import numpy as np
import requests
from datetime import datetime
import sys

os.system("cls")
print("Tool AutoPvP Eldorado By XuanBachDotDev")
print("Facebook: XuanBachDotDev")


def GetDevices():
    devices = subprocess.check_output("adb devices")
    p = str(devices).replace("b'List of devices attached", "").replace('\\r\\n', "").replace(" ", "").replace(
        "'", "").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached', "")
    if len(p) > 0:
        listDevices = p.split("\\tdevice")
        listDevices.pop()
        print("Device is running: " + listDevices[0])
        return listDevices[0]
    else:
        return 0


class ADB:
    def __init__(self, handle):
        self.handle = handle

    def screen_capture(self, name):
        os.system(
            f"adb -s {self.handle} exec-out screencap -p > {name}_temp.png ")

    def click(self, x, y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")

    def clickByPercent(self, xPercent, yPercent):
        displaySize = subprocess.check_output(
            f"adb -s {self.handle} shell wm size")
        p = str(displaySize).replace("b'List of devices attached", "").replace('\\r\\n', "").replace(" ", "").replace(
            "'", "").replace('bPhysicalsize:', "")
        temp = p.split("x")
        x_temp = int(temp[0])/100
        y_temp = int(temp[1])/100
        x = float(x_temp * xPercent)
        y = float(y_temp * yPercent)
        # print(x, y)
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")

    def sendKey(self, keyCode):
        os.system(f"adb -s {self.handle} shell input keyevent {keyCode}")

    def find(self, img='', template_pic_name=False, threshold=0.99):
        if template_pic_name == False:
            self.screen_capture(self.handle)
            template_pic_name = self.handle+'_temp.png'
        else:
            self.screen_capture(template_pic_name)
        img = cv2.imread(img)
        img2 = cv2.imread(template_pic_name)
        result = cv2.matchTemplate(img, img2, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        test_data = list(zip(*loc[::-1]))
        return test_data


class AutoPvP:
    def startbutton(d):
        while True:
            try:
                startbtn = d.find('img/startbtn.png')
                if startbtn > [(0, 0)]:
                    d.click(startbtn[0][0], startbtn[0][1])
                    startbtn(d)
                    break
            except:
                return 0

    def charspamclick(d):
        i = 1
        while i < 2:
            try:
                inGameDetect_1 = d.find('img/inGameDetectImage.png')
                if inGameDetect_1 > [(0, 0)]:
                    d.sendKey(8)
                    d.sendKey(9)
                    d.clickByPercent(23.1, 5.3)
                    d.clickByPercent(8.4, 90.5)
                    inGameDetect_2 = d.find('img/inGameDetectImage.png')
                    if inGameDetect_2 > [(0, 0)] != [] != [0] != [(0, 0)]:
                        i = 1
                    else:
                        i += 1
                        break
                else:
                    i = 1
            except:
                return 0

    def okbutton(d):
        while True:
            try:
                okbtn = d.find('img/okbtn.png')
                macrobtn = d.find('img/macroDetectImage.png')
                networkerr = d.find('img/networkErrorDetect.png')
                if networkerr > [(0, 0)]:
                    print("Network Error")
                    sys.exit()
                    # d.click(networkerrokbtn[0][0], networkerrokbtn[0][1])
                elif okbtn > [(0, 0)]:
                    if macrobtn > [(0, 0)]:
                        d.click(macrobtn[0][0], macrobtn[0][1])
                        print("Macro Detect Solved!")
                        time.sleep(0.5)
                        d.click(okbtn[0][0], okbtn[0][1])
                    else:
                        d.click(okbtn[0][0], okbtn[0][1])
                        okbtn(d)
                    break
            except:
                return 0


def main(id):
    log_file = "log.txt"
    i = int(0)
    device = ADB(GetDevices())
    point_res = requests.get(
        f'http://211.253.26.47:8092/ELDORADO_M/PvP/get_rank50_from_server_pvp.php?dbName=&HOST_ID={id}')
    x = point_res.text.split(",")
    y = len(x)
    temp_point = int(x[y - 2])
    while True:
        AutoPvP.startbutton(device)
        time.sleep(5.5)
        AutoPvP.charspamclick(device)
        AutoPvP.okbutton(device)
        i += int(1)
        point_res = requests.get(
            f'http://211.253.26.47:8092/ELDORADO_M/PvP/get_rank50_from_server_pvp.php?dbName=&HOST_ID={id}')
        x = point_res.text.split(",")
        y = len(x)
        point = int(x[y - 2])
        putPoint = point - temp_point
        result = ""
        timenow = datetime.now().strftime('%Y-%m-%d : %H:%M:%S')
        if putPoint < 60:
            result = "Lose"
        elif putPoint > 60:
            result = "Win "
        print(
            f"Run: {i} time | Point: {point} | Result: {result} | ID: {id} | Time: {timenow}")
        # temp_log = f"Point: {point} | Result: {result} | ID: {id} | Time: {timenow}\n"
        # with open(log_file, 'w', encoding='utf-8') as my_file:
        #     my_file.write(temp_log + '\n')
        temp_point = point


id_file = open("ID.txt", "r")

main(id_file.readlines()[0])
