---
sidebar_label: Image Generation
title: Image Generation
author: "Daniel Gattringer"
description: From Noise to Structure
draft: false
datePublished: 2025-08-01
sidebar_position: 1
---

# Image Generation

import DocCardList from '@theme/DocCardList';

Image generation is a fascinating area of AI that transforms random noise into images.

Of course. It's a fascinating and rapidly evolving field. Focusing on the mathematical fundamentals is an excellent approach, as it provides a solid foundation for understanding *why* these models work, not just *how*.

Here is a proposed learning path that we can follow. It's designed to build from foundational principles to the sophisticated architectures you see in models like Stable Diffusion 3. It intentionally bypasses GANs to focus on diffusion and flow-based models, which are at the core of current research.

**Part 1: The Foundations of Probabilistic Generative Modeling**
*   **Topic 1: The Core Idea: Learning a Data Distribution.** We'll start with the central goal: how can a model learn to represent the complex probability distribution of natural images, p(x)? We'll touch on concepts like maximum likelihood estimation (MLE) and why modeling p(x) directly is so challenging.
*   **Topic 2: Latent Variable Models.** We will introduce the concept of a latent space (a simpler, often lower-dimensional space) and how we can use a variable **z** to help model our complex data **x**. This is the foundation for almost all modern generative models.

**Part 2: Diffusion Models - From Noise to Structure**
*   **Topic 3: The Forward Process (Diffusion).** We will explore the elegant mathematical formulation of systematically and slowly adding Gaussian noise to an image until it becomes pure noise. We'll cover the Markov chain property and the closed-form solution for any timestep.
*   **Topic 4: The Reverse Process (Denoising).** This is the generative part. We'll cover how a neural network can learn to reverse the diffusion process, starting from noise and progressively denoising it to generate a clean image. We'll focus on the objective function (a variant of the evidence lower bound, or ELBO) and how it simplifies to a simple noise prediction task.
*   **Topic 5: Sampling and Guidance.** With a trained model, how do we generate images? We'll look at the sampling loop (e.g., DDPM, DDIM) and the introduction of classifier-free guidance, which is critical for controlling image generation with text prompts.

**Part 3: Flow-Based Models & The Rise of Flow Matching**
*   **Topic 6: Normalizing Flows.** We'll introduce a different family of models built on the principle of invertible transformations. We'll cover the change of variables formula and the role of the Jacobian determinant in calculating exact likelihoods.
*   **Topic 7: Continuous Normalizing Flows (CNFs) & The Connection to ODEs.** We'll move from discrete transformations to continuous ones, reframing generative modeling as learning a vector field (an Ordinary Differential Equation) that transports noise into data.
*   **Topic 8: Flow Matching.** This is a more recent and highly efficient training paradigm. We'll discuss how Flow Matching simplifies the training of CNFs by directly regressing a target vector field, avoiding the need for complex simulations during training. We will specifically look at Rectified Flows, which create straight-line paths between noise and data, simplifying the transport process significantly.

**Part 4: Modern Architectures - The Transformer Era**
*   **Topic 9: Diffusion Transformers (DiT).** We'll analyze why the field moved from U-Net architectures to Transformers for the denoising backbone. We will discuss how Transformers operate on latent patches and their scalability.
*   **Topic 10: Multi-Modal Architectures (e.g., MM-DiT).** This brings us to the state-of-the-art, like the architecture in Stable Diffusion 3. We'll examine how models like the Multi-Modal Diffusion Transformer (MM-DiT) use separate transformer-based pathways for different modalities (like text and image latents) and combine them effectively.

