import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
import torch
from flask import *
import core.main
import core.net.unet as net
# 导入新添加的DeepSeek API模块
import core.deepseek_api as deepseek_api

# 设置 pytorch 的 pth 模型路径
model_path = 'D:/CTAI-master/CTAI_model/best_unet_model.pth'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

ALLOWED_EXTENSIONS = set(['dcm'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = './uploads'

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
        # print(image_path)
        pid, image_info = core.main.c_main(image_path, current_app.model)
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


# 添加新的API接口，用于获取肿瘤辅助分析建议
@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    try:
        # 调用DeepSeek API生成分析建议
        analysis = deepseek_api.generate_tumor_analysis()
        return jsonify({
            'status': 1,
            'data': analysis
        })
    except Exception as e:
        print(f"获取分析建议时出错: {str(e)}")
        return jsonify({
            'status': 0,
            'message': '获取分析建议失败'
        })


# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    print(f"Requesting file: tmp/{file}")
    if request.method == 'GET':
        if file is None:
            print("File is None")
            pass
        else:
            try:
                image_path = f'tmp/{file}'
                print(f"Reading file: {image_path}")
                if not os.path.exists(image_path):
                    print(f"File not found: {image_path}")
                    return "File not found", 404
                image_data = open(image_path, "rb").read()
                print(f"File size: {len(image_data)} bytes")
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
            except Exception as e:
                print(f"Error reading file: {str(e)}")
                return str(e), 500
    else:
        pass


def init_model():
    model = net.Unet(1, 1).to(device)
    if torch.cuda.is_available():
        model.load_state_dict(torch.load(model_path))
    else:
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
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
    app.run(host='0.0.0.0', port=5003, debug=True)
