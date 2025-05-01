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
    role='researcher',
    goal='Uncoverer information about emerging cybersecurity vulnerabilities',
    backstory='You are a Top CyberSecurity researcher tasked with finding detailed information about emerging Cybersecurity vulnerabilities.',
    verbose=True,
    allow_delegation=False,
    llm=ollama_openhermes
)

#define the agent - note no tools so its only going to tell you what it knows
writer = Agent(
    role='A writer of a popular cybersecurity newsletter',
    goal='Generate a detailed Cybersecurity newsletter',
    backstory='You are a Top CyberSecurity writer known for writing detailed and engaging newsletters',
    verbose=True,
    allow_delegation=False,
    llm=ollama_openhermes
)

#define the tasks
task1 = Task(description='Investigate emerging cybersecurity vulnerabilities that have come out in the past few months', agent=researcher, expected_output='Text research')
task2 = Task(description='Write a compelling and detailed newsletter about cybersecurity vulnerabilities emerging in the past few months, make sure each vulnerability recieves its own section the newsletter', agent=writer, expected_output='A refined finalized version of report in text format')

#get working
crew = Crew(
    agents=[researcher,writer],
    tasks=[task1,task2],
    verbose=True,
    #process=Process.sequential
)

result = crew.kickoff()
