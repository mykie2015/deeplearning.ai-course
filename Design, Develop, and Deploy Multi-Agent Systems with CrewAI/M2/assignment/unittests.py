from crewai import TaskOutput
from pydantic import BaseModel

from dlai_grader.grading import test_case
from typing import Tuple, Any
import json

def create_mock_output_task(output):
    """
    create a mock a TaskOutput object for testing purposes.
    """
    if isinstance(output, str):
        output = TaskOutput(
                        description="Mock output for testing",
                        agent="test_agent",
                        raw=output,
        )
        
    elif isinstance(output, dict):
        output = TaskOutput(
                        description="Mock output for testing",
                        agent="test_agent",  # specify the agent that produced the output
                        raw=json.dumps(output, indent=2),   # simulate LLM response
                        json_dict=output,            # simulate schema-parsed object
                        output_format="json"
        )
    return output


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


def test_security_review_output_guardrail(security_review_output_guardrail):
    cases = []
    
    # Test 1: Test with valid input (should return (True, Any))
    t = test_case()
    valid_json = {"highest_risk": "high", 
                    "security_vulnerabilities": [{"risk_level": "medium"}, 
                                                {"risk_level": "high"}]}
    mock_output = create_mock_output_task(valid_json)
    try:
        result = security_review_output_guardrail(mock_output)
        if not (isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool)):
            t.failed = True
            t.msg = f"security_review_output_guardrail has a wrong return type for input: \n{valid_json}"
            t.want = Tuple(bool, Any)
            t.got = f"{type(result).__name__}[{type(result[0]).__name__}, {type(result[1]).__name__}]"
    except Exception as e:
        t.failed = True
        t.msg = f"security_review_output_guardrail raised an exception with input: \n{valid_json}"
        t.want = "No exception"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    # Test 2: Test with invalid highest_risk (should return (False, error_msg))
    t = test_case()
    invalid_json = {"highest_risk": "critical", 
                    "security_vulnerabilities": [{"risk_level": "medium"}]}
    mock_output = create_mock_output_task(invalid_json)
    try:
        result = security_review_output_guardrail(mock_output)
        if not (isinstance(result, tuple) and isinstance(result[0], bool) and isinstance(result[1], str)):
            t.failed = True
            t.msg = f"security_review_output_guardrail has a wrong return type for input: \n{invalid_json}"
            t.want = "Tuple[bool, str]"
            t.got = f"{type(result).__name__}[{type(result[0]).__name__}, {type(result[1]).__name__}]"
    except Exception as e:
        t.failed = True
        t.msg = f"security_review_output_guardrail raised an exception with input: \n{invalid_json}"
        t.want = "No exception"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    # Test 3: Test with invalid vulnerability risk_level (should return (False, error_msg))
    t = test_case()
    invalid_json = {"highest_risk": "high", 
                    "security_vulnerabilities": [{"risk_level": "critical"}]}
    mock_output = create_mock_output_task(invalid_json)
    try:
        result = security_review_output_guardrail(mock_output)
        if not (isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool) and isinstance(result[1], str)):
            t.failed = True
            t.msg = f"security_review_output_guardrail has a wrong return type for input: \n{invalid_json}"
            t.want = "Tuple[bool, str]"
            t.got = f"{type(result).__name__}[{type(result[0]).__name__}, {type(result[1]).__name__}]"
    except Exception as e:
        t.failed = True
        t.msg = f"security_review_output_guardrail raised an exception with input: \n{invalid_json}"
        t.want = "No exception"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    # Test 4: Test with highest_risk not matching highest risk in vulnerabilities (should return (False, error_msg))
    t = test_case()
    invalid_json = {"highest_risk": "medium", 
                    "security_vulnerabilities": [{"risk_level": "high"}, 
                                                    {"risk_level": "medium"}]}
    mock_output = create_mock_output_task(invalid_json)
    try:
        result = security_review_output_guardrail(mock_output)
        if not (isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool) and isinstance(result[1], str)):
            t.failed = True
            t.msg = f"security_review_output_guardrail has a wrong return type for input: \n{invalid_json}"
            t.want = "Tuple[bool, str]"
            t.got = f"{type(result).__name__}[{type(result[0]).__name__}, {type(result[1]).__name__}]"
    except Exception as e:
        t.failed = True
        t.msg = f"security_review_output_guardrail raised an exception with input: \n{invalid_json}"
        t.want = "No exception"
        t.got = f"Exception: {str(e)}"
    cases.append(t)

    # Test 5: Test with highest_risk value not in the vulnerability risks (should return (False, error_msg))
    t = test_case()
    invalid_json = {"highest_risk": "high", 
                    "security_vulnerabilities": [{"risk_level": "medium"}]}
    mock_output = create_mock_output_task(invalid_json)
    try:
        result = security_review_output_guardrail(mock_output)
        if not (isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], bool) and isinstance(result[1], str)):
            t.failed = True
            t.msg = f"security_review_output_guardrail has a wrong return type for input: \n{invalid_json}"
            t.want = "Tuple[bool, str]"
            t.got = f"{type(result).__name__}[{type(result[0]).__name__}, {type(result[1]).__name__}]"
        elif not result[0] == False:
            t.failed = True
            t.msg = f"security_review_output_guardrail has a wrong output for the Bool return value for input: \n{invalid_json}"
            t.want = False
            t.got = result[0]
    except Exception as e:
        t.failed = True
        t.msg = f"security_review_output_guardrail raised an exception with input: \n{invalid_json}"
        t.want = "No exception"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    print_results(cases)

