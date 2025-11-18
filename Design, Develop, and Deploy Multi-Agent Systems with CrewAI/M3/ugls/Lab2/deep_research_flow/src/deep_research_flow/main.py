#!/usr/bin/env python
from pydantic import BaseModel
from crewai import LLM
from crewai.flow import Flow, listen, start, router, or_
from crewai.flow.persistence import persist
from deep_research_flow.crews.deep_research_crew.crew import ParallelDeepResearchCrew
import os
import sys
os.environ["CREWAI_TESTING"] = "true"

# define the flow state
class ResearchState(BaseModel):
    user_query: str = ""
    ### START CODE HERE ###
    needs_research: bool = False # set the default value to False
    research_report: str = "" # set the default value to an empty string
    final_answer: str = "" # set the default value to an empty string
    ### END CODE HERE ###

### START CODE HERE ###
# add persistence to the flow
@persist()
### END CODE HERE ###

class DeepResearchFlow(Flow[ResearchState]):
    # define the entrypoint
    ### START CODE HERE ###
    @start()
    ### END CODE HERE ###
    def start_conversation(self):
        """Entry point for the flow"""
        print("\n" + "="*70)
        print("🔍 Deep Research Flow started")
        print("="*70)
        if self.state.user_query != "":
            print(f"\n💭 Previous query: {self.state.user_query}")
        print("\n❓ What would you like to know?")
        print(">> ", end="", flush=True)
        
        # Use raw_input style for better visibility
        import readline  # This helps with input echo on Unix/Mac
        try:
            self.state.user_query = input()  # Simple input() works best with readline imported
        except EOFError:
            self.state.user_query = ""
        
        print(f"\n✅ Query received: \"{self.state.user_query}\"")
        print("-"*70)

    # define the router
    ### START CODE HERE ###
    @router(start_conversation)
    ### END CODE HERE ###
    def analyze_query(self):
        """Router: Should trigger research?"""
        print("\n🤔 STEP 1: Analyzing query complexity...")
        print(f"   Query: \"{self.state.user_query[:100]}...\"" if len(self.state.user_query) > 100 else f"   Query: \"{self.state.user_query}\"")
        
        ### START CODE HERE ###
        prompt = (# Write the prompt for the LLM to decide if the query is simple or requires research 
                  "Analyze this query and determine if it requires deep research or can be answered simply.\n"
                  "Respond with 'RESEARCH' if it requires comprehensive research from multiple sources.\n"
                  "Respond with 'SIMPLE' if it can be answered with general knowledge.\n\n"
                  f"Query: \"{self.state.user_query}\"\n\n"
                  "Response (one word only):")
        ### END CODE HERE ###

        # define the llm for the decision 
        print("   🔄 Calling LLM to analyze...")
        llm = LLM(model="gpt-4o-mini",)
        # call the llm and save the result
        decision = llm.call(messages=prompt)

        if "RESEARCH" in decision.upper():
            self.state.needs_research = True
            print("\n📚 DECISION: Complex query - Initiating RESEARCH route")
            print("   ↳ Will deploy 4-agent research crew")
            print("-"*70)
            return "RESEARCH"
        else:
            print("\n💬 DECISION: Simple query - Using SIMPLE route")
            print("   ↳ Will use direct LLM answer")
            print("-"*70)
            return "SIMPLE"
    
    # define the simple answer task (no research needed)
    @listen("SIMPLE")
    def simple_answer(self):
        """LLM: Direct answer for simple queries"""
        print("\n✨ STEP 2: Generating direct answer...")
        print("   🔄 Calling GPT-4o-mini...")
        
        ### START CODE HERE ###
        prompt = (# Write the missing part of the query for the LLM 
                 "Provide a clear and helpful answer to the following query:\n\n"
                 f"Query: \"{self.state.user_query}\"\n\n"
                 "Answer:"
                 )
        # set up the LLM
        llm = LLM(model="gpt-4o-mini")
        # call the llm with the prompt and save the result to the final_answer state variable
        self.state.final_answer = llm.call(messages=prompt)
        ### END CODE HERE ###
        print("   ✅ Answer generated successfully")
        print("-"*70)

    # define the clarification task (if research is needed)
    ### START CODE HERE ###
    @listen("RESEARCH")
    #### END CODE HERE ###
    def clarify_query(self):
        """LLM: Clarification before research"""
        print("\n🔍 STEP 2: Reviewing query for research clarity...")
        print("   🔄 Analyzing if query needs clarification...")
        
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
            print("\n❓ Clarification needed:")
            print(clarification_needed)
            print("\n💡 Options:")
            print("   1. Provide more details")
            print("   2. Press Enter to skip and proceed anyway")
            print("   3. Type 'skip' to proceed with current query")
            print("\nYour response (will auto-skip in 60s):")
            print(">> ", end="", flush=True)
            
            # Set a timeout for input
            import select
            timeout = 60  # 60 seconds
            
            # Use select to implement timeout (Unix/macOS only)
            additional_info = ""
            if hasattr(select, 'select'):
                ready, _, _ = select.select([sys.stdin], [], [], timeout)
                if ready:
                    try:
                        import readline
                        additional_info = input()
                    except (EOFError, KeyboardInterrupt):
                        additional_info = "skip"
                else:
                    additional_info = "skip"
                    print("\n⏰ Timeout reached - proceeding with original query")
            else:
                # Fallback - just use input with timeout warning
                try:
                    import readline
                    additional_info = input()
                except (EOFError, KeyboardInterrupt):
                    additional_info = "skip"
            
            if additional_info and additional_info.lower() != 'skip':
                print(f"\n✅ Additional context received: {additional_info[:50]}...")
                # update the user_query state variable with the additional information
                self.state.user_query += f"\n\nAdditional context: {additional_info}"
                print(f"   ↳ Updated query with clarifications")
            else:
                print("\n⏭️  Skipping clarification - proceeding with original query")
        else:
            print("   ✅ Query is clear - proceeding to research")
        print("-"*70)
    
    # define the research execution task
    ### START CODE HERE ###
    @listen("clarify_query")
    ### END CODE HERE ###
    def execute_research(self):
        """Execute the Deep Research Crew"""
        print("\n🚀 STEP 3: Executing deep research crew...")
        print("="*70)
        print("📋 RESEARCH QUERY:")
        print(f"   {self.state.user_query}")
        print("="*70)
        
        print("\n👥 Deploying 4-Agent Research Crew:")
        print("   1️⃣  Research Planner - Breaking query into topics")
        print("   2️⃣  Topic Researcher - Gathering information (EXA + Web Scraping)")
        print("   3️⃣  Fact Checker - Validating accuracy")
        print("   4️⃣  Report Writer - Synthesizing findings")
        print("\n⏳ This may take 2-5 minutes. Please wait...\n")
        print("-"*70)

        # define the crew
        research_crew = ParallelDeepResearchCrew()

        ### START CODE HERE ###

        # kickoff the crew with the user query as input
        result = research_crew.crew().kickoff(
            # use the value in the user_query state variable as the input
            inputs={"user_query": self.state.user_query}
        )

        # update the research_report state variable with the crew's output (use the `raw` attribute)
        self.state.research_report = result.raw
        ### END CODE HERE ###
        
        print("\n" + "="*70)
        print("✅ Research completed successfully!")
        print(f"   📊 Report length: {len(self.state.research_report)} characters")
        print("="*70)

        
    # define the task to save and summarize the report
    ### START CODE HERE ###
    @listen("execute_research")
    ### END CODE HERE ###
    def save_report_and_summarize(self):
        """
        Save the final research report to a local markdown file
        """
        print("\n💾 STEP 4: Saving report and creating summary...")
        print("-"*70)
        
        # save the report
        try:
            report_path = "../research_report.md"
            with open(report_path, "w", encoding="utf-8") as f:
                ### START CODE HERE ###
                # write the content of the research_report state variable to the file
                f.write(self.state.research_report)
                ### END CODE HERE ###
            import os
            abs_path = os.path.abspath(report_path)
            print(f"✅ Report saved successfully!")
            print(f"   📁 Location: {abs_path}")
        except Exception as e:
            print(f"❌ Failed to save report: {str(e)}")
        
        # summarize the report
        print("\n📝 Generating executive summary...")
        print("   🔄 Calling GPT-4o-mini to summarize...")
        # define the LLM and and write the prompt
        llm = LLM(model="gpt-4o-mini")
        prompt = ("Summarize the following research report into a one paragraph, informative answer:\n\n"
                  f"Report: \"{self.state.research_report}\"\n\n"
                 )
        # update the final_answer state variable with the summary from the LLM call
        summary = llm.call(messages=prompt)
        self.state.final_answer = ("This is a summary of the final answer:\n\n" 
                                    f"{summary}\n\n"
                                    "A full report has been saved to research_report.md."
                                    )
        print("   ✅ Summary generated")
        print("-"*70)
    
    # define the final answer task
    @listen(or_("simple_answer", "save_report_and_summarize"))
    def return_final_answer(self):
        """Return the final answer to the user"""
        print("\n" + "="*70)
        print("📝 FINAL ANSWER")
        print("="*70)
        print(f"\n📌 Original Query: \"{self.state.user_query}\"")
        print("\n" + "-"*70)
        print(f"\n{self.state.final_answer}")
        print("\n" + "="*70)
        print("✨ Deep Research Flow completed!")
        print("="*70)

    

def kickoff():
    ### START CODE HERE ###
    # instantiate the DeepResearchFlow with tracing enabled
    deep_research_flow = DeepResearchFlow(tracing=True)
    ### END CODE HERE ###
    
    # kickoff the flow with a custom id, so you can persist the state
    deep_research_flow.kickoff(inputs={"id": "our-deep-research_flow"})
    

def plot():
    deep_research_flow = DeepResearchFlow()
    deep_research_flow.plot()


if __name__ == "__main__":
    kickoff()