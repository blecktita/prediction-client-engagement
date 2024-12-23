# Input request example for TensorFlow Serving on Kubernetes via API serve_input_eks.py script

curl -X POST http://localhost:5003/predict \
-H "Content-Type: application/json" \
-d '{"text": "Hello Welcome"}'
