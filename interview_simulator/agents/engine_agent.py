from typing import Any, Dict, List
from interview_simulator.workflows.graph import create_graph, AgentState

class InterviewEngineAgent:
    """Adapter between Vertex AI Agent Engine and your LangGraph app."""

    def __init__(self):
        self.app = create_graph()

    def query(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        jd_text = inputs.get("jd_text", "")
        resume_path = inputs.get("resume_path", "")
        max_questions = int(inputs.get("max_questions", 5))

        # Build initial state for your graph
        initial_state: AgentState = {
            "jd_text": jd_text,
            "resume_path": resume_path,
            "profile": None,
            "interview_history": [],
            "current_question_num": 0,
            "max_questions": max_questions,
            "interview_done": False,
            "evaluation": None,
            "evaluator_done": False,
            "error": "",
        }

        # Run the LangGraph workflow to completion
        final_state: AgentState = self.app.invoke(initial_state, config={"configurable": {"thread_id": "default-thread"}})

        # Decide what you want to return to the caller
        return {
            "jd_text": final_state.get("jd_text", ""),
            "resume_path": final_state.get("resume_path", ""),
            "profile": final_state.get("profile"),
            "interview_history": final_state.get("interview_history", []),
            "evaluation": final_state.get("evaluation"),
            "error": final_state.get("error", ""),
        }
