---
title: Introduction to Docker
author: "Daniel Gattringer"
description: ""
date: 2025-03-29
tags: ["Docker"]
page: 1
---

# Introduction to Docker


## ⚙️ Problem Statement: Environment Inconsistency in ML

  

Machine Learning development and deployment often face significant challenges related to environment consistency:


1. **"Works on my machine" syndrome:** Models or data pipelines developed locally fail in testing, staging, or production due to differences in operating systems, library versions (Python, system libraries like CUDA/cuDNN), or configurations.

2. **Dependency Hell:** Managing complex dependencies (e.g., specific versions of TensorFlow, PyTorch, Pandas, CUDA drivers) across different projects and team members becomes brittle and error-prone. Virtual environments (venv, conda) help locally but don't fully solve deployment consistency.

3. **Deployment Friction:** Packaging an ML application with all its dependencies for reliable deployment across various targets (bare metal, VMs, cloud, Kubernetes) is complex.
  

Docker addresses these issues by providing OS-level virtualization through **containers**, enabling consistent environments from development to production.

  

## 🛠 Technical Background: Core Docker Concepts

  
Understanding these core concepts is essential:

| Concept           | Description                                                                                                       | Analogy                   |
| :---------------- | :---------------------------------------------------------------------------------------------------------------- | :------------------------ |
| **Image**         | A read-only template containing the application code, runtime, system tools, libraries, and configurations.       | Blueprint for a house     |
| **Container**     | A runnable, isolated instance of an image. Executes the application within its own filesystem and process space.  | An actual built house     |
| **Dockerfile**    | A text file containing instructions (`FROM`, `COPY`, `RUN`, `CMD`, etc.) defining how to build a Docker image.    | Recipe/Construction Plan  |
| **Docker Engine** | The background service (daemon) that builds, runs, and manages containers.                                        | Construction Crew & Tools |
| **Docker Client** | The command-line interface (CLI) (`docker`) used to interact with the Docker Engine.                              | Site Foreman              |
| **Registry**      | A storage and distribution system for Docker images (e.g., Docker Hub, AWS ECR, GCP Artifact Registry, Azure CR). | Warehouse for Blueprints  |

  

## 🏗 Implementation Guide: Building and Running a Simple ML App Container

  

Let's containerize a basic Python script that uses `scikit-learn`.

  

**1. Project Structure:**

```bash
my_ml_app/
├── app.py
├── requirements.txt
└── Dockerfile
```
  

**2. `requirements.txt`:**


```txt
scikit-learn==1.3.2 # Use a specific version for reproducibility
numpy==1.26.2
pandas==2.1.3

```