def test_review_decision_guardrail(review_decision_guardrail):
    cases = []
    # Test 1: Test with valid input containing "approve" (should return (True, data))
    t = test_case()
    valid_output = "After reviewing the code, I approve this pull request."
    mock_output = create_mock_output_task(valid_output)
    try:
        result = review_decision_guardrail(mock_output)
        if not (isinstance(result, tuple) and len(result) == 2):
            t.failed = True
            t.msg = f"review_decision_guardrail has a wrong return type for input: \n{valid_output}"
            t.want = "Tuple[bool, Any]"
            t.got = f"{type(result).__name__}[{type(result[0]).__name__}, {type(result[1]).__name__}]"
        elif not result[0]==True:
            t.failed = True
            t.msg = f"review_decision_guardrail has a wrong output for the Bool return value for input: \n{valid_output}"
            t.want = True
            t.got = result[0]
        elif not result[1]==valid_output:
            t.failed = True
            t.msg = f"review_decision_guardrail has a wrong output for the data return value for input: \n{valid_output}"
            t.want = valid_output
            t.got = result[1]
    except Exception as e:
        t.failed = True
        t.msg = f"review_decision_guardrail raised an exception with input: \n{valid_output}"
        t.want = "No exception"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    # Test 2: Test with invalid input (should return (False, error_msg))
    t = test_case()
    invalid_output = "The code looks fine, no issues found."
    mock_output = create_mock_output_task(invalid_output)
    try:
        result = review_decision_guardrail(mock_output)
        if not (isinstance(result, tuple) and len(result) == 2):
            t.failed = True
            t.msg = f"review_decision_guardrail has a wrong return type for input: \n{invalid_output}"
            t.want = "Tuple[bool, str]"
            t.got = f"{type(result).__name__}[{type(result[0]).__name__}, {type(result[1]).__name__}]"
        elif not result[0]==False:
            t.failed = True
            t.msg = f"review_decision_guardrail has a wrong output for the Bool return value for input: \n{invalid_output}"
            t.want = False
            t.got = result[0]
        elif not isinstance(result[1], str):
            t.failed = True
            t.msg = f"review_decision_guardrail has a wrong output for the data return value for input: \n{invalid_output}"
            t.want = "str"
            t.got = type(result[1]).__name__
    except Exception as e:
        t.failed = True
        t.msg = f"review_decision_guardrail raised an exception with input: \n{invalid_output}"
        t.want = "No exception"
        t.got = f"Exception: {str(e)}"
    cases.append(t)

    print_results(cases)

def test_analyze_code_quality(analyze_code_quality):
    cases = []
    
    # Test 1: Check if description mentions the {file_content} 
    t = test_case()
    if hasattr(analyze_code_quality, 'description') and analyze_code_quality.description:
        if '{file_content}' not in analyze_code_quality.description:
            t.failed = True
            t.msg = "analyze_code_quality has no mention of where the code to analyze is"
            t.want = "Description instructing to read the content from {file_content}"
            t.got = "Description without {file_content} mention"
    cases.append(t)
    
    # Test 2: Check if task has output_json is set to the correct pydantic model
    t = test_case()
    try: 
        json_structure = analyze_code_quality.output_json
        if not json_structure.__name__ == 'CodeQualityJSON':
            t.failed = True
            if json_structure is None:
                t.failed = True
                t.msg = "analyze_code_quality should have output_json set"
                t.got = json_structure
            else:
                t.msg = "analyze_code_quality output_json is not set to the correct pydantic model"
                t.got = json_structure
            t.want = "CodeQualityJSON pydantic model"
    except Exception as e:
        t.failed = True
        t.msg = f"analyze_code_quality.output_json raised an exception"
        t.want = "No exceptions"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    print_results(cases)

