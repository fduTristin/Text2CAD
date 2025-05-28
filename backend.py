from flask import Flask, request, jsonify, send_file
import os
import time
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟数据
obj_file_base_path = "cube"  # 基础文件名
status_data = {
    "steps": [],
    "completed": False
}
lock = threading.Lock()

def simulate_generation(steps, interval=3):
    global status_data
    for step in range(1, steps + 1):
        time.sleep(interval)  # 模拟时间间隔
        with lock:
            status_data["steps"].append({
                "step": step,
                "filepath": f"{obj_file_base_path}{step % 3}.obj",  # 发送次数模3的文件
                "message": f"Step {step} completed"
            })
    with lock:
        status_data["completed"] = True

@app.route('/start_generation', methods=['POST'])
def start_generation():
    global status_data
    data = request.json
    steps = data.get("steps", 5)
    prompt = data.get("prompt", "")
    
    # 重置状态数据
    with lock:
        status_data = {
            "steps": [],
            "completed": False
        }
    
    # 启动模拟生成线程
    threading.Thread(target=simulate_generation, args=(steps,)).start()
    return jsonify({"message": "Generation started"}), 200

@app.route('/status', methods=['GET'])
def get_status():
    with lock:
        return jsonify(status_data), 200

@app.route('/download/<int:step_id>', methods=['GET'])
def download_step(step_id):
    with lock:
        if step_id <= len(status_data["steps"]):
            file_path = f"{obj_file_base_path}{step_id % 3}.obj"  # 根据 step_id 模3获取文件
            if os.path.exists(file_path):
                return send_file(file_path, as_attachment=True)
            else:
                return jsonify({"error": "File not found"}), 404
        else:
            return jsonify({"error": "Step not available"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)