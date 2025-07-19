from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

app = Flask(name)

# Carga del modelo
MODEL = tf.keras.models.load_model("modelo_signals.h5")

@app.route("/", methods=["GET"])
def ping():
    return "Servidor IA online ✅", 200

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if not payload or "features" not in payload:
        return jsonify({"error": "Debes enviar JSON {'features': [...] }"}), 400
    try:
        x = np.array(payload["features"]).reshape(1, -1)
        y = MODEL.predict(x)[0][0]
        label = "BUY" if y > 0.55 else "SELL"
        return jsonify({"signal": label, "confidence": float(y)})
    except Exception as err:
        return jsonify({"error": str(err)}), 500

if name == "main":
    # Solo para pruebas locales
    app.run(host="0.0.0.0", port=8000)
