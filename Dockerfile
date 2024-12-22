# Use the official TensorFlow Serving image
FROM tensorflow/serving:latest

# Set environment variable for TensorFlow Serving to use the model
ENV MODEL_NAME=saved_model

# Copy the saved model directory into TensorFlow Serving's model path
COPY ./saved_model /models/saved_model
