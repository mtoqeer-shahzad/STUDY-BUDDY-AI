# 🎯 Study Buddy AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)

**AI-powered quiz generator — MCQs & Fill-in-the-Blanks, generated live via Groq's LLaMA 3.3 70B**

[Features](#-features) • [Project Structure](#-project-structure) • [Installation](#-installation) • [Docker](#-docker) • [Kubernetes](#-kubernetes-deployment) • [CI/CD](#-cicd-pipeline)

</div>

---

## 📌 Overview

**Study Buddy AI** is an intelligent learning assistant that generates custom quizzes on any topic using **LLaMA 3.3 70B** via **Groq's ultra-fast inference API**. It supports Multiple Choice Questions (MCQ) and Fill-in-the-Blank formats with Easy / Medium / Hard difficulty levels, real-time evaluation, and CSV export.

Built with a full **MLOps pipeline** — Jenkins CI, Argo CD GitOps, Docker, and Kubernetes — for production-grade deployment.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI-Powered Questions | LLaMA 3.3 70B via Groq — ultra-fast inference |
| 📝 Question Types | Multiple Choice & Fill in the Blank |
| 📊 Difficulty Levels | Easy / Medium / Hard |
| 🎯 Real-time Evaluation | Instant scoring with detailed breakdown |
| ⬇️ Export Results | Download quiz results as CSV |
| 🌐 Streamlit UI | Clean cyberpunk dark theme interface |
| 🐳 Dockerized | Fully containerized for any environment |
| ☸️ Kubernetes Ready | Deploy with a single `kubectl apply` |
| 🔄 Jenkins CI | Auto build & push on every commit |
| 🚀 Argo CD GitOps | Auto sync & deploy on Docker Hub update |

---

## 📁 Project Structure

```
STUDY_BUDDY_AI/
│
├── application.py                  # Main Streamlit UI
├── Dockerfile                      # Container config
├── requirements.txt                # Python dependencies
├── .env                            # API keys (not committed)
│
├── src/
│   ├── generator/
│   │   └── question_generator.py   # LLM question generation logic
│   ├── prompts/
│   │   └── templates.py            # LangChain prompt templates
│   ├── schema/
│   │   └── models.py               # Pydantic data models
│   └── utils/
│       └── helper.py               # QuizManager & helpers
│
└── k8s/
    ├── deployment.yaml             # Kubernetes Deployment
    └── service.yaml                # Kubernetes Service (NodePort)
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- Docker Desktop
- Groq API Key → [console.groq.com](https://console.groq.com)

### 1. Clone the Repository

```bash
git clone https://github.com/mtoqeer-shahzad/STUDY_BUDDY_AI.git
cd STUDY_BUDDY_AI
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run Locally

```bash
streamlit run application.py
```

App will open at → `http://localhost:8501`

---

## 🐳 Docker

### Build Image

```bash
docker build -t study-buddy-ai:latest .
```

### Run Container

```bash
docker run -p 8501:8501 --env-file .env study-buddy-ai:latest
```

### Push to Docker Hub

```bash
docker tag study-buddy-ai:latest your-dockerhub-username/study-buddy-ai:latest
docker push your-dockerhub-username/study-buddy-ai:latest
```

---

## ☸️ Kubernetes Deployment

### Prerequisites

- Minikube or any K8s cluster
- kubectl installed

### Deploy

```bash
# Start Minikube (if local)
minikube start

# Create namespace
kubectl create namespace study-buddy

# Apply manifests
kubectl apply -f k8s/deployment.yaml -n study-buddy
kubectl apply -f k8s/service.yaml -n study-buddy

# Check status
kubectl get pods -n study-buddy
kubectl get svc -n study-buddy
```

### Access App

```bash
# Minikube
minikube service study-buddy-service -n study-buddy

# Cloud (LoadBalancer) — use EXTERNAL-IP:8501
kubectl get svc study-buddy-service -n study-buddy
```

---

## 🔄 CI/CD Pipeline

### Architecture

```
GitHub Push
    │
    ▼
Jenkins CI
    ├── Pull Code
    ├── Build Docker Image
    ├── Run Tests
    └── Push to Docker Hub
              │
              ▼
          Argo CD (GitOps)
              ├── Detect Image Update
              ├── Sync with Git Repo
              └── Deploy to Kubernetes ✅
```

### Jenkins — Jenkinsfile

```groovy
pipeline {
    agent any
    environment {
        IMAGE_NAME = "your-dockerhub-username/study-buddy-ai"
        IMAGE_TAG  = "latest"
    }
    stages {
        stage('Clone') {
            steps { git 'https://github.com/mtoqeer-shahzad/STUDY_BUDDY_AI.git' }
        }
        stage('Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh "docker login -u $DOCKER_USER -p $DOCKER_PASS"
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
    }
}
```

### Argo CD Setup

```bash
# Install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

Point Argo CD Application to your Git repo and `k8s/` folder. It will **auto-sync** every time a new image is pushed and the manifest is updated.

---

## 📦 Requirements

```txt
streamlit
langchain
langchain-groq
langchain-core
python-dotenv
groq
pydantic
pandas
```

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key from console.groq.com | ✅ Yes |

---

## 🧠 How It Works

```
User → Topic + Difficulty + Question Type
              │
              ▼
    LangChain Prompt Template
              │
              ▼
      Groq API → LLaMA 3.3 70B
              │
              ▼
    Pydantic Schema Validation
              │
              ▼
    QuizManager → Streamlit UI
              │
              ▼
  Answers → Score + Breakdown + CSV Export
```

---

## 📊 Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | LLaMA 3.3 70B (via Groq) |
| **Orchestration Framework** | LangChain |
| **UI** | Streamlit |
| **Data Validation** | Pydantic |
| **Containerization** | Docker |
| **Container Orchestration** | Kubernetes |
| **CI** | Jenkins |
| **CD** | Argo CD (GitOps) |
| **Language** | Python 3.10+ |

---

## 👨‍💻 Author

**Muhammad Toqeer Shahzad**  
Data Scientist | ML Engineer | LLM & GenAI Developer | MLOps Engineer

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/mtoqeer-shahzad)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/mtoqeer-shahzad)

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">
Made with ❤️ using Groq × LLaMA 3.3 × LangChain
</div>
