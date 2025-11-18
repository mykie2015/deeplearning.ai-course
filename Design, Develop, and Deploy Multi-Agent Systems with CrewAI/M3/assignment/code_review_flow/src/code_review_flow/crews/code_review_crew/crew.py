import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
    ScrapeWebsiteTool,
)
from pydantic import BaseModel
from code_review_flow.utils import get_serper_api_key, get_openai_api_key
# import the guardrails
from code_review_flow.crews.code_review_crew.guardrails.guardrails import security_review_output_guardrail

os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["SERPER_API_KEY"] = get_serper_api_key()

@CrewBase
class CodeReviewCrew:
    """CodeReview crew"""
    @agent
    def senior_developer(self) -> Agent:       
        return Agent(
            config=self.agents_config["senior_developer"],
            llm="gpt-4o-mini",
        )

    ### START CODE HERE ###
    @None
    ### END CODE HERE ###
    def security_engineer(self) -> Agent:
        os.environ["SERPER_API_KEY"] = get_serper_api_key()
        return Agent(
            config=self.agents_config["security_engineer"],
            tools=[
                # add the SerperDevTool to the agent's tools
                SerperDevTool(search_url="https://owasp.org",
                              base_url=os.getenv("DLAI_SERPER_BASE_URL")),
                ScrapeWebsiteTool() 
                ],
            llm="gpt-4o-mini"
        )
    
    ### START CODE HERE ###
    @None
    ### END CODE HERE ###
    def tech_lead(self) -> Agent:
        return Agent(
            config=self.agents_config["tech_lead"],
            llm="gpt-4o-mini",
        )
        
    @task
    def analyze_code_quality(self) -> Task:
        # Define the pydantic model for the code quality analysis output
        class CodeQualityJSON(BaseModel):
            critical_issues: list[str]
            minor_issues: list[str]
            reasoning: str
        return Task(
            config=self.tasks_config["analyze_code_quality"],
            output_json=CodeQualityJSON,
            
            ### START CODE HERE ###
            # allow for asynchronous execution
            async_execution=None,
            ### END CODE HERE ###
        )
    
    ### START CODE HERE ###
    @None
    ### END CODE HERE ###
    def review_security(self) -> Task:
        # Define the pydantic model for the security vulnerabilities
        class SecurityVulnerability(BaseModel):
            description: str 
            risk_level: str 
            evidence: str

        # Define the pydantic model for the security review output
        class ReviewSecurityJSON(BaseModel):
            security_vulnerabilities: list[SecurityVulnerability] 
            blocking: bool
            highest_risk: str
            security_recommendations: list[str]

        return Task(
            config=self.tasks_config["review_security"],
            output_json=ReviewSecurityJSON,

            ### START CODE HERE ###
            # allow for asynchronous execution
            async_execution=None,
            ### END CODE HERE ###

            # add the security review output guardrail (already imported above)
            guardrails=[security_review_output_guardrail]
        )
    
    ### START CODE HERE ###
    @None
    ### END CODE HERE ###
    def summarize_findings(self) -> Task:
        
        # Define the pydantic model for the fixes output
        class Fix(BaseModel):
            description: str 
            solutions: str 
            explanation: str

        ### START CODE HERE ###
        # Define the pydantic model for the summarized findings output
        class SummarizedFindingsJSON(BaseModel):
            confidence: None
            findings: None
            fix: None[Fix]
            recommendations: list[None]
        ### END CODE HERE ###
        
        return Task(
            config=self.tasks_config["summarize_findings"],
            # Set the Markdown parameter to get the final report in Markdown format
            output_json=SummarizedFindingsJSON,
        )
    

    ### START CODE HERE ###
    @None
    ### END CODE HERE ###
    def crew(self) -> Crew:
        """Creates the CodeReviewCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            # set the process to sequential
            process=Process.sequential,
            verbose=True,
            memory=True,
        )