import torch
from torch.nn import init
from torch.utils.data import DataLoader
from data_set import make
from net import unet
from utils import dice_loss
import matplotlib.pyplot as plt
import os

# 设置训练数据集目录路径
train_dataset_path = r"C:\Users\xxx\Downloads\datasets\\"
# 模型超参数设置
epochs = 20             # 训练轮次
batch_size = 2          # 每个批次的样本数
learn_rate = 0.001      # 学习率


# 设置GPU显卡，默认使用第一块显卡
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
# 设置CPU线程数（一般来说，线程数越多越好，但具体数量要根据CPU性能而定）
torch.set_num_threads(4)
# 根据CUDA可用性选择训练设备：GPU或CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 清理GPU缓存，以防内存占用过多
torch.cuda.empty_cache()

# 输出的二值化阈值，用于判断像素是否属于目标区域
rate = 0.50
# 记录训练状态（轮次、损失、dice准确性）
res = {'epoch': [], 'train_loss': [], 'test_dice': []}

# 模型权重初始化函数
def weights_init(m):
    # 获取当前层的类名
    classname = m.__class__.__name__
    # 如果是卷积层（Conv3d）
    if 'Conv3d' in classname:
        init.xavier_normal_(m.weight)  # 使用Xavier正态初始化卷积层权重
        init.constant_(m.bias, 0.0)   # 偏置项初始化为0
    # 如果是全连接层（Linear）
    elif 'Linear' in classname:
        init.xavier_normal_(m.weight)  # 使用Xavier正态初始化全连接层权重
        init.constant_(m.bias, 0.0)   # 偏置项初始化为0

# 使用make函数加载训练集和测试集数据
train_dataset, test_dataset = make.get_d1(train_dataset_path)
# 创建Unet模型并进行权重初始化
model = unet.Unet(1, 1).to(device).apply(weights_init)
# 损失函数（BCELoss用于二分类问题）
criterion = torch.nn.BCELoss().to(device)
# 优化器（Adam优化器）
optimizer = torch.optim.Adam(model.parameters(), learn_rate)

# 保存最优模型的变量
best_dice = 0.0  # 初始化最优Dice系数

# 训练函数
def train():
    global res, best_dice
    # 创建训练数据加载器（Dataloader）
    dataloaders = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    for epoch in range(epochs):
        dt_size = len(dataloaders)  # 每轮训练的数据批次数
        epoch_loss, epoch_dice = 0, 0  # 初始化每轮的损失和Dice系数
        for step, (x, y) in enumerate(dataloaders, 1):  # 遍历每个批次数据
            x, y = x[0].to(device), y[1].to(device)  # 将输入数据和标签移动到GPU
            # 清空优化器中的梯度
            optimizer.zero_grad()
            # 模型进行前向传播
            outputs = model(x).squeeze(1)  # 去除不必要的维度
            # 计算损失
            loss = criterion(outputs, y)
            # 进行反向传播，计算梯度
            loss.backward()
            # 更新模型参数
            optimizer.step()
            # 累加当前批次的损失
            epoch_loss += loss.item()

            # 每10个批次输出一次当前的训练状态，并进行测试
            if step % 10 == 0:
                print(f"Epoch {epoch+1}, Step {step}/{dt_size}, Loss: {loss.item():.3f}", end='   ')
                current_dice = test()
                # 如果当前Dice准确率优于之前保存的最优Dice值，则保存模型
                if current_dice > best_dice:
                    best_dice = current_dice
                    torch.save(model.state_dict(), 'best_unet_model.pth')
                    print(f" - Best model saved with Dice: {best_dice:.4f}")

        # 每轮训练结束后，记录损失
        res['epoch'].append(epoch + 1)  # 记录当前的epoch
        res['train_loss'].append(epoch_loss/dt_size)  # 记录当前的训练损失
        # 每轮训练结束后，进行测试并记录Dice准确率
        test_dice = test()
        res['test_dice'].append(test_dice)  # 保存每轮训练后的测试集Dice准确率

    # 保存训练过程中的损失曲线和测试集的Dice准确率曲线
    plt.figure(figsize=(10, 5))
    # 绘制训练损失曲线
    plt.subplot(1, 2, 1)
    plt.plot(res['epoch'], res['train_loss'], label='Train Loss', color='b')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.title('Train Loss over Epochs')
    plt.legend()
    # 绘制测试集Dice准确率曲线
    plt.subplot(1, 2, 2)
    plt.plot(res['epoch'], res['test_dice'], label='Test Dice', color='r')
    plt.xlabel('Epochs')
    plt.ylabel('Dice')
    plt.title('Test Dice over Epochs')
    plt.legend()
    plt.tight_layout()
    plt.savefig('train_and_test_curves.png')  # 保存训练和测试曲线图

# 测试函数
def test():
    epoch_dice = 0  # 初始化每轮测试的Dice系数
    with torch.no_grad():  # 在测试时不需要计算梯度，节省内存
        dataloaders = DataLoader(test_dataset, batch_size=1, shuffle=True, num_workers=0)
        for x, mask in dataloaders:
            x = x[0].to(device)  # 将输入数据移动到GPU
            # 模型进行前向传播
            outputs = model(x).squeeze(0).squeeze(0).cpu().numpy()  # 将输出移回CPU并转换为numpy数组
            mask_arr = mask[1].squeeze(0).cpu().numpy()  # 获取真实的标签并转换为numpy数组
            # 二值化处理：大于阈值的为目标区域，其他为背景
            outputs[outputs >= rate] = 1
            outputs[outputs < rate] = 0
            # 计算当前测试批次的Dice系数
            epoch_dice += dice_loss.dice(outputs, mask_arr)
        # 计算当前测试集的平均Dice系数
        avg_dice = epoch_dice / len(dataloaders)
        print(f'Test Dice: {avg_dice:.4f}')  # 输出平均Dice系数
        return avg_dice  # 返回当前Dice系数，用于模型保存判断

# 程序入口
if __name__ == '__main__':
    train()  # 开始训练
    test()   # 训练完成后进行测试
