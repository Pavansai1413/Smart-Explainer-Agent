from pydantic import BaseModel
from typing import List, Dict

class QuestionEvaluation(BaseModel):
    question_text: str
    candidate_answer: str
    score: float
    strengths: List[str]
    weaknesses: List[str]
    feedback: str
    areas_to_improve: List[str]


class InterviewEvaluation(BaseModel):
    overall_score: float
    evaluations: List[QuestionEvaluation]
    summary: str