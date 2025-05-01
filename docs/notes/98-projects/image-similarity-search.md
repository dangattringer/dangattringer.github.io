---
title: Image Similarity Search
author: "Daniel Gattringer"
description: ""
draft: false
sidebar_position: 1
---

# ML Platform for Image Similarity Search

:::note
Work in Progress  
These notes are a work in progress and may not be complete or fully accurate. They are intended for personal use and reference.
Content is added and updated regularly.
:::

## Project Goal

To design, build, and deploy a cloud-native platform that allows users to upload an image and find similar images within a large, dynamically updated dataset. This involves scalable training infrastructure for embedding models and a robust inference service, all managed via IaC and CI/CD.

## Core Scenario

1. Users upload images via a simple web interface or API.
2. A batch training pipeline periodically retrains an image embedding model (e.g., using contrastive learning like SimCLR) on an evolving dataset stored in cloud storage.
3. The trained model is used by an inference service to generate embeddings for new uploads and existing dataset images.
4. An approximate nearest neighbor (ANN) index (like Faiss) is built/updated using these embeddings.
5. The inference service takes an uploaded image, generates its embedding, queries the ANN index, and returns the most similar images.
