---
sidebar_label: "Mathematical Foundations"
title: "The Math of Generative AI: Learning Data Distributions"
author: "Daniel Gattringer"
description: " Discover the mathematical foundations of generative models. Learn how AI learns data distributions, overcomes intractable integrals, and uses latent variables in VAEs."
draft: false
datePublished: 2025-08-01
sidebar_position: 1
---

import ThemedAsset from '@site/src/components/ThemedAsset/ThemedAsset';

# The Math of Generative AI - Learning a Data Distribution

<details>
<summary>TL;DR</summary>

- Generative models aim to learn the underlying probability distribution of a dataset, like all "natural" images, which exist on a low-dimensional manifold within a high-dimensional space.
- A key challenge is the **intractable partition function**, an integral required to normalize the model's output into a true probability, which is computationally impossible for high-dimensional data like images.
- **Latent variable models** solve this by introducing a simpler, low-dimensional latent space (variable `z`) from which the complex data (`x`) is generated.
- **Variational Autoencoders (VAEs)** are a primary example, using an **encoder** to map data `x` to the latent space `z` and a **decoder** to reconstruct `x` from `z`.
- VAEs are trained by optimizing the Evidence Lower Bound (ELBO), which balances reconstruction accuracy with keeping the latent space well-organized.

</details>

At its heart, all generative modeling is about one thing: **learning to represent the probability distribution of data**. Let's call this true, underlying distribution $$p_{\text{data}}(x)$$.

Imagine the set of *all possible* $$512\times 512$$ pixel images. This is a space of staggering dimensionality $$(512 \cdot 512 \cdot 3 = 786,432)$$ dimensions for an RGB image. Almost every point in this space corresponds to meaningless static. However, a tiny, infinitesimally small fraction of this space contains images that we would recognize as "natural" pictures of cats, landscapes, people, etc.

These "natural images" aren't randomly scattered. They are highly structured and lie on what's known as a **low-dimensional manifold**. Think of a vast, empty three-dimensional room (the pixel space) where all the meaningful images lie on a complex, tangled 2D sheet of paper (the manifold).

The goal of a generative model, $$p_\theta(x)$$, is to learn the shape of this manifold. It should assign a high probability to any image $$x$$ that lies on or near this sheet of paper and a very low probability to any image far from it (i.e., static noise).

### The Manifold and the Probability Cloud

Imagine our dataset doesn't consist of images, but of simple 2D points $$(x_{1}, x_{2})$$ that lie perfectly on a circle with a radius of 2.

*   **The Data Space:** This is the entire 2D plane (ℝ²).
*   **The Manifold:** The manifold is the circle itself. It's a 1D curve living in a 2D space.
*   **The True Data Distribution $$p_{\text{data}}$$:** This distribution is zero everywhere *except* on the circumference of that circle. An ideal generative model would learn this perfectly.

Now, we train a neural network model, $$p_{\theta}$$, on points sampled from this circle. The model won't learn an infinitely thin, perfect circle. Instead, it will learn a **probability distribution that is concentrated around the circle**. Think of it as a "probabilistic doughnut" or a "probability cloud" that is thick and dense near the circle and rapidly fades to near-zero as you move away from it.

<figure align="center">
<ThemedAsset
  lightSource={require('./assets/generative_ai_manifold.png').default}
  darkSource={require('./assets/generative_ai_manifold.png').default}
  className="themed-image"
  alt="Diagram showing how an embedding model transforms unstructured data like text and images into high-dimensional vectors." />
  <figcaption>A diagram illustrating how different data types—text, images, audio—are converted into numerical vectors by an embedding model.</figcaption>
</figure>

On the left, we see the "ground truth" - the manifold where the data lives. On the right, we see what our trained model $$p_{\theta}$$ has learned. It has correctly identified the region of high probability.

### Connecting back to the Intractable Integral

Our model's network doesn't output the final, normalized probabilities you see on the color bar. It outputs an *unnormalized* value, let's call it $$q_\theta(x)$$. To get the true probability $$p_\theta(x)$$, we must compute:

