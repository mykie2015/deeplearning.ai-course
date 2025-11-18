import sys
import itertools

from crewai import Agent, Task, Crew, LLM, TaskOutput
from crewai_tools import WebsiteSearchTool
from pydantic import BaseModel

from dlai_grader.grading import test_case
from typing import Tuple, Any
import json

def print_results(cases):
    failed_cases = [t for t in cases if t.failed]
    if len(failed_cases) == 0:
        print("\033[92m All tests passed!\n")
    else:
        print(f"\033[91m You have {len(failed_cases)} failed tests:\n")
        for failed_case in failed_cases:
            feedback_msg = ""
            feedback_msg += f"Failed test case: {failed_case.msg}. \nExpected:\n{failed_case.want},\nbut got:\n{failed_case.got}.\n\n"
            print(feedback_msg)


def test_tools(serper_search_tool, scrape_website_tool):
    cases = []

    # Test 1: Check if the serper_search_tool can run
    t = test_case()
    try:
        content = serper_search_tool.run(query="SQL issues")
    except Exception as e:
        t.failed = True
        t.msg = f"Couldn't run SerperSearchTool instance"
        t.want = "No exception"
        t.got = str(e)
        cases.append(t)

    # Test 2: Check if the scrape_website_tool can run
    t = test_case()
    try:
        content = scrape_website_tool.run(website_url="https://owasp.org")
    except Exception as e:
        t.failed = True
        t.msg = f"Couldn't run ScrapeWebsiteTool instance"
        t.want = "No exception"
        t.got = str(e)
    cases.append(t)

    print_results(cases)

def test_senior_developer_agent(senior_developer): 
    cases = []

    t = test_case()
    if not hasattr(senior_developer, 'goal') or not isinstance(senior_developer.goal, str):
        t.failed = True
        t.msg = f"senior_developer should have a goal attribute. Make sure you didn't remove the line setting the config attribute"
        t.want = "str"
        t.got = type(senior_developer.goal).__name__ if hasattr(senior_developer, 'goal') else "missing"
    cases.append(t)
    t = test_case()
    if not hasattr(senior_developer, 'backstory') or not isinstance(senior_developer.backstory, str):
        t.failed = True
        t.msg = f"senior_developer should have a backstory attribute. Make sure you didn't remove the line setting the config attribute"
        t.want = "str"
        t.got = type(senior_developer.backstory).__name__ if hasattr(senior_developer, 'backstory') else "missing"
    cases.append(t)
    print_results(cases)

def test_security_engineer_agent(security_engineer):
    cases = []

    t = test_case()
    if not hasattr(security_engineer, 'goal') or not isinstance(security_engineer.goal, str):
        t.failed = True
        t.msg = f"security_engineer should have a goal attribute"
        t.want = "str"
        t.got = type(security_engineer.goal).__name__ if hasattr(security_engineer, 'goal') else "missing"
    cases.append(t)
    t = test_case()
    if not hasattr(security_engineer, 'backstory') or not isinstance(security_engineer.backstory, str):
        t.failed = True
        t.msg = f"security_engineer should have a backstory attribute"
        t.want = "str"
        t.got = type(security_engineer.backstory).__name__ if hasattr(security_engineer, 'backstory') else "missing"
    cases.append(t)

    if hasattr(security_engineer, 'tools') and security_engineer.tools:
        if len(security_engineer.tools) == 2:
            tools = security_engineer.tools
            tool_types = [type(tool).__name__ for tool in tools]
            if 'SerperDevTool' not in tool_types or 'ScrapeWebsiteTool' not in tool_types:
                t.failed = True
                t.msg = "security_engineer has the wrong type of tools"
                t.want = "List with SerperDevTool and ScrapeWebsiteTool instances"
                t.got = f"{tool_types}"
        else:
            t.failed = True
            t.msg = "security_engineer should have exactly 2 tools assigned"
            t.want = "List with the SerperDevTool and ScrapeWebsiteTool instances"
            t.got = f"{len(security_engineer.tools)} tools"
    else: 
        t.failed = True
        t.msg = "security_engineer agent should have tools assigned"
        t.want = "List with the SerperDevTool and ScrapeWebsiteTool instances"
        t.got = "Attribute is missing or None"
    cases.append(t)
    print_results(cases)

