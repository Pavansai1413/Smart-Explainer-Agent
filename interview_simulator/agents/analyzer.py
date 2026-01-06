from interview_simulator.tools.resume_parser import parse_resume
from interview_simulator.tools.llm_utils import call_llm
from interview_simulator.models.profile import CandidateProfile
from typing import List, Dict, Any
import json
import re

# Analyzer Agent
# This agent takes a resume and job description as input and returns a CandidateProfile object.
def analyzer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    resume_text = parse_resume(state["resume_path"])
    jd_text = state.get("jd_text", "").strip()
    
    # System prompt
    system_prompt = (
        "You are an expert resume and job description analyzer for technical roles"
        "Extract key skills, years of experience, gaps compared to the JD provided."
        "Output a valid JSON matching this structure:\n"
        "{\n"
        ' "skills": ["python", "SQL",...], \n'
        ' "experience": {"python":4, "machine learning":3, ...}, \n'
        ' "gaps": ["missing experinece with spark", ...], \n'
        "}"
    )

    # User prompt
    user_prompt = f"""
    Job Description: {jd_text}
    Resume: {resume_text}
    
    Analyze and output JSON only
    """
     
    response = call_llm(user_prompt, system_prompt)
    data = clean_and_parse_json(response) 
    profile = CandidateProfile(**data)
    state['profile'] = profile
    state.pop("error", None)
    return state

# Helper function to clean and parse JSON from LLM response
def clean_and_parse_json(llm_response: str) -> dict:
    text = llm_response.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```$', '', text, flags=re.MULTILINE)
    text = text.strip()
    start = text.find('{')
    if start == -1:
        raise ValueError("No opening brace found")
    end = text.rfind('}') + 1
    if end <= 1:
        raise ValueError("No closing brace found")
    json_str = text[start:end]
    return json.loads(json_str)