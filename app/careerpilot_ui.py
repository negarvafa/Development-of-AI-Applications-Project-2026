
import gradio as gr
from src.services.job_recommendation import recommend_jobs
from src.services.job_matcher import load_jobs, rank_jobs

def generate_recommendations(
    education, skills, experience, interests, location, language, total_experience
):
    return recommend_jobs(
        education, skills, experience, interests, location, language, total_experience
    )

def generate_job_matches(skills, total_experience, location):

    jobs = load_jobs()

    user_skills = [
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ]

    results = rank_jobs(
        user_skills,
        total_experience,
        location,
        jobs
    )

    output = "## Best Matching Jobs\n\n"

    for job in results[:5]:
        output += f"### {job['title']} - {job['company']}\n"
        output += f"**Location:** {job['location']}\n\n"
        output += f"**Overall match:** {job['score']}%\n\n"
        output += f"**Skill match:** {job['skill_score']}%\n\n"
        output += f"**Experience match:** {job['experience_score']}%\n\n"
        output += f"**Location match:** {job['location_score']}%\n\n"

        if job["matching_skills"]:
            output += (
                "**Matching skills:** "
                + ", ".join(job["matching_skills"])
                + "\n\n"
            )

        if job["missing_skills"]:
            output += (
                "**Missing skills:** "
                + ", ".join(job["missing_skills"])
                + "\n\n"
            )

        output += "---\n\n"

    return output

with gr.Blocks(title="CareerPilot") as demo:
    gr.Markdown("# CareerPilot - AI Job Recommendation Assistant")
    gr.Markdown(
        "Enter your background and preferences to discover suitable career paths."
    )

    education = gr.Textbox(
        label="Education",
        placeholder="e.g. ICT Engineering student"
    )

    skills = gr.Textbox(
        label="Skills",
        lines=3,
        placeholder="e.g. Python, networking, HTML"
    )

    experience = gr.Textbox(
        label="Work Experience",
        lines=3,
        placeholder="e.g. Customer service"
    )

    total_experience_slider = gr.Slider(
    minimum=0, 
    maximum=40, 
    step=1, 
    value=0, 
    label="Total work experience in years"
    )

    interests = gr.Textbox(
        label="Career Interests",
        placeholder="e.g. Software development, AI"
    )

    location = gr.Textbox(
        label="Preferred Job Location",
        value="Helsinki"
    )

    language = gr.Dropdown(
        choices=["English", "Finnish", "Swedish"],
        value="English",
        label="Response Language"
    )

    recommend_button = gr.Button(
        "Find Suitable Jobs",
        variant="primary"
    )

    results = gr.Markdown(label="AI Recommendations")

    recommend_button.click(
        fn=generate_job_matches,
        inputs=[
            skills,
            total_experience_slider,
            location
        ],
        outputs=results
    )

    # recommend_button.click(
    #     fn=generate_recommendations,
    #     inputs=[
    #         education,
    #         skills,
    #         experience,
    #         interests,
    #         location,
    #         language,
    #         total_experience_slider
    #     ],
    #     outputs=results
    # )
    
if __name__ == "__main__":
    demo.launch()