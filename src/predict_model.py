from flask import Flask, request, jsonify
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# Initialize Flask app
app = Flask(__name__)

# Load tokenizer and model
with open('tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)

model = load_model('engagement_model.keras')

# Set a maximum sequence length (should match what was used during training)
MAX_SEQUENCE_LENGTH = 20

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data.get('text', '')

    if not input_text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Convert text to sequences
        sequences = tokenizer.texts_to_sequences([input_text])
        
        # Pad the sequences to ensure consistent input shape
        padded_input = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH, padding='post')

        # Convert to NumPy array (Keras requires this)
        processed_input = np.array(padded_input)

        # Perform prediction
        prediction = model.predict(processed_input)

        # Return prediction
        return jsonify({'prediction': prediction.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