def test_tech_lead_agent(tech_lead):
    cases = []
    t = test_case()
    if not hasattr(tech_lead, 'goal') or not isinstance(tech_lead.goal, str):
        t.failed = True
        t.msg = f"tech_lead should have a goal attribute."
        t.want = "str"
        t.got = type(tech_lead.goal).__name__ if hasattr(tech_lead, 'goal') else "missing"
    cases.append(t)
    t = test_case()
    if not hasattr(tech_lead, 'backstory') or not isinstance(tech_lead.backstory, str):
        t.failed = True
        t.msg = f"tech_lead should have a backstory attribute. "
        t.want = "str"
        t.got = type(tech_lead.backstory).__name__ if hasattr(tech_lead, 'backstory') else "missing"
    cases.append(t)
    print_results(cases)


def test_analyze_code_quality_task(analyze_code_quality):
    cases = []
    
    # Test 1: Check description
    t = test_case()
    if analyze_code_quality.description == "":
        t.failed = True
        t.msg = "analyze_code_quality description is empty"
        t.want = "A description string with task instructions"
        t.got = analyze_code_quality.description
    cases.append(t)
    
    # Test 2: Check expected_output
    t = test_case()
    if analyze_code_quality.expected_output == "":
        t.failed = True
        t.msg = "analyze_code_quality expected_output is empty"
        t.want = "An expected_output string describing what the output should look like (in this case, a JSON formatted answer)"
        t.got = analyze_code_quality.expected_output
    cases.append(t)

    # Test 3: Check expected_output mentions JSON
    t = test_case()
    if 'json' not in analyze_code_quality.expected_output.lower():
        t.failed = True
        t.msg = "analyze_code_quality expected_output should mention JSON format"
        t.want = "Expected output mentioning JSON"
        t.got = f"Expected output without JSON mention: {analyze_code_quality.expected_output[:100]}..."
    cases.append(t)

    # Test 4: Check agent assignment
    t = test_case()
    if not analyze_code_quality.agent.role == "Senior Developer":
        t.failed = True
        if analyze_code_quality.agent is None:
            t.msg = "You forgot to assign an agent to this task"
        elif isinstance(analyze_code_quality.agent, Agent):
            t.msg = "It seems you assigned the wrong agent to this task"
        else:
            t.msg = "analyze_code_quality agent is not set correctly"
        t.want = "The Senior Developer agent"
        t.got = analyze_code_quality.agent
    cases.append(t)
    
    # Test 5: Check for code_changes variable in description
    t = test_case()
    if '{code_changes}' not in analyze_code_quality.description:
        t.failed = True
        t.msg = "analyze_code_quality description should include `{code_changes}` as context. If you did interpolate the variable, make sure you are not using f-strings."
        t.want = "Description with `{code_changes}`"
        t.got = "Description without `{code_changes}`"
    cases.append(t)
    
    
    print_results(cases)

