# 🚀 TaskFlow
A full-stack task management web application built with Python, Flask, and SQLite — featuring a clean, modern UI and complete CRUD functionality.
## 📋 Overview
TaskFlow lets users create, categorize, complete, and delete tasks through a simple and responsive web interface. This project was built as a hands-on learning exercise in full-stack web development and is part of an ongoing journey to build a complete DevOps pipeline (containerization, CI/CD, and cloud deployment).
## ✨ Features
- Add tasks with custom categories (General, Work, Personal, Urgent)
- Mark tasks as complete/incomplete
- Delete tasks
- Real-time task statistics (Total, Pending, Completed)
- Persistent storage using SQLite database
- Clean, responsive, modern UI
## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML, CSS (custom design)
## 🚀 Getting Started
### Prerequisites
- Python 3.x installed
### Installation
git clone https://github.com/ImadUdDin18/TaskFlow.git
cd TaskFlow
pip install flask flask-sqlalchemy
python app.py
Then open `http://127.0.0.1:5000` in your browser.
## 📌 Roadmap
This project is being progressively extended to cover a complete DevOps workflow:
- [x] Application development (Flask + SQLite)
- [x] Version control (Git + GitHub)
- [x] Containerization (Docker)
- [x] Cloud deployment (AWS)
- [x] CI/CD pipeline (GitHub Actions)
- [x] Infrastructure as Code (Terraform)
- [x] Container Orchestration (Kubernetes)
## 🏗️ Infrastructure as Code (Terraform)

This project uses **Terraform** to manage AWS infrastructure declaratively, instead of manual console configuration.

**What it does:**
- Manages the EC2 instance (`t3.micro`) hosting the TaskFlow application
- Defines provider, instance type, security group, subnet, and IAM role as code
- Enables reproducible, version-controlled infrastructure

**Files:**
- `terraform/provider.tf` — AWS provider configuration
- `terraform/main.tf` — EC2 instance resource definition

**Key commands used:**
```bash
terraform init
terraform import aws_instance.taskflow_server <instance-id>
terraform plan
terraform apply

## Container Orchestration (Kubernetes)

This project uses **Kubernetes (Minikube)** to run the TaskFlow app as a container-orchestrated deployment.

**What it does:**
- Runs the TaskFlow app as a Kubernetes Deployment with 2 replicas for basic load distribution
- Exposes the app via a NodePort Service for external access
- Uses the locally built Docker image (	askflow-app:latest) loaded directly into the Minikube cluster

**Files:**
- `k8s/deployment.yaml` � Deployment spec (replicas, container image, port)
- `k8s/service.yaml` � NodePort Service exposing the app on port 5000

**Key commands used:**
```bash
minikube start --driver=docker
minikube image load taskflow-app:latest
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
minikube service taskflow-service --url
## ?? Author
**Imad Ud Din**

