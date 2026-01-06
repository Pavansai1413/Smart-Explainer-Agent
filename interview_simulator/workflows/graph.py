from typing import Dict, Any, TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from interview_simulator.agents.interviewer import interviewer_agent
from interview_simulator.agents.analyzer import analyzer_agent
from interview_simulator.agents.evaluation import evaluation_agent

# Define the state of the interview
class AgentState(TypedDict):
    resume_path: str
    jd_text: str
    profile: Any
    interview_history: Annotated[list, lambda a, b: a+b]
    current_question_num: int
    max_questions: int
    interview_done: bool
    evaluation: Any
    evaluator_done: bool
    error: str

# Function to create the workflow
def create_graph():
    workflow = StateGraph(AgentState)

    #Nodes
    workflow.add_node("analyzer", analyzer_agent)
    workflow.add_node("interviewer", interviewer_agent)
    workflow.add_node("evaluator", evaluation_agent)
    
    #Entry Point
    workflow.set_entry_point("analyzer")

    #Edges
    workflow.add_edge("analyzer", "interviewer")

    #Conditional Edge
    workflow.add_conditional_edges(
        "interviewer",
        should_continue,
        {
            "interviewer": "interviewer",
            "evaluator": "evaluator",
            END: END
        }
    )

    workflow.add_edge("evaluator", END)

    memory = MemorySaver()

    app = workflow.compile(checkpointer=memory)
    return app

# Function to determine the next node to execute based on the state of the interview
def should_continue(state: AgentState) -> str:
    if state.get("error"):
        return END
    if state.get("evaluator_done"):
        return END
    if state.get("interview_done"):
        return "evaluator"
    return "interviewer"