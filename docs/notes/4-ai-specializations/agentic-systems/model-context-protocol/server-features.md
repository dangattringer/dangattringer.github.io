---
sidebar_label: "Server Features"
title: "MCP Server Features Explained: Prompts, Tools & Resources"
author: "Daniel Gattringer"
description: "Explore the core server features of the Model Context Protocol (MCP), with Python examples for implementing Prompts, Resources, Tools, Logging, and more."
datePublished: 2025-08-14
draft: false
sidebar_position: 2
---
import ThemedAsset from '@site/src/components/ThemedAsset/ThemedAsset';

<details>
<summary>TL;DR</summary>

- **Prompts:** User-controlled templates that guide LLM interactions, triggered via commands like slash commands
- **Resources:** Application-driven data (e.g., documents, lists) exposed via URIs to provide context for prompts or UI elements
- **Tools:** Model-controlled functions that allow an LLM to perform actions, like reading a file or calling an external API
- **Logging:** Logging provides structured feedback from the server to the client
- **Elicitation:** Allows the server to request structured input from the user
- **Sampling:** Enables the server to offload LLM generation tasks to the client, which manages API credentials and costs

</details>

The [Model Context Protocol (MCP)](../model-context-protocol) enhances interactions between clients, servers, and language models through a set of powerful server features. These capabilities provide context, enable actions, and streamline communication.

## Minimal Example

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

if __name__ == "__main__":
    mcp.run()   # default transport: stdio
