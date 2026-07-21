# TaskFlow

**A cloud-native task management web app — built, containerized, and deployed end-to-end using a full DevOps pipeline.**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20CloudWatch-FF9900?logo=amazonaws&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5?logo=kubernetes&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)

---

## About

TaskFlow is a full-stack task management application built to demonstrate a complete, production-style DevOps workflow — from writing the application code to deploying and monitoring it in the cloud. Every stage of the software delivery lifecycle is covered: development, containerization, automated deployment, infrastructure as code, orchestration, and monitoring.

## Features

- Full CRUD functionality for managing tasks (create, read, update, delete)
- Clean, responsive user interface
- RESTful backend built with Flask and SQLAlchemy
- Persistent data storage
- Fully containerized for consistent environments across dev, staging, and production

## Architecture & Workflow

```
Developer Push (main branch)
        │
        ▼
GitHub Actions CI/CD Pipeline
   (build → test → health check)
        │
        ▼
Docker Image Build
        │
        ▼
Deployment to AWS EC2 (static Elastic IP)
        │
        ▼
CloudWatch Alarms + SNS Email Alerts
   (real-time downtime detection)

Parallel Track:
Terraform (Infrastructure as Code) → provisions & manages AWS resources
Kubernetes (Minikube) → orchestrates the app with a 2-replica Deployment + NodePort Service
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, SQLAlchemy |
| Containerization | Docker |
| Orchestration | Kubernetes (Minikube, kubectl) |
| CI/CD | GitHub Actions |
| Cloud | AWS (EC2, VPC, IAM, S3, CloudWatch, Elastic IP) |
| Infrastructure as Code | Terraform |
| Monitoring & Alerting | AWS CloudWatch, SNS |

## CI/CD Pipeline

Every push to `main` automatically triggers the GitHub Actions pipeline, which:
1. Builds and tests the application
2. Builds the Docker image
3. Runs a pipeline health check — a faulty build is blocked and will **not** be deployed
4. Deploys the update to the live EC2 instance with zero downtime

## Infrastructure as Code

AWS infrastructure is provisioned and version-controlled with Terraform (`main.tf`, `provider.tf`), including provider configuration and state management of existing resources — no manual console changes required to reproduce the environment.

## Monitoring & Alerting

CloudWatch alarms are configured to continuously monitor application health. If the app goes down, an **SNS email alert** is sent immediately, enabling fast response before users are impacted.

## Getting Started (Local Setup)

```bash
# Clone the repository
git clone https://github.com/ImadUdDin18/TaskFlow.git
cd TaskFlow

# Build and run with Docker
docker build -t taskflow .
docker run -p 5000:5000 taskflow
```

The app will be available at `http://localhost:5000`.

## Roadmap

- [ ] Add Prometheus + Grafana monitoring stack
- [ ] Introduce an Application Load Balancer with Auto Scaling for high availability
- [ ] Add automated rollback on failed deployments

## Connect

- **GitHub:** [github.com/ImadUdDin18](https://github.com/ImadUdDin18)
- **LinkedIn:** [linkedin.com/in/imad-ud-din-8a4004295](https://linkedin.com/in/imad-ud-din-8a4004295)
- **Email:** iamimaduddin20@gmail.com

---

*Built by Imad Ud Din — Trainee DevOps Engineer*
