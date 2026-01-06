from typing import Dict, Any
from interview_simulator.tools.llm_utils import call_llm
from interview_simulator.models.question import Question
from interview_simulator.models.answer import Answer
from interview_simulator.agents.analyzer import clean_and_parse_json
from interview_simulator.models.evaluation import QuestionEvaluation, InterviewEvaluation
import statistics


# Evaluation Agent:
# This agent takes a list of questions and answers as input and returns a list of scores.
def evaluation_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("=="*30)
    print("\n [Evaluation Agent] Starting interview evaluation...")

    history = state.get("interview_history", [])
    if not history:
        state['error'] = "No interview history found"
        return state
    profile = state.get("profile")
    jd_text = state.get("jd_text", "")
    gaps = profile.gaps if profile else []

    evaluations = []

    for i, entry in enumerate(history, 1):
        question = entry["question"]
        answer = entry["answer"]
        system_prompt = (
            "You are an expert technical interviewer evaluator who evaluates candidate responses.\n"
            "Check if candidate answer is relevant to the question. If not provide less score.\n"
            "Score the answer on a scale of 1-10 based on provided answer and given question: \n"
            "-Technical accuracy\n"
            "-Relevance to the question\n"
            "-Clarity of explanation\n"
            "-Depth of knowledge\n"
            "-Problem-solving approach\n"
            "Return Only valid JSON with keys: score, strengths, weaknesses, feedback, areas to improve."
            "{\n"
            '  "score": give score between 1-10 for each question based on candidate answer,\n'
            '  "strengths": ["list of strengths"],\n'
            '  "weaknesses": ["list of weaknesses"],\n'
            '  "feedback": "detailed feedback text"\n'
            '  "areas_to_improve": ["list of areas to improve"]\n'
            "}"
        )

        user_prompt = f"""
        jd: {jd_text}
        known gaps: {', '.join(gaps)}
        Question {i}: {question.text}
        Candidate's Answer: {answer.text}

        Evaluate strictly but fairly. Return JSON only.
        """
        response = call_llm(system_prompt, user_prompt)
        evaluation_data = clean_and_parse_json(response)

        eval_item = QuestionEvaluation(
            question_text=question.text,
            candidate_answer=answer.text,
            score=float(evaluation_data["score"]),
            strengths=evaluation_data["strengths"],
            weaknesses=evaluation_data["weaknesses"],
            feedback=evaluation_data["feedback"],
            areas_to_improve=evaluation_data["areas_to_improve"],
        )
        evaluations.append(eval_item)

        scores = [e.score for e in evaluations]
        overall_score = round(statistics.mean(scores), 2) if scores else 0.0

        summary = f" Candidate performed {'strongly' if overall_score >= 7 else 'moderately' if overall_score >= 5 else 'with room for improvement'}. Average score: {overall_score}/10"
        
        full_evaluation = InterviewEvaluation(
            summary=summary,
            overall_score=overall_score,
            evaluations=evaluations,
        )
        state["evaluation"] = full_evaluation
        state["evaluator_done"] = True
        print("==="*30)
        print("\n Evaluation Completed! \n")
        print(summary)

        return state

    
