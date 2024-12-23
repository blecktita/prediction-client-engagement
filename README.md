# Client Engagement Prediction Model

---

## Project Overview
---

I basically created a predictive system that analyzes the social media engagement for most clients. I deployed the model using TensorFlow Serving for real-time predictions, packaged it in Docker containers, and orchestrated it with Kubernetes on AWS EKS
---

## Project Goals

My initiative focuses on several key objectives:
- Developing a predictive algorithm to evaluate tweet engagement potential by analyzing content and hashtag patterns
- Implementing TensorFlow Serving to enable instant prediction capabilities
- Creating a containerized solution with Docker infrastructure
- Leveraging Kubernetes on AWS EKS to establish a robust, scalable production environment

## Technical Stack
### Storage & Processing
- HDFS ecosystem for data persistence
- Pyspark framework for efficient data manipulation

### Model Development & Serving
- TensorFlow as the core deep learning framework
- Flask for RESTful API implementation
- TensorFlow Serving to optimize model performance in production

### Infrastructure & Deployment
- Docker for application containerization
- Kubernetes for container orchestration and scaling
- AWS EKS providing managed Kubernetes infrastructure

## Model

The project uses a deep learning model built using Keras to predict the engagement score. The model is then exported for TensorFlow Serving.

Steps:
1. Train and save the model in TensorFlow SavedModel format.
2. Use TensorFlow Serving to serve the model.
3. Create a Flask API to send input to TensorFlow Serving and return predictions.

---

## Repository Structures

   ```
   ├── README.md                                
   ├── config                                    
   │   ├── kube-deployment.yaml
   │   ├── kube-service.yaml
   │   ├── eks-deployment.yaml
   │   ├── eks-service.yaml
   ├── src                                       
   │   ├── train_model.py
   │   ├── predict_model.py
   │   ├── notebook.ipynb
   │   ├── EDA.ipynb
   ├── build-docker-image.md                      
   ├── kubectl-apply.md                          
   ├── Dockerfile                                
   ├── saved_model                               # Final saved model
   │   ├── assets
   │   ├── fingerprint.pb
   │   ├── saved_model.pb
   │   └── variables
   │       ├── variables.data-00000-of-00001
   │       └── variables.index
   ├── tokenizer.pkl                            

   ```

---
## Infrastructure Design
### Model Serving Layer
- Model preparation involves converting trained Keras models into TensorFlow's SavedModel standard
- Dedicated TensorFlow Serving instances handle prediction requests through RESTful endpoints

### Application Layer
- Custom Flask microservice routes client requests to model servers
- Dockerized application components ensure consistent deployment environments

### Orchestration Strategy
- Kubernetes manages container lifecycle and scaling
  - Handles service discovery and load balancing
  - Enables automated rollouts and rollbacks
  - Supports both local development and cloud deployment

### Cloud Infrastructure
- AWS EKS provides enterprise-grade Kubernetes management
  - Automated control plane operations
  - Integrated monitoring and logging
  - Dynamic scaling based on demand
--

## How to Run the Project
### Steps

1. Clone this repository
   ```
   git clone https://github.com/blecktita/prediction-client-engagement.git
   ```
   
2. Model Training and Saving

   Run the model training script and save the model in TensorFlow SavedModel format:

   ```
   cd prediction-client-engagement
   python src/train_model.py
   ```

3. Start Flask API
   ```
   python src/predict_model.py
   ```
   
4. Test model prediction via API (server port 5000:5000)

   Open new terminal.
   
   ```
   ./curl-api.sh
   ```
   
5. Build Docker Images with TensorFlow Serving   

   ```
   docker build -t prediction-client-engagement .
   ```

6. Create and Run Container
   ```
   docker run -p 8501:8501 --name tensorflow-serving prediction-client-engagement
   ```

7. Deploy TensorFlow Serving on Kubernetes

   - Register docker image with kind
     ```
     kind load docker-image prediction-client-engagement:latest
     ```
     
   - Apply deployment and service
     ```
     kubectl apply -f kube-deployment.yaml
     kubectl apply -f kube-service.yaml
     ```

   - kubectl (get pods, services, all)
     ```
     kubectl get pods
     kubectl get services
     kubectl get all
     ```  
     The pod should be Ready (1/1) and Status (Running).

   - Test TensorFlow Serving Model Prediction (server port 5002:8501)
     ```
     ./curl-kube.sh
     ```   

9. Deploy TensorFlow Serving on AWS EKS
   - Authenticate Docker to AWS ECR, use the AWS CLI to authenticate Docker client
       ```
       aws ecr get-login-password --region eu-south-2 | docker login --username AWS --password-stdin 847392156084.bt.ecr.eu-south-2.amazonaws.com
       ```
       
   - Create repository
       ```
       aws ecr create-repository --repository-name prediction-client-engagement
       ```
       
   - Tag image to AWS
      ```
      docker tag prediction-client-engagement 847392156084.bt.ecr.eu-south-2.amazonaws.com/prediction-client-engagement:latest
      ```
      
   - Push image
      ```
      docker push 847392156084.bt.ecr.eu-south-2.amazonaws.com/prediction-client-engagement:latest
      ```
      
   - Configure AWS CLI and EKS
      ```
      aws configure
      ```
      
   - Create AWS EKS Cluster
      ```
      eksctl create cluster \
        --name tf-serving-cluster \
        --region eu-south-2 \
        --nodegroup-name tf-serving-nodes \
        --nodes 2 \
        --node-type t3.medium \
        --managed
      ```
   - Deploy container to AWS:
       ```
       kubectl apply -f eks-deployment.yaml
       kubectl apply -f eks-service.yaml
       ```
       
    - Check nodes
       ```
       kubectl get nodes
       ```
       
    - Check all status (pod, services, deployment)
       ```
       kubectl get all
       ```
       
---

## API Usage

- Endpoint

  POST /predict

- Input

  A JSON payload containing the following field:

  text: The tweet content.

  Example input:

  ```
  {
  "text": "Black Friday Doorbusters: 70% off Electronics!"
  }
  ```

- Output

  The API returns a prediction:

  ```
  {
  "prediction": [[312.45983123779297]]
  }
  ```


---

## Results

The model successfully predicts the engagement score for a tweet. For example:

Input: "Huge Prime Day Deals at Amazon!"
Output: 367.41

This score can be interpreted as the expected combination of likes, replies, and retweets.

---


