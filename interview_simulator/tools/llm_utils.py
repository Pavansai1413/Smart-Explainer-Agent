from langchain_google_vertexai import ChatVertexAI
from interview_simulator.config.config import config
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project=config.PROJECT_ID, location=config.REGION)

# Initialize the Generative Model
model = GenerativeModel(model_name=config.GEMINI_MODEL)

# Function to call the LLM
def call_llm(prompt: str, system_prompt: str = "") -> str:
    response = model.generate_content(
        [system_prompt + "\n\n" + prompt] if system_prompt else [prompt],
        generation_config = {
            "temperature": 0.2
        }
    )
    return response.text




"""
# Function to call the LLM
def call_llm(prompt:str, system_prompt:str = "") -> str:
    response = llm.invoke([("system", system_prompt), ("human", prompt)])
    return response.content
"""