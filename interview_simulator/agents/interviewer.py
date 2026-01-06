import json
from typing import Dict, Any
from interview_simulator.tools.llm_utils import call_llm
from interview_simulator.models.question import Question
from interview_simulator.models.answer import Answer
from interview_simulator.agents.analyzer import clean_and_parse_json

# Interviwer Agent:
# This agent takes a CandidateProfile and job description as input and returns a list of questions and answers.
def interviewer_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("=="*30)
    print("\n [Interviewer Agent] Starting live interview stimulation....")

    profile = state.get("profile")
    if not profile:
        state['error'] = "No profile available from analyzer agent"
        return state
    
    jd_text = state.get("jd_text", "").strip()
    gaps = profile.gaps or []
    
    # This helps to keep track of the interview history and the current question number 
    if "interview_history" not in state:
        state["interview_history"] = []
        state["current_question_num"] = 0
        state["max_questions"] = 5

    history: List[Dict] = state["interview_history"]
    question_num: int = state["current_question_num"]
    
    # This helps to limit the number of questions to 5
    if question_num >= state["max_questions"]:
        print(" \n Interview complete! Moving to evaluation.")
        print("=="*30)
        state["interview_done"] = True
        return state
    
    # This helps to give introduction to the candidate
    if question_num == 0:
        intro_prompt = f"""
        You are an expert interviewer for Technical roles and your name is AQUA. 
        Greet the candidate, mention the this is technical interview, and
        outine the structure of the interview(3-5 interview questions on skills, gaps, experience). 
        """

        intro = call_llm(intro_prompt, "Keep it short professional and engaging.")
        print("=="*30)
        print("\nInterviewer:", intro)
    
    # This helps to keep track of the interview history
    history_str = "\n".join(
        f"Q: {h['question'].text}\nA: {h['answer'].text}" for h in history
    )
    
    # This helps to give the agent the ability to generate the next question
    system_prompt = (
        "You are an skilled technical interviewer and your name is AQUA. Generate ONE question at a time. \n"
        "Adapt based on previous answers and focus on gaps. \n"
        "Keep it more of situation based and real time scenario. \n"
        " Output only valid JSON\n"
        " {\n"
        ' "text": " The question comes here", \n'
        ' "difficulty": "easy/medium/hard", \n'
        "}"
    )
    
    # This helps to generate the next question
    user_prompt = f"""
    jd: {jd_text}
    gaps: {', '.join(gaps)}

    previous history: {history_str}

    Generate the NEXT question (#{question_num + 1}).
    Focus on unconvered areas.
    Return Only JSON.
    """

    response = call_llm(system_prompt, user_prompt)
    question_data = clean_and_parse_json(response)
    question = Question(**question_data)

    print(f"\nInterviewer (Q{question_num + 1}): {question.text}")

    user_input = input("\nCandidate's Answer: ").strip()
    if not user_input:
        state['error'] = "No answer provided by candidate"
        return state
    
    # This helps to store the answer
    answer = Answer(text=user_input, question=question)
    history.append({"question": question, "answer": answer})
    state["interview_history"] = history
    state["current_question_num"] += 1
    print("==="*30)
    print("\n Answer recorded. Waiting for next question...")
    return state
    
 
