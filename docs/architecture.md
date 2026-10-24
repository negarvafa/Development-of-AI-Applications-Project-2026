# Architecture Documentation

The final CareerPilot application uses a layered architecture that separates the user interface, AI model interaction, tool execution, and job retrieval logic.

## Baseline Architecture

The starter application originally followed the architecture below:

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local Inference Server)
  ↓
Local Model (e.g., llama3.2)
```

### CareerPilot Architecture

The final CareerPilot application extends the baseline architecture with tool calling and job retrieval functionality.

```text
User
  ↓
CareerPilot UI
  ↓
Tool Calling Service
  ↓
Llama 3.2 via Ollama
  ↓
Tool Call: search_jobs()
  ↓
csv_jobs.py
  ↓
jobs-export.csv (5000+ jobs)
  ↓
Retrieved Job Matches
  ↓
AI-generated Recommendation
  ↓
User
```

## CareerPilot Design Principles

### Separation of Concerns

The application separates user interface, AI logic, tool execution, and data retrieval into independent components:

UI
→ Tool Calling Service
→ Model Client
→ CSV Retrieval Service
→ Job Dataset

### Tool-Mediated Data Access

The language model never accesses the job dataset directly.

Instead, the model uses the `search_jobs()` tool, which retrieves matching vacancies from the CSV dataset and returns the results to the model.

### Controlled AI Responses

The language model is instructed to use only information returned by the job search tool and avoid inventing job requirements or vacancy status.

### Modular Architecture

Individual components can be modified independently:

- UI layer
- Tool calling layer
- Retrieval layer
- Dataset layer
- Model layer

## Additional AI Capability

CareerPilot implements Tool Calling as its additional AI capability.

The Llama 3.2 model can invoke the `search_jobs()` tool, which retrieves relevant vacancies from a dataset containing more than 5000 Finnish job advertisements.

This allows the model to use external application logic and real job data instead of relying only on its internal knowledge.


