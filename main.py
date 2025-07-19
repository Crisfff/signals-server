import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, request, jsonify
import numpy as np
import logging
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info("Cargando modelo...")
    model = load_model('modelo_signals.h5', compile=False)
    logger.info("✅ Modelo cargado exitosamente")
    model._make_predict_function()  # Fix para hilos
    logger.info("✅ Función de predicción inicializada")
except Exception as e:
    logger.error(f"❌ Error crítico cargando modelo: {str(e)}")
    # Detalles adicionales para diagnóstico
    import tensorflow as tf
    logger.error(f"Versión de TensorFlow: {tf.__version__}")
    logger.error(f"Ruta del modelo: {os.path.abspath('modelo_signals.h5')}")
    logger.error(f"Tamaño del modelo: {os.path.getsize('modelo_signals.h5')} bytes")
    exit(1)

@app.route('/', methods=['GET'])
def health_check():
    return "Servidor IA online ✅"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Validación robusta de entrada
        if 'features' not in data:
            return jsonify({"error": "Falta campo 'features'"}), 400
            
        features = data['features']
        
        if not isinstance(features, list) or len(features) != 6:
            return jsonify({"error": "Se requieren 6 valores numéricos en 'features'"}), 400
        
        # Conversión segura a float
        try:
            features = [float(x) for x in features]
        except ValueError:
            return jsonify({"error": "Valores no numéricos en 'features'"}), 400
        
        # Preprocesamiento
        features_arr = np.array(features).reshape(1, -1).astype(np.float32)
        
        # Predicción
        prediction = model.predict(features_arr, verbose=0)
        confidence = float(prediction[0][0])
        
        # Transformación a señal
        signal = "BUY" if confidence >= 0.5 else "SELL"
        confidence = confidence if signal == "BUY" else 1 - confidence
        
        return jsonify({
            "signal": signal,
            "confidence": round(confidence, 2)
        })
        
    except Exception as e:
        logger.error(f"Error en predicción: {str(e)}")
        return jsonify({"error": "Error interno en el servidor"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
