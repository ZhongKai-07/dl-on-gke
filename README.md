# Deep Learning on GKE

This project demonstrates how to perform deep learning training and inference on Google Kubernetes Engine (GKE) using a simple MNIST classifier.

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and configured
- Docker installed locally (for building images)

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/dl-on-gke.git
   cd dl-on-gke
   ```

2. Set your Google Cloud project ID:
   ```
   export PROJECT_ID=your-project-id
   ```

3. Enable the necessary APIs:
   ```
   gcloud services enable container.googleapis.com
   ```

4. Create a GKE cluster:
   ```
   gcloud container clusters create dl-cluster --num-nodes=3 --zone=us-central1-a --machine-type=n1-standard-4 --accelerator type=nvidia-tesla-k80,count=1
   ```

5. Configure `kubectl` to use the new cluster:
   ```
   gcloud container clusters get-credentials dl-cluster --zone=us-central1-a
   ```

## Building and Pushing Docker Images

1. Build the training image:
   ```
   docker build -t gcr.io/$PROJECT_ID/mnist-training:latest -f Dockerfile.train .
   ```

2. Build the inference image:
   ```
   docker build -t gcr.io/$PROJECT_ID/mnist-inference:latest -f Dockerfile.inference .
   ```

3. Push the images to Google Container Registry:
   ```
   docker push gcr.io/$PROJECT_ID/mnist-training:latest
   docker push gcr.io/$PROJECT_ID/mnist-inference:latest
   ```

## Running the Training Job

1. Update the `kubernetes/training-job.yaml` file, replacing `[PROJECT_ID]` with your actual project ID.

2. Apply the training job:
   ```
   kubectl apply -f kubernetes/training-job.yaml
   ```

3. Monitor the job:
   ```
   kubectl get jobs
   kubectl logs job/mnist-training
   ```

## Deploying the Inference Service

1. Update the `kubernetes/inference-deployment.yaml` file, replacing `[PROJECT_ID]` with your actual project ID.

2. Apply the inference deployment and service:
   ```
   kubectl apply -f kubernetes/inference-deployment.yaml
   ```

3. Get the external IP of the service:
   ```
   kubectl get services mnist-inference-service
   ```

## Testing the Inference Service

You can test the inference service using `curl` or any HTTP client. Here's an example using Python:

```python
import requests
import numpy as np

# Generate a random 28x28 image
image = np.random.rand(28, 28).tolist()

# Send a POST request to the inference service
response = requests.post('http://<EXTERNAL_IP>/predict', json={'image': image})

# Print the prediction
print(response.json())
```

Replace `<EXTERNAL_IP>` with the external IP of your service.

## Cleaning Up

To avoid incurring charges, delete the resources when you're done:

1. Delete the GKE cluster:
   ```
   gcloud container clusters delete dl-cluster --zone=us-central1-a
   ```

2. Delete the container images:
   ```
   gcloud container images delete gcr.io/$PROJECT_ID/mnist-training:latest
   gcloud container images delete gcr.io/$PROJECT_ID/mnist-inference:latest
   ```
