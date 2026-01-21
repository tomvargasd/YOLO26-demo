from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
import base64
from ultralytics import YOLO
import glob
import os

app = Flask(__name__)

# Buscar modelo activo
model_path = None
active_models = glob.glob('models/active_*.pt')
if active_models:
    model_path = active_models[0]
    print(f"Modelo activo cargado: {model_path}")
    model = YOLO(model_path)
else:
    print("No se encontró ningún modelo activo_*.pt")
    model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        if model is None:
            return jsonify({'error': 'Modelo no disponible'}), 500
        
        # Obtener imagen en base64 del request
        data = request.json
        image_data = data['image'].split(',')[1]
        
        # Decodificar imagen
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Realizar inferencia con YOLO
        results = model(frame, conf=0.25, verbose=False)
        
        # Dibujar detecciones en el frame
        annotated_frame = results[0].plot()
        
        # Codificar frame procesado a base64
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'image': f'data:image/jpeg;base64,{img_base64}',
            'detections': len(results[0].boxes)
        })
    
    except Exception as e:
        print(f"Error procesando frame: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
