from pydantic import BaseModel
from typing import List, Dict, Optional

# CandidateProfile model
class CandidateProfile(BaseModel):
    skills: List[str]
    experience: Dict[str, int]
    gaps: List[str]