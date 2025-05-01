---
title: Image Restoration
author: "Daniel Gattringer"
description: ""
draft: false
sidebar_position: 3
---

# Service for Image Restoration

:::note
Work in Progress  
These notes are a work in progress and may not be complete or fully accurate. They are intended for personal use and reference.
Content is added and updated regularly.
:::

## Project Goal

To build, deploy, and monitor a highly optimized, scalable web service that uses a finetuned diffusion model for restoring degraded images (e.g., upscaling low-resolution images or removing artifacts like JPEG compression noise). The entire process, from model training/finetuning to production deployment and monitoring, will follow best practices outlined in the job description.

## Core Scenario

1. Users upload degraded images via a simple web interface or API.
2. A batch training pipeline periodically retrains a diffusion model on a dataset of degraded and high-quality images stored in cloud storage.
3. The trained model is used by an inference service to restore the uploaded images.
4. The inference service returns the restored images to the users.
5. The model is continuously improved based on user feedback and performance metrics.
