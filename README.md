# CI/CD Final Project: Continuous Integration and Delivery for Accounts Service

[![CI Build](https://github.com/tiger638900/ci-cd-final-project/actions/workflows/workflow.yml/badge.svg)](https://github.com/tiger638900/ci-cd-final-project/actions/workflows/workflow.yml)

## Project Overview

This repository contains the completed final project for the **Continuous Integration and Continuous Delivery (CI/CD)** course as part of the IBM DevOps and Software Engineering program. It demonstrates an automated end-to-end CI/CD delivery pipeline for the **Accounts Service** RESTful application built with Python and Flask.

### Core CI/CD Highlights
- **Automated Continuous Integration (GitHub Actions)**:
  - Automates code quality verification on push and pull requests to `main`.
  - Static code analysis and style linting using `flake8`.
  - Automated unit testing and code coverage using `nose` (`nosetests`).
- **Cloud-Native Continuous Delivery (Tekton & OpenShift Pipelines)**:
  - Modular Tekton tasks defined in `.tekton/tasks.yml` (`cleanup`, `git-clone`, `flake8`, `nose`, `buildah`, `deploy`).
  - Declarative pipeline defined in `.tekton/pipeline.yaml` deployed on Red Hat OpenShift.
  - Persistent volume claim (`oc-lab-pvc`) dynamically provisioned with `skills-network-learner` storage class and 1GB requested capacity.
  - Containerization using non-root security principles exposing the service on port `8000`.

---

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── workflow.yml          # GitHub Actions CI workflow (flake8 lint & nose test)
├── .tekton/
│   ├── tasks.yml                 # Tekton Tasks (cleanup, flake8, nose, buildah, deploy)
│   └── pipeline.yaml             # Tekton CD Pipeline definition
├── k8s/
│   ├── deployment.yaml           # Kubernetes/OpenShift Deployment on port 8000
│   └── service.yaml              # Kubernetes/OpenShift Service definition
├── service/
│   ├── common/                   # Error handlers, log handlers, HTTP status constants
│   ├── models.py                 # Account data model & database persistence
│   ├── routes.py                 # RESTful CRUD API endpoints
│   └── __init__.py               # Flask app initialization, Talisman, CORS & logging
├── tests/
│   ├── test_models.py            # Unit tests for Account model
│   └── test_routes.py            # Unit tests for REST API endpoints
├── cicd-github-validate          # Terminal log of successful GitHub Actions workflow
├── oc-pipeline-application-logs  # OpenShift pod runtime application logs on port 8000
├── Dockerfile                    # Multi-stage container build running on port 8000
├── requirements.txt              # Application and testing dependencies
└── setup.cfg                     # Flake8 and Nose test configuration
```

---

## Continuous Integration Workflow (.github/workflows/workflow.yml)

The GitHub Actions workflow triggers on every `push` and `pull_request` to `main`:
1. **Lint with flake8**: Enforces code style, syntax constraints, and flake8 standards.
2. **Run unit tests with nose**: Runs all test suites with spec formatting and code coverage reporting.

---

## Continuous Delivery Pipeline (.tekton/pipeline.yaml)

The OpenShift Tekton pipeline executes the following sequential tasks:
1. `cleanup`: Cleans up the workspace to ensure an idempotent environment.
2. `git-clone`: Clones the latest commit from the repository.
3. `flake8`: Runs code linter across application and test suites.
4. `nose`: Executes unit tests to validate functionality.
5. `buildah`: Builds the container image and pushes to the OpenShift image registry.
6. `deploy`: Applies Kubernetes manifests and rolls out the deployment on port 8000.

---

## Application Verification

- **Endpoint**: `/accounts`
- **Port**: `8000`
- **Health / Root**: `GET /` returns status information and API metadata.
