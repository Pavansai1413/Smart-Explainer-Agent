from vertexai import agent_engines
from vertexai import Client
import vertexai
from interview_simulator.workflows.graph import create_graph 
from interview_simulator.config.config import config
from interview_simulator.agents.engine_agent import InterviewEngineAgent

print("Creating graph...")
local_agent = InterviewEngineAgent()

print("Deploying to vertex AI Agent Engine...")

vertexai.init(project=config.PROJECT_ID, location=config.REGION, staging_bucket=config.STAGING_BUCKET)



remote_agent = agent_engines.create(
    local_agent,
    requirements=[
        "google-cloud-aiplatform", 
        "langchain-google-vertexai", 
        "langgraph", 
        "vertexai", 
        "pydantic", 
        "PyPDF2",
        "python-docx",
        "pydantic_settings",
    ],
    display_name="Interview Simulator",
    description="Multi Agent technical interview simulator with analysis of the interview.",
    gcs_dir_name = f"gs://{config.PROJECT_ID}-interview-agent-artifacts/deployment/",
    extra_packages=["."],
)

print(" \n Deployment completed!")
print(f"Agent ID: {remote_agent.name}")
print(f"Test in console: https://console.cloud.google.com/vertex-ai/agents")


