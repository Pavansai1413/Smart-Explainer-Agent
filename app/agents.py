from typing import Literal
from typing_extensions import TypedDict
import os
import json

from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()


# Define the State TypedDict
class State(TypedDict):
    user_input: str
    topic: str
    level: str
    intent: str
    collected_info: str
    simplified_explanation: str
    final_answer: str
    messages: list


# Initialize the Google Generative AI model  
llm=ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
        max_output_tokens=500,
        max_retries=1,
    )

# For structured LLM output → Pydantic BaseModel
class Classification(BaseModel):
    topic: str = Field(..., description="Main topic")
    level: Literal["beginner","intermediate","advanced","super_simple"]
    intent: Literal["explain","compare","simplify"]


#1.Agent: Router Agent
def router_agent(state: State) -> State:
    prompt = f"""
    You are an expert to analyze the user request and extract these three things:
    User request: "{state['user_input']}"
    If user has not specified query properly, just respond by asking for clarification.
    If level is not specified, assume "beginner".
    If intent is not specified, assume "explain".
    The JSON schema is:
    {{
        "topic":"main topic",
        "level": "beginner" | "intermediate" | "advanced" | "super_simple",
        "intent": "explain" | "compare" | "simplify",
    }}
    """

    structured_llm = llm.with_structured_output(Classification)

    # One line → always correct
    result = structured_llm.invoke(prompt)

    return {
        "topic": result.topic,
        "level": result.level,
        "intent": result.intent,
        "messages": state["messages"]
    }


# Search Tool
search_tool = TavilySearchResults(max_results=3)


#2.Agent: Information Collection Agent
def info_collection_agent(state: State) -> State:

    llm_with_tools = llm.bind_tools([search_tool])

    prompt = f"""
    you are an expert information collector. Based on the topic "{state['topic']}" at a {state['level']} level with intent "{state['intent']}", 
    Decide if you need to search external info using the available tool. If yes, call the tool with a good query to capture relevant info.
    Then, summarize the key info collected.
    Keep only the concise and relevant information. Do not overfill the information.
    Be accurate but engaging.
    User input for context: {state['user_input']}
    """

    messages = [HumanMessage(content=prompt)] + state.get("messages", [])
    response = llm_with_tools.invoke(messages)
    collected = ""

    # Tool call handling
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call['name'] == search_tool.name:
                results = search_tool.invoke(tool_call['args'])
                collected += "\n".join([res['content'] for res in results if 'content' in res])

    if not collected:
        fallback_prompt = f"Summarize key information about {state['topic']} at {state['level']} level."
        collected = llm.invoke([HumanMessage(content=fallback_prompt)]).content

    return {
        "collected_info": collected,
        "messages": state["messages"] + [AIMessage(content=collected)]
    }


#3.Agent: Explanation Agent
def simplifier_agent(state: State) -> State:
    prompt = f"""
    Your are an expert explainer. Take this collected information and explain it clearly so everyone can understand.
    Use simple language, analogies, examples, like explaining to a beginner.
    Structure it with headings if helpful and conclude correctly.

    Collected Information:
    {state['collected_info']}
    Level: {state['level']}
    """
    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "simplified_explanation": response.content,
        "final_answer": response.content,
        "messages": state["messages"] + [AIMessage(content=response.content)],
    }

