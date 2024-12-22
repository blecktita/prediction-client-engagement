## Build docker images and run container for TensorFlow Serving
```
docker build -t e-commerce-engagement-model .
docker run -p 8501:8501 --name tensorflow-serving e-commerce-engagement-model
```
