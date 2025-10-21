from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        temp = request.form.get("temperature")
        hum = request.form.get("humidity")
        soil = request.form.get("soil")
        file_bytes = np.frombuffer(request.files['image'].read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        print(f"Temperature: {temp}, Humidity: {hum}, Soil: {soil}")
        # Simple disease detection
        avg_color = img.mean()
        result = "Healthy" if avg_color > 100 else "Possible disease"

        return jsonify({"temperature": temp, "humidity": hum, "soil": soil, "result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
