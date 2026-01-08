---
sidebar_label: "Transports"
title: "MCP Transports: STDIO vs. Streamable HTTP Explained"
author: "Daniel Gattringer"
description: "Explore the key MCP transports for client-server communication. Learn the differences between STDIO for local development and Streamable HTTP for remote servers."
datePublished: 2025-08-14
draft: false
sidebar_position: 1
---

<details>
  <summary>TL;DR</summary>
  
- The Model Context Protocol (MCP) uses transports to send **JSON-RPC 2.0** messages between clients and servers
- The **STDIO transport** is designed for local development, where a client launches the server as a subprocess and communicates via standard input/output
- The **Streamable HTTP transport** enables communication with remote servers over HTTP, using Server-Sent Events (SSE) for real-time, bidirectional messaging
- Streamable HTTP includes features for session management, message redelivery, and OAuth 2.1-based authorization
- Configuration flags like `stateless_http` and `json_response` can modify Streamable HTTP behavior for use cases like horizontal scaling or simpler integrations
- Custom transports can be developed, but they must follow the core MCP message format and lifecycle rules

</details>

The Model Context Protocol (MCP) relies on transport mechanisms to connect clients and servers, allowing them to exchange messages. Because all communication relies on the **[JSON-RPC 2.0 specification](https://www.jsonrpc.org/specification)**, MCP is transport-agnostic. This flexibility allows clients and servers to communicate over different protocols depending on their needs.

MCP defines two standard transports: **STDIO** and **Streamable HTTP**

## STDIO Transport

The STDIO (standard input/output) transport is the simplest way to connect an MCP client and server, making it a popular choice during development and testing.

- **How it Works**:
  - The **client launches the MCP server as a subprocess**
  - The server reads JSON-RPC messages from its **standard input (`stdin`)** and sends messages to its **standard output (`stdout`)**
  - Messages are individual JSON-RPC requests, notifications, or responses, and are delimited by newlines without embedded newlines
  - Either the server or client can send a message at any time, allowing for **seamless bidirectional communication**
  - The server may also write UTF-8 strings to its standard error (`stderr`) for logging purposes
- **Use Case**: This transport is ideal for **development and testing** when the client and server run on the **same machine**. You can even test an MCP server directly from your terminal by pasting JSON messages into stdin and observing responses on stdout
- **Authorization**: Implementations using STDIO transport **should not** follow the OAuth 2.1-based authorization specification; instead, they should retrieve credentials from the environment

<div style={{textAlign: 'center'}}>
<figure >
    ```mermaid
        sequenceDiagram
            participant Client
            participant Server Process

            Client->>Server Process: Launch subprocess
            loop [Message Exchange]
                Client->>Server Process: Write to stdin
                Server Process-->>Client: Write to stdout
                Server Process-->>Client: Optional logs on stderr
            end
            Client->>Server Process: Close stdin, terminate subprocess

    ```

<figcaption>Client-Server Process Communication Sequence (Source: [official MCP documentation](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#stdio))</figcaption>
</figure>
</div>

## Streamable HTTP Transport

The Streamable HTTP transport allows MCP clients to connect to **remotely hosted MCP servers over HTTP connections**, making public MCP servers accessible to anyone. It replaces the older HTTP+SSE transport.

- **Core Mechanism**: Streamable HTTP uses **HTTP POST and GET requests**, and can optionally leverage **Server-Sent Events (SSE)** to stream multiple server messages, enabling more feature-rich interactions like server-to-client notifications and requests.
  - **HTTP Communication Challenge**: Standard HTTP is primarily client-to-server. Features like sampling, notifications, and logging require the server to initiate requests to the client, which is challenging with plain HTTP. Streamable HTTP addresses this with a workaround.
- **Initial Connection Setup**:
    1. The client sends an **`Initialize` Request** to the server.
    2. The server responds with an **`Initialize` Result**, which includes a crucial **`mcp-session-id` header** to uniquely identify the client.
    3. The client then sends an **`Initialized` Notification** along with this session ID. This session ID **must be included in all subsequent HTTP requests** from the client to the server.
- **SSE Workaround for Server-to-Client Communication**: After initialization, the client can make an **HTTP GET request to the MCP endpoint** to establish a long-lived SSE connection. This persistent channel allows the server to stream requests, notifications, and other messages back to the client.
- **Tool Calls and Dual SSE Connections**: When a client makes a tool call via an HTTP POST request, the system can create two separate SSE connections:
  - **Primary SSE Connection**: Stays open indefinitely and is used for **server-initiated requests and progress notifications**.
  - **Tool-Specific SSE Connection**: Created for each tool call via the POST response and **closes automatically** when the tool result is sent. This is used for **logging messages and tool results**.
- **Resumability and Redelivery**: To mitigate message loss due to disconnections, servers may attach an `id` field to SSE events. Clients can use the `Last-Event-ID` header when reconnecting to indicate the last event received, allowing the server to replay missed messages on that specific stream.
- **Session Management**: A server may assign a session ID during initialization via the `Mcp-Session-Id` HTTP header. Clients must include this header in all subsequent requests. Servers requiring a session ID will return HTTP 400 for requests missing it, and HTTP 404 if the session is terminated. Clients can explicitly terminate a session by sending an HTTP DELETE request with the session ID.
- **Protocol Version Header**: When using HTTP, the client **must** include the `MCP-Protocol-Version` HTTP header (e.g., `MCP-Protocol-Version: 2025-06-18`) on all subsequent requests to the MCP server. This allows the server to respond based on the negotiated protocol version.
- **Authorization**: Implementations using HTTP-based transports **should conform** to the MCP authorization specification, which is based on OAuth 2.1.
- **Security Warnings**: When implementing Streamable HTTP, servers **must validate the `Origin` header**, **should bind only to localhost** (127.0.0.1) when running locally, and **should implement proper authentication**. These measures prevent attacks like DNS rebinding. The authorization specification provides further details on security best practices, including preventing token theft, ensuring communication security (HTTPS), authorization code protection (PKCE), and open redirection prevention.
- **Configuration Flags**: Two important flags, `stateless_http` and `json_response`, significantly control how the Streamable HTTP transport behaves and can limit server functionality.
  - **`stateless_http=True`**:
    - **Impact**: Disables session IDs, server-to-client requests (like sampling, progress reports, subscriptions), and client initialization.
    - **Benefit**: Enables **horizontal scaling with load balancers** for popular MCP servers, as it eliminates the complex coordination problem between multiple server instances. Clients can make requests directly without the initial handshake.
    - **Use Cases**: When horizontal scaling is necessary, server-to-client communication is not needed, and tools do not require AI model sampling.
  - **`json_response=True`**:
    - **Impact**: Disables streaming for POST request responses, meaning you only receive the **final result as plain JSON**. No intermediate progress messages or log statements during execution.
    - **Use Cases**: When streaming responses are not needed, or when integrating with systems that expect simple, non-streaming HTTP responses.
  - **Development vs. Production**: It's crucial to **test with the same transport** you plan to use in production, as behavioral differences between stateful and stateless modes can be significant.

### Custom Transports

MCP allows for **custom transport mechanisms** to be implemented in a pluggable fashion, beyond the standard STDIO and Streamable HTTP. Implementers of custom transports **must ensure they preserve the JSON-RPC message format and lifecycle requirements** defined by MCP. They should also document their specific connection establishment and message exchange patterns for interoperability.
