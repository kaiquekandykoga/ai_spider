from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage


def match_jobs(raw_text: str, profile: dict) -> str:
    """Use Ollama / llama3.2:3b via LangChain to match jobs against a candidate profile."""
    llm = ChatOllama(model="llama3.2:3b", temperature=0)

    skills = ", ".join(profile.get("skills", []))
    desired_titles = ", ".join(profile.get("desired_titles", []))
    location = profile.get("location", "Any")

    system_prompt = f"""You are a helpful job-search assistant. 
Given the candidate profile and the job listings provided, score each job from 1-10 based on how well it matches the candidate's profile.

Candidate Profile:
- Skills: {skills}
- Desired Titles: {desired_titles}
- Location: {location}

Instructions:
1. Score each job 1-10 based on: skill match, title match, and location match
2. Only return jobs that score 6 or above
3. Output format exactly as: Job Title | Company | Location | Score/10 | Reason
4. If no jobs score 6 or above, say so clearly"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Here are the job listings:\n\n{raw_text}"),
    ]
    print("Sending content to Ollama (llama3.2:3b) for job matching...\n")
    response = llm.invoke(messages)
    return response.content
