import re

def write_report_guardrail(output):
    # get the raw output from the TaskOutput object
    try:
        output = output if type(output)==str else output.raw 
    except Exception as e:
        return (False, ("Error retrieving the `raw` argument: "
                        f"\n{str(e)}\n"
                        )
                )
    
    # convert the output to lowecase
    output_lower = output.lower()

    # check that the summary section exists
    if not re.search(r'#+.*summary', output_lower):
        return (False, 
                "The report must include a Summary section with a header like '## Summary'"
                )

    # check that the insights or recommendations sections exist
    if not re.search(r'#+.*insights|#+.*recommendations', output_lower):
        return (False, 
                "The report must include an Insights section with a header like '## Insights'"
                )

    # check that the citations (or references) section exists
    if not re.search(r'#+.*citations|#+.*references', output_lower): 
        return (False, 
                "The report must include a Citations (or References) section with a header like '## Citations'"
                ) 
    return (True, output)