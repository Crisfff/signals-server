import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Reducir logs de TensorFlow

from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Cargar el modelo al iniciar la app
try:
    model = load_model('modelo_signals.h5')
    print("✅ Modelo cargado exitosamente")
except Exception as e:
    print(f"❌ Error cargando modelo: {str(e)}")
    raise e  # Falla explícitamente si no carga el modelo

@app.route('/', methods=['GET'])
def health_check():
    return "Servidor IA online ✅"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array(data['features']).reshape(1, -1).astype(np.float32)
        
        # Preprocesamiento adicional si es necesario
        # ...
        
        prediction = model.predict(features, verbose=0)
        confidence = float(prediction[0][0])
        
        # Convertir predicción a señal
        signal = "BUY" if confidence >= 0.5 else "SELL"
        confidence = confidence if signal == "BUY" else 1 - confidence
        
        return jsonify({
            "signal": signal,
            "confidence": round(confidence, 2)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
