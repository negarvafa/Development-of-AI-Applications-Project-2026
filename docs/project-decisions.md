# Project Decisions

Use this decision log to document significant technical and architectural choices made by your team during development.

---

## Decision 1 — Model Selection

**Decision:**

Use Llama 3.2 running locally through Ollama.

**Alternatives considered:**

- Cloud-hosted LLM services
- Other local Ollama models

**Why we chose this:**

Llama 3.2 is lightweight, easy to run locally, supports tool calling, and provides sufficient performance for job recommendation and explanation tasks. Running the model locally also avoids external API costs and dependencies.

---

## Decision 2 — Additional AI Capability

**Decision:**

Implement Tool Calling.

**Why it is needed:**

The language model needs access to real job advertisements instead of relying only on its internal knowledge.

**Alternatives considered:**

- Retrieval-Augmented Generation (RAG)
- Model Context Protocol (MCP)
- Agentic workflows

**Why we chose this:**

Tool calling provided the simplest and most practical solution for the project. It allows the model to retrieve relevant jobs from the dataset and generate personalized recommendations based on real data.

---

## Decision 3 — Architecture

**Decision:**

Use a layered architecture separating the UI, AI logic, tool execution, and job retrieval components.

**Why:**

This approach improves maintainability and allows components to be developed independently. The user interface, model interaction, CSV retrieval, and tool calling logic can be modified without affecting the rest of the system.

---

## Decision 4 — Job Data Source

**Decision:**

Use a CSV dataset containing over 5000 Finnish job advertisements.

**Alternatives considered:**

- Manual job examples stored in JSON
- Live job search APIs

**Why we chose this:**

The CSV dataset provided a large number of realistic job advertisements while remaining simple to integrate and available offline. It enabled development and evaluation without requiring external API access.
