# CareerPilot – AI Job Search & Recommendation Assistant

CareerPilot is an AI-powered job search and recommendation assistant developed for the Development of AI Applications course project.

## Team members

- Member 1 Ruut Hyvösaho (ruut.hyvosaho@student.hamk.fi)
- Member 2 Mikko Mutikainen (mikko.mutikainen@student.hamk.fi)
- Member 3 Erik Laakso (erik.laakso@student.hamk.fi)
- Member 4 Negar Vafa (negar.2.vafa@student.hamk.fi)

## Problem
Job seekers often find it difficult to understand how well their skills and experience match a job description. Preparing for job applications and identifying suitable opportunities can take a significant amount of time. Our AI-powered assistant helps users discover relevant positions and understand how their interests and skills relate to available jobs.

### Intended users
The intended users are job seekers who want help understanding job requirements and preparing better job applications. 

### Problem statement
Help job seekers discover relevant employment opportunities and better understand how their skills and interests match available positions.

### Why AI is appropriate
AI can give personalized suggestions based on the applicant's skills and the job requirements.

## Solution

Our group developed CareerPilot, an AI-powered job search and recommendation assistant. The application analyzes user skills, interests, and location preferences to identify relevant job opportunities from a dataset containing over 5000 Finnish job advertisements.

## Main User Workflow

1. The user enters skills, interests, and preferred location.
2. CareerPilot sends the request to Llama 3.2 running locally through Ollama.
3. The model uses tool calling to invoke the `search_jobs()` function.
4. The job search tool retrieves matching vacancies from the CSV dataset.
5. Retrieved jobs are returned to the model.
6. The model generates personalized recommendations and explanations.
7. Recommendations are displayed in the Gradio user interface.

## Architecture

A detailed architecture description is available in: [`docs/architecture.md`](docs/architecture.md).

```text
User
 ↓
Gradio UI (careerpilot_ui.py)
 ↓
Tool Calling Layer (job_tool_calling.py)
 ↓
Llama 3.2 (Ollama)
 ↓
search_jobs() Tool
 ↓
CSV Job Dataset (jobs-export.csv)
 ↓
AI Recommendations
```
### Architecture Overview

CareerPilot follows a modular architecture where the user interface, AI model interaction, job retrieval, and data storage are separated into independent components.

The architecture includes:

- Gradio user interface
- Llama 3.2 running through Ollama
- Tool calling functionality
- CSV-based job retrieval
- AI-generated job recommendations

> The user interface never accesses the job dataset directly. All model interactions and job retrieval operations are performed through dedicated service and tool-calling components.

## Model

### Model Used

Llama 3.2 (running locally through Ollama)

### Selection Rationale

Llama 3.2 was selected because it is lightweight, can run locally without external API costs, supports tool calling, and provides sufficient performance for job recommendation and explanation tasks.

## Additional AI capability

Select at least one additional capability to implement for your final project:

- [ ] RAG (Retrieval-Augmented Generation)
- [x] Tools / tool Calling
- [ ] Model Context Protocol (MCP)
- [ ] Agentic workflow (Model-selected actions based on observations)
- [ ] Memory / Persistent state
- [ ] Multimodal interaction (Text + Images)
- [ ] Other: ______________________

### Capability justification
CareerPilot uses Ollama and Llama 3.2 to call a Python job search tool.

The AI model can request the `search_jobs` function, which searches job advertisements from a local CSV dataset (`data/jobs-export.csv`).

The tool returns matching jobs based on the user's skills, interests, and preferred location.

The AI then uses these results to explain suitable job opportunities.

This feature has been tested successfully in the Gradio user interface.

The CSV dataset is local, and job advertisements are not verified as currently open.

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

Copy `.env.example` to create your local `.env` file.

Linux / macOS:

```bash
cp .env.example .env
```

Windows:

```powershell
copy .env.example .env
```

Ensure the following values are configured:

```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2
```

### 4. Start Ollama

Download and run the model:

```bash
ollama pull llama3.2
ollama run llama3.2
```

### 5. Run the Applications

#### CareerPilot (Project Application)

```bash
python -m app.careerpilot_ui
```

Open:

```text
http://localhost:7860
```

#### Application Starter (Reference Application)

The original starter application is still included in the repository for reference:

```bash
python -m app.main
```

### 6. Run Automated Tests

```bash
pytest
```

## Evaluation

CareerPilot was evaluated using six different test profiles:

- AI / Software Developer
- Data Analyst
- Cybersecurity Specialist
- Healthcare Professional
- Space Researcher (edge case)
- Empty Profile (robustness test)

The evaluation showed that the system successfully retrieved relevant jobs from the CSV dataset and generated AI-assisted recommendations using tool calling.

Detailed test cases, evaluation methodology, and results can be found in: [`evaluation/test_cases.json`](evaluation/test_cases.json).
Refer to [`evaluation/README.md`](evaluation/README.md) for evaluation criteria, success definitions, edge cases, and failure scenario guidelines.

## Known Limitations

- Job recommendations depend on the quality of the CSV dataset.
- The dataset may contain outdated job advertisements.
- The language model occasionally generates generic advice not present in the retrieved data.
- Highly specialized interests may result in limited matching opportunities.

## Future Improvements

- Replace the static CSV dataset with a live job search API.
- Improve job matching using richer job descriptions.
- Add CV and cover letter assistance.
- Improve recommendation accuracy and filtering.
- Expand evaluation with additional user profiles and real-world users.
