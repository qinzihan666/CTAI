# 🏥  CTAI
## **基于深度学习的肿瘤辅助诊断系统**

系统以图像分割为核心，利用人工智能完成肿瘤区域的识别勾画并提供肿瘤区域的特征来辅助医生进行诊断。有完整的**模型构建、后端架设和前端访问**功能。  
医生只需通过web上传ct图像文件，后台就会使用训练好的模型进行肿瘤区域的分割，然后将勾画好肿瘤区域的图像返回，还有肿瘤区域的一些特征（如面积、周长、强度等），并且提供前几次诊断的特征数据并绘制成图表进行对比来辅助医生诊断。  
<img width="600" height="100" src="https://github.com/xming521/picture/blob/master/QQ截图20200218193846.png"/>

本项目优化并解决了关于环境适配，前端界面无法上传文件，卡死在进度99%等问题，添加了后端功能测试代码：

1.备份好了environment backup.yml虚拟环境和requirements backup.txt依赖包，修改了无脑fork就可以一键运行

2.解决了在 process.py 文件中的 last_process 函数和get_feature.py 文件中的get_geometry_feature 函数，使用了 cv2.findContours 函数，但是函数的返回值解包不正确问题（在 OpenCV 4.x 版本中，cv2.findContours 只返回两个值：轮廓和层次结构，而不是三个值：阈值、轮廓和层次结构。但是原代码中试图解包三个值）

3.修复了Content.vue下载功能使用的是 localhost:5003，而上传功能使用的是 this.server_url不一致的问题，增加了下载失败的返回结果

4.添加了test_upload.py用来测试后端功能是否正常

## 觉得不错欢迎给star⭐哦


## 注意事项
文件下载后记得在本地配置好写入权限，或者鼠标右键用管理员身份打开编辑器

## 项目结构

```plain
CTAI
├── CTAI_flask_onnx
│   ├── core
│   ├── data
│   ├── static
│   ├── tmp
│   ├── uploads
│   ├── app_onnx.py
│   ├── best_unet_model.onnx
│   └── to_oonx.py
├── CTAI_flask_torch
│   ├── core
│   ├── data
│   ├── static
│   ├── tmp
│   ├── upload
│   └── sapp.py
├── CTAI_model
│   ├── cv
│   ├── data_set
│   ├── net
│   ├── utils
│   ├── best_unet_model.pth
│   ├── test.py
│   └── train.py
├── CTAI_web
│   ├── dist
│   ├── node_modules
│   ├── public
│   ├── src
│   ├── babel.config.js
│   ├── package-lock.json
│   ├── package.json
│   ├── vue.config.js
│   └── yarn.lock
├── README.md
└── environment backup.yml
└── requirements backup.txt
└──test_upload.py


## 模型训练

进入`CTAI_model`目录，修改`train.py`中的数据集路径和训练参数：
```bash
# 设置训练数据集目录路径！！！
# 路径中不能有中文字符！！！
# Windows目录使用 \\ 结尾，Linux目录使用 / 结尾 ！！！
train_dataset_path = r"C:\Users\xxx\Downloads\datasets\\"
# train_dataset_path = r"/mnt/datasets/"

# 模型超参数设置
epochs = 20             # 训练轮次（太少不行）
batch_size = 2          # 每个批次的样本数（看显存，24G建议8）
learn_rate = 0.001      # 学习率（不建议修改）
```
训练
```bash
cd CTAI_model
python train.py
```



## 数据集下载

通过网盘分享的文件：直肠癌数据.7z
链接: https://pan.baidu.com/s/1ePpIVhsN2YNYezhSZPfPlQ?pwd=33xc 提取码: 33xc 
--来自百度网盘超级会员v6的分享

由原作者提供，致谢！




## 本地开发环境运行步骤
CTAI_flask_onnx（cpu）与CTAI_flask_torch(gpu)二选一即可
如果自己训练的模型对照项目结构放到训练好的路径即可
如果用原作者训练的模型把模型下载好放到对应的路径

  下载路径

  通过网盘分享的文件：CTAI模型
链接: https://pan.baidu.com/s/1POSMfXKaVzjijS9cql0IqA?pwd=rx4b 提取码: rx4b 
--来自百度网盘超级会员v6的分享

启动后端flask服务
```bash
cd CTAI_flask_torch
python app.py
```

考虑到配置前端时node_modules比较大下载缓慢，作者这里提前准备好了存到百度网盘下载放到对应路径即可


下载路径


通过网盘分享的文件：node_modules
链接: https://pan.baidu.com/s/1jmZK-mxKeNq2E2cCXvKt8A?pwd=5cmq 提取码: 5cmq 
--来自百度网盘超级会员v6的分享

启动Vue前端渲染服务
```bash
cd CTAI_web
npm run serve
```


## 自己配置服务器时生产环境部署

- 进行模型转换, pth --> onnx
```bash
cd CTAI_flask_onnx
python to_oonx.py
```

- 进行Vue前端代码编译, 编译完后的`dist`目录即可用于部署
```bash
cd CTAI_web
yarn build
```

- 仅需将 `CTAI_flask_onnx` 和 `CTAI_web/dist` 两个目录下的文件压缩复制到服务器。
```plain
CTAI
├── CTAI_flask_onnx
│   ├── core
│   ├── data
│   ├── static
│   ├── tmp
│   ├── uploads
│   ├── app_onnx.py
│   ├── best_unet_model.onnx
│   └── to_oonx.py
├── CTAI_web
│   └── dist
└── environment backup.yml
└── requirements backup.txt
```

- 在服务器安装 `python 3.8` 和依赖包，此处**不需要安装pytorch**
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.8 python3.8-distutils -y
cd CTAI
python3.8 -m pip install -r requirements.txt
```

