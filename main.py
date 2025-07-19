from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf

app = Flask(name)
MODEL = tf.keras.models.load_model("modelo_signals.h5")

@app.route("/", methods=["GET"])
def ping():
    return "Servidor IA online ✅", 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data or "features" not in data:
        return jsonify({"error": "Envía JSON {'features': [o,h,l,c,vol,rsi]}"}), 400
    try:
        x = np.array(data["features"]).reshape(1, -1)
        y = MODEL.predict(x)[0][0]
        label = "BUY" if y > 0.55 else "SELL"
        return jsonify({"signal": label, "confidence": float(y)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if name == "main":
    app.run(host="0.0.0.0", port=8000)