def test_review_security_task(review_security):
    cases = [] 

    # Test 1: Check description
    t = test_case()
    if review_security.description == "":
        t.failed = True
        t.msg = "review_security description is empty"
        t.want = "A description string with security analysis instructions"
        t.got = review_security.description
    cases.append(t)
    
    # Test 2: Check expected_output
    t = test_case()
    if review_security.expected_output == "":
        t.failed = True
        t.msg = "review_security expected_output is empty"
        t.want = "An expected_output string describing what the output should look like (in this case, a JSON formatted answer)"
        t.got = review_security.expected_output
    cases.append(t)
    
    # Test 4: Check expected_output mentions JSON
    t = test_case()
    if 'json' not in review_security.expected_output.lower():
        t.failed = True
        t.msg = "review_security expected_output should mention JSON format"
        t.want = "Expected output mentioning JSON"
        t.got = f"Expected output without JSON mention"
    cases.append(t)
    
    # Test 5: Check expected_output mentions required keys
    t = test_case()
    required_keys = ['security_vulnerabilities', 'blocking', 'highest_risk', 'security_recommendations']
    missing_keys = [key for key in required_keys if key not in review_security.expected_output]
    if missing_keys:
        t.failed = True
        t.msg = f"review_security expected_output is missing mentioning the required keys: {missing_keys}"
        t.want = f"Expected output mentioning keys: {required_keys}"
        t.got = f"Expected output missing keys: {missing_keys}"
    cases.append(t)
    
    # Test 6: Check agent assignment
    t = test_case()
    if not review_security.agent.role == "Security Engineer":
        t.failed = True
        if review_security.agent is None:
            t.msg = "You forgot to assign an agent to this task"
        elif isinstance(review_security.agent, Agent):
            t.msg = "It seems you assigned the wrong agent to this task"
        else:
            t.msg = "review_security agent is not set correctly"
        t.want = "The Security Engineer agent"
        t.got = review_security.agent
    cases.append(t)

    # Test 7: Check for code_changes variable in description
    t = test_case()
    if '{code_changes}' not in review_security.description:
        t.failed = True
        t.msg = "review_security description should include `{code_changes}` as context. If you did interpolate the variable, make sure you are not using f-strings."
        t.want = "Description with `{code_changes}`"
        t.got = "Description without `{code_changes}`"
    cases.append(t)
    print_results(cases)

def test_make_review_decision_task(make_review_decision):
    cases = []
    
    # Test 2: Check description
    t = test_case()
    if make_review_decision.description == "":
        t.failed = True
        t.msg = "make_review_decision description is empty"
        t.want = "A description string with decision-making instructions"
        t.got = make_review_decision.description
    cases.append(t)
    
    # Test 3: Check expected_output
    t = test_case()
    if make_review_decision.expected_output == "":
        t.failed = True
        t.msg = "make_review_decision expected_output is empty"
        t.want = "An expected_output string describing what the output should look like (in this case, a report)"
        t.got = make_review_decision.expected_output
    cases.append(t)
    
    # Test 4: Check agent assignment
    t = test_case()
    if not make_review_decision.agent.role == "Tech Lead":
        t.failed = True
        if make_review_decision.agent is None:
            t.msg = "You forgot to assign an agent to this task"
        elif isinstance(make_review_decision.agent, Agent):
            t.msg = "It seems you assigned the wrong agent to this task"
        else:
            t.msg = "make_review_decision agent is not set correctly"
        t.want = "The Tech Lead agent"
        t.got = make_review_decision.agent
    cases.append(t)
    
    # Test 5: check context
    t = test_case()
    if not make_review_decision.context or len(make_review_decision.context) != 2:
        t.failed = True
        t.msg = "make_review_decision should have context with 2 tasks"
        t.want = "List with 2 tasks as context"
        t.got = f"{len(make_review_decision.context) if make_review_decision.context else 'missing or None'} tasks"
    cases.append(t)

    # Test 6: Check for code_changes variable in description
    t = test_case()
    if '{code_changes}' not in make_review_decision.description:
        t.failed = True
        t.msg = "make_review_decision description should include `{code_changes}` as context. If you did interpolate the variable, make sure you are not using f-strings."
        t.want = "Description with `{code_changes}`"
        t.got = "Description without `{code_changes}`"
    cases.append(t)
    print_results(cases)


def test_crew(crew):
    cases = []
    
    # Test 1: Check if memory is enabled
    t = test_case()
    if not len(crew.agents) == 3:
        t.failed = True
        t.msg = "crew should have exactly 3 agents"
        t.want = "3 agents"
        t.got = ", ".join([agent.role for agent in crew.agents])
    cases.append(t)
    t = test_case()
    if not len(crew.tasks) == 3:
        t.failed = True
        t.msg = "crew should have exactly 3 tasks"
        t.want = "3 tasks"
        t.got = ", ".join([task.name for task in crew.tasks])
    cases.append(t)

    print_results(cases)