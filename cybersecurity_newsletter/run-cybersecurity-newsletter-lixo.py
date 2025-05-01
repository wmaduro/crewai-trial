from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM
import os
import dotenv

dotenv.load_dotenv()

# to change the ollama url, you can change the OLLAMA_URL environment variable at .env
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")

ollama_openhermes = LLM(
    model="openhermes",         # Nome do modelo que você tem localmente
    base_url=ollama_url,  # Default do Ollama
    api_key=None,               # Ollama não precisa de API Key
    custom_llm_provider="ollama"
)


#define the agent - note no tools so its only going to tell you what it knows
researcher = Agent(
    role='merda',
    goal='Uncoverer information about emerging cybersecurity vulnerabilities',
    backstory="""
        You are a Top CyberSecurity researcher tasked with finding detailed information about emerging Cybersecurity vulnerabilities.
    """,
    verbose=False,
    allow_delegation=False,
    llm=ollama_openhermes
)
task1 = Task(description='Investigate emerging cybersecurity vulnerabilities that have come out in the past few months. The result must be written in just one paragraph with max 10 words.', agent=researcher, expected_output='Text research')

#get working
crew = Crew(
    agents=[researcher,],
    tasks=[task1,],
    verbose=False,
    #process=Process.sequential
)

result = crew.kickoff()

print(f"---> result:  {result}")
