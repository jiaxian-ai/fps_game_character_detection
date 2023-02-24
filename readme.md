#### 介绍：

本项目为CF网游，人物角色识别定位模型，采用yolov5框架实现，仅供学习研究使用。

##### 模型效果展示
![1fa21655bb4c66b44e97fc9bd2a3595a.jpeg](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3586)
![702a8be8aad67c4a8c53078d275c72e6.jpeg](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3587)
![25fad2e520a7bcd14c07c2f1849464c8.jpeg](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3585)

##### 开发思路与流程

**思路**
CV领域的目标检测模型已经非常成熟，特别是yolov5系列
为什么不是用v6、v7？因为坑很多，而且效果不尽然好。
FPS游戏中，主要以击败敌方角色为目标，影响比赛成绩最主要的因素就是玩家的枪法。
使用深度学习的模型就可以对敌方角色进行准确定位，从而帮助玩家进行瞄准。而yolov5的预训练模型对于人物的识别已经很成熟。这时候只需要准备一定的数据样本，就可以实现不错效果。


**流程**

1. 样本采集
开发游戏中的截图代码`sample_util/collecting_data.py`
运行代码，进游戏后，会监听键盘，按`F`键将自动截图，并剪裁中心区域640X640，保存图片至`sample/data/`目录。按`~`键，将切换角色
![984752bd95a246e12afc3e7c7385530c.png](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3590)
进去游戏中，分别收集潜伏者和保卫者各500条数据

2. 样本标注
使用开源数据标注工具[labelImg](https://github.com/heartexlabs/labelImg/archive/refs/heads/master.zip)
![09c97e4e113479acb76e472c465e3fdf.png](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3591)
3. 模型训练
下载最新的[yolov5.7.0](https://github.com/ultralytics/yolov5/archive/refs/tags/v7.0.zip)
下载预训练模型[yolov5n.pt](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n.pt)，保存到yolov5.7.0目录下
更改几个文件配置，就可以进行训练了。
**修改`models/yolov5n.yaml`**
![01baf7c4e9fc412cf6475ac7c89b735f.png](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3592)
**参考coco128.yaml创建`data\cf.yaml`文件**
`../cfdata`为样本图片目录
我们只有“保卫”和“潜伏”这两种类别
![509b0f2ff85bd66f8fe644046bdea0c1.png](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3593)
**修改`train.py`文件**
`--epochs`设置为`300`，迭代300轮就会有不错的效果
`--workers`根据电脑CPU核心数配置，本地16和电脑，最多填`2-4`
![9b5d288e451aa0fe3ba6a33d64d3683f.png](evernotecid://A56B546B-09BE-47DD-BE1C-3D5FA50387AB/appyinxiangcom/19947355/ENResource/p3594)
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


# fps_game_character_detection