import re

def security_review_output_guardrail(output):
    
    # get the (JSON) output from the TaskOutput object
    try: 
        json_output = output if type(output)==dict else output.json_dict
    except Exception as e:
        return (False, ("Error retrieving the `json_dict` argument: "
                        f"\n{str(e)}\n"
                        "Make sure you set the output_json parameter in the Task."
                        )
                )

    # define risk levels
    valid_risk_levels = ['low', 'medium', 'high']

    # validate that the highest risk level has a valid value
    if json_output["highest_risk"].lower() not in valid_risk_levels: 
        error_message = "Invalid highest risk level."
        return (False, error_message)
    
    # validate that each of the risk levels has a valid value
    for vuln in json_output['security_vulnerabilities']:
        # validate the risk level
        if vuln['risk_level'].lower() not in valid_risk_levels:
            error_message = f"Invalid risk level: {vuln['risk_level']}" 
            return (False, error_message)
    
    # validate that the highest risk level matches the highest risk level in the vulnerabilities
    # get all risk_level values
    risk_levels = [vuln['risk_level'].lower() for vuln in json_output['security_vulnerabilities']] 
    
    # if "high" in risk levels, then highest risk level should be high
    if "high" in risk_levels: 
        if json_output["highest_risk"].lower() != "high":
            error_message = "Highest risk level does not match the highest risk level in the vulnerabilities."
            return (False, error_message) 
    # if high is not present and medium is in risk levels, then highest risk level should be medium
    elif "medium" in risk_levels: 
        if json_output["highest_risk"].lower() != "medium":
            error_message = "Highest risk level does not match the highest risk level in the vulnerabilities."
            return (False, error_message)
    # if high and medium are not present, then lowest risk level should be low
    elif "low" in risk_levels: 
        if json_output["highest_risk"].lower() != "low":
            error_message = "Highest risk level does not match the highest risk level in the vulnerabilities."
            return (False, error_message)
    return (True, output.json_dict)