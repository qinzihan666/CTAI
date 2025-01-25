import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
import numpy as np
import core.main_onnx
import onnxruntime as ort
from flask import *
from gevent.pywsgi import WSGIServer


# 设置 onnx 模型路径
model_path = "./best_unet_model.onnx"


ALLOWED_EXTENSIONS = set(['dcm'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = './uploads'

# 配置 flask 日志记录器
werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/ct')
        image_path = os.path.join('./tmp/ct', file.filename)

        # 调用推理函数
        pid, image_info = core.main_onnx.c_main_onnx(image_path, current_app.model)
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/image/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info': image_info
                        })

    return jsonify({'status': 0})

@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)

# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if file is None:
            pass
        else:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

def init_model():
    # 加载 ONNX 模型
    ort_session = ort.InferenceSession(model_path)

    def model(input_data):
        """
        推理函数：将输入数据传递给 ONNX 模型并返回结果
        """
        # 获取输入
        input_name = ort_session.get_inputs()[0].name
        input_data = input_data.astype(np.float32)  # 假设模型需要 float32 类型

        # 推理
        output = ort_session.run(None, {input_name: input_data})
        return output[0]  # 返回模型的推理结果

    return model

if __name__ == '__main__':
    # 创建需要的临时目录
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('./tmp/ct', exist_ok=True)
    os.makedirs('./tmp/image/', exist_ok=True)
    os.makedirs('./tmp/mask/', exist_ok=True)
    os.makedirs('./tmp/draw/', exist_ok=True)

    with app.app_context():
        current_app.model = init_model()

    # 使用 gevent 的 WSGI 服务器
    http_server = WSGIServer(('0.0.0.0', 5003), app, log=werkzeug_logger)
    print("Starting server on http://0.0.0.0:5003")
    http_server.serve_forever()
