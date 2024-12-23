# Input request example for Flask API
# Port: 5000

curl -X POST http://localhost:5000/predict \
-H "Content-Type: application/json" \
-d '{"text": "Hello welcome!"}'
