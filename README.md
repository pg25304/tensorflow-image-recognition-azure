# TensorFlow Image Recognition on Azure

An end-to-end AI and cloud computing project that builds, evaluates, containerises, and deploys an image-recognition model using **TensorFlow, Keras, FastAPI, Docker, Azure Container Registry, and Azure Container Apps**.

## Project Overview

The objective of this project was to build my own image-recognition model and take it through the complete lifecycle:

**Dataset → Model Training → Evaluation → API → Docker → Azure Container Registry → Azure Container Apps → HTTPS Prediction**

The model was trained on the **CIFAR-10** dataset and deployed as a containerised REST API on Microsoft Azure.

## Architecture

```text
CIFAR-10 Images
       │
       ▼
TensorFlow / Keras CNN
       │
       ▼
Trained Keras Model
       │
       ▼
FastAPI REST API
       │
       ▼
Docker Container
       │
       ▼
Azure Container Registry
       │
       ▼
Azure Container Apps
       │
       ▼
HTTPS /predict Endpoint
```

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.12 | Application and model development |
| TensorFlow / Keras | CNN development, training and inference |
| CIFAR-10 | Image-recognition dataset |
| NumPy / Pillow | Image preprocessing |
| FastAPI / Uvicorn | REST API |
| Docker | Application containerisation |
| Azure Container Registry | Private container-image storage |
| Azure Container Apps | Serverless cloud deployment |
| Azure Managed Identity / RBAC | Secure ACR authentication |

## Model

The CNN contains:

- Conv2D layers for feature extraction
- MaxPooling layers for dimensionality reduction
- Flatten layer
- Dense hidden layer
- Softmax output layer for 10 CIFAR-10 classes

The model was trained for **5 epochs**.

### Evaluation

Final test accuracy:

**66.71%**

The trained model was saved as:

```text
image_classifier.keras
```

The saved model was then reloaded successfully before deployment.

## Local Image Recognition

The model was tested against unseen CIFAR-10 test data.

One visual test correctly produced:

```text
Predicted: ship
Actual: ship
```

This verified inference before introducing the API, Docker, or Azure layers.

## FastAPI

The trained model is exposed through a FastAPI application.

### Endpoints

```text
GET /
```

Returns a basic API status response.

```text
POST /predict
```

Accepts an uploaded image and returns a predicted CIFAR-10 class and model confidence.

Example cloud response:

```json
{
  "prediction": "ship",
  "confidence": 0.9247
}
```

## Docker

The application and trained model were packaged into a Docker image:

```text
tensorflow-image-api:1.0
```

The container exposes port `8000` and runs the FastAPI application using Uvicorn.

The container was tested locally before cloud deployment.

## Azure Deployment

The Docker image was pushed to a private **Azure Container Registry (ACR)**.

The application was then deployed to **Azure Container Apps** in the **UK South** region using the Consumption workload profile.

The deployment used:

- External HTTPS ingress
- Target port `8000`
- Minimum replicas: `0`
- Maximum replicas: `1`
- System-assigned managed identity
- `AcrPull` RBAC permission

The ACR administrator account was not required for the deployed application.

## Security

The Container App used a **system-assigned managed identity** to retrieve the private image from Azure Container Registry.

Only the required `AcrPull` role was assigned to the runtime identity.

This avoided embedding registry usernames or passwords in the application configuration.

Other security practices included:

- HTTPS ingress
- Private container registry
- Least-privilege registry access
- No credentials stored in source code
- Sensitive Azure identifiers excluded or redacted from public evidence

## Cloud Prediction Result

The deployed `/predict` endpoint was tested using `test_ship.png`.

Azure returned:

```text
HTTP 200 OK
Prediction: ship
Confidence: 0.9247
```

This confirmed successful end-to-end inference through the deployed cloud service.

## Resource Optimisation

Azure Container Apps was configured with:

```text
Minimum replicas: 0
Maximum replicas: 1
```

After inactivity, the application successfully **scaled to zero replicas**.

When a new HTTPS request arrived, Azure started a replica and served the application again.

This demonstrated demand-driven cloud resource allocation and reduced unnecessary idle compute.

## Troubleshooting

Several useful issues were encountered during implementation.

### PowerShell virtual-environment activation

PowerShell initially prevented execution of the virtual-environment activation script.

A process-scoped execution-policy change was used rather than making a permanent machine-wide change.

### TensorFlow GPU warning

TensorFlow reported that a compatible GPU runtime was unavailable.

GPU acceleration was unnecessary for this small educational model, so the project intentionally used CPU-based TensorFlow.

### Azure Container Apps target port

The installed Azure CLI/Container Apps extension did not accept `--target-port` with the original update command.

The deployment was completed by updating the container image first and then configuring ingress separately:

```text
az containerapp ingress update ... --target-port 8000
```

## Project Structure

```text
TensorFlow-Image-Recognition/
├── app.py
├── train_model.py
├── predict.py
├── image_classifier.keras
├── test_ship.png
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

## Limitations

This project is an educational AI/cloud implementation rather than a production image-recognition service.

The model achieved **66.71% test accuracy**, so significant improvement would be required for production use.

CIFAR-10 images are only 32×32 pixels. Arbitrary uploaded photographs are resized to this format, meaning real-world performance is not established by the CIFAR-10 test result.

The reported confidence is the model's softmax output and should not be interpreted as a guarantee that a prediction is correct.

## Future Improvements

Possible extensions include:

- Data augmentation
- Deeper CNN architectures
- Transfer learning
- Confusion-matrix and per-class evaluation
- API authentication
- Rate limiting and upload-size validation
- Automated CI/CD
- Infrastructure as Code
- Load testing with multiple replicas
- Cloud monitoring and alerting

## Cloud Resource Cleanup

After successful deployment, testing, and evidence collection, the Azure resource group was deleted.

This removed the Azure Container App, Container Apps Environment, Azure Container Registry, and associated logging resources, preventing unnecessary ongoing cloud-resource consumption.

The source code, trained model, documentation, and implementation evidence remain available in this repository.

## Author

**Payman G.**

MSc Cybersecurity  
University of Essex Online

## Purpose

This project was completed as part of my practical study of **AI and Cloud Computing** and is also maintained as professional portfolio evidence of hands-on experience with machine learning, containerisation, cloud deployment, identity-based access control, and cloud resource optimisation.