$$
p_\theta(x) = \frac{q_\theta(x)}{\int q_\theta(x') dx'}
$$

For our 2D circle example, this integral means calculating the total "volume" under the entire probability surface across the whole 2D plane. This is computationally feasible for a 2D toy problem.

Now, scale this up to a $$512\times 512$$ RGB image. Our space is no longer 2D; it's $$786,432$$-dimensional. The integral is over all of those dimensions. This computation is not just slow; it is fundamentally impossible with current and foreseeable technology.

This is the wall that generative modeling research hit. We can define models that produce a score $$q_\theta(x)$$, but we can't turn that score into a proper probability $$p_\theta(x)$$ to use in our Maximum Likelihood objective function.

This is precisely the problem that latent variable models are designed to circumvent. They provide a clever "side door" to defining and optimizing $$p_\theta(x)$$ without ever having to calculate the partition function.


## How do we train such a model?

The classic approach is **Maximum Likelihood Estimation (MLE)**. Given a dataset of real images $$\{x_1, x_2, ..., x_N\}$$, we want to adjust our model's parameters $$\theta$$ (the neural network weights) to maximize the probability, or likelihood, that our model would have generated this data. Mathematically, we maximize the log-likelihood:

$$
L(\theta) = \sum log(p_\theta(x_i))
$$

$$
F=\int_{a}^{b} f(t)\,dt
$$

However, we immediately run into a critical problem. For most deep models, we can't easily define a normalized probability function $$p_\theta(x)$$. To be a valid probability distribution, the total probability over all possible images must sum to 1. This requires computing an integral over the entire 786,432-dimensional space:

$$
p_\theta(x) = \frac{q_\theta(x)}{\int q_\theta(x') dx'}
$$

The integral in the denominator, $$ \int q_\theta(x') dx' $$, is called the **partition function** or normalization constant. It is computationally intractable to compute for any non-trivial model.

This intractability is the central challenge that drives the design of modern generative models. Diffusion models and flow models are, in essence, highly ingenious methods for defining and training expressive probability distributions $$p_\theta(x)$$ while sidestepping the impossible task of computing this integral.

## Latent Variable Models

Since modeling $$p(x)$$ directly is too hard, we introduce a helper, or **latent variable**, which we'll call $$z$$. The core idea is to assume that our complex data $$x$$ is generated from this simpler, unobserved variable $$z$$.

Think of it like this:
*   $$x$$ is a final, detailed oil painting of a cat.
*   $$z$$ is a set of high-level instructions or a simple sketch: "A fluffy cat, sitting, facing left, looking curious."

It's much easier to work with the instructions ($$z$$) than with the millions of individual pixel values ($$x$$). We choose the *latent space* where $$z$$ lives to be very simple, typically a standard multivariate Gaussian distribution $$(N(0, I))$$.

### The Generative Process

This reframes our generative process into two steps:
1.  **Sample a latent code:** Draw a simple $$z$$ from a known prior distribution $$p(z)$$. For example, pick a random point from a standard Gaussian bell curve.
2.  **Decode the latent code:** Use a powerful neural network, called a **decoder** or **generator**, to map $$z$$ to a distribution over images. We denote this as $$p_\theta(x|z)$$.

Now, the probability of an image $$x$$ is the sum of probabilities of generating it from *all possible* latent codes $$z$$:

$$
p_\theta(x) = \int p_\theta(x|z) p(z) dz
$$

This might look like we've just swapped one integral for another, but we've gained a lot. We are no longer trying to define a complex function over the messy data space. Instead, we are learning a *mapping* from a simple, structured space ($$z$$) to the complex data manifold ($$x$$). The decoder's job is to learn this transformation.

### The New Problem: Training

We've defined a generative path ($$z \rightarrow x$$), but how do we train it? To compute the likelihood $$p_\theta(x)$$ for a real image $$x$$ from our dataset, we'd need to solve that integral over $$z$$. This is still intractable.

Furthermore, to update our network weights for a given $$x$$, we need to know which latent codes $$z$$ were likely responsible for generating it. This requires computing the **posterior distribution**, $$p_\theta(z|x)$$. Using Bayes' theorem:

$$
p_\theta(z|x) = \frac{(p_\theta(x|z) p(z))}{p_\theta(x)}
$$

Notice our old enemy, $$p_\theta(x)$$, the intractable evidence, is in the denominator. We are stuck again.

**The Solution: Variational Inference and the Encoder**

This is where a foundational concept from machine learning, **variational inference**, comes in. Since we cannot compute the true posterior $$p_\theta(z|x)$$, we approximate it.

We introduce a *second* neural network called an **encoder** or **inference network**, $$q_φ(z|x)$$.
*   **The Encoder's Job:** To take a real image $$x$$ and predict a distribution in the latent space from which $$x$$ was likely generated. It learns to approximate the true (but intractable) posterior.
*   **The Decoder's Job:** To take a point $$z$$ from that predicted distribution and reconstruct the original image $$x$$.

This encoder-decoder structure is the core of a **Variational Autoencoder (VAE)**, a landmark generative model. Training optimizes both networks simultaneously to maximize the **Evidence Lower Bound (ELBO)**, which elegantly balances two goals:
1.  **Reconstruction Quality:** The decoder must be able to reconstruct $$x$$ from its encoding $$z$$. (This corresponds to $$log p_\theta(x|z)$$).
2.  **Latent Space Regularization:** The encoded distributions $$q_φ(z|x)$$ must stay close to the simple prior $$p(z)$$. This forces the latent space to be smooth and well-organized, making it possible to sample from later.

This encoder-decoder paradigm is fundamental. Diffusion models can be understood as a sophisticated, multi-step generalization of this very principle.

---

### Summary & Next Steps

By introducing a simple latent variable $$z$$, we reframe the problem from modeling $$p(x)$$ directly to learning a mapping $$z -> x$$. This creates a new problem (an intractable posterior $$p(z|x)$$), which we solve by introducing an encoder $$q(z|x)$$ to approximate it. This encoder-decoder setup is central to modern generative modeling.

*   **Reflection Prompt:** In your own words, explain the distinct roles of the prior $$p(z)$$, the decoder $$p_\theta(x|z)$$, and the encoder $$q_φ(z|x)$$. Why is simply having a decoder not enough to train the model?
*   **Conceptual Link to Code:** Think about how you would structure this in PyTorch. You would have two $$nn.Module$$ classes: an $$Encoder$$ that takes $$x$$ and outputs the parameters of a Gaussian (mean and variance), and a $$Decoder$$ that takes a sample $$z$$ from that Gaussian and outputs a reconstructed $$x$$.
*   **Next Topic Preview:** We are now ready to tackle diffusion models. The "forward process" in diffusion is conceptually similar to an encoder, but it's a fixed, non-learned process that gradually maps data $$x$$ to pure noise. The "reverse process" is like a powerful, multi-step decoder that learns to undo this noising process.

Shall we move to **Part 2, Topic 3: The Forward Process in Diffusion Models**?




# The Math of Generative AI: Learning Data Distributions

Generative modeling is fundamentally about one task: learning to represent the probability distribution of data. For any given dataset, there's a true, underlying distribution, which we can call $$p_{\text{data}}(x)$$. A generative model's goal is to create its own distribution, $$p_\theta(x)$$, that perfectly mimics the original.

Consider the space of all possible 512x512 pixel RGB images. This is a space with 786,432 dimensions ($$512 \times 512 \times 3$$). Nearly every point in this vast space represents meaningless static. Only a tiny fraction contains images we would recognize as "natural"—pictures of cats, landscapes, or people.

These natural images are not scattered randomly. They are highly structured and lie on what is known as a **low-dimensional manifold**. Imagine a huge, empty room (the pixel space) where all meaningful images are located on a complex, tangled sheet of paper (the manifold). The model's job is to learn the exact shape of this sheet, assigning high probability to any image on or near it and near-zero probability to everything else.

## Understanding the Data Manifold

To make this concrete, let's simplify from images to 2D points $$(x_{1}, x_{2})$$ that lie on a circle with a radius of 2.

*   **Data Space:** The entire 2D plane (ℝ²).
*   **Manifold:** The circle itself—a 1D curve existing in a 2D space.
*   **True Data Distribution ($$p_{\text{data}}$$)**: This distribution is zero everywhere except on the circumference of the circle.

When we train a neural network, $$p_{\theta}$$, on points sampled from this circle, it won't learn a perfect, infinitely thin line. Instead, it learns a **probability distribution concentrated around the circle**. This creates a "probabilistic doughnut" or a "probability cloud" that is dense near the circle and fades away as you move from it.

*[Image: A side-by-side comparison. On the left, a perfect black circle on a white background, labeled "Ground Truth Manifold." On the right, a heat map showing a thick, doughnut-shaped ring of high probability (red/yellow) that fades to low probability (blue/green), labeled "Learned Distribution pθ(x)."]*
**Alt Text:** Diagram showing the difference between a perfect data manifold (a circle) and the learned probability distribution, which is a cloud concentrated around the circle.

The model correctly identifies the region of high probability, even if it's not a perfect representation of the manifold.

## The Central Challenge: The Intractable Partition Function

The classic method for training a model is **Maximum Likelihood Estimation (MLE)**. Given a dataset of real images $$\{x_1, x_2, ..., x_N\}$$, we adjust the model's parameters $$\theta$$ (its network weights) to maximize the probability that the model would have generated this data. We do this by maximizing the log-likelihood:

$$
L(\theta) = \sum \log(p_\theta(x_i))
$$

However, a critical problem arises immediately. A neural network doesn't directly output a normalized probability. It outputs an unnormalized score or value, let's call it $$q_\theta(x)$$. To convert this score into a valid probability $$p_\theta(x)$$, the total probability over all possible images must sum to 1. This requires an integral:

$$
p_\theta(x) = \frac{q_\theta(x)}{\int q_\theta(x') dx'}
$$

The integral in the denominator, $$ \int q_\theta(x') dx' $$, is known as the **partition function**. For our 2D circle example, calculating the volume under the probability surface is feasible. But for a 512x512 image, the integral is over a 786,432-dimensional space. This calculation is not just slow; it is fundamentally impossible with current technology.

This intractability is the core challenge that drives the design of modern generative models. Architectures like [diffusion models](https://example.com/what-are-diffusion-models) and flow-based models are ingenious solutions for defining and training expressive probability distributions while avoiding this impossible integral.

## Latent Variable Models: A Smarter Approach

Since modeling $$p(x)$$ directly is too difficult, we introduce a "helper" or **latent variable**, denoted as $$z$$. The idea is to assume that our complex data $$x$$ is generated from this simpler, unobserved variable $$z$$.

Think of it this way:
*   **`x`** is a final, detailed oil painting of a cat.
*   **`z`** is a simple sketch or a set of high-level instructions: "A fluffy cat, sitting, facing left, looking curious."

It is far easier to work with the simple instructions ($$z$$) than the millions of pixel values ($$x$$). We define the latent space where $$z$$ lives to be simple and structured, typically a standard multivariate Gaussian distribution ($$N(0, I)$$).

### The Two-Step Generative Process

This approach reframes generation into two distinct steps:

1.  **Sample a Latent Code:** Draw a simple vector $$z$$ from a known prior distribution $$p(z)$$, like picking a random point from a Gaussian bell curve.
2.  **Decode the Latent Code:** Use a powerful neural network, called a **decoder** or **generator**, to map the simple code $$z$$ to a distribution over complex images, denoted as $$p_\theta(x|z)$$.

The probability of any image $$x$$ is then the sum of probabilities of generating it from *all possible* latent codes $$z$$:

$$
p_\theta(x) = \int p_\theta(x|z) p(z) dz
$$

While this looks like we've just swapped one integral for another, we've made significant progress. We are no longer defining a function over the messy data space. Instead, we are learning a **mapping** from a simple, structured latent space to the complex data manifold.

### The Training Dilemma: The Intractable Posterior

We have a clear generative path ($$z \rightarrow x$$), but training remains a challenge. To calculate the likelihood $$p_\theta(x)$$ for a real image from our dataset, we still need to solve the integral over $$z$$. This is still intractable.

Moreover, to update our network for a given image $$x$$, we need to know which latent codes $$z$$ were likely responsible for creating it. This requires computing the **posterior distribution**, $$p_\theta(z|x)$$. Using [Bayes' theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem):

$$
p_\theta(z|x) = \frac{p_\theta(x|z) p(z)}{p_\theta(x)}
$$

Our old problem, the intractable evidence $$p_\theta(x)$$, is back in the denominator. We are stuck again.

## The Solution: Variational Autoencoders (VAEs)

This is where **variational inference**, a foundational machine learning concept, provides a solution. Since we cannot compute the true posterior $$p_\theta(z|x)$$, we approximate it with a second neural network.

This network is called an **encoder** or **inference network**, denoted as $$q_φ(z|x)$$. This leads to the classic encoder-decoder structure of a **Variational Autoencoder (VAE)**, a landmark generative model.

*   **The Encoder's Job:** Takes a real image $$x$$ and predicts a distribution in the latent space from which $$x$$ was likely generated. It learns to approximate the true (but intractable) posterior.
*   **The Decoder's Job:** Takes a point $$z$$ sampled from the encoder's predicted distribution and reconstructs the original image $$x$$.

*[Image: A diagram of the VAE architecture. An input image 'x' goes into the Encoder, which outputs a latent distribution 'qφ(z|x)'. A sample 'z' is drawn and fed into the Decoder, which outputs the reconstructed image 'x-hat'.]*
**Alt Text:** Architecture of a Variational Autoencoder, showing the encoder mapping an image to a latent space and the decoder reconstructing the image from the latent space.

Training a VAE involves optimizing both networks simultaneously to maximize the **Evidence Lower Bound (ELBO)**. The ELBO elegantly balances two competing goals:

1.  **Reconstruction Quality:** The decoder must accurately reconstruct the input image $$x$$ from its latent code $$z$$.
2.  **Latent Space Regularization:** The encoded distributions $$q_φ(z|x)$$ produced by the encoder must stay close to the simple prior distribution $$p(z)$$. This forces the latent space to be smooth and well-organized, making it suitable for generating new images by sampling from it.

This powerful encoder-decoder paradigm is fundamental to modern generative AI. More advanced architectures, including diffusion models, can be understood as sophisticated, multi-step extensions of this core principle.

---

## Frequently Asked Questions (FAQ)

### What is the main goal of a generative model?
The primary goal of a generative model is to learn the underlying probability distribution of a given dataset. By doing so, it can create new, synthetic data samples that are statistically similar to the original data.

### Why is the partition function a problem in generative modeling?
The partition function is a normalization constant required to turn a model's raw output scores into valid probabilities. It involves an integral over the entire data space, which is computationally intractable for high-dimensional data like images, making it impossible to train models using standard Maximum Likelihood Estimation.

### How do latent variable models solve this problem?
Latent variable models circumvent the intractable partition function by introducing a simpler, low-dimensional latent space. Instead of modeling the complex data distribution directly, they learn a mapping from the simple latent space to the complex data space, which is a more manageable task.

### What is a Variational Autoencoder (VAE)?
A VAE is a type of generative model that uses an encoder-decoder architecture. The encoder maps input data into a latent distribution, and the decoder reconstructs the data from a sample of that distribution. It's trained to both reconstruct data accurately and keep its latent space well-organized, allowing it to generate new data.