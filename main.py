from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)
model = load_model('modelo_signals.h5')

@app.route('/', methods=['GET'])
def health_check():
    return "Servidor IA online ✅"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = np.array(data['features']).reshape(1, -1)
    
    prediction = model.predict(features)
    confidence = float(prediction[0][0])
    signal = "BUY" if confidence >= 0.5 else "SELL"
    confidence = confidence if signal == "BUY" else 1 - confidence
    
    return jsonify({
        "signal": signal,
        "confidence": round(confidence, 2)
    })

if __name__ == '__main__':
    app.run()
