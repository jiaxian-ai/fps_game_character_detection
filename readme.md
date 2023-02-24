## fps_game_character_detection

### 介绍：
本项目为CF网游，人物角色识别定位模型，采用yolov5框架实现，仅供学习研究使用。

#### 模型效果展示

![](https://image-static.segmentfault.com/253/642/2536425189-63f74fbd7a530_fix732)
![](https://image-static.segmentfault.com/213/616/2136164778-63f74fbd5ee7d_fix732)
![](https://image-static.segmentfault.com/251/983/2519833025-63f74fbd7afef_fix732)

#### 开发思路与流程

**思路**

CV领域的目标检测模型已经非常成熟，特别是yolov5系列
为什么不是用v6、v7？因为坑很多，而且效果不尽然好。

FPS游戏中，主要以击败敌方角色为目标，影响比赛成绩最主要的因素就是玩家的枪法。
使用深度学习的模型就可以对敌方角色进行准确定位，从而帮助玩家进行瞄准。而yolov5的预训练模型对于人物的识别已经很成熟。这时候只需要准备一定的数据样本，就可以实现不错效果。


**流程**

**样本采集**   
开发游戏中的截图代码`sample_util/collecting_data.py`  
运行代码，进游戏后，会监听键盘。  
截图会剪裁中心区域640X640（官方预训练模型的图片尺寸）
按`F`键将自动截图  
按`~`键，将切换角色  
保存图片至`sample/data/QF`目录和`sample/data/BW`目录
尽量选择**团队竞技**模式，游戏节奏会快很多，对不同的角色皮肤，不同的视角分别截图，我大概采集了500+保卫者和500+潜伏者图片
根据经验，图片样本主要不在于多，而是覆盖的角度、皮肤、光影等模式的分布广  
![](https://image-static.segmentfault.com/361/679/3616797238-63f74fbd825fc_fix732)
**样本标注**   
使用开源数据标注工具[labelImg](https://github.com/heartexlabs/labelImg/archive/refs/heads/master.zip)
![](https://image-static.segmentfault.com/144/722/144722219-63f74fcccd7ce_fix732)
**模型训练**
下载最新的[yolov5.7.0](https://github.com/ultralytics/yolov5/archive/refs/tags/v7.0.zip)
下载预训练模型[yolov5n.pt](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n.pt)，保存到yolov5.7.0目录下
更改几个文件配置，就可以进行训练了。
**修改`models/yolov5n.yaml`**
![](https://segmentfault.com/img/bVc6xt8)
**参考coco128.yaml创建`data\cf.yaml`文件**
`../cfdata`为样本图片目录
我们只有“保卫”和“潜伏”这两种类别
![](https://segmentfault.com/img/bVc6xt5)
**修改`train.py`文件**
`--epochs`设置为`300`，迭代300轮就会有不错的效果
`--workers`根据电脑CPU核心数配置，本地16和电脑，最多填`2-4`
![](https://segmentfault.com/img/bVc6xt3)
训练结果的模型和分析将保存在 `yolov5-7.0/runs/train/exp/`目录，`bast.pt`就是训练好的模型

#### 体验模型

项目地址：https://github.com/jiaxian-ai/fps_game_character_detection

`git clone https://github.com/jiaxian-ai/fps_game_character_detection.git`

#### 环境配置

##### 系统要求：**windows10+GPU**

**python>=3.8**

安装依赖包
```
cd yolov5-7.0 #进入yolov5-7.0目录
pip install -r requirements.txt
```

##### 模型测试
测试模型效果，判断是否正常运行
```
python detect.py
```
测试结果的图片标注将保存在 `yolov5-7.0/runs/detect/` 目录

##### 在真实游戏中使用

运行predict.py文件
```
python predict.py
```

会连续截屏，并在定位到目标后，等待“鼠标右键”点击，如果捕获到右键，则会自动移动鼠标到目标位置
