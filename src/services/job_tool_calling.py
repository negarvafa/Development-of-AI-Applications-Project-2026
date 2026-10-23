
import json
from src.models.model_client import OllamaModelClient
from src.services.csv_jobs import select_csv_jobs


def search_jobs(
    skills: str,
    interests: str,
    location: str = "Finland",
):
    """Search job advertisements from the local CSV dataset."""
    return select_csv_jobs(
        education="",
        skills=skills,
        experience="",
        interests=interests,
        location=location,
        limit=3,
    )


def generate_tool_recommendations(
    skills, interests, location, language
):
    try:
        client = OllamaModelClient(model_name="llama3.2:3b")

        messages = [
            {
                "role": "system",
                # "content": (
                #     "You are CareerPilot, an AI career assistant. "
                #     "Use the search_jobs tool to search local CSV jobs. "
                #     "Only describe information provided by the tool. "
                #     "Do not invent job requirements, employment type, "
                #     "or whether a vacancy is still open. "
                #     f"Write your final answer in {language}."
                # ),

                "content": (
                    "You are CareerPilot, an AI career assistant. "
                    "Use the search_jobs tool to search local CSV jobs. "
                    "Only describe information provided by the tool. "
                    "Always include the job URL for every recommended vacancy. "
                    "For every job, show: title, company, location, date, source and URL. "
                    "Do not invent job requirements, employment type, "
                    "or whether a vacancy is still open. "
                    f"Write your final answer in {language}."
                ),  
            },
            {
                "role": "user",
                "content": (
                    f"My skills: {skills}\n"
                    f"My interests: {interests}\n"
                    f"My preferred location: {location}\n"
                    "Find suitable jobs using the search_jobs tool."
                ),
            },
        ]

        response = client._client.chat(
            model=client.model_name,
            messages=messages,
            tools=[search_jobs],
        )

        messages.append(response.message)
        tool_calls = response.message.tool_calls or []

        if not tool_calls:
            return (
                "The AI did not call the job search tool. "
                "Please try again."
            )

        jobs_found = False

        for call in tool_calls:
            if call.function.name != "search_jobs":
                continue

            arguments = call.function.arguments or {}

            # Use the actual Gradio form values.
            jobs = search_jobs(
                skills=skills,
                interests=interests,
                location=location,
            )

            if jobs:
                jobs_found = True

            messages.append(
                {
                    "role": "tool",
                    "tool_name": "search_jobs",
                    "content": json.dumps(
                        jobs, ensure_ascii=False
                    ),
                }
            )

        if not jobs_found:
            return "No matching jobs were found in the CSV dataset."

        final_response = client._client.chat(
            model=client.model_name,
            messages=messages,
        )

        return final_response.message.content or (
            "The AI did not generate a response."
        )

    except Exception as error:
        return f"Tool Calling error: {error}"
