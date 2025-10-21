from flask import Flask, request, render_template, redirect
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Store latest data
latest_data = {
    "temperature": "N/A",
    "humidity": "N/A",
    "soil": "N/A",
    "result": "Waiting for data...",
    "image": None
}

@app.route('/')
def index():
    img_html = ""
    if latest_data["image"]:
        img_html = f'<img src="data:image/jpeg;base64,{latest_data["image"]}" width="320">'
    return f"""
    <h1>Plant Monitoring Dashboard</h1>
    {img_html}
    <p><b>Disease:</b> {latest_data['result']}</p>
    <p><b>Temperature:</b> {latest_data['temperature']} °C</p>
    <p><b>Humidity:</b> {latest_data['humidity']} %</p>
    <p><b>Soil Moisture:</b> {latest_data['soil']}</p>
    """

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Read sensor values
        temp = request.form.get("temperature")
        hum = request.form.get("humidity")
        soil = request.form.get("soil")

        # Read image
        file = request.files['image']
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Simple disease detection
        avg_color = img.mean()
        result = "Healthy" if avg_color > 100 else "Possible disease"

        # Convert image to base64 to show in HTML
        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        # Update latest data
        latest_data["temperature"] = temp
        latest_data["humidity"] = hum
        latest_data["soil"] = soil
        latest_data["result"] = result
        latest_data["image"] = img_base64

        print(f"Data received - Temp:{temp}, Hum:{hum}, Soil:{soil}, Result:{result}")

        return "Data uploaded successfully"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
