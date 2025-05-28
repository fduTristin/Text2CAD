from flask import Flask, send_file, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/get-cube', methods=['GET'])
def get_cube_obj():
    # 获取文件路径
    file_path = os.path.join(os.getcwd(), 'cube.obj')
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({"error": f"{file_path} 不存在"}), 404
    
    # 发送文件
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)