```

This minimal example sets up a basic MCP server using the FastMCP framework. It initializes the server with a name and runs it, allowing clients to connect and interact.

## Prompts: User-Controlled Instructions

Prompts are pre-defined templates that guide language model interactions. They are explicitly selected by a user, often through a UI element like a slash command, giving them direct control over the LLM's task. As a server author, you can engineer high-quality prompts to ensure consistent results, abstracting the complexity away from the end-user.

- **Control:** Prompts are **user-controlled**
- **Purpose:** Provide consistent, high-quality instructions for common tasks
- **Content:** Can include text, images, audio, and embedded resources for rich, multi-modal interactions
- **Declaration:** Servers must declare the `prompts` capability during initialization

### Python Example: Defining a Prompt

The [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) uses the `@mcp.prompt` decorator to simplify prompt creation, automatically handling argument parsing and message formatting.

```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(
    doc_id: str = Field(description="Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra text, but don't change the meaning of the report.
    Use the 'edit_document' tool to edit the document. After the document has been edited, respond with the final version of the doc. Don't explain your changes.
    """

    return [base.UserMessage(prompt)]
```

This function defines a prompt that reformats a document into Markdown. The `@mcp.prompt` decorator handles the necessary boilerplate, allowing you to focus on the prompt's content.

## Resources: Providing Structured Context

Resources are structured data or content that the server exposes to the client. They function much like GET request handlers in an HTTP server, where each resource is identified by a unique URI.

- **Control:** Resources are **application-driven**. The client application decides when to fetch and use resource data
- **Purpose:** Augment prompts with context or populate UI elements like autocomplete lists
- **Types:** MCP supports **Direct Resources** (static URIs) and **Templated Resources** (URIs with parameters)
- **Declaration:** Servers must declare the `resources` capability during initialization

### Python Example: Defining Resources

The `@mcp.resource` decorator can define both direct and templated resources.

```python
@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
```

Here, `list_docs` returns a list of available document IDs, while `fetch_doc` retrieves the content of a specific document. The client can use these resources to provide context for prompts or populate UI elements.

## Tools: Enabling Model-Driven Actions

Tools are executable functions that allow a language model to interact with external systems. This empowers the model to perform actions like querying a database, calling an API, or modifying a file system.

- **Control:** Tools are **model-controlled**. The LLM (e.g., Claude) decides when to invoke a tool based on the conversation context
- **Purpose:** Enable the LLM to perform actions and retrieve real-time information
- **Schema:** The MCP Python SDK uses decorators and Python type hints to automatically generate the JSON schemas that AI models need to understand and use the tools. For more complex validation, you can use libraries like [Pydantic](https://pydantic.dev/)
- **Declaration:** Servers must declare the `tools` capability during initialization

### Python Example: Defining Tools

```python
from pydantic import Field

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(
    doc_id: str = Field(description="Id of the document to read"),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string",
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(
        description="The text to replace. Must match exactly, including whitespace"
    ),
    new_str: str = Field(
        description="The new text to insert in place of the old text"
    ),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

```

These examples define tools for reading and editing documents. An LLM can decide to call these functions autonomously during a conversation to fulfill a user's request.

## Logging: Standardized Server Feedback

MCP provides a standardized way for servers to send structured log messages to clients. This is useful for providing real-time feedback during long-running operations or for debugging.

- **Purpose:** Offer visibility into server-side processes
- **Structure:** Log messages include a severity level (e.g., debug, info, warning, error), an optional logger name, and JSON-serializable data
- **Control:** Clients can set a minimum log level to control verbosity
- **Declaration:** Servers must declare the `logging` capability

### Python Example: Sending Log and Progress Notifications

The `context` object, automatically injected into tool functions, provides methods for sending log and progress updates to the client.

```python
import asyncio
from mcp.server.fastmcp import Context

@mcp.tool()
async def add(a: int, b: int, ctx: Context) -> int:
    await ctx.info("Preparing to add...")
    await ctx.report_progress(20, 100)

    await asyncio.sleep(2)

    await ctx.info("OK, adding...")
    await ctx.report_progress(80, 100)

    return a + b
```

## Elicitation: Requesting User Input

Elicitation allows a server to request additional, structured information from the user through the client. This enables interactive workflows where the server needs specific input to proceed.

- **Purpose:** Dynamically gather structured information from the user
- **Process:** The server sends an `elicitation/create` request with a message and a JSON Schema defining the required input. The client then renders a UI to collect and validate the data
- **Security:** Servers **must not** use elicitation to request sensitive information
- **Declaration:** Clients supporting this feature must declare the `elicitation` capability

### Python Example: Eliciting User Input

The server initiates an elicitation request by sending a JSON-RPC message. A Python SDK would typically wrap this in a convenient function call.

```python
from pydantic import BaseModel, Field

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession


class BookingPreferences(BaseModel):
    """Schema for collecting user preferences."""

    checkAlternative: bool = Field(description="Would you like to check another date?")
    alternativeDate: str = Field(
        default="2024-12-26",
        description="Alternative date (YYYY-MM-DD)",
    )


@mcp.tool()
async def book_table(date: str, time: str, party_size: int, ctx: Context[ServerSession, None]) -> str:
    """Book a table with date availability check."""
    # Check if date is available
    if date == "2024-12-25":
        # Date unavailable - ask user for alternative
        result = await ctx.elicit(
            message=(f"No tables available for {party_size} on {date}. Would you like to try another date?"),
            schema=BookingPreferences,
        )

        if result.action == "accept" and result.data:
            if result.data.checkAlternative:
                return f"[SUCCESS] Booked for {result.data.alternativeDate}"
            return "[CANCELLED] No booking made"
        return "[CANCELLED] Booking cancelled"

    # Date available
    return f"[SUCCESS] Booked for {date} at {time}"
```

## Sampling: Offloading LLM Generation

Sampling enables a server to request an LLM completion from the client. This design shifts the responsibility of LLM API calls from the server to the client, which already manages the necessary credentials.

- **Purpose:** Allow the server to use LLM generation without managing API keys or billing
- **Process:** The server sends a `sampling/createMessage` request with the conversation history, model preferences (e.g., `costPriority`, `speedPriority`), a system prompt, and `maxTokens`
- **Use Case:** Ideal for implementing agentic behaviors where LLM calls are nested within other server-side logic
- **Declaration:** Clients supporting this feature must declare the `sampling` capability

### Python Example: Requesting Sampling from a Tool

The server can use the `context` object to initiate a sampling request to the client.

```python
@mcp.tool()
async def summarize(text_to_summarize: str, ctx: Context):
    prompt = f"""
        Please summarize the following text:
        {text_to_summarize}
    """

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user", content=TextContent(type="text", text=prompt)
            )
        ],
        max_tokens=4000,
        system_prompt="You are a helpful research assistant.",
    )

    if result.content.type == "text":
        return result.content.text
    else:
        raise ValueError("Sampling failed")
```

## FAQ: MCP Server Features

<details>
  <summary>What is the difference between MCP Tools and Prompts?</summary>

  The main difference is control.

- **Prompts** are user-controlled; the user explicitly chooses a prompt to run a pre-defined task
- **Tools** are model-controlled; the language model decides when to use a tool to perform an action or get information based on the conversation

</details>

<details>
  <summary>Why does MCP use sampling to offload LLM calls to the client?</summary>

  Sampling shifts the responsibility and cost of LLM API calls to the client. The client application typically already has the user's API credentials and billing relationship with the LLM provider. This allows the server to trigger LLM generations without needing to manage sensitive keys or payment information.
</details>

<details>
  <summary>How does an MCP server declare its capabilities?</summary>

  An MCP server declares its supported features (e.g., `prompts`, `tools`, `resources`) during the initialization phase of the connection. This allows the client to know which features it can use when interacting with that specific server.
</details>
