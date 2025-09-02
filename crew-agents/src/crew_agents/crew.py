from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pathlib import Path
from crewai import LLM
import yaml
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CrewAgents():
    """CrewAgents crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

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

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config.get('researcher'),
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config.get('reporting_analyst'),
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config.get('research_task'),
            output_file='report.md'
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config.get('reporting_task'),
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewAgents crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
