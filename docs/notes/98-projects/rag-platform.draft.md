---
title: RAG Platform
author: "Daniel Gattringer"
description: ""
draft: true
sidebar_position: 2
---

# RAG Platform

:::note
Work in Progress  
These notes are a work in progress and may not be complete or fully accurate. They are intended for personal use and reference.
Content is added and updated regularly.
:::

## Project Goal

To build a scalable, secure, and maintainable platform that allows users to ask natural language questions about a specific corpus of documents (e.g., internal technical documentation, research papers, product manuals) and receive accurate answers generated by an LLM, backed by retrieved context.

## Core Scenario

1. A collection of documents (PDFs, TXTs, Markdown files) relevant to a specific domain is stored in cloud object storage.
2. An automated Data Ingestion Pipeline processes these documents: extracts text, chunks it, generates vector embeddings, and stores the chunks and embeddings in a Vector Database.
3. A RAG API Service deployed on Kubernetes receives user questions.
4. The API service generates an embedding for the question, queries the Vector Database to find the most relevant document chunks (context).
5. It constructs a prompt containing the retrieved context and the original question.
6. This prompt is sent to a Large Language Model (LLM) API (like OpenAI, Anthropic, or a self-hosted model) to generate a final answer.
7. The answer is returned to the user via the API.
8. A simple frontend allows interaction with the API.
