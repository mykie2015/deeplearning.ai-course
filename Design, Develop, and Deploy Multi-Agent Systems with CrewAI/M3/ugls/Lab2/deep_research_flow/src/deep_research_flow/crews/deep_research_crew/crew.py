import os
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai_tools import (
	ScrapeWebsiteTool,
	EXASearchTool
)
from deep_research_flow.utils import get_exa_api_key

# import the guardrail
from deep_research_flow.crews.deep_research_crew.guardrails.guardrails import write_report_guardrail

from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

# set the exa API key
os.environ["EXA_API_KEY"] = get_exa_api_key()

@CrewBase
class ParallelDeepResearchCrew:
    """ParallelDeepResearchCrew crew"""
    # Define the agents
    @agent
    def research_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["research_planner"],
            llm='gpt-4o-mini',
            verbose=True
        )

    @agent
    def topic_researcher(self) -> Agent:
        
        return Agent(
            config=self.agents_config["topic_researcher"],
            # Define the tools
            tools=[
				EXASearchTool(base_url=os.getenv("EXA_BASE_URL")),
                ScrapeWebsiteTool()
            ],
            llm='gpt-4o-mini',
            verbose=True
        )
    
    @agent
    def fact_checker(self) -> Agent:
        
        return Agent(
            config=self.agents_config["fact_checker"],
            tools=[
				EXASearchTool(base_url=os.getenv("EXA_BASE_URL")),
                ScrapeWebsiteTool()
            ],
            llm='gpt-4o-mini',
            verbose=True
        )
    
    @agent
    def report_writer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["report_writer"],
            llm='gpt-4o-mini',
            verbose=True
        )

    
    @task
    def create_research_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_research_plan"],
            llm='gpt-4o-mini',
        )
    

    # Define the tasks
    @task
    def research_main_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_main_topics"],
            async_execution=True,
        )
    
    @task
    def research_secondary_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_secondary_topics"],
            async_execution=True,
        )
    
    @task
    def validate_main_topics(self) -> Task:
        return Task(
            config=self.tasks_config["validate_main_topics"],
        )
    
    @task
    def validate_secondary_topics(self) -> Task:
        return Task(
            config=self.tasks_config["validate_secondary_topics"],
        )
    
    @task
    def write_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["write_final_report"],
            # add the guardrail
            guardrails=[write_report_guardrail],
            markdown=True,
            output_file='report.md'
        )


    # Define the crew
    @crew
    def crew(self) -> Crew:
        """Creates the ParallelDeepResearchCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            # Define the sequential process
            process=Process.sequential,
            # Set the memory to True so the crew remembers previous interactions
            memory=True,  
            verbose=True,
            knowledge_sources=[TextFileKnowledgeSource(
                file_paths=["user_preference.txt"]
            )]
        )