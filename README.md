# DevOps Capstone Project - Customer Accounts Microservice

[![CI Build](https://github.com/tiger638900/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/tiger638900/devops-capstone-project/actions/workflows/ci-build.yaml)

## Overview

This project implements a production-ready **Customer Accounts** RESTful microservice built with Python and Flask. It demonstrates end-to-end DevOps best practices including:
- **Agile Planning & Kanban**: User stories, estimation, sprint tracking.
- **Test-Driven Development (TDD)**: Comprehensive unit tests using `nosetests` and coverage analysis.
- **RESTful API**: Full CRUD operations (Create, Read, Update, Delete, List).
- **Application Security**: HTTP security headers using `Flask-Talisman` and Cross-Origin Resource Sharing (`Flask-CORS`).
- **Continuous Integration (CI)**: Automated GitHub Actions pipeline for linting (`flake8`, `pylint`) and automated unit testing.
- **Containerization**: Optimized multi-stage `Dockerfile` running as non-root user.
- **Continuous Deployment (CD)**: Automated deployment to Kubernetes/OpenShift via Tekton pipelines.

## Project Structure

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── user-story.md
│   └── workflows/
│       └── ci-build.yaml
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── service/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── common/
│       ├── error_handlers.py
│       ├── log_handlers.py
│       └── status.py
├── tests/
│   ├── __init__.py
│   ├── factories.py
│   ├── test_models.py
│   └── test_routes.py
├── Dockerfile
├── requirements.txt
├── setup.cfg
└── README.md
```

## Running the Service Locally

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   gunicorn --bind=0.0.0.0:8080 service:app
   ```

3. Run unit tests and code coverage:
   ```bash
   nosetests
   ```
