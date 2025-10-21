from flask import Flask, request, jsonify
import cv2, numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Plant Disease Detection Server</h1><p>Send photo from ESP32-CAM to /upload</p>"

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file_bytes = np.frombuffer(request.data, np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        avg_color = img.mean()

        if avg_color < 100:
            result = "Possible disease (dark leaf)"
        else:
            result = "Healthy leaf"

        print("Result:", result)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

