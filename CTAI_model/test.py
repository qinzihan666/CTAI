import os
import cv2
import torch
from torch.utils.data import DataLoader
from data_set import make
from net import unet

# 设置训练数据集目录路径
test_data_path = r"C:\Users\xxx\Downloads\datasets\\"

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
torch.set_num_threads(4)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.cuda.empty_cache()
res = {'epoch': [], 'loss': [], 'dice': []}
rate = 0.5

test_dataset = make.get_d1_local(test_data_path)

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


def onlytest():
    model = unet.Unet(1, 1).to(device)
    model.load_state_dict(torch.load('best_unet_model.pth'))
    global res, img_y, mask_arrary
    epoch_dice = 0
    with torch.no_grad():
        dataloaders = DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers=0)
        for x in dataloaders:
            id = x[1:]  # ('1026',), ('10018',)]先病人号后片号
            # print(id, 'id')
            x = x[0].to(device)
            y = model(x)
            img_y = torch.squeeze(y).cpu().numpy()
            img_y[img_y >= rate] = 1
            img_y[img_y < rate] = 0
            img_y = img_y * 255
            mkdir(f'./test-out/{id[0][0].split(os.sep)[-1]}/arterial phase/')
            cv2.imwrite(f'./test-out/{id[0][0].split(os.sep)[-1]}/arterial phase/{id[1][0]}_mask.png', img_y,
                        (cv2.IMWRITE_PNG_COMPRESSION, 0))


if __name__ == '__main__':
    onlytest()
