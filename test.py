import vertexai
from vertexai import agent_engines

vertexai.init(project="vertex-ai-demo-psg", location="us-central1")

agent_engine = agent_engines.get(
    "projects/630041212894/locations/us-central1/reasoningEngines/6339965465174999040"
)

jd_text = "A Tier 1 technology organization within the Chief Data Office (CDO) is seeking a highly motivated Developer with 3–5 years of experience supporting development teams in a data-driven, migration-focused environment, working closely with data engineers, product teams, and application developers to support platform development, ETL migration, and full-stack implementation using modern data and AI technologies. The role involves supporting data migration initiatives, data pipelines, application and REST API integrations, contributing to full-stack development across backend, frontend, and API layers, developing and troubleshooting ETL workflows, collaborating with cross-functional teams to meet enterprise CDO requirements, and following best practices in code reviews, version control, and structured development processes. The ideal candidate holds a B.S. in Computer Science or a related field, has strong experience with Palantir (mandatory), Databricks or Snowflake (at least one), SQL, Python, PySpark, data engineering fundamentals, REST APIs, and full-stack web development using Node.js, TypeScript (critical for Palantir), and React.js, with familiarity in GitHub Copilot and exposure to tools like IBM WatsonX.data or Windsurf as a plus. Preferred qualifications include exposure to AI and GenAI concepts such as RAG architectures, chatbots, and agentic AI frameworks including LangGraph, LangChain, agent architectures, or MCP servers, along with strong collaboration, problem-solving, and analytical skills, and a high level of motivation to grow in a fast-paced enterprise CDO environment."
resume_path = r"C:\IVORSOURCE\Vertex_AI_Agent_Builder\vertex_ai_agent_builder\my_resume.docx"

response = agent_engine.query(
    inputs={
        "jd_text": jd_text,
        "resume_path": resume_path,
    }
)

print(response)