def test_review_security(review_security, SecurityVulnerability, ReviewSecurityJSON):
    cases = [] 
    
    # Test 1: Check if description mentions the {file_content} 
    t = test_case()
    if hasattr(review_security, 'description') and review_security.description:
        if '{file_content}' not in review_security.description:
            t.failed = True
            t.msg = "review_security has no mention of where the code to analyze is"
            t.want = "Description instructing to read the content from {file_content}"
            t.got = "Description without {file_content} mention"
    cases.append(t)
    
    # Test 2: Check if task has output_json is set to the correct pydantic model
    t = test_case()
    try: 
        json_structure = review_security.output_json
        if not json_structure.__name__ == 'ReviewSecurityJSON':
            t.failed = True
            if json_structure is None:
                t.failed = True
                t.msg = "review_security should have output_json set"
                t.got = json_structure
            else:
                t.msg = "review_security output_json is not set to the correct pydantic model"
                t.got = json_structure.__name__
            t.want = "ReviewSecurityJSON pydantic model"
    except Exception as e:
        t.failed = True
        t.msg = f"review_security.output_json raised an exception"
        t.want = "No exceptions"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    # Test 3: Check if task has guardrails, and if it is the correct one
    t = test_case()
    try:
        guardrail = review_security.guardrails[0] if review_security.guardrails else review_security.guardrail
        guardrail = guardrail.__name__ if guardrail else None
        sol_guardrail = 'security_review_output_guardrail'
        if guardrail != sol_guardrail:
            t.failed = True
            if guardrail is None:
                t.msg = "review_security guardrail is not set"
            else:
                t.msg = "review_security guardrail is not set to the correct function"
            t.want = f"{sol_guardrail} guardrail function"
            t.got = f"{guardrail} guardrail function"
    except Exception as e:
        t.failed = True
        t.msg = f"review_security.guardrails raised an exception"
        t.want = "No exceptions"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    
    # Test 4: Check SecurityVulnerability model structure
    t = test_case()
    try:
        # Check if SecurityVulnerability has the required fields
        security_vuln_fields = SecurityVulnerability.model_fields
        required_fields = {'description', 'risk_level', 'evidence'}
        missing_fields = required_fields - set(security_vuln_fields.keys())
        
        if missing_fields:
            t.failed = True
            t.msg = f"SecurityVulnerability model is missing required fields"
            t.want = f"Fields: {sorted(required_fields)}"
            t.got = f"Missing fields: {sorted(missing_fields)}"
    except Exception as e:
        t.failed = True
        t.msg = f"Error checking SecurityVulnerability model structure"
        t.want = "Valid pydantic model with description, risk_level, evidence fields"
        t.got = f"Exception: {str(e)}"
    cases.append(t)

    # Test 5: Check ReviewSecurityJSON model structure
    t = test_case()
    try:
        # Check if ReviewSecurityJSON has the required fields
        review_json_fields = ReviewSecurityJSON.model_fields
        required_fields = {'security_vulnerabilities', 'blocking', 'highest_risk', 'security_recommendations'}
        missing_fields = required_fields - set(review_json_fields.keys())
        
        if missing_fields:
            t.failed = True
            t.msg = f"ReviewSecurityJSON model is missing required fields"
            t.want = f"Fields: {sorted(required_fields)}"
            t.got = f"Missing fields: {sorted(missing_fields)}"
    except Exception as e:
        t.failed = True
        t.msg = f"Error checking ReviewSecurityJSON model structure"
        t.want = "Valid pydantic model with security_vulnerabilities, blocking, highest_risk, security_recommendations fields"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    print_results(cases)

def test_make_review_decision(make_review_decision):
    cases = []
    
    # Test 1: Check if description mentions the {file_content} 
    t = test_case()
    if hasattr(make_review_decision, 'description') and make_review_decision.description:
        if '{file_content}' not in make_review_decision.description:
            t.failed = True
            t.msg = "make_review_decision has no mention of where the code to analyze is"
            t.want = "Description instructing to read the content from {file_content}"
            t.got = "Description without {file_content} mention"
    cases.append(t)
    
    # Test 2: Check if task has markdown set to True
    t = test_case()
    if not hasattr(make_review_decision, 'markdown'):
        t.failed = True
        t.msg = "review_decision has no attribute markdown"
        t.want = True
        t.got = "Missing attribute"
    elif make_review_decision.markdown != True:
        t.failed = True
        t.msg = "review_decision markdown argument has the wrong value"
        t.want = True
        t.got = make_review_decision.markdown
    cases.append(t)
    
    # Test 3: Check if task has guardrails, and if it is the correct one
    t = test_case()
    try:
        guardrail = make_review_decision.guardrails[0] if make_review_decision.guardrails else make_review_decision.guardrail
        guardrail = guardrail.__name__ if guardrail else None
        sol_guardrail = 'review_decision_guardrail'
        if guardrail != sol_guardrail:
            t.failed = True
            if guardrail is None:
                t.msg = "make_review_decision guardrail is not set"
            else:
                t.msg = "make_review_decision guardrail is not set to the correct function"
            t.want = f"{sol_guardrail} guardrail function"
            t.got = f"{guardrail} guardrail function"
    except Exception as e:
        t.failed = True
        t.msg = f"make_review_decision.guardrails raised an exception"
        t.want = "No exceptions"
        t.got = f"Exception: {str(e)}"
    cases.append(t)
    
    print_results(cases)

