from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pathlib import Path
from crewai import LLM
import yaml
from typing import List
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

@CrewBase
class CrewAgents():
    """CrewAgents crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self) -> None:
        # Get the current script's folder
        base_dir = Path(__file__).parent

        # Form the complete file path
        agent_file_path = base_dir / 'config/agents.yaml'
        task_file_path = base_dir / 'config/tasks.yaml'

        try:
            with agent_file_path.open('r') as afile:
                self.agents_config = yaml.safe_load(afile)
            with task_file_path.open('r') as tfile:
                self.tasks_config = yaml.safe_load(tfile)
        except FileNotFoundError as e:
            print(f"Error: file not found in the same directory: {e}")

        self.llm = ChatOllama(model="mistral")
    

    @agent
    def customer_service(self) -> Agent:
        return Agent(
            config=self.agents_config.get('customer_service'),
            llm=self.llm,
            verbose=True
        )

    @agent
    def payment_service(self) -> Agent:
        return Agent(
            config=self.agents_config.get('payment_service'),
            llm=self.llm,
            verbose=True
        )
    
    @task
    def customer_service_task(self) -> Task:
        return Task(
            config=self.tasks_config.get('research_task'),
            output_file='report.md'
        )

    @task
    def payment_service_task(self) -> Task:
        return Task(
            config=self.tasks_config.get('reporting_task'),
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewAgents crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
