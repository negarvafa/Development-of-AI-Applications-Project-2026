# CareerPilot – AI Job Search & Application Assistant

Starter template for the **Development of AI Applications** course final group project.

## Team members

- Member 1 Ruut Hyvösaho (ruut.hyvosaho@student.hamk.fi)
- Member 2 Mikko Mutikainen (mikko.mutikainen@student.hamk.fi)
- Member 3 Erik Laakso (erik.laakso@student.hamk.fi)
- Member 4 Negar Vafa (negar.2.vafa@student.hamk.fi)

## Problem
Job seekers often find it difficult to understand how well their skills and experience match a job description. Preparing for job applications and interviews can also take a significant amount of time. Our AI-powered assistant bridges this gap by automatically searching for relevant positions, analyzing requirements, and tailoring your application materials instantly.

### Intended users
The intended users are job seekers who want help understanding job requirements and preparing better job applications. 

### Problem statement
help applicants or job seekers find jobs 

### Why AI is appropriate
AI can give personalized suggestions based on the applicant's skills and the job requirements.


## Solution

Our group plans to develop CareerPilot, an AI-powered job search and application assistant. The application analyzes the user's profile and helps identify suitable job opportunities. It can compare the user's background with job requirements and provide personalized suggestions to support the application process.

## Main user workflow

1. **User Input: ** The user provides information about their education, skills, work experience, and career interests.
2. **Processing & Guardrails: ** The application service layer (`src/services/ai_service.py`)is responsible for validating user input, applying guardrails, and formatting requests before they are sent to the language model.
3. **Model Response: ** The model client calls Ollama locally. The AI analyzes the user's profile and suggests suitable job roles and career options based on their education, skills, work experience, and interests. The response is returned through the service layer to the UI.

## Architecture

Below is the initial starter architecture. As your project evolves with additional capabilities, replace or extend this diagram in [`docs/architecture.md`](docs/architecture.md).

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local LLM Server)
```

> **Core Architectural Rule:** The user interface must NEVER communicate directly with the model client or Ollama. All interactions must pass through the service layer (`ai_service.py`).

## Model
LIama 3.2 
- **Model used:** e.g., `llama3.2` (or specified local Ollama model)
- **Selection rationale:** Why was this specific model chosen for your project (e.g., lightweight, performance, context size)?

## Additional AI capability

Select at least one additional capability to implement for your final project:

- [ok ] RAG (Retrieval-Augmented Generation)
- [ ] Tools / External API integration
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [ ] Other: ______________________

### Capability justification
RAG allows the assistant to retrieve relevant information from the user's CV and job descriptions before generating a response. This make the advice more accurate and personalized because the AI can base its suggestions on the candidate's actual skills and the specific requriements of each job.

## Setup

### 1. Create the Conda environment

```bash
conda env create -f environment.yml
```

### 2. Activate the environment

```bash
conda activate dev-ai-project
```

### 3. Configure environment variables

Copy `.env.example` to create your local `.env` configuration file:

On Linux / macOS:
```bash
cp .env.example .env
```

On Windows (Command Prompt / PowerShell):
```powershell
copy .env.example .env
```

Ensure `.env` contains valid values for `OLLAMA_BASE_URL` and `MODEL_NAME`:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2
```

### 4. Start Ollama

Make sure Ollama is installed and running locally, then pull your configured model:

```bash
ollama run llama3.2
```

### 5. Run the application

Run the application from the root directory of the project:

```bash
python -m app.main
```

Then open your browser at `http://localhost:7860`.

### 6. Run automated tests

```bash
pytest
```

## Evaluation
Describe your evaluation methodology and summarize key results. Starter test cases can be found in [`evaluation/test_cases.json`](evaluation/test_cases.json).
test case 1
User Profile:
information technology student 
python
machine
Data Analysis 
Expected Result: Ai recommends Data analyst, junior Ai Engineer,



Refer to [`evaluation/README.md`](evaluation/README.md) for guidelines on defining success, edge cases, and failure scenarios.

## Known limitations

The assistant may misunderstand information and may not always accurately judge how well a candidate matches a position. job listing may also become outdated, and the system depends on the information.

## Future improvements

future versions could connect to more job platforms, improve job matching, and provide more personalized CV and cover letter suggestions based on the user's skills and preference.
