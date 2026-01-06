from pydantic_settings import BaseSettings

# Holds GCP variables
class Config(BaseSettings):
    PROJECT_ID: str = "vertex-ai-demo-psg"
    REGION: str = "us-central1"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    STAGING_BUCKET: str = "gs://vertex-ai-demo-psg-interview-agent-artifacts"

config = Config()