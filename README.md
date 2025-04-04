# 🏥 CTAI
## **基于深度学习的肿瘤辅助诊断系统**

系统以图像分割为核心，利用人工智能完成肿瘤区域的识别勾画并提供肿瘤区域的特征来辅助医生进行诊断。有完整的**模型构建、后端架设和前端访问**功能。  
医生只需通过web上传ct图像文件，后台就会使用训练好的模型进行肿瘤区域的分割，然后将勾画好肿瘤区域的图像返回，还有肿瘤区域的一些特征（如面积、周长、强度等），并且提供前几次诊断的特征数据并绘制成图表进行对比来辅助医生诊断。

## ✨ 主要特性

- **AI肿瘤分割**：使用Unet深度学习模型自动识别并勾画肿瘤区域
- **多指标分析**：提供面积、周长等多种肿瘤特征量化指标
- **趋势可视化**：自动生成病情发展趋势图表，支持多维度数据对比
- **诊断历史记录**：记录并展示患者历次诊断结果，方便跟踪病情变化
- **DeepSeek AI分析**：🆕 集成DeepSeek大模型API，自动生成专业的医学分析建议
- **响应式设计**：适配不同尺寸的屏幕，提供良好的用户体验

## 📸 系统截图

![系统界面展示](https://github.com/xming521/picture/blob/master/QQ截图20200218193846.png)

## 🔍 项目结构

```plain
CTAI
├── CTAI_flask_torch        # 基于PyTorch的后端
│   ├── core                # 核心功能模块
│   ├── data                # 数据处理
│   └── app.py              # 后端主程序
├── CTAI_model              # 模型训练与测试
│   ├── cv                  # 计算机视觉工具
│   ├── data_set            # 数据集加载与处理
│   ├── net                 # 神经网络模型定义
│   ├── utils               # 实用工具函数
│   ├── train.py            # 模型训练脚本
│   ├── test.py             # 模型测试脚本
│   └── best_unet_model.pth # 训练好的模型权重
├── CTAI_web                # 前端Vue项目
│   ├── public              # 静态资源
│   ├── src                 # 源代码
│   │   ├── components      # 组件
│   │   │   └── TrendAnalysis.vue # 趋势分析组件(支持DeepSeek AI)
│   │   ├── App.vue         # 主应用组件
│   │   └── main.js         # 入口文件
│   ├── package.json        # 依赖管理
│   └── vue.config.js       # Vue配置
├── tmp                     # 临时文件夹
│   ├── ct                  # DICOM文件临时存储
│   ├── draw                # 处理结果图像
│   ├── image               # 转换后的图像
│   └── mask                # 分割掩膜
├── uploads                 # 用户上传文件夹
├── README.md               # 项目说明文档
└── requirements.txt        # Python依赖列表
```


## 🛠️ 开发环境
- **Python 3.8**: **PyTorch 1.10.0** , OpenCV 3, Flask
- **Node 16+**: axios, ElementUI, ECharts
- **Vue 2**: Vue-cli
- **浏览器**: Chrome（内核版本60以上）


### 安装 PyTorch 1.10.0
- CUDA 11.1
```bash
pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
```

- CUDA 10.2
```bash
pip install torch==1.10.0+cu102 torchvision==0.11.0+cu102 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
```
- CPU only
```bash
pip install torch==1.10.0+cpu torchvision==0.11.0+cpu torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
```

### 安装Python依赖包
```bash
pip install -r requirements.txt
```

注意，在 requirements.txt 中:
```plain
numpy==1.23.0               # 差不多相近的版本就行，不能太新
opencv-python==3.4.8.29     # 差不多相近的版本就行，不能用 4.x 版本的
gevent                      # 用于生产环境部署
requests                    # 用于API请求
```

### 安装Node环境

- Windows:  
 
  [官网下载安装](https://nodejs.org/)

- Linux: 

  ```bash
  # 使用nvm管理Node版本
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
  nvm install 16
  nvm use 16
  ````
  
### 安装Vue依赖

```bash
cd CTAI_web
npm install -g @vue/cli
npm install
# 或者使用yarn
npm install -g yarn
yarn install
```

## 🔄 开发环境运行

启动Vue前端渲染服务
```bash
cd CTAI_web
npm run serve
```
启动后端flask服务
```bash
cd CTAI_flask_torch
python app.py
```

## 🚀 生产环境部署

### 前端构建
编译Vue前端代码
```bash
cd CTAI_web
yarn build
# 或使用npm
npm run build
```

### 部署步骤
1. 将`CTAI_flask_torch`和`CTAI_web/dist`目录复制到服务器
2. 安装Python 3.8及依赖包(包括PyTorch)
```bash
pip install -r requirements.txt
pip install torch==1.10.0+cpu torchvision==0.11.0+cpu torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
```
3. 配置DeepSeek API (可选)
   - 在`CTAI_flask_torch/app.py`中设置您的DeepSeek API密钥
   - 如果不需要AI分析功能，可以注释相关代码

4. 后台启动Python服务
```bash
cd CTAI_flask_torch
nohup python app.py > app.log 2>&1 &
```

5. 使用Nginx或其他Web服务器部署前端
```bash
# Nginx配置示例
server {
    listen 80;
    server_name your_domain.com;

    # 前端静态文件
    location / {
        root /path/to/CTAI_web/dist;
        try_files $uri $uri/ /index.html;
        index index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://localhost:5003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

6. 也可使用`PM2`来管理前端服务
```bash
npm install -g serve pm2
cd CTAI_web
pm2 serve ./dist 8080
```

## 🔑 DeepSeek API配置

本项目集成了DeepSeek大语言模型API用于生成医学分析建议。要启用此功能：

1. 注册DeepSeek账户并获取API密钥: https://platform.deepseek.com/
2. 在`CTAI_flask_torch/app.py`中设置API密钥:
```python
# 设置DeepSeek API密钥
api_key = "your_api_key_here"
```

## 📦 资源下载

- [测试数据集](https://share.weiyun.com/5eS2jDk)
- [PyTorch模型下载](http://47.237.94.141:5244/%E6%95%B0%E6%8D%AE/best_unet_model.pth)

## 🔧 模型说明
本项目使用U-Net架构进行肿瘤分割。U-Net是一种广泛应用于医学图像分割的卷积神经网络架构，其特点是对称的编码器-解码器结构和跳跃连接。

<img width="80%" height="80%" src="https://github.com/xming521/picture/blob/master/图片3.png"/>

### 训练参数
- 损失函数: 交叉熵损失
- 优化器: Adam
- 学习率: 0.001
- 批次大小: 2-8 (取决于GPU内存)
- 训练轮次: 20+

## 🧠 模型训练

项目包含完整的模型训练和测试代码，位于`CTAI_model`目录：

### 训练新模型

1. 准备数据集，并更新`train.py`中的数据集路径：

```python
# 设置训练数据集目录路径！！！
# 路径中不能有中文字符！！！
# Windows目录使用 \\ 结尾，Linux目录使用 / 结尾
train_dataset_path = r"C:\Users\xxx\Downloads\datasets\\"
# train_dataset_path = r"/mnt/datasets/"
```

2. 根据需要调整超参数：

```python
# 模型超参数设置
epochs = 20             # 训练轮次
batch_size = 2          # 每个批次的样本数
learn_rate = 0.001      # 学习率
```

3. 开始训练：

```bash
cd CTAI_model
python train.py
```

训练过程会自动保存最佳模型，并生成训练过程的损失曲线。

### 测试模型

1. 修改`test.py`中的测试数据路径：

```python
# 设置测试数据集目录路径
test_data_path = r"C:\Users\xxx\Downloads\datasets\\"
```

2. 运行测试脚本：

```bash
cd CTAI_model
python test.py
```

测试结果将保存在`./test-out/`目录中。

## 📝 许可证
本项目采用MIT许可证
