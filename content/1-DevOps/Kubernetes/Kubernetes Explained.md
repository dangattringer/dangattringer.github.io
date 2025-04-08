---
title: "K8s Explained"
author: "Daniel Gattringer"
description: ""
date: 2025-03-29
tags: ["kubernetes", "devops"]
page: 1
---

# Kubernetes Explained

> [!info] Work in Progress
> These notes are a work in progress and may not be complete or fully accurate. They are intended for personal use and reference.
> Content is added and updated regularly.

The official [Kubernetes website](https://kubernetes.io) defines it concisely as **Production-Grade Container Orchestration**:

<figure align="center">
  <img src="k8s-website.png" alt="Screenshot of the Kubernetes.io homepage showing the tagline 'Production-Grade Container Orchestration'">
  <figcaption>Kubernetes Website Homepage</figcaption>
</figure>

This phrase effectively captures Kubernetes' core purpose: it's a platform designed to automate the deployment, scaling, and management of containerized applications, specifically for reliable production environments.

It's important to understand that Kubernetes doesn't replace container runtimes like [[1-DevOps/Docker/index|Docker]]. Instead, it works *with* them. Kubernetes manages the **clusters** of machines (nodes) where these container runtimes are running, orchestrating the containers across the available infrastructure.

**The Need for Orchestration: From Monoliths to Microservices at Scale**

Managing production workloads has changed significantly. In the past, applications often ran as large **monoliths** on a few physical servers. Today, driven by cloud platforms (like AWS, Azure, GCP) and modern architecture patterns, applications are commonly built as **containerized microservices**. While containers offer portability and efficiency, deploying and managing them across potentially hundreds or thousands of virtual machines or instances introduces new challenges.

Imagine needing to deploy, update, monitor, and network a containerized application across 100 machines manually using basic `docker run` commands on each. This approach quickly becomes inefficient, error-prone, and doesn't scale.

**Kubernetes as the Solution**

This is precisely the problem Kubernetes solves. It acts as the "operating system" for your cluster, providing a unified **API** and control plane to manage containerized workloads across all the underlying machines (nodes). While Kubernetes itself is a complex system composed of multiple components (often running as microservices), it presents a coherent interface for managing your applications.

## Why Kubernetes is Key for DevOps and Production

Kubernetes directly addresses many critical challenges faced when running containers in production, making it a cornerstone technology for DevOps practices:

* **Automation:** Automates deployment rollouts and rollbacks, scaling, service discovery, load balancing, and self-healing, reducing manual intervention.
* **Scalability & Resource Management:** Allows applications to scale horizontally (adding more container instances) automatically or manually based on demand. Optimizes resource utilization across the cluster nodes.
* **High Availability:** Helps ensure applications remain accessible by automatically restarting failed containers, rescheduling them onto healthy nodes, and managing traffic distribution.
* **Consistent Environments:** Provides a consistent way to define and manage application deployments across different environments (dev, staging, prod).
* **Release Management:** Supports strategies like rolling updates and canary releases for safer application updates with minimal downtime.
* **Networking:** Offers built-in service discovery and load balancing, along with sophisticated network policies for isolating workloads.
* **Stateful Applications:** Provides primitives (like PersistentVolumes and StatefulSets) to manage applications that require persistent storage and stable network identities.
* **Configuration & Secret Management:** Allows secure injection and management of application configuration and sensitive data (like passwords or API keys).
* **Access Control (RBAC):** Implements Role-Based Access Control to define granular permissions for users and services interacting with the Kubernetes API.

By tackling these production-specific problems, Kubernetes enables teams to deploy and manage complex, containerized applications reliably and efficiently at scale.
