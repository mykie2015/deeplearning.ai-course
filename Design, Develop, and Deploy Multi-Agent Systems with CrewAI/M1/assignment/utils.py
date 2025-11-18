# Add your utilities or helper functions to this file.

import os
from dotenv import load_dotenv, find_dotenv
import json

# these expect to find a .env file at the directory above the lesson.                                                                                                                     # the format for that file is (without the comment)                                                                                                                                       #API_KEYNAME=AStringThatIsTheLongAPIKeyFromSomeService
def load_env():
    _ = load_dotenv(find_dotenv())

def get_openai_api_key():
    load_env()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

def get_serper_api_key():
    load_env()
    serper_api_key = os.getenv("SERPER_API_KEY")
    return serper_api_key

def get_dict_keys(task_output):
    """
    Extracts the keys from a dictionary-like string.
    """
    # Check if task outputs are dictionaries and show their keys
    if isinstance(task_output, str):
        try:
            
            parsed = json.loads(task_output)
            if isinstance(parsed, dict):
                print(f"  ✅ Can be parsed as JSON dictionary")  
                print(f"  Keys: {list(parsed.keys())}")
            else:
                print(f"  ❌ JSON parses but not as dictionary")
        except json.JSONDecodeError:
            print(f"  ❌ Cannot parse as JSON")
    print()