def test_before_kickoff_hook(read_file_hook):
    cases = []

    # Test 1: Test with missing file_path key
    t = test_case()
    test_inputs = {"other_param": "test"}
    try:
        result = read_file_hook(test_inputs)
        t.failed = True
        t.msg = "read_file_hook should raise ValueError when 'file_path' is missing"
        t.want = "ValueError exception"
        t.got = "No exception raised"
    except ValueError as e:
        # This is expected
        if "file_path" not in str(e):
            t.failed = True
            t.msg = "ValueError message should mention missing 'file_path'"
            t.want = "ValueError mentioning 'file_path'"
            t.got = f"ValueError: {str(e)}"
    except Exception as e:
        t.failed = True
        t.msg = f"read_file_hook should raise ValueError, not other exceptions"
        t.want = "ValueError"
        t.got = f"Exception: {type(e).__name__}: {str(e)}"
    cases.append(t)
    
    # Test 2: Test with empty file_path
    t = test_case()
    test_inputs = {"file_path": "", "other_param": "test"}
    try:
        result = read_file_hook(test_inputs)
        t.failed = True
        t.msg = "read_file_hook should raise ValueError when 'file_path' is empty"
        t.want = "ValueError exception"
        t.got = "No exception raised"
    except ValueError as e:
        # This is expected
        if "file_path" not in str(e):
            t.failed = True
            t.msg = "ValueError message should mention missing 'file_path'"
            t.want = "ValueError mentioning 'file_path'"
            t.got = f"ValueError: {str(e)}"
    except Exception as e:
        t.failed = True
        t.msg = f"read_file_hook should raise ValueError, not other exceptions"
        t.want = "ValueError"
        t.got = f"Exception: {type(e).__name__}: {str(e)}"
    cases.append(t)

    # Test 3: Test with missing file_path key
    t = test_case()
    test_inputs = {"file_path": "non_existent_file.txt"}
    try:
        result = read_file_hook(test_inputs)
        t.failed = True
        t.msg = "read_file_hook should raise RuntimeError when file doesn't exist"
        t.want = "RuntimeError exception"
        t.got = "No exception raised"
    except RuntimeError as e:
        # This is expected
        pass
    except Exception as e:
        t.failed = True
        t.msg = f"read_file_hook should raise RuntimeError for file errors, not other exceptions"
        t.want = "RuntimeError"
        t.got = f"Exception: {type(e).__name__}: {str(e)}"
    cases.append(t)

    print_results(cases)

def test_read_file_hook(read_file_hook):
    cases = []
    # Test 1: Test with valid inputs containing file_path
    t = test_case()
    test_inputs = {"file_path": "files/code_changes.txt"}

    result = read_file_hook(test_inputs)
    if not isinstance(result, dict):
        t.failed = True
        t.msg = "read_file_hook should return a dictionary"
        t.want = dict
        t.got = type(result)
    elif "file_content" not in result:
        t.failed = True
        t.msg = "The output of read_file_hook is missing the 'file_content' key"
        t.want = "Dictionary with 'file_content' key"
        t.got = f"Dictionary with keys: {list(result.keys())}"
    elif not isinstance(result["file_content"], str):
        t.failed = True
        t.msg = "The value for the `file_content` key has the wrong type"
        t.want = str
        t.got = type(result["file_content"])
    cases.append(t)
    print_results(cases)

        

def test_crew(crew):
    cases = []
    
    # Test 1: Check if memory is enabled
    t = test_case()
    if not hasattr(crew, 'memory') or crew.memory != True:
        t.failed = True
        t.msg = "crew should have memory enabled"
        t.want = True
        t.got = getattr(crew, 'memory', 'None or missing')
    cases.append(t)
    
    print_results(cases)