import tensorflow as tf
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Load the saved model
model = tf.keras.models.load_model('/model/mnist_model')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json['image']
    image = np.array(data).reshape(1, 28, 28) / 255.0
    prediction = model.predict(image)
    return jsonify({'prediction': int(np.argmax(prediction))})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)