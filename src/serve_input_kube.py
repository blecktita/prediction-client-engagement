from flask import Flask, request, jsonify
import requests
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Load tokenizer
with open('tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)

# Maximum sequence length
MAX_SEQUENCE_LENGTH = 20

# TensorFlow Serving URL
TF_SERVING_URL = "http://localhost:8501/v1/models/saved_model:predict"

def preprocess_input(text):
    # Convert text to sequences and pad
    sequences = tokenizer.texts_to_sequences([text])
    padded_input = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post')
    return padded_input.tolist()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data.get('text', '')

    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Preprocess input
        processed_input = preprocess_input(input_text)
        payload = {"instances": processed_input}

        # Send request to TensorFlow Serving
        response = requests.post(TF_SERVING_URL, json=payload)
        prediction = response.json()

        return jsonify({'prediction': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
