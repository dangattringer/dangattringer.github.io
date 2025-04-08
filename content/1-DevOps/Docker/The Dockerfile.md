---
title: The Dockerfile
author: Daniel Gattringer
description: ""
date: 2025-04-04
tags:
  - Docker
draft: true
page: 5
---

# The Dockerfile

A Dockerfile or Containerfile is a text document that contains a set of instructions for building a container image. It defines the base image, sets up the environment, copies the application code, installs the dependencies, and configures the runtime settings. Dockerfiles provide a reproducible and automated way to create consistent images, enabling developers to version and share their application configurations.

A sample Dockerfile can be seen in the following code snippet:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 3000
```

Docker aims to make it easy to build, share, and run applications. We call this containerization and the process looks like this:

1. Write your applications and create the list of dependencies
2. Create a Dockerfile that tells Docker how to build and run the app
3. Build the app into an image
4. Push the image to a registry (optional)
5. Run a container from the image

<figure align="center">
  <img src="docker-basic-flow-of-containerizing.svg" alt="">
  <figcaption></figcaption>
</figure>
