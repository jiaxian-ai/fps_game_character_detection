
import math
import threading
import time

import numpy as np
import torch,win32api
from utils.augmentations import letterbox
from models.common import DetectMultiBackend
from utils.general import (cv2, non_max_suppression, scale_boxes, xyxy2xywh)
from utils.plots import Annotator
from utils.torch_utils import select_device, smart_inference_mode
from core.corefn import screenshot,Dynamic_AttackRange
from core.send_input import *

from pynput import mouse
from pynput.mouse import Listener

import mss,cv2,win32api,os,time,win32print,win32con,win32gui

control = mouse.Controller()

weights = 'best.pt'

device = select_device("0")
model = DetectMultiBackend(weights, device=device, dnn=False, data=False, fp16=True)

Detect = 640
# 获取真实的分辨率
ScreenX = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPHORZRES)
ScreenY = win32print.GetDeviceCaps(win32gui.GetDC(0), win32con.DESKTOPVERTRES)
# 以中心为单位，向左上角偏移320
XLeft = int((ScreenX / 2) - (Detect / 2))
YLeft = int((ScreenY / 2) - (Detect / 2))
XRight = XLeft + Detect
YRight = YLeft + Detect
# # 中心点（目标点-中心点使用）
CoreX = ((XRight - XLeft) / 2)
CoreY = ((YRight - YLeft) / 2)
print(ScreenX,ScreenY,XLeft,YLeft,XRight,YRight,CoreX,CoreY)

is_right_pressed = False
def mouse_click(x, y, button, pressed):
    global is_right_pressed
    # print(x, y, button, pressed)
    #如果右键按下
    if pressed and button == mouse.Button.right:
        is_right_pressed = True
    elif not pressed and button == mouse.Button.right:
        is_right_pressed = False


def mouse_listener():
    with Listener(on_click=mouse_click) as listener:
        listener.join()


# print(model)
# 读取图片
def run():
    while True:
        global is_right_pressed
        im0 = screenshot(XLeft, YLeft)
        src_shape = im0.shape
        # 处理图片
        im = letterbox(im0, (640, 640), stride=32, auto=True)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous
        im = torch.from_numpy(im).to(model.device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        # 推理
        pred = model(im, augment=False, visualize=False)
        # 非极大值抑制
        pred = non_max_suppression(pred, conf_thres=0.6, iou_thres=0.45, classes=(0,1), max_det=2)[0]
        if not len(pred):
            # print("未检测到目标")
            pass
        else:
            dis_list = []
            target_list = []
            for *xyxy, scores, labels in reversed(pred):  # 处理推理出来每个目标的信息
                #用map函数将x1,y1,x2,y2转换为round类型
                x1,y1,x2,y2 = map(round,(torch.tensor(xyxy).view(1, 4).view(-1).tolist()))
                x,y,w,h = map(round,((xyxy2xywh(torch.tensor(xyxy).view(1, 4))).view(-1).tolist()))
                scores = float(scores)
                im0 = Dynamic_AttackRange(x1,y1,x2,y2,x,y,im0)
                if int(labels) == 0 or int(labels) == 1:
                    #计算距离
                    dis = math.sqrt(math.pow(x - CoreX, 2) + \
                        math.pow(y - CoreY, 2))
                    dis_list.append(dis)
                    target_list.append([x, y, w, h])
            if len(dis_list) != 0:
                x,y,w,h = target_list[dis_list.index(max(dis_list))]
                print("目标信号坐标：",x,y,w,h)
                x1 = round(x-CoreX)
                y1 = round(y-CoreY)
                if is_right_pressed:
                    mouse_xy(x1,y1)
                    time.sleep(0.05)  # 主动睡眠，防止推理过快,鼠标移动相同的两次

        #cv2.imshow('window', im0)
        cv2.waitKey(1)


if __name__ == "__main__":
    threading.Thread(target=mouse_listener).start()
    run()
