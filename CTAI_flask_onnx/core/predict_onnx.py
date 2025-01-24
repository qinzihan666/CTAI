import cv2

rate = 0.5


def predict_onnx(dataset,model):

    global res, img_y, mask_arrary
    x = dataset[0][0]
    file_name = dataset[1]
    y = model(x)
    img_y = y[0][0]
    img_y[img_y >= rate] = 1
    img_y[img_y < rate] = 0
    img_y = img_y * 255
    cv2.imwrite(f'./tmp/mask/{file_name}_mask.png', img_y,
                (cv2.IMWRITE_PNG_COMPRESSION, 0))


if __name__ == '__main__':
    # 写保存模型
    # train()
    predict_onnx()
