from pydantic import BaseModel
from interview_simulator.models.question import Question

class Answer(BaseModel):
    text: str
    question: Question