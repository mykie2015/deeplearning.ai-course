#!/usr/bin/env python
from pydantic import BaseModel
from crewai import LLM
from crewai.flow import Flow, listen, start, router, or_
from crewai.flow.persistence import persist
from deep_research_flow.crews.deep_research_crew.crew import ParallelDeepResearchCrew
import os
os.environ["CREWAI_TESTING"] = "true"

# define the flow state
class ResearchState(BaseModel):
    user_query: str = ""
    ### START CODE HERE ###
    needs_research: None = None # set the default value to False
    research_report: None = None # set the default value to an empty string
    final_answer: None = None # set the default value to an empty string
    ### END CODE HERE ###

### START CODE HERE ###
# add persistence to the flow
@None()
### END CODE HERE ###

class DeepResearchFlow(Flow[ResearchState]):
    # define the entrypoint
    ### START CODE HERE ###
    @None()
    ### END CODE HERE ###
    def start_conversation(self):
        """Entry point for the flow"""
        print("🔍 Deep Research Flow started")
        print(self.state.user_query)
        if self.state.user_query != "":
            print(f"I remember last time you wanted to know about {self.state.user_query}")
        self.state.user_query = input("\033[1;31m What would you like to know?\033[0m  \n>> \n")
        print(f"Query received: \"{self.state.user_query}\"")

    # define the router
    ### START CODE HERE ###
    @None(start_conversation)
    ### END CODE HERE ###
    def analyze_query(self):
        """Router: Should trigger research?"""
        print("🤔 Analyzing query complexity...")
        
        ### START CODE HERE ###
        prompt = (# Write the prompt for the LLM to decide if the query is simple or requires research 
                  None
                  f"Query: \"{self.state.user_query}\"\n\n"
                  "Response (one word only):")
        ### END CODE HERE ###

        # define the llm for the decision 
        llm = LLM(model="gpt-4o-mini",)
        # call the llm and save the result
        decision = llm.call(messages=prompt)

        if "RESEARCH" in decision.upper():
            self.state.needs_research = True
            print("📚 Complex query detected - initiating research process")
            return "RESEARCH"
        else:
            print("💬 Simple query detected - providing direct answer")
            return "SIMPLE"
    
    # define the simple answer task (no research needed)
    @listen("SIMPLE")
    def simple_answer(self):
        """LLM: Direct answer for simple queries"""
        print("✨ Generating direct answer...")
        
        ### START CODE HERE ###
        prompt = (# Write the missing part of the query for the LLM 
                 None
                 f"Query: \"{self.state.user_query}\"\n\n"
                 "Answer:"
                 )
        # set up the LLM
        llm = None(model="gpt-4o-mini")
        # call the llm with the prompt and save the result to the final_answer state variable
        self.state.final_answer = llm.call(messages=None)
        ### END CODE HERE ###

    # define the clarification task (if research is needed)
    ### START CODE HERE ###
    @None(None)
    #### END CODE HERE ###
    def clarify_query(self):
        """LLM: Clarification before research"""
        print("🔍 Reviewing query for research clarity...")
        
        # write the prompt to decide if the query is clear enough
        prompt = ("Review this research query and determine if it's clear enough "
                 "for comprehensive research.\n\n"
                 "Respond in one of these formats:\n"
                 "- If clear and specific: \"PROCEED\"\n"
                 "- If needs clarification: \"CLARIFY: [specific questions to ask the user]\"\n\n"
                 f"Query: \"{self.state.user_query}\"\n\n"
                 "Response:"
                 )
        # define the llm and call it with the prompt
        llm = LLM(model="gpt-4o-mini",)
        response = llm.call(messages=prompt)

        # if the query is not clear, ask the user for clarification
        if "PROCEED" not in response:
            clarification_needed = response.replace("CLARIFY:", "").strip()
            print(f"❓ \033[1;31m Clarification needed:\n\033[0m {clarification_needed}")
            additional_info = input("\033[1;31m Please provide more details: \n>> \n\033[0m")
            # update the user_query state variable with the additional information
            self.state.user_query += f"\n\nAdditional context: {additional_info}"
    
    # define the research execution task
    ### START CODE HERE ###
    @None("clarify_query")
    ### END CODE HERE ###
    def execute_research(self):
        """Execute the Deep Research Crew"""
        print("🚀 Executing deep research crew...")
        print(f"🔍 Researching: \"{self.state.user_query}\"")

        # define the crew
        research_crew = ParallelDeepResearchCrew()

        ### START CODE HERE ###

        # kickoff the crew with the user query as input
        result = research_crew.crew().None(
            # use the value in the user_query state variable as the input
            inputs={"user_query": self.None.None}
        )

        # update the research_report state variable with the crew's output (use the `raw` attribute)
        self.state.research_report = result.None
        ### END CODE HERE ###
        
        print("✅ Research completed successfully!")

        
    # define the task to save and summarize the report
    ### START CODE HERE ###
    @None(None)
    ### END CODE HERE ###
    def save_report_and_summarize(self):
        """
        Save the final research report to a local markdown file
        """
        # save the report
        try:
            with open("../research_report.md", "w", encoding="utf-8") as f:
                ### START CODE HERE ###
                # write the content of the research_report state variable to the file
                f.write(self.state.None)
                ### END CODE HERE ###
            print("✅ Report saved successfully!")
        except Exception as e:
            print(f"❌ Failed to save report: {str(e)}")
        
        # summarize the report
        # define the LLM and and write the prompt
        llm = LLM(model="gpt-4o-mini")
        prompt = ("Summarize the following research report into a one paragraph, informative answer:\n\n"
                  f"Report: \"{self.state.research_report}\"\n\n"
                 )
        # update the final_answer state variable with the summary from the LLM call
        self.state.final_answer = ("This is a summary of the final answer:\n\n" 
                                    f"{llm.call(messages=prompt)}\n\n"
                                    "A full report has been saved to research_report.md."
                                    )
    
    # define the final answer task
    @listen(or_("simple_answer", "save_report_and_summarize"))
    def return_final_answer(self):
        """Return the final answer to the user"""
        print("📝 Final Answer:")
        print(f"📌 Original Query: \"{self.state.user_query}\"")
        print(f"{self.state.final_answer}")
        print("\n✨ Deep Research Flow completed!")

    

def kickoff():
    ### START CODE HERE ###
    # instantiate the DeepResearchFlow with tracing enabled
    deep_research_flow = DeepResearchFlow(None=True)
    ### END CODE HERE ###
    
    # kickoff the flow with a custom id, so you can persist the state
    deep_research_flow.kickoff(inputs={"id": "our-deep-research_flow"})
    

def plot():
    deep_research_flow = DeepResearchFlow()
    deep_research_flow.plot()


if __name__ == "__main__":
    kickoff()