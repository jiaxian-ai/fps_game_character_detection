import time
import mss, cv2, win32api, os
import os
import numpy as np
from pynput import mouse, keyboard
from threading import Thread
from multiprocessing import Manager
from PIL import ImageGrab
class MouseListener():
    def __init__(self, share_dict):
        self.share_dict = share_dict
        # 截取开关
        self.share_dict['intercept'] = False
        self.share_dict['tag'] = 2
        # 敌我开关
        self.share_dict['defender'] = False

    def on_release(self, key):
        if str(key) == "'f'":
            self.share_dict['intercept']

    def on_press(self, key):
        # 按下空格键截图
        if str(key) == "'f'":
            self.share_dict['intercept'] = True
            print('开始截图')

        elif str(key) == "'`'":
            self.share_dict['defender'] = not self.share_dict['defender']

            if self.share_dict['defender']:
                self.share_dict['tag'] = 1
                print('现在收集"保卫者"')
            else:
                self.share_dict['tag'] = 0
                print('现在收集"潜伏者"')

    def on_release(self, key):
        if str(key) == "'f'":
            self.share_dict['intercept'] = False

    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def start(self):
        t = Thread(target=self.listen)
        t.start()


def screenshot(share_dict):
    os.makedirs('./Game_Data/BW', exist_ok=True)
    os.makedirs('./Game_Data/QF', exist_ok=True)

    # sct = mss.mss()
    # 创建截图对象
    sct = mss.mss()
    # 以中心未单位，向左上角偏移320
    left = int((win32api.GetSystemMetrics(0) / 2) - 320)
    top = int((win32api.GetSystemMetrics(1) / 2) - 320)

    monitor = {'left': left, 'top': top, 'width': 640, 'height': 640}

    while True:
        img = sct.grab(monitor)
        img = np.array(img)
        if share_dict['intercept']:
            if share_dict['tag'] == 0:
                file_name = str(time.time())
                cv2.imwrite('./data/QF/' + str(file_name) + '.jpg', img)
            elif share_dict['tag'] == float(1):
                file_name = str(time.time())
                cv2.imwrite('./data/BW/' + str(file_name) + '.jpg', img)
            share_dict['intercept'] = False
            # cv2.imshow('screenshot img', img)
            cv2.waitKey(1)


if __name__ == '__main__':
    # 创建共享字典
    manager = Manager()
    share_dict = manager.dict()

    # 启动监听
    mouse_listener = MouseListener(share_dict)
    mouse_listener.start()

    screenshot(share_dict)
