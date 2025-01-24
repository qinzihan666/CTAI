from core import process_onnx, predict_onnx, get_feature


def c_main_onnx(path,model):
    image_data = process_onnx.pre_process_onnx(path)
    # print(image_data)
    predict_onnx.predict_onnx(image_data,model)
    process_onnx.last_process(image_data[1])
    image_info = get_feature.main(image_data[1])

    return image_data[1] + '.png', image_info


if __name__ == '__main__':
    pass
