# 🚀 TaskFlow

*A cloud-native task management web app — built, containerized, and deployed end-to-end using a full DevOps pipeline.*



![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)




![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)




![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)




![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)




![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)




![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)




![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)



### 🔗 [*Live Demo → 3.232.63.140*](http://3.232.63.140)

---

## 📖 About

TaskFlow is a full-stack task management application built to demonstrate a complete, *production-style DevOps workflow* — from writing the application code to deploying and monitoring it in the cloud. Every stage of the software delivery lifecycle is covered: development, containerization, automated deployment, infrastructure as code, orchestration, and monitoring.

---

## ✨ Features

*Task Management*
- ✅ Full CRUD functionality (create, read, update, delete)
- ✅ Inline task editing — double-click any task to edit instantly
- 🎯 Priority levels (High / Medium / Low) with color-coded badges
- 📅 Due dates with automatic overdue highlighting
- 🏷️ Tags/labels system for flexible organization
- ⚡ One-click task templates — Meeting, Bug Fix, Content
- 🔍 Live search and filtering (All / Pending / Completed)

*UI/UX*
- 🎨 Clean, modern SaaS-style dashboard with sidebar navigation
- 🌗 Dark mode / Light mode toggle
- 🔔 Toast notifications for every action
- ⚠️ Delete confirmation to prevent accidental removal

*Analytics*
- 📊 Weekly completed-tasks chart (Chart.js)

*Reliability & Monitoring*
- 🛡️ Custom 404 and 500 error pages
- 📝 Structured error logging (app_errors.log)
- 💓 /health endpoint for uptime monitoring
- ✔️ Input validation on all forms

---
'''
## 🏗️ Architecture & Workflow
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
---
'''
## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| *Backend* | Python, Flask, SQLAlchemy |
| *Frontend* | HTML, CSS, Vanilla JS, Chart.js |
| *Containerization* | Docker |
| *Orchestration* | Kubernetes (Minikube, kubectl) |
| *CI/CD* | GitHub Actions |
| *Cloud* | AWS (EC2, VPC, IAM, S3, CloudWatch, Elastic IP) |
| *IaC* | Terraform |
| *Monitoring* | AWS CloudWatch, SNS, custom health checks |

---

## ⚙️ CI/CD Pipeline

Every push to main automatically triggers the GitHub Actions pipeline, which:

1. 🔨 Builds and tests the application
2. 🐳 Builds the Docker image
3. 🧪 Runs a pipeline health check — a faulty build is blocked and will not be deployed
4. 🚀 Deploys the update to the live EC2 instance with *zero downtime*

---

## 🌍 Infrastructure as Code

AWS infrastructure is provisioned and version-controlled with Terraform (main.tf, provider.tf) — no manual console changes required to reproduce the environment.

---

## 📡 Monitoring & Alerting

CloudWatch alarms continuously monitor application health. If the app goes down, an *SNS email alert* is sent immediately, enabling fast response before users are impacted. A /health endpoint and structured error logging support early failure detection at the application level.

---

## 🚦 Getting Started (Local Setup)

Clone the repository:
git clone https://github.com/ImadUdDin18/TaskFlow.git
cd TaskFlow

Install dependencies:
pip install -r requirements.txt

Run the app:
python app.py

App runs at http://localhost:5000

### 🐳 Docker

docker build -t taskflow .
docker run -p 5000:5000 taskflow

---

## 🗺️ Roadmap

- [ ] Prometheus + Grafana monitoring stack
- [ ] Application Load Balancer with Auto Scaling
- [ ] Automated rollback on failed deployments
- [ ] User authentication (login/register)
- [ ] Kanban board view

---

## 📫 Connect

- *GitHub:* [github.com/ImadUdDin18](https://github.com/ImadUdDin18)
- *LinkedIn:* [linkedin.com/in/imad-ud-din-8a4004295](https://linkedin.com/in/imad-ud-din-8a4004295)
- *Email:* iamimaduddin20@gmail.com

---

<p align="center">Built with ☕ and 🐳 by <b>Imad Ud Din</b> — Trainee DevOps Engineer</p>
