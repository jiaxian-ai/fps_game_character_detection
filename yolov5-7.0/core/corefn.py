import mss,cv2,win32api,os,time,win32print,win32con,win32gui
import numpy as np
from pynput import mouse,keyboard
from threading import Thread
#导入共享字典
from multiprocessing import Manager

#创建mss 实例
sct = mss.mss()

def screenshot(left,top):
    #设置截图区域
    monitor = {"left": left,"top": top, "width": 640, "height": 640}
    img = sct.grab(monitor)
    # img = np.array(img)
    img = np.array(img)  # 转换成numpy数组
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # 图片4通道转3通道
    return img


def Dynamic_AttackRange(x1,y1,x2,y2,x,y,img):
    #目标画框
    img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 1)
    #画出原中心点
    img = cv2.circle(img, (round(x), round(y)), 2, (255, 0, 0), 1)
    return img


# if __name__ == "__main__":
#     #创建共享字典
#     manager = Manager()
#     share_dict = manager.dict()
#     #创建鼠标监听对象
#     mouse_listener = MouseListener(share_dict)
#     #启动监听
#     mouse_listener.start()
#     screenshot(share_dict)