- 在服务器安装 `node` 和 `npm`
```bash
# Download and install fnm:
curl -o- https://fnm.vercel.app/install | bash
# Download and install Node.js:
fnm install 22
```

- 在服务器后台运行python服务
```bash
cd CTAI_flask_onnx
nohup python3.8 app_onnx.py > app_onnx.log 2>&1 &
```

- 在服务器使用`PM2`启动和管理Vue服务
```bash
# 安装PM2
npm install -g serve pm2
cd CTAI_web
# 启动服务，将目录dist作为静态服务器根目录，端口为8080
pm2 serve ./dist 8080
```
启动成功后显示类似如下界面：
```plain
[PM2] Starting C:\GreenApps\Nodejs22\node_modules\pm2\lib\API\Serve.js in fork_mode (1 instance)
[PM2] Done.
[PM2] Serving D:\SourceCode\PycharmProjects\CTAI\CTAI_web\dist on port 8080
┌────┬────────────────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name                       │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ static-page-server-8080    │ default     │ 5.4.3   │ fork    │ 29652    │ 0s     │ 0    │ online    │ 0%       │ 50.3mb   │ xxx      │ disabled │
└────┴────────────────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
```

`PM2`基本使用
```bash
# 查看 pm2 启动的项目
pm2 list
# 开机自启
pm2 startup
# 停止对应的id服务
pm2 stop [id]
# 重启对应的id服务
pm2 reload  [id]
# 删除对应的id服务
pm2 delete [id]
```


## 模型介绍
训练的数据来源于国外的数据集。因数据和精力有限只训练了针对直肠肿瘤模型。首先对CT文件进行整理，使用SimpleITK读取CT文件，读取肿瘤的掩膜文件并映射到肿瘤CT图像来获取肿瘤区域，然后进行数据的归一化，预处理后制作训练和测试的数据集。
使用**PyTorch框架**编写。使用**交叉熵损失函数**，**Adam优化器**。
网络结构采用**U-Net**，**U-Net**是基于FCN的一种语义分割网络，适用于做医学图像的分割。结构如下，实际使用稍有改动。    
<img width="80%" height="80%" src="https://github.com/xming521/picture/blob/master/图片3.png"/>  

训练过程如下：  
<img width="50%" height="50%" src="https://github.com/xming521/picture/blob/master/图片4.png"/>  

## 后端介绍
整个系统采取前后分离的方案，确保足够轻量，低耦合。后端采用Python的Flask库，能与AI框架更好的结合，使得系统能更高内聚。  
后端运行流程如下：  
<img width="60%" height="60%" src="https://github.com/xming521/picture/blob/master/图片1.png"/>  

项目运行后的目录介绍：  
|  目录   | 功能  |
|  ----  | ----  |
| uploads	| 		直接上传目录   | 
| tmp/ct	| 		dcm文件副本目录 | 
| tmp/image| 		dcm读取转换为png目录| 
| tmp/mask	| 	预测结果肿瘤掩膜目录| 
| tmp/draw	| 	勾画肿瘤后处理结果目录| 

## 系统截图
<img width="60%" height="60%" src="https://github.com/xming521/picture/blob/master/图片32.png"/>
<img width="60%" height="60%" src="https://github.com/xming521/picture/blob/master/图片31.png"/>
<img width="60%" height="60%" src="https://github.com/xming521/picture/blob/master/图片2(1).png"/>

## 贡献者

这个项目由以下人员共同创建：

- [qinzihan666](https://github.com/qinzihan666) 
- [Caoyan-qzh](https://github.com/Caoyan-qzh) 
