import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from gjob.mcp_adapter import sponsorship_mcp, job_mcp
from typing import List

load_dotenv()

llm = LLM(
    model="gpt-4.1",
    provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
    temperature=0.2,
)

@CrewBase
class Gjob():
    """Gjob crew"""
    user_query: str = ""

    agents: List[BaseAgent]
    tasks: List[Task]

   
    @agent
    def parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['parser_agent'], 
            llm=llm,
            verbose=True
        )

    @agent
    def sponsor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['sponsor_agent'], 
            tools=sponsorship_mcp,
            verbose=True
        )

    @agent
    def job_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_agent'], 
            tools=job_mcp,
            verbose=True
        )

   
    @task
    def parse_user_intent(self) -> Task:
        return Task(
            config=self.tasks_config['parse_user_intent'], 
            output_file='parse.json'
        )

    @task
    def find_sponsoring_employers(self) -> Task:
        return Task(
            config=self.tasks_config['find_sponsoring_employers'], 
            output_file='employers.md'
        )

    @task
    def discover_matching_jobs(self) -> Task:
        return Task(
            config=self.tasks_config['discover_matching_jobs'], 
            output_file='jobs.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Gjob crew"""

        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            
        )