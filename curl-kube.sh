# Input request example for TensorFlow Serving on Kubernetes via API serve_input_kube.py script

curl -X POST http://localhost:5002/predict \
-H "Content-Type: application/json" \
-d '{"text": "Hadiah langsung"}'
